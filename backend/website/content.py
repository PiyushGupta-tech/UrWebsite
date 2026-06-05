"""Urbanrupee marketing content — Urbanrupee.com + product catalogue."""

from .catalogue import CATALOGUE_TAGLINE, PRODUCT_SUITE
from .dashboard_demo import DASHBOARD_DEMO
from .merchant_map import MERCHANT_MAP

SITE = {
    "name": "Urbanrupee",
    "tagline": "Unified Payment Ecosystem · Product Catalogue",
    "sign_in_url": "https://merchant.urbanrupee.in/login",
    "get_started_url": "/contact",
    "copyright": "Copyright © 2025 Urbanrupee Techsolution Pvt Ltd. All rights reserved.",
    "footer_blurb": CATALOGUE_TAGLINE,
    "certifications": ["PCI DSS Compliant", "ISO 27001:2022 Certification"],
}

NAV = {
    "links": [
        {"label": "Home", "href": "/"},
        {"label": "About Us", "href": "/about"},
    ],
    "services": [
        {"label": "Payment Services", "href": "/services/payment"},
        {"label": "AML Detector", "href": "/services/aml"},
        {"label": "Automatic Reconciliation", "href": "/services/reconciliation"},
    ],
    "products": [
        {"label": "Payment Orchestration", "href": "/products/orchestration"},
        {"label": "White Label Platform", "href": "/products/white-label"},
        {"label": "Payout Portal", "href": "/products/payout"},
        {"label": "Close Route Wallet", "href": "/products/wallet"},
        {"label": "Hyper Checkout", "href": "/products/hyper-checkout"},
        {"label": "Custom Checkout", "href": "/products/custom-checkout"},
        {"label": "UPI Switch", "href": "/products/upi-switch"},
        {"label": "Affordability (EMI & Pay Later)", "href": "/products/affordability"},
    ],
    "resources": [
        {"label": "FAQ", "href": "/faq"},
        {"label": "Blog", "href": "/blog"},
        {"label": "Privacy Policy", "href": "/privacy-policy"},
    ],
    "contact_href": "/contact",
}

HOME_SEO = {
    "title": "Best Payment Gateway in India | Urbanrupee",
    "description": (
        "Urbanrupee provides secure payment gateway solutions with UPI, cards, net banking, "
        "high success rates, fast settlements and seamless onboarding for businesses across India."
    ),
}

HERO = {
    "headline": "Best Payment Gateway in India for Growing Businesses",
    "subheadline": (
        "Urbanrupee provides secure payment gateway solutions with UPI, cards, net banking, "
        "high success rates, fast settlements and seamless onboarding for businesses across India."
    ),
    "cta_primary": "Get Started",
    "cta_secondary": "Sign In",
    "social_proof": "Trusted by businesses across India",
    "fee_chips": [
        {"label": "UPI", "value": "Low MDR"},
        {"label": "Cards", "value": "Competitive rates"},
        {"label": "Net Banking", "value": "1-tap checkout"},
        {"label": "Wallets", "value": "All major brands"},
    ],
    "badges": [
        "Payment Orchestration",
        "UPI Switch",
        "Hyper Checkout",
        "White Label",
        "Affordability",
    ],
}

PRODUCT_CATALOGUE = PRODUCT_SUITE
DASHBOARD_PREVIEW = DASHBOARD_DEMO

PAYMENT_SOLUTION = {
    "eyebrow": "SMART PAYMENT ECOSYSTEM",
    "title": "Smart Payment Experiences Designed for Modern Businesses",
    "feature_title": "Secure & High-Performance Infrastructure for Modern Payments",
    "feature_body": (
        "From startups to enterprises, our payment ecosystem helps businesses simplify "
        "operations, improve success rates, and enhance customer trust."
    ),
    "bullets": [
        "UPI, cards, wallets, and net banking in one stack",
        "Intelligent routing for better success rates",
        "Automated reconciliation and reporting",
        "Secure onboarding and compliant workflows",
        "Optimized checkout experience for customers",
    ],
    "closing": (
        "Secure and scalable payment solutions designed to improve customer trust and transaction success."
    ),
    "merchant_map": MERCHANT_MAP,
}

BANKING_PARTNERS = [
    "Airpay",
    "Easebuzz",
    "Cashfree Payments",
    "Jio Pay",
    "PayU",
    "IDFC First Bank",
    "Kotak Mahindra Bank",
    "Unlimit",
]

MERCHANT_PARTNERS = [
    "Bharat COD",
    "Green Web Solutions",
    "Groots Pay",
    "Paidkiya",
    "BingoPay",
    "AAI Wallet",
    "BB Pay",
    "Indyapay",
]

FEATURES = {
    "eyebrow": "From the Product Catalogue",
    "title": "Powerful Products Designed for Faster, Smarter Payments",
    "items": [
        {
            "title": "Payout Portal",
            "body": (
                "Simplify vendor, merchant, and customer payouts through one centralized payout "
                "management platform with automated workflows and real-time visibility."
            ),
        },
        {
            "title": "Seamless UPI Switch",
            "body": (
                "A high-performance UPI infrastructure built to deliver faster transaction processing, "
                "intelligent routing, and reliable uptime even during peak traffic."
            ),
        },
        {
            "title": "Affordability",
            "body": (
                "Offer flexible EMI and Pay Later solutions that improve affordability, increase "
                "order values, and enhance customer retention."
            ),
        },
    ],
}

STATS = [
    {"value": "75%", "label": "Candidate match rate"},
    {"value": "02+", "label": "Years of experience as a PSP"},
    {"value": "30+", "label": "Our Partner Banks"},
]

WHY_CHOOSE = {
    "eyebrow": "Why Choose Urbanrupee?",
    "title": "Built for businesses that demand reliability, security, and scale",
    "items": [
        {
            "title": "Bank-Grade Security",
            "body": (
                "PCI DSS compliant infrastructure with end-to-end encryption. Your "
                "transactions and data are protected with industry-leading security standards."
            ),
        },
        {
            "title": "Lightning Fast",
            "body": (
                "Process payments in milliseconds with our optimized infrastructure. "
                "Real-time settlements and instant notifications keep your business moving."
            ),
        },
        {
            "title": "Scalable Infrastructure",
            "body": (
                "Built to handle millions of transactions. Scale from startup to enterprise "
                "without worrying about infrastructure limitations."
            ),
        },
        {
            "title": "24/7 Support",
            "body": (
                "Our dedicated support team is available around the clock to assist you "
                "with technical issues, integrations, and business queries."
            ),
        },
        {
            "title": "Easy Integration",
            "body": (
                "Developer-friendly APIs and comprehensive documentation. Get up and "
                "running in minutes, not weeks."
            ),
        },
        {
            "title": "Real-time Analytics & Insights",
            "body": (
                "Comprehensive dashboards with real-time transaction monitoring, detailed "
                "reports, and actionable insights to optimize your payment performance "
                "and business growth."
            ),
        },
    ],
}

TESTIMONIALS = {
    "title": "Our beloved clients share their Urbanrupee experience",
    "videos": [
        {
            "video": "/videos/testimonials/finlix.mp4",
            "name": "Finlix Capital",
            "role": "Urbanrupee Partner",
        },
        {
            "video": "/videos/testimonials/grootspay.mov",
            "name": "Groots Pay",
            "role": "Urbanrupee Partner",
        },
    ],
    "quotes": [
        {
            "title": "Game-Changing Payment Solution!",
            "quote": (
                "Integrating Urbanrupee's payment gateway was surprisingly smooth for our "
                "website. Our customers appreciate the easy checkout, and the dashboard "
                "makes tracking payments simple. Their support team is also very helpful!"
            ),
            "name": "Priya Sharma",
            "role": "E-commerce Store Owner",
        },
        {
            "title": "Enterprise-Grade Security!",
            "quote": (
                "Security was key for our business. Urbanrupee, as a Payment Service Provider, "
                "provides a robust and secure payment environment. We trust them completely "
                "with our transactions. The setup was straightforward, and it works flawlessly."
            ),
            "name": "Vikram Singh",
            "role": "Financial Services Director",
        },
    ],
}

FAQS = {
    "eyebrow": "Our Questions & Answers",
    "items": [
        {
            "question": "How can I add money to my Urbanrupee wallet?",
            "answer": (
                "You can easily add money to your Urbanrupee wallet using various methods "
                "like UPI, Net Banking, Debit Cards, or Credit Cards. Simply navigate to the "
                "'Wallet' section in our app or website, select 'Add Money', enter the desired "
                "amount, choose your preferred payment method, and follow the secure steps "
                "to complete the transaction."
            ),
        },
        {
            "question": "How do I create my Urbanrupee account?",
            "answer": (
                "Creating your Urbanrupee account is quick and easy. Download our mobile app "
                "or visit our website. Click on 'Sign Up' or 'Register'. You'll need to provide "
                "your mobile number, verify it with an OTP (One-Time Password), and set a secure "
                "password. Follow the on-screen instructions to complete your profile setup."
            ),
        },
        {
            "question": "How can I view my transaction history?",
            "answer": (
                "To view your transaction history with Urbanrupee, go to the 'Transaction History' "
                "or 'My Orders' section within our app or website. Here you can see details of "
                "all your past payments and recharges made through Urbanrupee."
            ),
        },
        {
            "question": "Is it safe to make payments online with Urbanrupee?",
            "answer": (
                "Yes, making payments through Urbanrupee is secure. We prioritize your safety "
                "by using industry-standard security measures, including SSL encryption for data "
                "transmission and compliance with relevant payment security standards (like PCI DSS). "
                "We also employ robust fraud detection mechanisms to protect your account and "
                "transactions. Always ensure you are using a secure network and keep your login "
                "credentials confidential."
            ),
        },
        {
            "question": "Can I make payments using my phone through Urbanrupee?",
            "answer": (
                "Yes, absolutely! You can conveniently make payments using your smartphone through "
                "the Urbanrupee mobile app. Simply log in, navigate to the relevant payment section, "
                "enter the required details, and proceed to pay using your wallet balance, UPI, "
                "linked bank accounts, or saved cards."
            ),
        },
    ],
}

FOOTER = {
    "company": [
        {"label": "Our Team", "href": "/team"},
        {"label": "Privacy Policy", "href": "/privacy-policy"},
        {"label": "Contact Us", "href": "/contact"},
    ],
    "services": NAV["services"],
    "products": NAV["products"],
}

CHECKOUT_DEMO = {
    "merchant": "Urbanrupee Merchant",
    "merchant_email": "payments@urbanrupee.com",
    "customer": "Your Customer",
    "customer_email": "customer@example.com",
    "amount": "₹24,999.00",
    "amount_raw": "24999.00",
    "due_date": "May 30, 2026",
    "invoice_no": "UR-0001",
    "order_id": "UR722026051910375191393",
    "merchant_id": "UR72",
    "currency": "INR",
    "payment_note": "Payment to Demo",
    "rotate_interval_ms": 5000,
    "payment_methods": [
        {"id": "upi", "label": "UPI", "icon": "upi"},
        {"id": "cards", "label": "Cards", "icon": "card"},
        {"id": "netbanking", "label": "Netbanking", "icon": "bank"},
        {"id": "wallets", "label": "Wallets", "icon": "wallet"},
        {"id": "emi", "label": "EMI", "icon": "emi"},
    ],
}

PROBLEM_TRIO = {
    "title": "Legacy payment stacks are slow, expensive, and fragmented",
    "items": [
        {
            "title": "Slow",
            "body": (
                "Your customers expect instant UPI and cards—but you're stuck reconciling "
                "multiple gateways and waiting on settlements."
            ),
        },
        {
            "title": "Expensive",
            "body": (
                "You pay platform fees, gateway charges, and hidden FX spreads—without "
                "the unified reporting you actually need."
            ),
        },
        {
            "title": "Confusing",
            "body": (
                "You need one orchestration layer—not five dashboards, three vendors, "
                "and a migration project every year."
            ),
        },
    ],
}

VALUE_PROP = {
    "headline": "Unified Payments Infrastructure for Modern Businesses",
    "subheadline": (
        "Urbanrupee is a unified payment ecosystem that combines payment processing, smart "
        "routing, reconciliation, analytics, and settlement management into one seamless platform "
        "enabling businesses to accept payments across UPI, cards, wallets, net banking, and EMI "
        "options with speed, security, reliability, and enhanced transaction success rates."
    ),
    "bullets": [
        "Single API integration for UPI, cards, wallets, and net banking",
        "Intelligent routing for higher transaction success rates",
        "Real-time settlement tracking and reporting",
        "PCI DSS & ISO 27001 certified security standards",
        "White-label checkout and payout solutions",
        "Automated reconciliation and fraud monitoring",
        "Dedicated onboarding and 24/7 support assistance",
    ],
    "cta": "Get Started",
}

PERSONAS = [
    {
        "title": "E-commerce",
        "body": "Boost conversions with fast checkouts, multiple payment methods, and higher transaction success rates.",
    },
    {
        "title": "SaaS & Startups",
        "body": "Launch and scale quickly with developer-friendly APIs, smart billing systems, and real-time payment visibility.",
    },
    {
        "title": "Marketplaces",
        "body": "Manage split settlements, vendor payouts, and transaction reconciliation through one unified platform.",
    },
    {
        "title": "Enterprises",
        "body": "Enterprise-grade infrastructure with advanced security, scalable architecture, and dedicated support.",
    },
    {
        "title": "Fintechs",
        "body": "Build white-label payment experiences, wallet systems, and embedded financial solutions under your own brand.",
    },
    {
        "title": "Retail & COD",
        "body": "Enable seamless online and offline payment experiences with wallet integrations, COD support, and faster settlements.",
    },
]
