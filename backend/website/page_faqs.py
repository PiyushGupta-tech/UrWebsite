"""Closing FAQ block for inner pages, keyed by page slug.

Answers only restate what each page (``page_content.PAGES``) or the site-wide
company details already say, so the FAQ never promises more than the page.
Slugs without an entry fall back to the generic ``content.HOME_CLOSING`` items.
"""

from . import content

PAGE_FAQS = {
    "collections": {
        "intro": (
            "Answers to common questions about accepting, tracking, and reconciling "
            "payments with Urbanrupee Collections."
        ),
        "items": [
            {
                "question": "What is Urbanrupee Collections?",
                "answer": (
                    "Collections is a digital collections solution that helps businesses accept, "
                    "track, reconcile, and manage payments across multiple channels from a single API."
                ),
            },
            {
                "question": "How do I send payment requests to customers?",
                "answer": (
                    "Create payment requests with flexible workflows and share them through your "
                    "preferred channel, such as email, WhatsApp, SMS, or QR."
                ),
            },
            {
                "question": "Which payment methods can my customers use?",
                "answer": (
                    "Customers can pay with cards, UPI, net banking, wallets, and EMI, so they can "
                    "choose the method that suits them best."
                ),
            },
            {
                "question": "Will I know when a payment succeeds or fails?",
                "answer": (
                    "Yes. Instant payment status updates keep your systems informed, with clear "
                    "visibility into successful, pending, and failed transactions."
                ),
            },
            {
                "question": "How are collections settled and reconciled?",
                "answer": (
                    "Payments are automatically matched with the relevant orders, invoices, or "
                    "accounts, and you can track settlements with clear visibility into every outcome."
                ),
                "links": [{"label": "Reconciliation", "href": "/services/reconciliation"}],
            },
        ],
    },
    "payouts": {
        "intro": (
            "Answers to common questions about sending, managing, and tracking payouts "
            "with Urbanrupee."
        ),
        "items": [
            {
                "question": "Who can I send payouts to with Urbanrupee?",
                "answer": (
                    "Send payouts to customers, vendors, partners, employees, freelancers, and other "
                    "beneficiaries through one unified payout flow."
                ),
            },
            {
                "question": "Which payout methods are supported?",
                "answer": (
                    "Payouts can be sent over UPI, cards, bank transfer, and wallets through one "
                    "connected infrastructure."
                ),
            },
            {
                "question": "Can I send payouts in bulk or on a schedule?",
                "answer": (
                    "Yes. Manage high-volume disbursements, automate repetitive tasks, and send "
                    "instant or scheduled payouts from one platform."
                ),
            },
            {
                "question": "How do I manage beneficiaries?",
                "answer": (
                    "Add, manage, and organize beneficiaries while keeping recipient details secure, "
                    "up to date, and ready for every payout."
                ),
            },
            {
                "question": "How can I track the status of a payout?",
                "answer": (
                    "Monitor every payout from initiation to completion with real-time status "
                    "updates, so issues can be identified and resolved quickly."
                ),
            },
        ],
    },
    "risk-fraud-management": {
        "intro": (
            "Answers to common questions about monitoring risk and preventing fraud "
            "with Urbanrupee."
        ),
        "items": [
            {
                "question": "What does Urbanrupee Risk & Fraud Management do?",
                "answer": (
                    "It combines intelligent monitoring, configurable controls, and real-time "
                    "transaction insights to identify suspicious activity and reduce transaction risk."
                ),
            },
            {
                "question": "Which risk signals are monitored?",
                "answer": (
                    "Monitoring covers IP activity, transaction frequency and value, timing, location, "
                    "and transactions that match predefined risk conditions."
                ),
            },
            {
                "question": "Can I control how flagged transactions are handled?",
                "answer": (
                    "Yes. Structured workflows let your team approve, decline, review, or challenge "
                    "flagged transactions."
                ),
            },
            {
                "question": "How does it help with chargebacks?",
                "answer": (
                    "It tracks dispute exposure with transaction and merchant-level risk insights, "
                    "giving you better visibility into chargeback triggers."
                ),
            },
            {
                "question": "Does it keep up with new fraud patterns?",
                "answer": (
                    "Transaction patterns and changing risk signals are monitored continuously, so "
                    "you can respond proactively as new threats emerge."
                ),
            },
        ],
    },
    "reconciliation": {
        "intro": (
            "Answers to common questions about matching transactions and resolving "
            "exceptions with Urbanrupee Reconciliation."
        ),
        "items": [
            {
                "question": "What is Urbanrupee Reconciliation?",
                "answer": (
                    "It is one operational layer that connects transaction records, payment data, "
                    "and financial records, so every payment can be traced to its settlement."
                ),
            },
            {
                "question": "Which data sources can be reconciled?",
                "answer": (
                    "Reconciliation brings together data from payment gateways, banks, and your "
                    "internal systems, including orders and financial records."
                ),
            },
            {
                "question": "How does automated matching work?",
                "answer": (
                    "Payment transactions are automatically matched with settlement records, "
                    "improving accuracy and reducing manual effort."
                ),
            },
            {
                "question": "What happens when records don't match?",
                "answer": (
                    "Mismatches, missing transactions, and settlement exceptions are flagged with "
                    "clear visibility into the issues that need attention."
                ),
            },
            {
                "question": "How does it help finance teams resolve discrepancies?",
                "answer": (
                    "Finance and operations teams get the information they need to investigate "
                    "discrepancies and resolve settlement issues faster."
                ),
            },
        ],
    },
    "financial-operations": {
        "intro": (
            "Answers to common questions about building financial workflows on "
            "Urbanrupee infrastructure."
        ),
        "items": [
            {
                "question": "What is Urbanrupee's financial operations infrastructure?",
                "answer": (
                    "It is scalable infrastructure that simplifies banking operations, payment flows, "
                    "account services, and financial workflows through one connected ecosystem."
                ),
            },
            {
                "question": "Do I need to build the infrastructure myself?",
                "answer": (
                    "No. Ready-to-integrate infrastructure lets you launch financial capabilities "
                    "without building every component from scratch."
                ),
            },
            {
                "question": "Which financial flows does it cover?",
                "answer": (
                    "Collections, payouts, operational insights, and reconciliation are connected "
                    "through one unified platform."
                ),
            },
            {
                "question": "Can I embed financial capabilities into my own product?",
                "answer": (
                    "Yes. Financial capabilities can be embedded directly into your products to "
                    "create smoother, more connected experiences for your customers."
                ),
            },
            {
                "question": "Will it scale as my business grows?",
                "answer": (
                    "The infrastructure adapts to growing transaction volumes and evolving business "
                    "requirements."
                ),
            },
        ],
    },
    "white-label-platform": {
        "intro": (
            "Answers to common questions about launching a branded payment platform "
            "with Urbanrupee."
        ),
        "items": [
            {
                "question": "What is the Urbanrupee White Label Platform?",
                "answer": (
                    "It lets you launch a payment platform under your own brand, powered by "
                    "Urbanrupee technology and managed from one centralized solution."
                ),
            },
            {
                "question": "How much of the platform can I customize?",
                "answer": (
                    "Add your logo and brand colors, and choose the features, settings, and "
                    "workflows that match your business requirements."
                ),
            },
            {
                "question": "Do I need to manage the payment infrastructure?",
                "answer": (
                    "No. The underlying payment infrastructure is handled for you, so your team can "
                    "focus on customers and growth."
                ),
            },
            {
                "question": "Can it replace multiple payment systems?",
                "answer": (
                    "It reduces the need for multiple payment systems and simplifies how your "
                    "business manages its payment ecosystem."
                ),
            },
            {
                "question": "Will the platform support my growth?",
                "answer": (
                    "Yes. It supports growing transaction volumes and evolving business needs "
                    "without rebuilding your payment operations."
                ),
            },
        ],
    },
    "custom-checkout": {
        "intro": (
            "Answers to common questions about building a branded checkout with "
            "Urbanrupee Custom Checkout."
        ),
        "items": [
            {
                "question": "What is Urbanrupee Custom Checkout?",
                "answer": (
                    "Custom Checkout is a branded checkout that lets you own every step from cart to "
                    "payment, designed to match your brand."
                ),
            },
            {
                "question": "Will customers be redirected to a third-party page?",
                "answer": (
                    "Your logo and brand identity appear throughout checkout, so every payment step "
                    "feels like part of your product rather than a third-party redirect."
                ),
            },
            {
                "question": "Can I choose which payment methods to offer?",
                "answer": (
                    "Yes. Choose and manage the payment methods you offer, including UPI, cards, net "
                    "banking, wallets, and EMI."
                ),
            },
            {
                "question": "Which parts of checkout can I customize?",
                "answer": (
                    "You can customize the layout, visual elements, branding, and checkout flows "
                    "based on your business requirements."
                ),
            },
            {
                "question": "How is Custom Checkout different from Hyper Checkout?",
                "answer": (
                    "Custom Checkout focuses on control over branding, layout, and flows. Hyper "
                    "Checkout focuses on conversion, with intelligent payment selection and smart routing."
                ),
                "links": [{"label": "Hyper Checkout", "href": "/products/hyper-checkout"}],
            },
        ],
    },
    "hyper-checkout": {
        "intro": (
            "Answers to common questions about improving checkout conversion with "
            "Urbanrupee Hyper Checkout."
        ),
        "items": [
            {
                "question": "What is Urbanrupee Hyper Checkout?",
                "answer": (
                    "Hyper Checkout delivers faster UPI, card, net banking, wallet, and EMI payments "
                    "with smart routing and one-click flows for higher conversion rates."
                ),
            },
            {
                "question": "How does Hyper Checkout reduce drop-offs?",
                "answer": (
                    "It presents relevant payment options, removes unnecessary steps, and lets repeat "
                    "customers pay with less input."
                ),
            },
            {
                "question": "What happens when a payment attempt fails?",
                "answer": (
                    "Customers are guided toward relevant alternatives instead of restarting checkout, "
                    "and real-time alerts flag payment downtimes."
                ),
            },
            {
                "question": "Does it work on mobile and desktop?",
                "answer": (
                    "Yes. The checkout adapts across devices and customer journeys for a simple, "
                    "consistent payment experience."
                ),
            },
            {
                "question": "How does intelligent routing help?",
                "answer": (
                    "Transactions are routed through the most suitable payment path to improve "
                    "reliability and payment success."
                ),
                "links": [{"label": "Payment Orchestration", "href": "/products/orchestration"}],
            },
        ],
    },
    "payment-orchestration": {
        "intro": (
            "Answers to common questions about routing and managing payments with "
            "Urbanrupee Payment Orchestration."
        ),
        "items": [
            {
                "question": "What is payment orchestration?",
                "answer": (
                    "Payment orchestration is a centralized layer between your business and payment "
                    "providers that connects, manages, routes, and optimizes payments through a "
                    "single integration."
                ),
            },
            {
                "question": "How are transactions routed?",
                "answer": (
                    "Flexible rules route each transaction based on performance, cost, and gateway "
                    "priority, so every payment takes the most suitable path."
                ),
            },
            {
                "question": "Can orchestration recover failed transactions?",
                "answer": (
                    "Yes. A failed payment can fall back to another gateway or cascade across merchant "
                    "IDs, recovering transactions that might otherwise fail."
                ),
            },
            {
                "question": "Do I need a separate integration for each provider?",
                "answer": (
                    "No. Multiple providers and payment methods are managed through one integration."
                ),
            },
            {
                "question": "Can I monitor payment performance?",
                "answer": (
                    "Transaction activity and payment performance are available in one centralized view."
                ),
                "links": [{"label": "Unified Dashboard", "href": "/products/unified-dashboard"}],
            },
        ],
    },
    "upi-switch": {
        "intro": (
            "Answers to common questions about connecting and routing UPI payments "
            "with the Urbanrupee UPI Switch."
        ),
        "items": [
            {
                "question": "What is the Urbanrupee UPI Switch?",
                "answer": (
                    "It is switching infrastructure that connects your merchant ecosystem to the UPI "
                    "network through one centralized transaction layer."
                ),
            },
            {
                "question": "How are UPI transactions routed?",
                "answer": (
                    "Business rules and routing intelligence guide each UPI transaction through the "
                    "most suitable path."
                ),
            },
            {
                "question": "Which UPI payment journeys are supported?",
                "answer": "The switch supports both intent-based and QR-based UPI journeys.",
            },
            {
                "question": "Can I see transaction and settlement status?",
                "answer": (
                    "Yes. A centralized view shows transaction activity, payment performance, and "
                    "settlement and outcome status."
                ),
            },
            {
                "question": "Can it handle high UPI volumes?",
                "answer": (
                    "The switch is designed for high-throughput payment environments and growing "
                    "transaction volumes."
                ),
            },
        ],
    },
    "affordability": {
        "intro": (
            "Answers to common questions about offering EMI and Pay Later options "
            "with Urbanrupee Affordability."
        ),
        "items": [
            {
                "question": "Which affordability options can I offer?",
                "answer": (
                    "You can offer EMI, Cardless EMI, and Buy Now Pay Later (BNPL) directly within "
                    "checkout."
                ),
            },
            {
                "question": "How do affordability options help my business?",
                "answer": (
                    "They make higher-value purchases more manageable, which helps lift average order "
                    "value, conversion rates, and repeat purchases."
                ),
            },
            {
                "question": "Do customers have to leave checkout to apply?",
                "answer": (
                    "No. Affordability options are embedded in the payment journey, without extra "
                    "redirects or complex application processes."
                ),
            },
            {
                "question": "How do customers know whether they are eligible?",
                "answer": (
                    "Real-time eligibility checks and simple plan selection happen inside checkout."
                ),
            },
            {
                "question": "Are repayment terms shown clearly?",
                "answer": (
                    "Yes. Customers see transparent repayment breakdowns before they choose a plan."
                ),
            },
        ],
    },
    "unified-dashboard": {
        "intro": (
            "Answers to common questions about managing payment operations from the "
            "Urbanrupee Unified Dashboard."
        ),
        "items": [
            {
                "question": "What is the Urbanrupee Unified Dashboard?",
                "answer": (
                    "It is one dashboard for managing transactions, settlements, payment performance, "
                    "and merchant operations."
                ),
            },
            {
                "question": "What can I see in the dashboard?",
                "answer": (
                    "Payment activity, transaction status, settlements, providers, MIDs, and "
                    "chargeback exposure are all shown in one place."
                ),
            },
            {
                "question": "Can I track routing and MID performance?",
                "answer": (
                    "Yes. Track provider performance, MID usage, fallback routes, and cascading "
                    "activity across your parent and child MIDs."
                ),
            },
            {
                "question": "How does the dashboard help with chargebacks?",
                "answer": (
                    "Monitor dispute status, held funds, response timelines, and evidence handling so "
                    "your team can act faster."
                ),
            },
            {
                "question": "Does it include reporting and insights?",
                "answer": (
                    "Yes. Reports and trend views cover transaction outcomes, provider performance, "
                    "and operational patterns."
                ),
            },
        ],
    },
    "close-route-wallet": {
        "intro": (
            "Answers to common questions about running closed-loop wallet programs "
            "with Urbanrupee Close Route Wallet."
        ),
        "items": [
            {
                "question": "What is Urbanrupee Close Route Wallet?",
                "answer": (
                    "It lets businesses run secure, closed-loop wallet ecosystems on a ledger-based "
                    "architecture, where funds move only through approved channels."
                ),
            },
            {
                "question": "How are funds kept within approved channels?",
                "answer": (
                    "Approved funding sources, route-specific permissions, transaction control "
                    "policies, and configurable spending limits govern every movement of value."
                ),
            },
            {
                "question": "Which transactions does the wallet support?",
                "answer": (
                    "It supports wallet-to-wallet transfers and wallet-to-merchant transactions within "
                    "controlled spending environments."
                ),
            },
            {
                "question": "Can it connect to my apps and systems?",
                "answer": (
                    "Yes. Deliver branded wallet functionality inside your apps, connect it to "
                    "Urbanrupee payments and payouts, and automate workflows with webhooks and "
                    "real-time events."
                ),
            },
            {
                "question": "What reporting is available?",
                "answer": (
                    "Statements, transaction exports, reconciliation reports, and audit-ready records "
                    "are available whenever you need them."
                ),
            },
        ],
    },
    "about": {
        "intro": "Answers to common questions about Urbanrupee and the businesses we work with.",
        "items": [
            {
                "question": "What does Urbanrupee do?",
                "answer": (
                    "Urbanrupee helps businesses accept, process, route, and manage transactions "
                    "through a secure, scalable, and intelligent payment ecosystem."
                ),
            },
            {
                "question": "Which businesses does Urbanrupee work with?",
                "answer": (
                    "We work with e-commerce businesses and marketplaces, fintechs and payment "
                    "platforms, digital businesses, and large enterprises."
                ),
            },
            {
                "question": "Which products does Urbanrupee offer?",
                "answer": (
                    "Our suite covers collections, payouts, payment orchestration, checkout, UPI "
                    "switching, reconciliation, and analytics."
                ),
                "links": [{"label": "All products", "href": "/products"}],
            },
            {
                "question": "What values guide Urbanrupee?",
                "answer": (
                    "Our core values are Leadership, Excellence, Accountability, and Drive: we lead "
                    "by example, raise the standard in what we build, own outcomes, and keep "
                    "moving forward."
                ),
            },
            {
                "question": "Where is Urbanrupee based?",
                "answer": (
                    "Urbanrupee Techsolution Private Limited is based at NX-One, Techzone 4, "
                    "Greater Noida, Uttar Pradesh, India."
                ),
                "links": [{"label": "Contact us", "href": "/contact"}],
            },
        ],
    },
    "blog": {
        "intro": "Answers to common questions about the Urbanrupee blog and where to learn more.",
        "items": [
            {
                "question": "What does the Urbanrupee blog cover?",
                "answer": (
                    "The blog covers payments, orchestration, compliance, and building resilient "
                    "fintech products."
                ),
            },
            {
                "question": "Where can I find quick answers about Urbanrupee products?",
                "answer": (
                    "Our FAQ page answers common questions about products, UPI, checkout, "
                    "orchestration, security, and onboarding."
                ),
                "links": [{"label": "FAQ", "href": "/faq"}],
            },
            {
                "question": "Where can I explore the products mentioned in articles?",
                "answer": "Every Urbanrupee product is listed with an overview on the products page.",
                "links": [{"label": "All products", "href": "/products"}],
            },
            {
                "question": "How can I discuss an article with the Urbanrupee team?",
                "answer": (
                    "Reach out through our contact page and our team will get back to you shortly."
                ),
                "links": [{"label": "Contact us", "href": "/contact"}],
            },
        ],
    },
    "privacy-policy": {
        "intro": "Answers to common questions about how Urbanrupee handles your information.",
        "items": [
            {
                "question": "What information does Urbanrupee collect?",
                "answer": (
                    "Depending on how you interact with us, we may collect contact details, merchant and "
                    "business information, KYC and compliance documents, transaction and payment "
                    "information, and technical data such as IP address, browser, and device."
                ),
            },
            {
                "question": "How does Urbanrupee protect payment information?",
                "answer": (
                    "Urbanrupee maintains PCI DSS and ISO 27001-related security controls applicable to "
                    "its operations and scope, along with safeguards such as access controls, encryption, "
                    "monitoring, and security testing."
                ),
            },
            {
                "question": "How long does Urbanrupee retain data?",
                "answer": (
                    "Urbanrupee generally follows a 90-day retention period for standard operational "
                    "data. Certain information may remain in backend systems for a minimum of one year "
                    "as part of system and service operations."
                ),
            },
            {
                "question": "Does Urbanrupee sell merchant or personal information?",
                "answer": (
                    "No. We do not sell, rent, or commercially exploit merchant information. Access is "
                    "limited to authorised personnel, systems, and service providers with a legitimate "
                    "need, or where required by law or regulation."
                ),
            },
            {
                "question": "How can I access, correct, or delete my data?",
                "answer": (
                    "Subject to applicable laws, you can request access, correction, updates, or deletion "
                    "by emailing it.support@urbanrupee.com. Some information may need to be retained for "
                    "legal, regulatory, or security purposes, and we may verify your identity first."
                ),
            },
        ],
    },
    "terms-and-conditions": {
        "intro": "Answers to common questions about the terms for using Urbanrupee services.",
        "items": [
            {
                "question": "Who can use Urbanrupee services?",
                "answer": (
                    "Anyone legally capable of entering binding contracts who is authorized to act for "
                    "the business or entity they represent."
                ),
            },
            {
                "question": "What are merchants responsible for?",
                "answer": (
                    "Merchants must provide accurate onboarding information, keep credentials and API "
                    "keys confidential, comply with applicable laws, and handle support, refunds, and "
                    "disputes."
                ),
            },
            {
                "question": "Why might Urbanrupee ask for KYC or verification documents?",
                "answer": (
                    "Verification may be required by law, internal risk controls, or partner "
                    "obligations. Services may be restricted if required information is not provided."
                ),
            },
            {
                "question": "Can services be suspended or terminated?",
                "answer": (
                    "Yes, where needed to meet legal obligations, protect platform security, "
                    "investigate suspicious activity, or enforce these terms."
                ),
            },
            {
                "question": "Which law governs these terms?",
                "answer": (
                    "The terms are governed by the laws of India, with disputes subject to the courts "
                    "in Greater Noida, Uttar Pradesh."
                ),
            },
        ],
    },
    "contact": {
        "intro": "Answers to common questions about getting in touch with the Urbanrupee team.",
        "items": [
            {
                "question": "How can I reach the Urbanrupee team?",
                "answer": (
                    "Send us a message through the contact form, email it.support@urbanrupee.com, or "
                    "call +91 9305697870."
                ),
            },
            {
                "question": "Can I request a product demo?",
                "answer": (
                    "Yes. Our team can help with demos, merchant onboarding, and payment "
                    "infrastructure support."
                ),
            },
            {
                "question": "What should I include in my message?",
                "answer": (
                    "Share your name, email, phone number, a subject, and a short message about what "
                    "you need so the right team can respond."
                ),
            },
            {
                "question": "Where is the Urbanrupee office?",
                "answer": (
                    "A01 & A03, UG, Tower 3, NX-One, Techzone 4, Greater Noida, Uttar Pradesh, "
                    "India, 201301."
                ),
            },
            {
                "question": "Where can I find quick answers before contacting you?",
                "answer": "Our FAQ page covers common questions about products, onboarding, and security.",
                "links": [{"label": "FAQ", "href": "/faq"}],
            },
        ],
    },
    "products-index": {
        "intro": "Answers to common questions about the Urbanrupee product suite.",
        "items": [
            {
                "question": "Which products does Urbanrupee offer?",
                "answer": (
                    "The suite includes Collections, Payment Orchestration, Hyper Checkout, Custom "
                    "Checkout, UPI Switch, Affordability, White Label, Payouts, Unified Dashboard, "
                    "and Close Route Wallet."
                ),
            },
            {
                "question": "Which payment methods are supported?",
                "answer": "Urbanrupee products support UPI, cards, net banking, wallets, and EMI.",
            },
            {
                "question": "Can I use more than one product together?",
                "answer": (
                    "Yes. Orchestration, checkout, payouts, and analytics are built to work together "
                    "as one suite."
                ),
            },
            {
                "question": "Should I choose Hyper Checkout or Custom Checkout?",
                "answer": (
                    "Hyper Checkout focuses on conversion with smart routing and one-click flows. "
                    "Custom Checkout focuses on a fully branded on-site checkout experience."
                ),
            },
            {
                "question": "How do I get started?",
                "answer": (
                    "Talk to our team about demos, merchant onboarding, and the right products for "
                    "your business."
                ),
                "links": [{"label": "Contact us", "href": "/contact"}],
            },
        ],
    },
    "resources-index": {
        "intro": "Answers to common questions about Urbanrupee resources and support.",
        "items": [
            {
                "question": "What resources does Urbanrupee offer?",
                "answer": (
                    "Our resources include FAQs, blog articles, our Privacy Policy, and our Terms & "
                    "Conditions."
                ),
            },
            {
                "question": "Where can I find answers about Urbanrupee products?",
                "answer": (
                    "The FAQ page covers products, UPI, checkout, orchestration, security, and "
                    "onboarding."
                ),
                "links": [{"label": "FAQ", "href": "/faq"}],
            },
            {
                "question": "How does Urbanrupee protect my data?",
                "answer": (
                    "Our Privacy Policy explains how we collect, use, and protect your data across "
                    "our website and services."
                ),
                "links": [{"label": "Privacy Policy", "href": "/privacy-policy"}],
            },
            {
                "question": "How can I get support?",
                "answer": (
                    "Talk to our team for demos, merchant onboarding, and payment infrastructure "
                    "support."
                ),
                "links": [{"label": "Contact us", "href": "/contact"}],
            },
        ],
    },
}


def _numbered(items: list[dict]) -> list[dict]:
    return [{**item, "number": f"{index:02d}"} for index, item in enumerate(items, start=1)]


def page_faq_items(slug: str | None) -> list[dict]:
    """Page-specific FAQ items (numbered), or an empty list if the page has none."""
    entry = PAGE_FAQS.get(slug or "")
    return _numbered(entry["items"]) if entry else []


def closing_for_slug(slug: str | None) -> dict:
    """Shared closing section with the FAQ swapped for the page's own questions."""
    entry = PAGE_FAQS.get(slug or "")
    if not entry:
        return content.HOME_CLOSING
    return {
        **content.HOME_CLOSING,
        "faq_intro": entry.get("intro") or content.HOME_CLOSING["faq_intro"],
        "faq_items": _numbered(entry["items"]),
    }
