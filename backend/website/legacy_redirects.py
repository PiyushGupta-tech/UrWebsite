"""301 redirects for old WordPress URLs still listed in Google Search Console."""

from __future__ import annotations

from django.http import HttpResponseGone
from django.views import View

# Old path (no leading slash) -> new canonical path
LEGACY_REDIRECTS: dict[str, str] = {
    "apk-contact": "/contact",
    "manager-engineering": "/about",
    "about-us": "/about",
    "category/blog": "/blog",
    "services-3": "/products",
    "pricing-tables": "/contact",
    "team": "/about",
    "services": "/products",
}

# Retired WordPress sitemaps — no longer valid XML endpoints
LEGACY_GONE_PATHS = frozenset({
    "sitemap_index.xml",
    "category-sitemap.xml",
    "post-sitemap.xml",
    "page-sitemap.xml",
})


class LegacyGoneView(View):
    """410 Gone for retired WordPress assets (old sitemaps, etc.)."""

    def get(self, _request, *_args, **_kwargs):
        return HttpResponseGone("This resource has been permanently removed.")
