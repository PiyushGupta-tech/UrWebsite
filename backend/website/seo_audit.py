"""Phase 7 — SEO audit helpers for API and management command."""

from __future__ import annotations

from django.conf import settings

from . import content
from .page_content import PAGES, ROUTE_SLUGS, SLUG_TO_ROUTE
from .page_seo import PAGE_SEO, RELATED_LINKS, resolve_page_seo
from .seo_discovery import sitemap_urls

SITE_BASE_URL = getattr(settings, "SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")

TITLE_MAX = 60
DESCRIPTION_MIN = 50
DESCRIPTION_MAX = 160
KEYWORDS_MAX = 8


def _check_meta(slug: str, seo: dict) -> list[dict]:
    issues = []

    title = seo.get("title", "")
    if not title:
        issues.append({"slug": slug, "level": "error", "message": "Missing title."})
    elif len(title) > TITLE_MAX:
        issues.append({
            "slug": slug,
            "level": "warn",
            "message": f"Title length {len(title)} exceeds {TITLE_MAX} characters.",
        })

    description = seo.get("description", "")
    if not description:
        issues.append({"slug": slug, "level": "error", "message": "Missing meta description."})
    elif len(description) < DESCRIPTION_MIN:
        issues.append({
            "slug": slug,
            "level": "warn",
            "message": f"Description length {len(description)} is under {DESCRIPTION_MIN} characters.",
        })
    elif len(description) > DESCRIPTION_MAX:
        issues.append({
            "slug": slug,
            "level": "warn",
            "message": f"Description length {len(description)} exceeds {DESCRIPTION_MAX} characters.",
        })

    keywords = [k for k in seo.get("keywords", "").split(",") if k.strip()]
    if len(keywords) > KEYWORDS_MAX:
        issues.append({
            "slug": slug,
            "level": "warn",
            "message": f"{len(keywords)} meta keywords exceeds {KEYWORDS_MAX}; avoid keyword stuffing.",
        })

    return issues


def _check_page(slug: str, page: dict) -> list[dict]:
    seo = resolve_page_seo(slug, page)
    route = SLUG_TO_ROUTE.get(slug, f"/{slug}")
    issues = []

    if slug not in PAGE_SEO:
        issues.append({"slug": slug, "level": "warn", "message": "Missing entry in PAGE_SEO."})

    issues.extend(_check_meta(slug, seo))

    if not seo.get("h1"):
        issues.append({"slug": slug, "level": "warn", "message": "Missing H1."})

    canonical = seo.get("canonical", "")
    expected = f"{SITE_BASE_URL}{route}" if route != "/" else f"{SITE_BASE_URL}/"
    if canonical != expected:
        issues.append({
            "slug": slug,
            "level": "error",
            "message": f"Canonical mismatch: {canonical!r} expected {expected!r}.",
        })

    if slug in RELATED_LINKS and not RELATED_LINKS[slug]:
        issues.append({"slug": slug, "level": "warn", "message": "Empty related_links."})

    return issues


def run_seo_audit() -> dict:
    """Return a structured SEO audit report."""
    issues = []
    pages_checked = 0

    home_seo = content.HOME_SEO
    pages_checked += 1
    if not home_seo.get("canonical"):
        issues.append({"slug": "home", "level": "error", "message": "Homepage missing canonical."})
    issues.extend(_check_meta("home", home_seo))

    for slug, page in sorted(PAGES.items()):
        pages_checked += 1
        issues.extend(_check_page(slug, page))

    sitemap_count = len(sitemap_urls())
    route_count = len(ROUTE_SLUGS) + 1
    if sitemap_count != route_count:
        issues.append({
            "slug": "sitemap",
            "level": "warn",
            "message": f"Sitemap has {sitemap_count} URLs; expected {route_count}.",
        })

    errors = [i for i in issues if i["level"] == "error"]
    warnings = [i for i in issues if i["level"] == "warn"]

    return {
        "site_base_url": SITE_BASE_URL,
        "pages_checked": pages_checked,
        "sitemap_urls": sitemap_count,
        "related_link_slugs": len(RELATED_LINKS),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "ok": len(errors) == 0,
        "issues": issues,
        "product_urls": content.SITE.get("product_urls", {}),
        "gsc_configured": bool(getattr(settings, "GSC_SITE_VERIFICATION", "")),
    }
