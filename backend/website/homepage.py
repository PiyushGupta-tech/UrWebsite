"""Homepage API payload — shared by REST endpoint and SSR bootstrap."""

from __future__ import annotations

from . import content
from .seo_schema import structured_data_graph


def homepage_payload() -> dict:
    return {
        "site": content.SITE,
        "nav": content.NAV,
        "seo": content.HOME_SEO,
        "structured_data": structured_data_graph(
            None,
            {"title": content.HOME_SEO.get("h1", "Home")},
            content.HOME_SEO,
        ),
        "hero": content.HERO,
        "banking_partners": content.BANKING_PARTNERS,
        "merchant_partners": content.MERCHANT_PARTNERS,
        "stats": content.STATS,
        "footer": content.FOOTER,
        "problem_trio": content.PROBLEM_TRIO,
        "ecosystem": content.ECOSYSTEM,
        "perform": content.PERFORM,
        "products": content.PRODUCTS,
        "closing": content.HOME_CLOSING,
    }
