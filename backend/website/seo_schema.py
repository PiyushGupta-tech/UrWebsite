"""Phase 5 — JSON-LD structured data for search engines."""

from __future__ import annotations

import json

from django.conf import settings

from . import content
from .page_faqs import page_faq_items
from .page_seo import breadcrumb_trail, resolve_page_seo

SITE_BASE_URL = getattr(settings, "SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")


def organization_jsonld() -> dict:
    return {
        "@type": "Organization",
        "@id": f"{SITE_BASE_URL}/#organization",
        "name": content.SITE["name"],
        "url": SITE_BASE_URL,
        "logo": f"{SITE_BASE_URL}/logos/favicon.svg",
        "description": content.HOME_SEO.get("description", ""),
        "sameAs": [
            "https://www.linkedin.com/company/urbanrupeex/",
            "https://youtube.com/@urbanrupee.1",
            "https://www.facebook.com/profile.php?id=61586173843401",
            "https://www.instagram.com/urbanrupee_",
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "A01 & A03, UG, Tower 3, NX-One, Techzone 4",
            "addressLocality": "Greater Noida",
            "addressRegion": "Uttar Pradesh",
            "postalCode": "201301",
            "addressCountry": "IN",
        },
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
    if slug and seo.get("service_type"):
        data["mainEntity"] = {"@id": f"{page_id}#service"}
    return data


def service_jsonld(seo: dict, slug: str) -> dict | None:
    service_type = seo.get("service_type")
    if not service_type:
        return None
    page_id = seo.get("canonical", SITE_BASE_URL)
    return {
        "@type": "Service",
        "@id": f"{page_id}#service",
        "name": seo.get("h1", seo.get("title", "")),
        "serviceType": service_type,
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


def _nav_url(href: str) -> str:
    if href.startswith("http"):
        return href
    return f"{SITE_BASE_URL}{href}" if href.startswith("/") else f"{SITE_BASE_URL}/{href}"


def faq_page_jsonld(items: list[dict] | None = None, page_url: str | None = None) -> dict:
    """FAQ rich results — similar to Razorpay 'People also ask' eligibility."""
    if items is None:
        items = content.FAQS.get("items", [])[:6]
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq" if page_url else f"{SITE_BASE_URL}/#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"],
                },
            }
            for item in items
        ],
    }


def site_navigation_jsonld() -> list[dict]:
    """Primary nav URLs — helps Google understand key pages for sitelinks."""
    links = [
        {"name": "Login", "href": content.SITE["sign_in_url"]},
        {"name": "Products", "href": "/products"},
        {"name": "Contact", "href": content.NAV["contact_href"]},
        {"name": "Resources", "href": "/resources"},
        {"name": "About Us", "href": "/about"},
        {"name": "Payment Gateway", "href": "/products/orchestration"},
        {"name": "FAQ", "href": "/faq"},
        *[
            {"name": item["label"], "href": item["href"]}
            for item in content.NAV["products"]
            if item["href"] != "/products"
        ],
        *[{"name": item["label"], "href": item["href"]} for item in content.NAV["resources"]],
        *[{"name": item["label"], "href": item["href"]} for item in content.NAV["services"]],
    ]
    seen: set[str] = set()
    nodes: list[dict] = []
    for link in links:
        url = _nav_url(link["href"])
        if url in seen:
            continue
        seen.add(url)
        nodes.append({
            "@type": "SiteNavigationElement",
            "@id": f"{url}#navigation",
            "name": link["name"],
            "url": url,
            "isPartOf": {"@id": f"{SITE_BASE_URL}/#website"},
        })
    return nodes


def main_sections_itemlist() -> dict:
    """Homepage section list — contact, products hub links, resources."""
    sections = [
        {"name": "Login", "href": content.SITE["sign_in_url"]},
        {"name": "Products", "href": "/products"},
        {"name": "Contact", "href": content.NAV["contact_href"]},
        {"name": "Resources", "href": "/resources"},
        {"name": "FAQ", "href": "/faq"},
        {"name": "Payment Orchestration", "href": "/products/orchestration"},
    ]
    return {
        "@type": "ItemList",
        "@id": f"{SITE_BASE_URL}/#main-sections",
        "name": "Urbanrupee site sections",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item["name"],
                "url": _nav_url(item["href"]),
            }
            for index, item in enumerate(sections)
        ],
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
    if slug is None:
        graph.extend(site_navigation_jsonld())
        graph.append(main_sections_itemlist())
        graph.append(faq_page_jsonld())
    service = service_jsonld(seo, slug) if slug else None
    if service:
        graph.append(service)
    page_faqs = page_faq_items(slug) if slug else []
    if page_faqs:
        graph.append(faq_page_jsonld(page_faqs, canonical))
    return graph


def structured_data_script(slug: str | None, page: dict, seo: dict) -> str:
    graph = structured_data_graph(slug, page, seo)
    payload = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    return json.dumps(payload, ensure_ascii=False)
