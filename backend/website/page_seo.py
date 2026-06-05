"""Per-page SEO metadata — title, description, H1, canonical path."""

from .page_content import PAGES, ROUTE_SLUGS, SLUG_TO_ROUTE

# Slugs that receive server-injected meta (products, resources, contact).
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
RESOURCE_SLUGS = frozenset({"faq", "blog", "privacy-policy"})
CONTACT_SLUGS = frozenset({"contact"})
SERVICE_SLUGS = frozenset({
    "payment-services",
    "aml-detector",
    "automatic-reconciliation",
})
HUB_SLUGS = frozenset({"products-index", "resources-index"})

SEO_INJECT_SLUGS = (
    PRODUCT_SLUGS
    | RESOURCE_SLUGS
    | CONTACT_SLUGS
    | SERVICE_SLUGS
    | HUB_SLUGS
    | frozenset({"about"})
)

PAGE_SECTION = {
    "products-index": ("Products", "/products"),
    "resources-index": ("Resources", "/resources"),
    **{slug: ("Products", None) for slug in PRODUCT_SLUGS},
    **{slug: ("Services", None) for slug in SERVICE_SLUGS},
    "faq": ("Resources", "/faq"),
    "blog": ("Resources", "/blog"),
    "privacy-policy": ("Resources", "/privacy-policy"),
    "about": ("Company", "/about"),
    "contact": ("Contact", "/contact"),
}

RELATED_LINKS = {
    "hyper-checkout": [
        {
            "label": "Custom Checkout",
            "href": "/products/custom-checkout",
            "description": "Branded on-site checkout with UPI, cards, and wallets.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Route transactions across PSPs for higher success rates.",
        },
        {
            "label": "Affordability",
            "href": "/products/affordability",
            "description": "EMI and BNPL options at checkout.",
        },
    ],
    "custom-checkout": [
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "One-click UPI and fast payment flows.",
        },
        {
            "label": "White Label Platform",
            "href": "/products/white-label",
            "description": "Launch payments under your own brand.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Smart routing behind your checkout.",
        },
    ],
    "payment-orchestration": [
        {
            "label": "UPI Switch",
            "href": "/products/upi-switch",
            "description": "High-volume UPI routing and connectivity.",
        },
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Conversion-focused checkout on top of orchestration.",
        },
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "Full-stack gateway and infrastructure services.",
        },
    ],
    "white-label-platform": [
        {
            "label": "Custom Checkout",
            "href": "/products/custom-checkout",
            "description": "Tailored checkout experiences for your merchants.",
        },
        {
            "label": "Payout Portal",
            "href": "/products/payout",
            "description": "Automated disbursements and bulk payouts.",
        },
        {
            "label": "Close Route Wallet",
            "href": "/products/wallet",
            "description": "Controlled wallet infrastructure.",
        },
    ],
    "upi-switch": [
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Multi-rail routing beyond UPI.",
        },
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Fast UPI-first checkout for end customers.",
        },
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "Gateway services that pair with UPI Switch.",
        },
    ],
    "affordability": [
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Surface EMI and BNPL in the payment flow.",
        },
        {
            "label": "Custom Checkout",
            "href": "/products/custom-checkout",
            "description": "Embed affordability options in branded checkout.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Route affordability providers intelligently.",
        },
    ],
    "payout-portal": [
        {
            "label": "Close Route Wallet",
            "href": "/products/wallet",
            "description": "Wallet balances and payout controls.",
        },
        {
            "label": "Automatic Reconciliation",
            "href": "/services/reconciliation",
            "description": "Match payouts with settlements automatically.",
        },
        {
            "label": "White Label Platform",
            "href": "/products/white-label",
            "description": "Offer payouts under your brand.",
        },
    ],
    "close-route-wallet": [
        {
            "label": "Payout Portal",
            "href": "/products/payout",
            "description": "Disburse funds to vendors and customers.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Connect wallet flows with payment rails.",
        },
        {
            "label": "Custom Checkout",
            "href": "/products/custom-checkout",
            "description": "Wallet-aware checkout experiences.",
        },
    ],
    "payment-services": [
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "High-converting checkout for your gateway stack.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Orchestrate multiple PSP connections.",
        },
        {
            "label": "UPI Switch",
            "href": "/products/upi-switch",
            "description": "Enterprise UPI routing layer.",
        },
    ],
    "aml-detector": [
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "Gateway infrastructure with compliance built in.",
        },
        {
            "label": "Automatic Reconciliation",
            "href": "/services/reconciliation",
            "description": "Audit-ready reconciliation workflows.",
        },
        {
            "label": "Privacy Policy",
            "href": "/privacy-policy",
            "description": "How Urbanrupee protects your data.",
        },
    ],
    "automatic-reconciliation": [
        {
            "label": "Payout Portal",
            "href": "/products/payout",
            "description": "Reconcile payouts alongside collections.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Unified view across payment partners.",
        },
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "End-to-end payment operations.",
        },
    ],
    "faq": [
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Fast UPI, card, and wallet checkout.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Smart routing across payment providers.",
        },
        {
            "label": "Contact Urbanrupee",
            "href": "/contact",
            "description": "Talk to our team about onboarding.",
        },
    ],
    "blog": [
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Product page for orchestration solutions.",
        },
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Checkout product built for conversion.",
        },
        {
            "label": "FAQ",
            "href": "/faq",
            "description": "Common questions about Urbanrupee.",
        },
    ],
    "about": [
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "Core gateway and infrastructure services.",
        },
        {
            "label": "Product catalogue",
            "href": "/products/hyper-checkout",
            "description": "Explore Hyper Checkout and other products.",
        },
        {
            "label": "Contact",
            "href": "/contact",
            "description": "Request a demo or speak with sales.",
        },
    ],
    "products-index": [
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Intelligent routing across PSPs and banks.",
        },
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "Fast UPI and card checkout flows.",
        },
        {
            "label": "Contact Sales",
            "href": "/contact",
            "description": "Request a demo or speak with our team.",
        },
    ],
    "resources-index": [
        {
            "label": "FAQ",
            "href": "/faq",
            "description": "Common questions about Urbanrupee.",
        },
        {
            "label": "All Products",
            "href": "/products",
            "description": "Explore the full Urbanrupee product suite.",
        },
        {
            "label": "Contact",
            "href": "/contact",
            "description": "Get started with Urbanrupee.",
        },
    ],
    "contact": [
        {
            "label": "Hyper Checkout",
            "href": "/products/hyper-checkout",
            "description": "See our flagship checkout product.",
        },
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Learn about intelligent payment routing.",
        },
        {
            "label": "FAQ",
            "href": "/faq",
            "description": "Answers before you reach out.",
        },
    ],
    "privacy-policy": [
        {
            "label": "Payment Services",
            "href": "/services/payment",
            "description": "How Urbanrupee handles payment data.",
        },
        {
            "label": "Contact",
            "href": "/contact",
            "description": "Questions about privacy or data requests.",
        },
        {
            "label": "FAQ",
            "href": "/faq",
            "description": "Common questions about Urbanrupee.",
        },
    ],
}

# slug -> { title, description, h1 }
# h1 must match the visible PageHero heading (page.title) on each route.
PAGE_SEO = {
    "about": {
        "title": "About Urbanrupee | Payment Infrastructure Company India",
        "description": (
            "Learn about Urbanrupee — a unified payment ecosystem for orchestration, UPI, "
            "checkout, payouts, and white-label solutions built for businesses across India."
        ),
        "h1": "About Urbanrupee",
    },
    "payment-services": {
        "title": "Payment Gateway & Infrastructure India | Urbanrupee",
        "description": (
            "Urbanrupee payment services: UPI, cards, net banking, wallets, orchestration, and "
            "checkout with high success rates, fast settlements, and seamless onboarding."
        ),
        "h1": "Payment Infrastructure That Powers Growth",
    },
    "aml-detector": {
        "title": "AML Detector & Compliance Platform | Urbanrupee",
        "description": (
            "AI-powered AML detection and risk intelligence from Urbanrupee. Real-time monitoring, "
            "suspicious activity alerts, and regulatory compliance for Indian businesses."
        ),
        "h1": "AML Detector",
    },
    "automatic-reconciliation": {
        "title": "Automatic Payment Reconciliation | Urbanrupee",
        "description": (
            "Automate payment reconciliation with Urbanrupee. Match transactions, reduce manual "
            "effort, resolve discrepancies faster, and gain real-time financial visibility."
        ),
        "h1": "Automatic Reconciliation",
    },
    "products-index": {
        "title": "Urbanrupee Payment Products | Gateway, Checkout & UPI",
        "description": (
            "Explore Urbanrupee payment products — orchestration, Hyper Checkout, custom checkout, "
            "UPI switch, white-label platform, payouts, wallets, and EMI solutions for India."
        ),
        "h1": "Urbanrupee Payment Products",
    },
    "resources-index": {
        "title": "Urbanrupee Resources | FAQ, Blog & Guides",
        "description": (
            "Urbanrupee resources: FAQs, blog posts, and guides on payment gateways, UPI, checkout, "
            "orchestration, and fintech for Indian businesses."
        ),
        "h1": "Urbanrupee Resources",
    },
    "white-label-platform": {
        "title": "White Label Payment Platform | Urbanrupee",
        "description": (
            "Launch your branded payment platform with Urbanrupee white-label solutions. "
            "Custom UI, multi-rail acceptance, APIs, and scalable infrastructure under your brand."
        ),
        "h1": "White Label Solutions",
    },
    "custom-checkout": {
        "title": "Custom Checkout Solutions | Urbanrupee",
        "description": (
            "Urbanrupee custom checkout keeps customers on your site with branded payment flows, "
            "UPI, cards, net banking, wallets, EMI, and conversion-focused checkout design."
        ),
        "h1": "Customized Checkout Solutions",
    },
    "hyper-checkout": {
        "title": "Urbanrupee Hyper Checkout | UPI, Cards & Fast Payments",
        "description": (
            "Urbanrupee Hyper Checkout delivers faster UPI, card, net banking, wallet, and EMI "
            "payments with smart routing, one-click flows, and higher conversion rates."
        ),
        "h1": "Hyper Checkout Experience",
    },
    "payment-orchestration": {
        "title": "Payment Orchestration Platform | Urbanrupee",
        "description": (
            "Urbanrupee payment orchestration routes transactions intelligently across PSPs and "
            "banks to maximize success rates, uptime, and performance at scale."
        ),
        "h1": "Payment Orchestration Platform",
    },
    "payout-portal": {
        "title": "Payout Portal & Disbursements | Urbanrupee",
        "description": (
            "Urbanrupee Payout Portal simplifies vendor, merchant, and customer disbursements with "
            "automated workflows, bulk payouts, and real-time payout tracking."
        ),
        "h1": "Payout Portal",
    },
    "close-route-wallet": {
        "title": "Close Route Wallet | Urbanrupee",
        "description": (
            "Urbanrupee Close Route Wallet offers secure, controlled wallet infrastructure with "
            "real-time visibility, reconciliation, and operational control for businesses."
        ),
        "h1": "Close Route Wallet",
    },
    "upi-switch": {
        "title": "UPI Switch & Transaction Routing | Urbanrupee",
        "description": (
            "Urbanrupee UPI Switch provides high-volume UPI routing, multi-bank connectivity, "
            "low-latency processing, and enterprise-grade reliability for payment businesses."
        ),
        "h1": "Seamless UPI Switch",
    },
    "affordability": {
        "title": "EMI & BNPL Affordability Solutions | Urbanrupee",
        "description": (
            "Urbanrupee affordability solutions offer EMI, cardless EMI, and Buy Now Pay Later at "
            "checkout to increase AOV, conversions, and customer purchasing power."
        ),
        "h1": "Affordability Solutions",
    },
    "faq": {
        "title": "FAQ | Urbanrupee Payment Solutions",
        "description": (
            "Answers to common questions about Urbanrupee payment gateway, UPI, checkout, "
            "orchestration, payouts, integration, security, and onboarding for businesses."
        ),
        "h1": "Frequently Asked Questions",
    },
    "blog": {
        "title": "Blog | Urbanrupee Payments & Fintech Insights",
        "description": (
            "Urbanrupee blog: insights on payment gateways, UPI, checkout optimization, "
            "orchestration, compliance, and fintech trends for Indian businesses."
        ),
        "h1": "Urbanrupee Blog",
    },
    "privacy-policy": {
        "title": "Privacy Policy | Urbanrupee",
        "description": (
            "Urbanrupee privacy policy: how we collect, use, protect, and handle your data across "
            "our website and payment services. PCI-aware practices and your rights explained."
        ),
        "h1": "Privacy Policy",
    },
    "contact": {
        "title": "Contact Urbanrupee | Get Started",
        "description": (
            "Contact Urbanrupee for payment gateway demos, merchant onboarding, and support. "
            "Reach our team in Greater Noida for UPI, checkout, and payout solutions."
        ),
        "h1": "Connect with us",
    },
}


def resolve_page_seo(slug: str, page: dict) -> dict:
    """Return SEO payload for a page; falls back to page title if slug is not catalogued."""
    meta = PAGE_SEO.get(slug, {})
    route = SLUG_TO_ROUTE.get(slug, f"/{slug}")
    from django.conf import settings

    base = getattr(settings, "SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")
    canonical = f"{base}{route}" if route != "/" else f"{base}/"

    title = meta.get("title") or f"{page.get('title', 'Urbanrupee')} | Urbanrupee"
    description = meta.get("description") or ""
    h1 = meta.get("h1") or page.get("title", "")

    return {
        "title": title,
        "description": description,
        "h1": h1,
        "canonical": canonical,
        "path": route,
    }


def normalize_path(path: str) -> str:
    """Normalize request path for ROUTE_SLUGS lookup."""
    if not path or path == "/":
        return "/"
    return "/" + path.strip("/")


def slug_for_path(path: str) -> str | None:
    return ROUTE_SLUGS.get(normalize_path(path))


def breadcrumb_trail(slug: str | None, page: dict, seo: dict) -> list[dict]:
    """Phase 4 — breadcrumb trail for UI and JSON-LD."""
    if not slug:
        return [{"name": seo.get("h1", "Home"), "path": "/", "current": True}]

    trail = [{"name": "Home", "path": "/"}]
    section = PAGE_SECTION.get(slug)
    if section:
        label, section_path = section
        crumb = {"name": label}
        if section_path:
            crumb["path"] = section_path
        trail.append(crumb)

    trail.append({
        "name": seo.get("h1") or page.get("title", ""),
        "path": seo.get("path"),
        "current": True,
    })
    return trail


def related_links_for_slug(slug: str) -> list[dict]:
    """Phase 4 — curated cross-links to related products and pages."""
    return list(RELATED_LINKS.get(slug, []))


def page_context_for_slug(slug: str, page: dict) -> dict:
    """SEO plus Phase 4 enrichment for API and SPA."""
    seo = resolve_page_seo(slug, page)
    return {
        "seo": seo,
        "breadcrumbs": breadcrumb_trail(slug, page, seo),
        "related_links": related_links_for_slug(slug),
    }


def seo_for_path(path: str, *, home_seo: dict | None = None) -> dict | None:
    """Resolve SEO for a URL path. Homepage uses home_seo when provided."""
    normalized = normalize_path(path)
    if normalized == "/":
        return home_seo

    slug = slug_for_path(normalized)
    if not slug:
        return None

    page = PAGES.get(slug)
    if not page:
        return None

    return resolve_page_seo(slug, page)
