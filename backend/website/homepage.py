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
        "payment_solution": content.PAYMENT_SOLUTION,
        "banking_partners": content.BANKING_PARTNERS,
        "merchant_partners": content.MERCHANT_PARTNERS,
        "features": content.FEATURES,
        "stats": content.STATS,
        "why_choose": content.WHY_CHOOSE,
        "testimonials": content.TESTIMONIALS,
        "faqs": content.FAQS,
        "footer": content.FOOTER,
        "checkout_demo": content.CHECKOUT_DEMO,
        "problem_trio": content.PROBLEM_TRIO,
        "value_prop": content.VALUE_PROP,
        "personas": content.PERSONAS,
        "product_catalogue": content.PRODUCT_CATALOGUE,
        "dashboard_preview": content.DASHBOARD_PREVIEW,
    }
