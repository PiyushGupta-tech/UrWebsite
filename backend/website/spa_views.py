"""Serve SPA index.html with per-route SEO injected for crawlers."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from html import escape
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views import View

from . import content
from .homepage import homepage_payload
from .page_content import PAGES
from .page_seo import normalize_path, seo_for_path, slug_for_path
from .seo_schema import structured_data_script

FRONTEND_DIST = Path(settings.BASE_DIR).parent / "frontend" / "dist"
INDEX_PATH = FRONTEND_DIST / "index.html"


@lru_cache(maxsize=1)
def _index_template() -> str:
    if not INDEX_PATH.is_file():
        raise Http404("Frontend build not found.")
    return INDEX_PATH.read_text(encoding="utf-8")


def _attr(value: str) -> str:
    return escape(value, quote=True)


def inject_seo(html: str, seo: dict) -> str:
    """Replace title, description, OG tags, and canonical in index.html."""
    title = seo.get("title", "")
    description = seo.get("description", "")
    canonical = seo.get("canonical", "")

    if title:
        html = re.sub(
            r"<title>[^<]*</title>",
            f"<title>{escape(title)}</title>",
            html,
            count=1,
        )
        html = re.sub(
            r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
            rf"\1{_attr(title)}\2",
            html,
            count=1,
        )

    if description:
        html = re.sub(
            r'(<meta\s+name="description"\s+content=")[^"]*(")',
            rf"\1{_attr(description)}\2",
            html,
            count=1,
        )
        html = re.sub(
            r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
            rf"\1{_attr(description)}\2",
            html,
            count=1,
        )

    if canonical:
        html = re.sub(
            r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
            rf"\1{_attr(canonical)}\2",
            html,
            count=1,
        )
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


def inject_homepage_bootstrap(html: str, payload: dict) -> str:
    """Embed homepage JSON so the SPA can paint without waiting on /api/homepage/."""
    if 'id="homepage-bootstrap"' in html:
        return html
    blob = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    tag = f'<script type="application/json" id="homepage-bootstrap">{blob}</script>'
    return html.replace("</body>", f"    {tag}\n  </body>", 1)


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

        if normalized == "/":
            html = inject_homepage_bootstrap(html, homepage_payload())

        gsc_token = getattr(settings, "GSC_SITE_VERIFICATION", "")
        if gsc_token:
            html = inject_gsc_verification(html, gsc_token)

        return HttpResponse(html, content_type="text/html; charset=utf-8")
