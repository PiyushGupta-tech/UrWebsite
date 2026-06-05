"""Phase 5 — JSON-LD structured data for search engines."""

from __future__ import annotations

import json

from django.conf import settings

from . import content
from .page_seo import breadcrumb_trail, resolve_page_seo

SITE_BASE_URL = getattr(settings, "SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")

PRODUCT_SLUGS = frozenset({
    "white-label-platform",
    "custom-checkout",
    "hyper-checkout",
    "payment-orchestration",
    "upi-switch",
    "affordability",
    "payout-portal",
    "close-route-wallet",
})


def organization_jsonld() -> dict:
    return {
        "@type": "Organization",
        "@id": f"{SITE_BASE_URL}/#organization",
        "name": content.SITE["name"],
        "url": SITE_BASE_URL,
        "logo": f"{SITE_BASE_URL}/logos/urlogo.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+91-9305697870",
            "contactType": "customer support",
            "email": "it.support@urbanrupee.com",
            "areaServed": "IN",
        },
    }


def breadcrumb_jsonld(trail: list[dict], canonical: str) -> dict:
    items = []
    for index, crumb in enumerate(trail):
        item = {
            "@type": "ListItem",
            "position": index + 1,
            "name": crumb["name"],
        }
        if crumb.get("current"):
            item["item"] = canonical
        elif crumb.get("path"):
            item["item"] = f"{SITE_BASE_URL}{crumb['path']}"
        items.append(item)
    return {
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": items,
    }


def webpage_jsonld(seo: dict, slug: str | None) -> dict:
    page_id = seo.get("canonical", SITE_BASE_URL)
    data = {
        "@type": "WebPage",
        "@id": f"{page_id}#webpage",
        "url": page_id,
        "name": seo.get("title", ""),
        "description": seo.get("description", ""),
        "isPartOf": {"@id": f"{SITE_BASE_URL}/#website"},
        "about": {"@id": f"{SITE_BASE_URL}/#organization"},
    }
    if slug in PRODUCT_SLUGS:
        data["@type"] = "WebPage"
        data["mainEntity"] = {"@id": f"{page_id}#service"}
    return data


def service_jsonld(seo: dict, slug: str) -> dict | None:
    if slug not in PRODUCT_SLUGS:
        return None
    page_id = seo.get("canonical", SITE_BASE_URL)
    return {
        "@type": "Service",
        "@id": f"{page_id}#service",
        "name": seo.get("h1", seo.get("title", "")),
        "description": seo.get("description", ""),
        "url": page_id,
        "provider": {"@id": f"{SITE_BASE_URL}/#organization"},
        "areaServed": "IN",
    }


def website_jsonld() -> dict:
    return {
        "@type": "WebSite",
        "@id": f"{SITE_BASE_URL}/#website",
        "url": SITE_BASE_URL,
        "name": content.SITE["name"],
        "publisher": {"@id": f"{SITE_BASE_URL}/#organization"},
    }


def structured_data_graph(slug: str | None, page: dict, seo: dict) -> list[dict]:
    """Build JSON-LD @graph nodes for a page."""
    canonical = seo.get("canonical", SITE_BASE_URL)
    trail = breadcrumb_trail(slug, page, seo)

    graph = [
        organization_jsonld(),
        website_jsonld(),
        webpage_jsonld(seo, slug),
        breadcrumb_jsonld(trail, canonical),
    ]
    service = service_jsonld(seo, slug) if slug else None
    if service:
        graph.append(service)
    return graph


def structured_data_script(slug: str | None, page: dict, seo: dict) -> str:
    graph = structured_data_graph(slug, page, seo)
    payload = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    return json.dumps(payload, ensure_ascii=False)
