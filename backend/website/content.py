"""Urbanrupee marketing content — Urbanrupee.com + product catalogue."""

from .catalogue import CATALOGUE_TAGLINE, PRODUCT_SUITE
from .dashboard_demo import DASHBOARD_DEMO
from .merchant_map import MERCHANT_MAP

SITE = {
    "name": "Urbanrupee",
    "tagline": "Unified Payment Ecosystem · Product Catalogue",
    "website_url": "https://urbanrupee.com",
    "sign_in_url": "https://merchant.urbanrupee.in/login",
    "get_started_url": "/contact",
    "copyright": "Copyright © 2025 Urbanrupee Techsolution Pvt Ltd. All rights reserved.",
    "footer_blurb": CATALOGUE_TAGLINE,
    "certifications": ["PCI DSS Compliant", "ISO 27001:2022 Certification"],
    # Phase 6 — canonical product URLs for social, docs, and external listings
    "product_urls": {
        "hyper_checkout": "https://urbanrupee.com/products/hyper-checkout",
        "custom_checkout": "https://urbanrupee.com/products/custom-checkout",
        "orchestration": "https://urbanrupee.com/products/orchestration",
        "white_label": "https://urbanrupee.com/products/white-label",
        "upi_switch": "https://urbanrupee.com/products/upi-switch",
        "affordability": "https://urbanrupee.com/products/affordability",
        "payout_portal": "https://urbanrupee.com/products/payout",
        "close_route_wallet": "https://urbanrupee.com/products/wallet",
    },
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
        {"label": "All Products", "href": "/products"},
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
        {"label": "All Resources", "href": "/resources"},
        {"label": "FAQ", "href": "/faq"},
        {"label": "Blog", "href": "/blog"},
        {"label": "Privacy Policy", "href": "/privacy-policy"},
    ],
    "contact_href": "/contact",
}

HOME_SEO = {
    "title": "Urbanrupee",
    "description": (
        "Online payments India: accept UPI, cards, net banking and more with Urbanrupee's payment "
        "suite — orchestration, checkout, payouts, and analytics for growing businesses."
    ),
    "h1": "The Payment Infrastructure Built for Scale.",
    "canonical": "https://urbanrupee.com/",
    "path": "/",
}

HERO = {
    "headline": "The Payment Infrastructure Built for Scale.",
    "subheadline": (
        "UrbanRupee unifies payments, routing, payouts, and reconciliation to simplify operations "
        "and help businesses scale confidently."
    ),
    "cta_primary": "Talk to Expert",
    "cta_secondary": "Sign In",
    "compliance_badges": ["PCI-DSS COMPLIANT", "ISO CERTIFIED"],
    "social_proof": "Trusted by Leading Businesses",
    "fee_chips": [],
    "badges": [],
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
    {"value": "10M+", "label": "Transactions Processed"},
    {"value": "99.9%+", "label": "Payment Success Rate"},
    {"value": "₹1B+", "label": "Transaction Value Processed"},
    {"value": "<100ms", "label": "Average Processing Time"},
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
            "question": "What is Urbanrupee Hyper Checkout?",
            "answer": (
                "Hyper Checkout is Urbanrupee's fast payment experience for UPI, cards, net banking, "
                "wallets, and EMI — with smart routing and one-click flows designed to lift conversion."
            ),
            "links": [
                {"label": "Urbanrupee Hyper Checkout", "href": "/products/hyper-checkout"},
            ],
        },
        {
            "question": "What is payment orchestration?",
            "answer": (
                "Payment orchestration routes each transaction across multiple PSPs and banks to "
                "maximize success rates, uptime, and performance at scale."
            ),
            "links": [
                {"label": "Payment Orchestration Platform", "href": "/products/orchestration"},
            ],
        },
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
        {"label": "About Us", "href": "/about"},
        {"label": "Contact Us", "href": "/contact"},
        {"label": "Privacy Policy", "href": "/privacy-policy"},
    ],
    "services": NAV["services"],
    "products": NAV["products"],
    "resources": NAV["resources"],
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
    "title": "Your Payments Are Working. Your Infrastructure Is Holding You Back.",
    "intro": (
        "Multiple providers, fragmented systems, failed transactions, and manual operations "
        "make it harder to scale—and harder to know where your money is going."
    ),
    "items": [
        {
            "title": "Too Many Payment Partners",
            "body": (
                "Multiple PSPs, gateways, APIs, and dashboards create unnecessary "
                "integration and operational complexity."
            ),
            "icon": "partners",
        },
        {
            "title": "Payments Are Hard to Control",
            "body": (
                "Without intelligent routing and failover, you're dependent on individual "
                "providers when performance drops."
            ),
            "icon": "control",
        },
        {
            "title": "Failed Payments = Lost Revenue",
            "body": (
                "Declines, downtime, and poor routing can cost you customers and revenue "
                "every single day."
            ),
            "icon": "failed",
        },
        {
            "title": "Reconciliation Becomes Manual",
            "body": (
                "Transaction data, settlements, payouts, and refunds live across systems, "
                "making reconciliation slow and error-prone."
            ),
            "icon": "reconcile",
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

ECOSYSTEM = {
    "eyebrow": "Why us",
    "title": "The Payment Ecosystem Built Around You",
    "body": (
        "Accept, route, move, reconcile, and manage every payment flow through one unified "
        "infrastructure."
    ),
    "items": [
        {
            "number": "01",
            "title": "LOW MDR",
            "body": "Accept UPI, cards, wallets & EMI with competitive transaction costs.",
            "side": "left",
        },
        {
            "number": "02",
            "title": "ORCHESTRATE",
            "body": "Intelligent routing across multiple PSPs with automatic failover",
            "side": "left",
        },
        {
            "number": "03",
            "title": "CUSTOM CHECKOUT",
            "body": "Branded, high-converting checkout experiences built for your business.",
            "side": "left",
        },
        {
            "number": "04",
            "title": "PAYOUT",
            "body": "Move money faster with real-time payouts and settlement visibility.",
            "side": "right",
        },
        {
            "number": "05",
            "title": "RECONCILE",
            "body": "Bring transactions, settlements, refunds and payouts into one view.",
            "side": "right",
        },
        {
            "number": "06",
            "title": "ANALYZE",
            "body": "Turn payment data into actionable insights and better decisions.",
            "side": "right",
        },
    ],
}

PERFORM = {
    "title": "Payments That Perform. Operations That Scale.",
    "body": (
        "UrbanRupee helps you turn a fragmented payment stack into a simpler, more reliable "
        "infrastructure built for growth."
    ),
    "cta": "Talk to Expert",
    "cards": [
        {
            "title": "More Control Over Payments",
            "body": (
                "Choose how transactions are routed and optimize performance across your "
                "payment ecosystem."
            ),
            "graphic": "/images/figma-home/perform/graphic-control@2x.png",
        },
        {
            "title": "Higher Payment Success",
            "body": (
                "Recover more transactions with smarter routing, retries, and automatic failover."
            ),
            "graphic": "/images/figma-home/Frame%202147225707.svg",
        },
        {
            "title": "Faster & Cleaner Reconciliation",
            "body": "Get a unified view of transactions, settlements, refunds, and payouts.",
            "graphic": "/images/figma-home/perform/graphic-reconcile@2x.png",
        },
    ],
}

PRODUCTS = {
    "title": "Everything You Need to Power Payments.",
    "body": (
        "One unified infrastructure for payment acceptance, orchestration, payouts, checkout, "
        "reconciliation, and analytics — built to simplify operations and scale with your business."
    ),
    "cta": "Talk to Expert",
    "items": [
        {
            "title": "White Label Solutions",
            "body": (
                "Offer a complete payment experience under your own brand—without building the "
                "infrastructure from scratch."
            ),
            "image": "/images/figma-home/Frame%202147225785.svg",
            "points": [
                {
                    "title": "01 — Full Brand Control",
                    "body": "Your brand, your identity, your customer experience.",
                },
                {
                    "title": "02 — Your Choice of Services",
                    "body": "Choose the payment capabilities your business needs.",
                },
                {
                    "title": "03 — Smart Routing & Higher Success",
                    "body": (
                        "Optimize payment flows with intelligent routing and automatic failover."
                    ),
                },
            ],
        },
        {
            "title": "Custom Checkout",
            "body": (
                "Create a seamless, fully branded checkout experience that gives customers more "
                "ways to pay—while helping you convert more payment attempts into successful "
                "transactions."
            ),
            "image": "/images/figma-home/Frame%202147225787.svg",
            "points": [
                {
                    "title": "01 — Full Brand Control",
                    "body": (
                        "Customize the checkout to match your brand, colors, logo, and customer "
                        "journey."
                    ),
                },
                {
                    "title": "02 — Multiple Payment Methods",
                    "body": (
                        "Offer UPI, cards, net banking, wallets, EMI, and other payment options "
                        "in one checkout."
                    ),
                },
                {
                    "title": "03 — Secure by Design",
                    "body": (
                        "Deliver a trusted payment experience with secure payment processing and "
                        "data protection."
                    ),
                },
            ],
        },
        {
            "title": "Payment Orchestration",
            "body": (
                "Route every transaction through the best available payment path with intelligent "
                "orchestration, automatic failover, and real-time optimization."
            ),
            "image": "/images/figma-home/Group%201171275326.svg",
            "points": [
                {
                    "title": "01 — Multi-PSP Connectivity",
                    "body": (
                        "Connect and manage multiple payment providers through one unified layer."
                    ),
                },
                {
                    "title": "02 — Automatic Failover",
                    "body": (
                        "Keep payments moving when a provider experiences downtime or failures."
                    ),
                },
                {
                    "title": "03 — Real-Time Optimization",
                    "body": (
                        "Continuously optimize routing based on performance, availability, and "
                        "transaction conditions"
                    ),
                },
            ],
        },
    ],
}

HOME_CLOSING = {
    "testimonials_title": "Trusted by Businesses. Proven in Practice.",
    "testimonials": [
        {
            "quote": (
                "Zeepay is my go-to app for all payments. Whether I'm paying bills or "
                "transferring money to friends, it's super convenient and secure! The app has "
                "taken the hassle out of managing my finances, and I love the easy interface "
                "that keeps everything organized."
            ),
            "name": "Sneha P.",
            "role": "Regular User",
            "avatar": "/images/figma-about/testimonial-avatar-default.svg",
        },
        {
            "quote": (
                "Zeepay makes online payments a breeze! It's fast, reliable, and so easy to "
                "use. I handle all my transactions with just a few taps, whether I'm paying for "
                "groceries, services, or sending money to friends. Zeepay truly simplifies my "
                "day-to-day payments."
            ),
            "name": "Priya K.",
            "role": "Small Business Owner",
            "avatar": "/images/figma-about/testimonial-avatar-1.png",
        },
        {
            "quote": (
                "With Zeepay, sending and receiving money has never been simpler. The app is "
                "intuitive, and transactions are instant, which means no more waiting! Whether "
                "I'm transferring funds to family or paying bills, Zeepay has made it quick and "
                "convenient every time."
            ),
            "name": "Vikram S",
            "role": "Freelancer",
            "avatar": "/images/figma-about/testimonial-avatar-2.png",
        },
    ],
    "audiences_title": "Built for Businesses That Move Money",
    "audiences": [
        {
            "number": "1",
            "title": "E-commerce & Marketplaces",
            "body": (
                "Handle high-volume payments, payouts, and settlements with greater reliability."
            ),
        },
        {
            "number": "2",
            "title": "Fintechs & Payment Platforms",
            "body": "Launch and scale payment products with one unified infrastructure layer.",
        },
        {
            "number": "3",
            "title": "Digital Businesses & Platforms",
            "body": (
                "Offer seamless payment experiences without building complex infrastructure "
                "from scratch."
            ),
        },
        {
            "number": "4",
            "title": "Enterprises & Large Businesses",
            "body": (
                "Unify multiple payment providers, optimize transaction performance, and "
                "simplify operations."
            ),
        },
    ],
    "faq_title": "Got any Questions? We have got you covered!!",
    "faq_intro": (
        "Multiple providers, fragmented systems, failed transactions, and manual operations "
        "make it harder to scale—and harder to know where your money is going."
    ),
    "faq_items": [
        {
            "number": "01",
            "question": "What is Urbanrupee Hyper Checkout?",
            "answer": (
                "Hyper Checkout delivers faster UPI, card, net banking, wallet, and EMI payments "
                "with smart routing and one-click flows for higher conversion rates."
            ),
        },
        {
            "number": "02",
            "question": "What is payment orchestration?",
            "answer": (
                "Payment orchestration intelligently routes transactions across PSPs and banks "
                "to maximize success rates, uptime, and performance."
            ),
        },
        {
            "number": "03",
            "question": "How do I create my Urbanrupee account?",
            "answer": (
                "Download our mobile app or visit our website. Click 'Sign Up' or 'Register', "
                "provide your mobile number, verify with OTP, and set a secure password."
            ),
        },
        {
            "number": "04",
            "question": "How can I add money to my Urbanrupee wallet?",
            "answer": (
                "Use UPI, Net Banking, Debit Cards, or Credit Cards. Navigate to 'Wallet', "
                "select 'Add Money', enter the amount, and follow the secure steps."
            ),
        },
        {
            "number": "05",
            "question": "How can I view my transaction history?",
            "answer": (
                "Go to 'Transaction History' or 'My Orders' in the app or website to see all "
                "past payments and recharges."
            ),
        },
    ],
    "cta_title": "Ready to Build a Better Payment Infrastructure?",
    "cta_body": (
        "Bring payments, routing, payouts, reconciliation, and analytics together on one "
        "unified platform—built to scale with your business."
    ),
    "cta_label": "Talk to Expert",
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
