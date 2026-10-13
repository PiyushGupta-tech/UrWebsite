"""JSON payloads shared by the REST API and the HTML bootstrap tags."""

from __future__ import annotations

from . import content, page_content
from .page_faqs import closing_for_slug
from .page_seo import page_context_for_slug
from .seo_schema import structured_data_graph


def site_payload() -> dict:
    return {"site": content.SITE, "nav": content.NAV, "footer": content.FOOTER}


def page_detail_payload(slug: str) -> dict | None:
    page = page_content.PAGES.get(slug)
    if not page:
        return None
    ctx = page_context_for_slug(slug, page)
    return {
        "slug": slug,
        "route": page_content.SLUG_TO_ROUTE.get(slug),
        **ctx,
        "structured_data": structured_data_graph(slug, page, ctx["seo"]),
        "page": page,
        "site": content.SITE,
        "nav": content.NAV,
        "footer": content.FOOTER,
        "common_closing": closing_for_slug(slug),
        "checkout_demo": content.CHECKOUT_DEMO,
        "dashboard_preview": content.DASHBOARD_PREVIEW,
    }
