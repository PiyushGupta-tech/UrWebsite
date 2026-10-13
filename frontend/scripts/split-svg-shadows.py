#!/usr/bin/env python3
"""Split Figma drop-shadow filters so SVG content is never drawn through a filter.

Safari rasterises filtered SVG groups at low resolution, so a Figma export whose
drop shadow wraps a whole card renders the card's text and icons blurred on iPhone.
For each group with a drop-shadow filter this rewrites

    <g ATTRS filter="url(#f)">CONTENT</g>

to

    <g ATTRS>
      <use href="#ur-sh-N" filter="url(#f-ur-sh)"/>    (shadow only)
      <g id="ur-sh-N">CONTENT</g>                      (content, unfiltered)
    </g>

where `f-ur-sh` is `f` without its final "draw SourceGraphic on top" blend. The
paint order (shadow, then content) matches what the original filter produced, and
the group's own opacity, transform, clip, mask and classes still apply to the pair
as one, as they did to the filter output.

A filtered shape (rect, path, ...) becomes `<use/>` plus the shape wrapped in a
referenced group, and is left alone if it carries opacity, transform, clip-path,
mask or inline style. Non-drop-shadow filters (glows, inner shadows) are untouched.

Usage: split-svg-shadows.py [--write] PATH...
"""

import re
import sys
from pathlib import Path

TAG_RE = re.compile(r"<(/?)([A-Za-z][\w:.-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)(/?)>")
FILTER_ATTR_RE = re.compile(r'\sfilter="url\(#([^)"]+)\)"')
ATTR_NAME_RE = re.compile(r'\s([\w:.-]+)="')
FINAL_BLEND_RE = re.compile(
    r'\s*<feBlend\s+mode="normal"\s+in="SourceGraphic"\s+in2="[^"]+"\s+result="shape"\s*/>\s*$'
)
BLOCKING_ATTRS = ("opacity", "transform", "clip-path", "mask", "style")
SHADOW_SUFFIX = "-ur-sh"
REF_PREFIX = "ur-sh-"


def non_markup_spans(text):
    spans = []
    for pattern in (r"<style\b.*?</style>", r"<script\b.*?</script>", r"<!--.*?-->", r"<!\[CDATA\[.*?\]\]>"):
        spans.extend(m.span() for m in re.finditer(pattern, text, re.S))
    return spans


def element_tags(text):
    spans = non_markup_spans(text)
    return [
        m for m in TAG_RE.finditer(text)
        if not any(a < m.start() < b for a, b in spans)
    ]


def parse_filters(text):
    """id -> (opening-tag attributes, body) for every <filter>."""
    filters = {}
    for m in re.finditer(r"<filter\b([^>]*)>(.*?)</filter>", text, re.S):
        fid = re.search(r'\sid="([^"]+)"', m.group(1))
        if fid:
            filters[fid.group(1)] = (m.group(1), m.group(2))
    return filters


def shadow_only_body(body):
    """Filter body without the trailing SourceGraphic blend, or None if not a plain drop shadow."""
    if "feOffset" not in body and "feDropShadow" not in body:
        return None
    match = FINAL_BLEND_RE.search(body)
    if not match:
        return None
    head = body[: match.start()]
    if "SourceGraphic" in head or 'operator="arithmetic"' in head:
        return None
    return head + "\n"


def element_end(tags, index):
    """Offset just past the element whose start tag is tags[index]."""
    start = tags[index]
    if start.group(4) == "/":
        return start.end()
    name = start.group(2)
    depth = 0
    for m in tags[index:]:
        if m.group(2) != name or m.group(4) == "/":
            continue
        depth += -1 if m.group(1) == "/" else 1
        if depth == 0:
            return m.end()
    raise ValueError(f"unclosed <{name}> at offset {start.start()}")


def candidates(text, shadow_bodies):
    """(start, end, filter attr match) for every splittable filtered element, plus skip reasons."""
    tags = element_tags(text)
    found, skipped = [], {}
    for i, m in enumerate(tags):
        if m.group(1) == "/" or m.group(2) == "use":
            continue
        fm = FILTER_ATTR_RE.search(m.group(3))
        if not fm:
            continue
        reason = None
        if shadow_bodies.get(fm.group(1)) is None:
            reason = "not-drop-shadow"
        elif m.group(2) != "g":
            names = set(ATTR_NAME_RE.findall(m.group(3)))
            blocking = next((a for a in BLOCKING_ATTRS if a in names), None)
            if blocking:
                reason = f"has-{blocking}"
        if reason:
            skipped[reason] = skipped.get(reason, 0) + 1
            continue
        found.append((m.start(), element_end(tags, i), m, fm))
    return found, skipped


def transform(text):
    if f'id="{REF_PREFIX}' in text:
        return text, {"already-split": 1}
    filters = parse_filters(text)
    shadow_bodies = {fid: shadow_only_body(body) for fid, (_, body) in filters.items()}
    used, split, skipped = set(), 0, {}

    while True:
        found, skipped = candidates(text, shadow_bodies)
        if not found:
            break
        # Innermost first: an element with no splittable element inside it.
        start, end, tag, fm = next(
            c for c in found
            if not any(o is not c and c[0] < o[0] and o[1] <= c[1] for o in found)
        )
        split += 1
        ref = f"{REF_PREFIX}{split}"
        fid = fm.group(1)
        shadow = f'<use href="#{ref}" filter="url(#{fid}{SHADOW_SUFFIX})"/>'
        open_tag = tag.group(0).replace(fm.group(0), "", 1)
        if tag.group(2) == "g" and tag.group(4) != "/":
            if text[end - len("</g>"):end] != "</g>":
                raise ValueError(f"unexpected closing tag at offset {end}")
            content = text[tag.end():end - len("</g>")]
            replacement = f'{open_tag}{shadow}<g id="{ref}">{content}</g></g>'
        else:
            replacement = f'{shadow}<g id="{ref}">{open_tag}{text[tag.end():end]}</g>'
        text = text[:start] + replacement + text[end:]
        used.add(fid)

    if used:
        defs = []
        for fid in sorted(used):
            attrs, _ = filters[fid]
            attrs = attrs.replace(f'id="{fid}"', f'id="{fid}{SHADOW_SUFFIX}"', 1)
            defs.append(f"<filter{attrs}>{shadow_bodies[fid]}</filter>")
        block = "\n".join(defs) + "\n"
        close = text.rfind("</defs>")
        if close == -1:
            close = text.rfind("</svg>")
            block = "<defs>\n" + block + "</defs>\n"
        text = text[:close] + block + text[close:]

    stats = {"split": split}
    stats.update(skipped)
    return text, stats


def main(argv):
    write = "--write" in argv
    paths = [Path(a) for a in argv if a != "--write"]
    files = []
    for p in paths:
        files.extend(sorted(p.rglob("*.svg")) if p.is_dir() else [p])
    totals, changed = {}, []
    for f in files:
        text = f.read_text(encoding="utf-8")
        try:
            new, stats = transform(text)
        except ValueError as exc:
            print(f"SKIP {f}: {exc}", file=sys.stderr)
            continue
        for k, v in stats.items():
            totals[k] = totals.get(k, 0) + v
        if new != text:
            changed.append(f)
            if write:
                f.write_text(new, encoding="utf-8")
    print(f"files scanned: {len(files)}  files {'changed' if write else 'to change'}: {len(changed)}")
    print("elements:", totals)


if __name__ == "__main__":
    main(sys.argv[1:])
