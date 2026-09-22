"""Phase 3 — robots.txt and sitemap.xml for search engine discovery."""

from __future__ import annotations

from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.views import View

from .page_content import ROUTE_SLUGS
from .page_seo import PRODUCT_SLUGS, RESOURCE_SLUGS

SITE_BASE_URL = getattr(settings, "SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")

SERVICE_SLUGS = frozenset({
    "collections",
    "payouts",
    "financial-operations",
    "risk-fraud-management",
    "reconciliation",
})


def _priority_for_slug(slug: str) -> str:
    if slug in {"products-index", "resources-index"}:
        return "0.95"
    if slug in PRODUCT_SLUGS:
        return "0.90"
    if slug in SERVICE_SLUGS:
        return "0.85"
    if slug == "about":
        return "0.75"
    if slug in RESOURCE_SLUGS:
        return "0.65"
    if slug == "contact":
        return "0.80"
    return "0.60"


def _changefreq_for_slug(slug: str) -> str:
    if slug in PRODUCT_SLUGS or slug in SERVICE_SLUGS:
        return "weekly"
    return "monthly"


def sitemap_urls() -> list[dict]:
    """Ordered list of public URLs for sitemap.xml."""
    entries = [
        {"loc": f"{SITE_BASE_URL}/", "changefreq": "weekly", "priority": "1.00"},
    ]

    for path in sorted(ROUTE_SLUGS.keys()):
        slug = ROUTE_SLUGS[path]
        entries.append({
            "loc": f"{SITE_BASE_URL}{path}",
            "changefreq": _changefreq_for_slug(slug),
            "priority": _priority_for_slug(slug),
        })

    return entries


def render_sitemap_xml() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in sitemap_urls():
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(entry['loc'])}</loc>")
        lines.append(f"    <changefreq>{entry['changefreq']}</changefreq>")
        lines.append(f"    <priority>{entry['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_robots_txt() -> str:
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {SITE_BASE_URL}/sitemap.xml\n"
    )


class RobotsTxtView(View):
    def get(self, _request, *_args, **_kwargs):
        return HttpResponse(
            render_robots_txt(),
            content_type="text/plain; charset=utf-8",
        )


class SitemapXmlView(View):
    def get(self, _request, *_args, **_kwargs):
        return HttpResponse(
            render_sitemap_xml(),
            content_type="application/xml; charset=utf-8",
        )
