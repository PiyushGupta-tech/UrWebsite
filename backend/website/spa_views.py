"""Serve SPA index.html with per-route SEO injected for crawlers."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.views import View

from . import content
from .homepage import homepage_payload
from .page_api import page_detail_payload, site_payload
from .page_content import PAGES, ROUTE_SLUGS
from .page_seo import normalize_path, seo_for_path, slug_for_path
from .seo_schema import structured_data_script

# Paths the Vue router renders that are not content pages.
APP_ONLY_PATHS = frozenset({"/admin", "/admin/dashboard", "/thank-you"})
NOT_FOUND_TITLE = "Page not found | Urbanrupee"
THANK_YOU_PATH = "/thank-you"
THANK_YOU_TITLE = "Thank you | Urbanrupee"

FRONTEND_DIST = Path(settings.BASE_DIR).parent / "frontend" / "dist"
INDEX_PATH = FRONTEND_DIST / "index.html"

_index_cache: tuple[int, str] | None = None


def _index_template() -> str:
    """Read SPA shell; re-read when frontend/dist/index.html changes after deploy."""
    global _index_cache
    if not INDEX_PATH.is_file():
        raise Http404("Frontend build not found.")
    mtime_ns = INDEX_PATH.stat().st_mtime_ns
    if _index_cache and _index_cache[0] == mtime_ns:
        return _index_cache[1]
    html = INDEX_PATH.read_text(encoding="utf-8")
    _index_cache = (mtime_ns, html)
    return html


def _attr(value: str) -> str:
    return escape(value, quote=True)


def _meta_pattern(attr: str, key: str) -> str:
    return rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*"\s*/?>'


def _set_meta(html: str, attr: str, key: str, value: str) -> str:
    """Set a meta tag's content, inserting it before </head> when absent."""
    tag = f'<meta {attr}="{key}" content="{_attr(value)}" />'
    if re.search(_meta_pattern(attr, key), html):
        return re.sub(_meta_pattern(attr, key), lambda _m: tag, html, count=1)
    return html.replace("</head>", f"    {tag}\n  </head>", 1)


def _remove_meta(html: str, attr: str, key: str) -> str:
    return re.sub(rf"[ \t]*{_meta_pattern(attr, key)}\n?", "", html, count=1)


def inject_seo(html: str, seo: dict) -> str:
    """Replace title, description, keywords, OG/Twitter tags, and canonical in index.html."""
    title = seo.get("title", "")
    description = seo.get("description", "")
    keywords = seo.get("keywords", "")
    canonical = seo.get("canonical", "")

    if title:
        html = re.sub(
            r"<title>[^<]*</title>",
            lambda _m: f"<title>{escape(title)}</title>",
            html,
            count=1,
        )
        html = _set_meta(html, "property", "og:title", title)
        html = _set_meta(html, "name", "twitter:title", title)

    if description:
        html = _set_meta(html, "name", "description", description)
        html = _set_meta(html, "property", "og:description", description)
        html = _set_meta(html, "name", "twitter:description", description)

    if keywords:
        html = _set_meta(html, "name", "keywords", keywords)
    else:
        html = _remove_meta(html, "name", "keywords")

    if canonical:
        html = _set_meta(html, "property", "og:url", canonical)
        if re.search(r'<link\s+rel="canonical"', html):
            html = re.sub(
                r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
                rf"\1{_attr(canonical)}\2",
                html,
                count=1,
            )
        else:
            html = html.replace(
                "</head>",
                f'    <link rel="canonical" href="{_attr(canonical)}" />\n  </head>',
                1,
            )

    return html


def inject_json_ld(html: str, json_ld: str) -> str:
    """Insert Phase 5 JSON-LD before </head>."""
    if not json_ld:
        return html
    tag = f'<script type="application/ld+json">{json_ld}</script>'
    if 'type="application/ld+json"' in html:
        return html
    return html.replace("</head>", f"    {tag}\n  </head>", 1)


def inject_json_bootstrap(html: str, element_id: str, payload: dict) -> str:
    """Embed JSON so the SPA can paint without waiting on an API round trip."""
    if f'id="{element_id}"' in html:
        return html
    blob = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    tag = f'<script type="application/json" id="{element_id}">{blob}</script>'
    return html.replace("</body>", f"    {tag}\n  </body>", 1)


def inject_homepage_bootstrap(html: str, payload: dict) -> str:
    """Embed homepage JSON so the SPA can paint without waiting on /api/homepage/."""
    return inject_json_bootstrap(html, "homepage-bootstrap", payload)


def is_known_path(normalized: str) -> bool:
    return normalized == "/" or normalized in ROUTE_SLUGS or normalized in APP_ONLY_PATHS


def inject_not_found(html: str) -> str:
    """Head for unknown URLs: own title, noindex, no canonical pointing at the homepage."""
    return inject_utility_head(html, NOT_FOUND_TITLE)


def inject_utility_head(html: str, title: str) -> str:
    """Title plus noindex, without the homepage canonical, for pages that are not content."""
    html = re.sub(
        r"<title>[^<]*</title>",
        lambda _m: f"<title>{escape(title)}</title>",
        html,
        count=1,
    )
    html = _set_meta(html, "property", "og:title", title)
    html = _set_meta(html, "name", "twitter:title", title)
    html = _set_meta(html, "name", "robots", "noindex, follow")
    html = _remove_meta(html, "name", "keywords")
    html = _remove_meta(html, "property", "og:url")
    return re.sub(r'[ \t]*<link\s+rel="canonical"\s+href="[^"]*"\s*/?>\n?', "", html, count=1)


GA_MEASUREMENT_ID_RE = re.compile(r"^G-[A-Z0-9]{4,20}$")


def inject_ga_measurement_id(html: str, measurement_id: str) -> str:
    """Expose the GA4 ID to the SPA, which loads analytics only after cookie consent."""
    if not GA_MEASUREMENT_ID_RE.match(measurement_id or "") or 'name="ga-measurement-id"' in html:
        return html
    meta = f'<meta name="ga-measurement-id" content="{_attr(measurement_id)}" />'
    return html.replace("</head>", f"    {meta}\n  </head>", 1)


def inject_gsc_verification(html: str, token: str) -> str:
    """Insert Google Search Console verification meta when configured."""
    if not token or 'name="google-site-verification"' in html:
        return html
    meta = f'<meta name="google-site-verification" content="{_attr(token)}" />'
    return html.replace("</head>", f"    {meta}\n  </head>", 1)


class SpaIndexView(View):
    """Return index.html with per-route SEO and JSON-LD for crawlers."""

    def get(self, request, *_args, **_kwargs):
        try:
            html = _index_template()
        except Http404:
            raise

        normalized = normalize_path(request.path)
        lowered = normalized.lower()
        # The Vue router matches case-insensitively; send mixed-case links to the one URL.
        if lowered != normalized and is_known_path(lowered):
            query = request.META.get("QUERY_STRING", "")
            return HttpResponsePermanentRedirect(f"{lowered}?{query}" if query else lowered)
        status = 200 if is_known_path(normalized) else 404

        seo = seo_for_path(request.path, home_seo=content.HOME_SEO)
        if seo:
            html = inject_seo(html, seo)

            if normalized == "/":
                slug = None
                page = {"title": content.HOME_SEO.get("h1", "Home")}
            else:
                slug = slug_for_path(normalized)
                page = PAGES.get(slug, {"title": seo.get("h1", "")})
            html = inject_json_ld(html, structured_data_script(slug, page, seo))

        if status == 404:
            html = inject_not_found(html)
        elif normalized == THANK_YOU_PATH:
            html = inject_utility_head(html, THANK_YOU_TITLE)

        if normalized == "/admin" or normalized.startswith("/admin/"):
            html = _set_meta(html, "name", "robots", "noindex, nofollow")

        html = inject_json_bootstrap(html, "site-bootstrap", site_payload())
        if normalized == "/":
            html = inject_homepage_bootstrap(html, homepage_payload())
        else:
            slug = slug_for_path(normalized)
            payload = page_detail_payload(slug) if slug else None
            if payload:
                html = inject_json_bootstrap(html, "page-bootstrap", payload)

        gsc_token = getattr(settings, "GSC_SITE_VERIFICATION", "")
        if gsc_token:
            html = inject_gsc_verification(html, gsc_token)

        if not (normalized == "/admin" or normalized.startswith("/admin/")):
            html = inject_ga_measurement_id(html, getattr(settings, "GA_MEASUREMENT_ID", ""))

        return HttpResponse(
            html,
            status=status,
            content_type="text/html; charset=utf-8",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
