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
    "close-route-wallet",
    "unified-dashboard",
})
RESOURCE_SLUGS = frozenset({"faq", "blog", "privacy-policy", "terms-and-conditions"})
CONTACT_SLUGS = frozenset({"contact"})
SERVICE_SLUGS = frozenset({
    "collections",
    "payouts",
    "financial-operations",
    "risk-fraud-management",
    "reconciliation",
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
    "terms-and-conditions": ("Resources", "/terms-and-conditions"),
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
            "label": "Collections",
            "href": "/services/collections",
            "description": "Accept, track, and reconcile payments across channels.",
        },
    ],
    "white-label-platform": [
        {
            "label": "Custom Checkout",
            "href": "/products/custom-checkout",
            "description": "Tailored checkout experiences for your merchants.",
        },
        {
            "label": "Payouts",
            "href": "/services/payouts",
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
            "label": "Collections",
            "href": "/services/collections",
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
    "payouts": [
        {
            "label": "Close Route Wallet",
            "href": "/products/wallet",
            "description": "Wallet balances and payout controls.",
        },
        {
            "label": "Financial Operations Infrastructure",
            "href": "/services/financial-operations",
            "description": "Match payouts with settlements automatically.",
        },
        {
            "label": "White Label Platform",
            "href": "/products/white-label",
            "description": "Offer payouts under your brand.",
        },
    ],
    "unified-dashboard": [
        {
            "label": "Payment Orchestration",
            "href": "/products/orchestration",
            "description": "Route transactions across PSPs for higher success rates.",
        },
        {
            "label": "Financial Operations",
            "href": "/services/financial-operations",
            "description": "Collections, payouts, and settlement operations in one layer.",
        },
        {
            "label": "Reconciliation",
            "href": "/services/reconciliation",
            "description": "Match transactions and settle exceptions faster.",
        },
    ],
    "close-route-wallet": [
        {
            "label": "Payouts",
            "href": "/services/payouts",
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
    "collections": [
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
    "financial-operations": [
        {
            "label": "Collections",
            "href": "/services/collections",
            "description": "Digital collections with compliance built in.",
        },
        {
            "label": "Payouts",
            "href": "/services/payouts",
            "description": "Disburse funds to vendors, partners, and beneficiaries.",
        },
        {
            "label": "Reconciliation",
            "href": "/services/reconciliation",
            "description": "Match transactions and settlements in one layer.",
        },
    ],
    "risk-fraud-management": [
        {
            "label": "Collections",
            "href": "/services/collections",
            "description": "Digital collections with compliance built in.",
        },
        {
            "label": "Payouts",
            "href": "/services/payouts",
            "description": "Disburse funds to vendors, partners, and beneficiaries.",
        },
        {
            "label": "Reconciliation",
            "href": "/services/reconciliation",
            "description": "Match transactions and settlements in one layer.",
        },
    ],
    "reconciliation": [
        {
            "label": "Collections",
            "href": "/services/collections",
            "description": "Digital collections with compliance built in.",
        },
        {
            "label": "Payouts",
            "href": "/services/payouts",
            "description": "Disburse funds to vendors, partners, and beneficiaries.",
        },
        {
            "label": "Risk & Fraud Management",
            "href": "/services/risk-fraud-management",
            "description": "Detect risk and protect every transaction.",
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
            "label": "Collections",
            "href": "/services/collections",
            "description": "Digital collections infrastructure.",
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
            "label": "Collections",
            "href": "/services/collections",
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
    "terms-and-conditions": [
        {
            "label": "Privacy Policy",
            "href": "/privacy-policy",
            "description": "How Urbanrupee collects, uses, and protects your data.",
        },
        {
            "label": "Contact",
            "href": "/contact",
            "description": "Questions about legal terms or service usage.",
        },
        {
            "label": "FAQ",
            "href": "/faq",
            "description": "Common questions about Urbanrupee.",
        },
    ],
}

# slug -> { title, description, h1, keywords?, service_type? }
# h1 must match the visible PageHero heading (page.title) on each route.
# keywords: a short list (<= 8) of terms the page's copy already supports; Google
# ignores meta keywords, so these are for other engines only — never stuff them.
# service_type: set only on pages describing a real Urbanrupee service (Service JSON-LD).
PAGE_SEO = {
    "about": {
        "title": "About Urbanrupee | Payment Technology Company India",
        "description": (
            "Urbanrupee is a payment technology company in India building secure, scalable "
            "infrastructure for payment orchestration, checkout, payouts, and reconciliation."
        ),
        "h1": "Powering the Future of Digital Payments",
        "keywords": [
            "payment technology company India",
            "payment infrastructure India",
            "fintech payment platform India",
            "digital payment platform India",
        ],
    },
    "collections": {
        "title": "Online Payment Collection Platform India | Urbanrupee",
        "description": (
            "Accept, track, and reconcile online payments across UPI, cards, net banking, "
            "wallets, and EMI from a single API with Urbanrupee Collections."
        ),
        "h1": "Collect Payments. Simplify Operations. Accelerate Growth from single API.",
        "keywords": [
            "online payment collection India",
            "payment collection platform",
            "online payment processing India",
            "UPI payment collection",
            "digital payment platform India",
        ],
        "service_type": "Online payment collection",
    },
    "payouts": {
        "title": "Payout Platform India | Bulk & Instant Payouts | Urbanrupee",
        "description": (
            "Send bulk, instant, and scheduled payouts to vendors, employees, and partners over "
            "UPI, bank transfer, cards, and wallets with real-time tracking."
        ),
        "h1": "Send every payout faster with greater control and visibility",
        "keywords": [
            "payout platform India",
            "bulk payout solution",
            "instant payout platform",
            "automated payouts India",
            "payment disbursement platform",
        ],
        "service_type": "Payouts and disbursements",
    },
    "financial-operations": {
        "title": "Financial Operations Infrastructure India | Urbanrupee",
        "description": (
            "Embed collections, payouts, reconciliation, and financial workflows into your "
            "product with Urbanrupee's ready-to-integrate financial infrastructure."
        ),
        "h1": "Build Smarter Financial Experiences Without Building the Infrastructure",
        "keywords": [
            "financial operations infrastructure",
            "payment infrastructure for fintech",
            "fintech payment infrastructure",
            "embedded finance platform India",
        ],
        "service_type": "Financial operations infrastructure",
    },
    "risk-fraud-management": {
        "title": "Payment Risk & Fraud Management India | Urbanrupee",
        "description": (
            "Detect suspicious transactions in real time with Urbanrupee risk monitoring across "
            "IP, location, and payment patterns, plus chargeback visibility."
        ),
        "h1": "Stay Ahead of Risk. Protect Every Transaction.",
        "keywords": [
            "payment fraud detection",
            "payment risk management",
            "fraud management India",
            "transaction monitoring",
            "chargeback risk management",
        ],
        "service_type": "Payment risk and fraud management",
    },
    "reconciliation": {
        "title": "Payment Reconciliation Software India | Urbanrupee",
        "description": (
            "Automate payment reconciliation with Urbanrupee: match transactions to settlements, "
            "flag mismatches and exceptions, and resolve discrepancies faster."
        ),
        "h1": "One Connected Layer for Reconciliation",
        "keywords": [
            "payment reconciliation software",
            "automated payment reconciliation",
            "payment settlement reconciliation",
            "transaction reconciliation",
            "payment reconciliation India",
        ],
        "service_type": "Payment reconciliation",
    },
    "products-index": {
        "title": "Urbanrupee Payment Products | Checkout, UPI & Payouts",
        "description": (
            "Explore Urbanrupee payment products: orchestration, Hyper Checkout, custom checkout, "
            "UPI switch, white label, payouts, wallets, and EMI for India."
        ),
        "h1": "Urbanrupee Payment Products",
        "keywords": [
            "payment products India",
            "payment platform India",
            "payment orchestration platform",
            "payment checkout solution",
            "payout platform India",
        ],
    },
    "resources-index": {
        "title": "Urbanrupee Resources | FAQ, Blog & Guides",
        "description": (
            "Urbanrupee resources: FAQs, blog posts, and guides on payment gateways, UPI, checkout, "
            "orchestration, and fintech for Indian businesses."
        ),
        "h1": "Urbanrupee Resources",
        "keywords": [
            "payment guides India",
            "payments FAQ",
            "fintech blog India",
        ],
    },
    "white-label-platform": {
        "title": "White Label Payment Platform India | Urbanrupee",
        "description": (
            "Launch a branded payment platform with Urbanrupee white label: your logo and "
            "colours, configurable features, and managed payment infrastructure."
        ),
        "h1": "White Label Solutions",
        "keywords": [
            "white label payment platform India",
            "white label payment solution",
            "branded payment platform",
            "white label fintech platform",
            "payment platform under your brand",
        ],
        "service_type": "White label payment platform",
    },
    "custom-checkout": {
        "title": "Custom Payment Checkout & Branded Payment Page | Urbanrupee",
        "description": (
            "Build a branded checkout with Urbanrupee: custom layout, your logo, and UPI, cards, "
            "net banking, wallets, and EMI, with no third-party redirect."
        ),
        "h1": "Customized Checkout Solutions",
        "keywords": [
            "custom payment checkout",
            "branded checkout",
            "custom payment page",
            "payment checkout solution",
            "online checkout solution India",
        ],
        "service_type": "Custom payment checkout",
    },
    "hyper-checkout": {
        "title": "Hyper Checkout: High-Conversion Checkout | Urbanrupee",
        "description": (
            "Urbanrupee Hyper Checkout speeds up UPI, card, net banking, wallet, and EMI payments "
            "with smart routing and one-click flows for higher conversion."
        ),
        "h1": "Hyper Checkout Experience",
        "keywords": [
            "hyper checkout",
            "high conversion checkout",
            "fast payment checkout",
            "one click payment checkout",
            "payment checkout optimization",
            "UPI checkout",
        ],
        "service_type": "High-conversion payment checkout",
    },
    "payment-orchestration": {
        "title": "Payment Orchestration Platform India | Urbanrupee",
        "description": (
            "Connect multiple payment providers, route transactions with smart rules, recover "
            "failed payments with failover, and improve payment success rates."
        ),
        "h1": "Simplify and optimize your payments with your rules.",
        "keywords": [
            "payment orchestration platform India",
            "payment orchestration",
            "smart payment routing",
            "intelligent payment routing",
            "multi gateway payment platform",
            "payment failover",
        ],
        "service_type": "Payment orchestration",
    },
    "unified-dashboard": {
        "title": "Unified Payment Dashboard & Analytics | Urbanrupee",
        "description": (
            "Track transactions, settlements, MIDs, routing, chargebacks, and payment performance "
            "in one Urbanrupee dashboard built for payment operations."
        ),
        "h1": "One Dashboard. Complete Payment Visibility.",
        "keywords": [
            "unified payment dashboard",
            "payment analytics dashboard",
            "payment operations dashboard",
            "transaction analytics platform",
            "payment reporting platform",
        ],
        "service_type": "Payment analytics dashboard",
    },
    "close-route-wallet": {
        "title": "Closed-Loop Wallet Infrastructure India | Urbanrupee",
        "description": (
            "Run secure closed-loop wallet programs with Urbanrupee Close Route Wallet: "
            "ledger-based control, spending limits, approved routes, and full visibility."
        ),
        "h1": "Close Route Wallet",
        "keywords": [
            "closed loop wallet",
            "closed loop wallet platform",
            "wallet infrastructure India",
            "digital wallet platform",
        ],
        "service_type": "Closed-loop wallet infrastructure",
    },
    "upi-switch": {
        "title": "UPI Switch & UPI Payment Routing India | Urbanrupee",
        "description": (
            "Connect, route, and manage UPI payments through Urbanrupee UPI Switch, with intent "
            "and QR journeys, smart routing, and real-time visibility."
        ),
        "h1": "Power every UPI transaction with smarter switching",
        "keywords": [
            "UPI switch",
            "UPI payment routing",
            "UPI payment infrastructure",
            "UPI payment processing platform",
            "UPI intent",
            "UPI QR payment",
        ],
        "service_type": "UPI payment switching",
    },
    "affordability": {
        "title": "EMI, Cardless EMI & BNPL at Checkout | Urbanrupee",
        "description": (
            "Offer EMI, cardless EMI, and Buy Now Pay Later at checkout with Urbanrupee to lift "
            "conversions and order value, with real-time eligibility checks."
        ),
        "h1": "Affordability Solutions",
        "keywords": [
            "EMI at checkout",
            "cardless EMI",
            "buy now pay later India",
            "BNPL checkout",
            "EMI payment option",
        ],
        "service_type": "EMI and Buy Now Pay Later",
    },
    "faq": {
        "title": "FAQ | Urbanrupee Payment Solutions",
        "description": (
            "Answers to common questions about Urbanrupee payment orchestration, UPI, checkout, "
            "payouts, integration, security, and onboarding for businesses."
        ),
        "h1": "Frequently Asked Questions",
        "keywords": [
            "Urbanrupee FAQ",
            "payment orchestration FAQ",
            "UPI payments FAQ",
        ],
    },
    "blog": {
        "title": "Blog | Urbanrupee Payments & Fintech Insights",
        "description": (
            "Urbanrupee blog: insights on payment gateways, UPI, checkout optimization, "
            "orchestration, compliance, and fintech trends for Indian businesses."
        ),
        "h1": "Urbanrupee Blog",
        "keywords": [
            "payments blog India",
            "fintech insights India",
            "payment orchestration guide",
        ],
    },
    "privacy-policy": {
        "title": "Privacy Policy | Urbanrupee",
        "description": (
            "How Urbanrupee collects, uses, shares, and protects your information across our "
            "website and payment services, and the privacy rights you have."
        ),
        "h1": "Privacy Policy",
    },
    "terms-and-conditions": {
        "title": "Terms and Conditions | Urbanrupee",
        "description": (
            "Terms governing use of Urbanrupee's website, payment platform, checkout, payouts, "
            "APIs, reconciliation, dashboards, and merchant tools."
        ),
        "h1": "Terms and Conditions",
    },
    "contact": {
        "title": "Contact Urbanrupee | Payment Solutions Demo & Support",
        "description": (
            "Contact Urbanrupee for product demos, merchant onboarding, and support for payment "
            "orchestration, UPI, checkout, and payouts. Based in Greater Noida."
        ),
        "h1": "Let’s Start a Conversation",
        "keywords": [
            "contact Urbanrupee",
            "payment solutions demo",
            "merchant onboarding India",
        ],
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
        "keywords": ", ".join(meta.get("keywords", [])),
        "service_type": meta.get("service_type", ""),
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
