"""Content for inner marketing pages — sourced from Urbanrupee.com."""

from website import content

# slug -> page payload
PAGES = {
    "about": {
        "type": "about",
        "title": "About Urbanrupee",
        "hero_title": "Powering the Future of Digital Payments",
        "intro": (
            "Urbanrupee brings intelligent payment technology, secure infrastructure, and "
            "seamless experiences together to help businesses move money smarter, faster, and "
            "at scale."
        ),
        "merchant_partners": content.MERCHANT_PARTNERS,
        "overview_title": "Building smarter payment experiences for a digitally connected world.",
        "overview_body": (
            "Urbanrupee is a leading payment technology company providing a comprehensive "
            "technology stack for modern digital payments. We help businesses simplify complex "
            "transaction challenges while enabling fast, secure, seamless, and reliable payment "
            "journeys for customers and businesses."
        ),
        "stats": [
            {"value": "10+", "label": "Partners"},
            {"value": "100+", "label": "Clients Served"},
            {"value": "1Cr", "label": "Transactions Processed"},
        ],
        "mission": {
            "title": "Our Mission",
            "body": (
                "To achieve RBI PA-PG (Payment Aggregator and Payment Gateway) authorization by "
                "2027 while delivering seamless, secure, and technology-driven payment solutions "
                "that help businesses simplify transactions, enhance customer experiences, and "
                "scale with confidence."
            ),
        },
        "vision": {
            "title": "Our Vision",
            "body": (
                "To become a trusted leader in digital payment infrastructure by empowering "
                "businesses of every size and sector with secure, scalable, and innovative payment "
                "solutions that drive sustainable growth and advance financial inclusion for "
                "more people and communities."
            ),
        },
        "journey_title": "Our Journey",
        "journey_intro": (
            "From a vision to a growing fintech ecosystem, our journey is driven by innovation, "
            "meaningful connections, and a commitment to simplifying digital payments."
        ),
        "journey": [
            {
                "title": "2023 | STARTED",
                "body": "Founded as a bank referral partner, providing SaaS solutions.",
            },
            {
                "title": "2024 | BUILT",
                "body": (
                    "Launched payment orchestration and customized checkout solutions, onboarding "
                    "100+ MSME merchants."
                ),
            },
            {
                "title": "2025 | SECURED",
                "body": (
                    "Achieved PCI DSS compliance and strengthened our customized checkout "
                    "technology."
                ),
            },
            {
                "title": "2026 | SCALED",
                "body": (
                    "Entered the ₹100 Crore processing volume club, serving Education, Travel, "
                    "and E-commerce."
                ),
            },
            {
                "title": "2027 | NEXT MILESTONE",
                "body": (
                    "Targeting PPI and PAG licenses to strengthen our regulated payments ecosystem."
                ),
            },
        ],
        "partnerships_title": "Partnerships That Power Progress",
        "partnerships_intro": (
            "Collaborating with industry leaders to strengthen payment connectivity and create "
            "smarter financial solutions."
        ),
        "leaders_title": "Leaders Behind Urbanrupee",
        "leaders_intro": (
            "Our leaders bring together expertise in fintech, technology, product development, "
            "and business operations to build payment solutions that help businesses move forward."
        ),
        "leaders": [
            {
                "name": "Nakul Kushwaha",
                "role": "Founder",
                "image": "/images/2.png",
            },
            {
                "name": "Jay Chaudhary",
                "role": "CEO",
                "image": "/images/1.png",
            },
        ],
        "values_title": "Our Core Values",
        "values_intro": (
            "The principles that drive us forward, shape our decisions, and define how we build "
            "the future of digital payments."
        ),
        "values": [
            {
                "letter": "L",
                "title": "Leadership",
                "body": "Lead by action, ownership, and strong example.",
                "icon": "users",
            },
            {
                "letter": "E",
                "title": "Excellence",
                "body": "Raise the standard in everything we consistently build.",
                "icon": "star",
            },
            {
                "letter": "A",
                "title": "Accountability",
                "body": "Own the outcome, not just the assigned task.",
                "icon": "shield-check",
            },
            {
                "letter": "D",
                "title": "Drive",
                "body": "Move faster, think bigger, keep forward momentum.",
                "icon": "zap",
            },
        ],
        "testimonials_title": "Trusted by Businesses. Proven in Practice.",
        "testimonials": [
            {
                "quote": (
                    "Groots Pay supports stores and retailers who can offer Assisted Digital "
                    "Financial Services, including Aadhaar ATM, SMS payment, khata service, "
                    "utility payment, prepaid cards, insurance, and money transfer. Through "
                    "AWESOMEPAY, Urbanrupee infrastructure helps deliver dependable processing "
                    "and a polished brand presence at the point of sale."
                ),
                "company": "Groots Pay",
                "logo": "/logos/merchants/groots.png",
            },
            {
                "quote": (
                    "Finlix Capital is a performance-based proprietary trading evaluation platform "
                    "for traders in India, offering simulated challenges, clear rules, and a path "
                    "to internal capital for those who demonstrate consistency and discipline. "
                    "Simulated trading, education, and evaluation drive the experience, not a "
                    "broker. We do not execute trades or hold public investment funds."
                ),
                "company": "Finlix Capital",
                "logo": "",
            },
            {
                "quote": (
                    "Green Web Software Development Private Limited builds digital payment and web "
                    "platforms for businesses across India. With Urbanrupee infrastructure, they "
                    "deliver dependable collections, payouts, and branded checkout experiences, "
                    "helping merchants launch online faster and scale transaction volume with "
                    "confidence."
                ),
                "company": "Green Web Software Development Private Limited",
                "logo": "/logos/merchants/green-web.png",
            },
            {
                "quote": (
                    "BingoPay empowers retailers and agents with assisted digital financial "
                    "services, from UPI collections and bill payments to wallet and voucher flows. "
                    "Powered by Urbanrupee rails, BingoPay offers a secure, compliant stack that "
                    "keeps last-mile payment experiences fast and dependable."
                ),
                "company": "BingoPay",
                "logo": "/logos/merchants/bingopay.png",
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
                "body": (
                    "Launch and scale payment products with one unified infrastructure layer."
                ),
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
        "faq_title": "Got any questions? We've got you covered.",
        "faq_intro": (
            "Find clear answers about Urbanrupee products, payment orchestration, checkout, "
            "and how our platform helps businesses scale with better visibility and control."
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
            "unified platform, built to scale with your business."
        ),
        "cta_label": "Talk to Expert",
    },
    "collections": {
        "type": "collections",
        "eyebrow": "collections",
        "title": "Collect Payments. Simplify Operations. Accelerate Growth from single API.",
        "intro": (
            "A smarter digital collections solution designed to help businesses accept, track, "
            "reconcile, and manage payments seamlessly across multiple channels."
        ),
        "cta_label": "Talk to Expert",
        "stats": [
            {"value": "80%", "label": "Reduction in Operational Time"},
            {"value": "93%", "label": "Transaction Success Rate"},
            {"value": "40%", "label": "Reduction in Failover Time"},
            {"value": "90+", "label": "Transaction Per Seconds"},
        ],
        "smarter": {
            "title": "A Smarter Way to Manage Every Collection",
                "body": (
                "Built for businesses handling high-volume payments, the solution helps reduce "
                "manual processes, improve visibility, and create a smoother collection "
                "experience for both businesses and customers."
            ),
            "image": "/images/figma-collections/diagram.png",
            "image_alt": (
                "Collections platform connecting customers, Urbanrupee, merchants, and payment methods"
            ),
        },
        "flow": {
            "title": "How Your Payment Journey Works",
            "body": (
                "From integration to settlement, manage every step through one "
                "connected payment infrastructure."
            ),
            "steps": [
                {
                    "number": "01.",
                    "title": "API Integration",
                    "body": (
                        "Connect your business to Urbanrupee APIs and access unified payment "
                        "capabilities through a seamless integration."
                    ),
                    "side": "left",
                    "visual": "api",
                },
                {
                    "number": "02.",
                    "title": "Payment Initiation",
                    "body": (
                        "Create and initiate payment requests with flexible workflows designed "
                        "around your business requirements."
                    ),
                    "side": "right",
                    "visual": "initiate",
                },
                {
                    "number": "03.",
                    "title": "Customer Pays",
                    "body": (
                        "Customers complete payments through their preferred payment method, "
                        "creating a smooth and reliable checkout experience."
                    ),
                    "side": "left",
                    "visual": "pay",
                },
                {
                    "number": "04.",
                    "title": "Real-Time Notification",
                    "body": (
                        "Receive instant payment status updates and keep your business systems "
                        "informed throughout the transaction journey."
                    ),
                    "side": "right",
                    "visual": "notify",
                },
                {
                    "number": "05.",
                    "title": "Settlement & Reconciliation",
                    "body": (
                        "Track settlements and reconcile transaction records with clear visibility "
                        "into payment data and financial outcomes."
                    ),
                    "side": "left",
                    "visual": "settle",
                },
            ],
        },
        "journey": {
            "title": "From Payment Request to Reconciliation",
            "body": (
                "Built for businesses handling high-volume payments, the solution helps reduce "
                "manual processes, improve visibility, and create a smoother collection experience."
            ),
            "cards": [
                {
                    "title": "Initiate Collection",
                "body": (
                        "Create and send payment requests through your preferred collection "
                        "channel, making it easy for customers."
                    ),
                    "icon": "/images/figma-collections/journey/initiate.svg",
                },
                {
                    "title": "Accept Payments",
                    "body": (
                        "Let customers pay through multiple digital payment modes with a smooth "
                        "and convenient payment experience."
                    ),
                    "icon": "/images/figma-collections/journey/accept.svg",
                },
                {
                    "title": "Track & Reconcile",
                    "body": (
                        "Monitor transactions in real time and automatically match payments with "
                        "the relevant orders, invoices, or accounts."
                    ),
                    "icon": "/images/figma-collections/journey/track.svg",
                },
                {
                    "title": "Settle & Analyze",
                    "body": (
                        "Access timely settlements and actionable transaction insights to improve "
                        "collection performance."
                    ),
                    "icon": "/images/figma-collections/journey/settle.svg",
                },
            ],
        },
        "experiences": {
            "title": "Designed for Frictionless Payment Experiences",
            "body": (
                "Make every collection simple for your customers and effortless for your business "
                "with a payment journey built for speed, convenience, and reliability."
            ),
            "cards": [
                {
                    "title": "Easy Payment Initiation",
                "body": (
                        "Make it simple for customers to start a payment with intuitive payment "
                        "requests and streamlined collection journeys."
                    ),
                    "image": "/images/figma-collections/experiences/easy-payment-initiation.svg",
                    "image_alt": (
                        "Payment request card connected to email, WhatsApp, SMS, QR, and send channels"
                    ),
                },
                {
                    "title": "Seamless Checkout",
                    "body": (
                        "Reduce payment friction with a smooth, responsive checkout experience "
                        "designed to help customers complete transactions effortlessly."
                    ),
                    "image": "/images/figma-collections/experiences/seamless-checkout.svg",
                    "image_alt": (
                        "Checkout card with product, delivery to Home Bengaluru, Pay Securely CTA, "
                        "and progress steps Details, Payment, Review, Complete"
                    ),
                },
                {
                    "title": "Multiple Payment Modes",
                    "body": (
                        "Give customers the flexibility to pay using their preferred digital "
                        "payment method for a more convenient experience."
                    ),
                    "image": "/images/figma-collections/experiences/multiple-payment-modes.svg",
                    "image_alt": (
                        "Payment methods panel with Cards, UPI, Net Banking, Wallets, and EMI "
                        "connected to Visa, Mastercard, UPI, GPay, PhonePe, and Paytm"
                    ),
                },
                {
                    "title": "Smart Payment Journeys",
                    "body": (
                        "Deliver optimized payment flows based on transaction requirements, "
                        "helping create a more efficient and reliable collection experience."
                    ),
                    "image": "/images/figma-collections/experiences/smart-payment-journeys.svg",
                    "image_alt": (
                        "Transaction request routed through smart routing to Card, UPI, "
                        "Net Banking, and Alternate Route"
                    ),
                },
                {
                    "title": "Real-Time Payment Status",
                    "body": (
                        "Keep customers and businesses informed with instant visibility into "
                        "successful, failed, and pending payment transactions."
                    ),
                    "image": "/images/figma-collections/experiences/realtime-payment-status.svg",
                    "image_alt": (
                        "Stacked payment status cards for successful, pending, and failed transactions"
                    ),
                },
                {
                    "title": "Secure Transactions",
                    "body": (
                        "Build customer confidence with secure payment journeys designed to "
                        "protect transaction data throughout the collection process."
                    ),
                    "image": "/images/figma-collections/experiences/secure-transactions.svg",
                    "image_alt": (
                        "Security shield surrounded by data encryption, fraud detection, "
                        "secure APIs, and regulatory compliance"
                    ),
                },
            ],
        },
    },
    "payouts": {
        "type": "payouts",
        "eyebrow": "Payouts",
        "title": "Send every payout faster with greater control and visibility",
        "intro": (
            "Send fast, secure, and reliable payouts through one unified platform, built to "
            "simplify operations and keep every transaction on track."
        ),
        "cta_label": "Talk to Expert",
        "hero_image_alt": (
            "Distribute funds card sending payouts to employees, vendors, partners, and freelancers"
        ),
        "stats": [
            {"value": "<5 sec", "label": "Transaction Latency"},
            {"value": "99.8%", "label": "Platform Uptime"},
            {"value": "10 sec", "label": "Failure Alert Time"},
            {"value": "<1 min", "label": "Downtime Alerts"},
        ],
        "platform": {
            "title": "One Platform for Every Payout",
            "body": (
                "Connect your business, beneficiaries, and multiple payout methods "
                "through one unified platform for faster, simpler, and more reliable payouts."
            ),
            "image_alt": (
                "Urbanrupee withdrawals platform connecting customers, beneficiaries, "
                "and payment methods"
            ),
        },
        "features": {
            "title": "Built for smarter payout operations",
            "body": (
                "Streamline payouts through one unified platform, automate repetitive tasks, "
                "and manage high-volume disbursements with less manual effort."
            ),
            "cards": [
                {
                    "title": "Beneficiary Ready",
                "body": (
                        "Easily add, manage, and organize beneficiaries while keeping recipient "
                        "details secure, updated, and ready for every payout."
                    ),
                    "icon": "/images/figma-payouts/icons/beneficiary.svg",
                },
                {
                    "title": "Operational Visibility",
                    "body": (
                        "Get real-time visibility into payout activity, track transaction status, "
                        "and quickly identify issues to keep operations running smoothly."
                    ),
                    "icon": "/images/figma-payouts/icons/visibility.svg",
                },
                {
                    "title": "Simplify Disbursement",
                    "body": (
                        "Streamline payouts on one platform, automate repetitive tasks, and "
                        "manage high-volume disbursements with less effort."
                    ),
                    "icon": "/images/figma-payouts/icons/disbursement.svg",
                },
                {
                    "title": "Fast payouts",
                    "body": (
                        "Move funds quickly with reliable infrastructure, support instant or "
                        "scheduled payouts, and track every transaction with real-time updates."
                    ),
                    "icon": "/images/figma-payouts/icons/fast.svg",
                },
            ],
        },
        "path": {
            "title": "Where every payout finds its path.",
            "body": [
                (
                    "Manage every payout from initiation to completion through one unified "
                    "platform. Connect multiple payout methods, automate transactions, choose "
                    "the right payment route, and keep every disbursement on track."
                ),
            ],
            "icons": [
                {
                    "id": "bank",
                    "src": "/images/figma-payouts/path/badge-1.svg",
                    "left": "22px",
                    "top": "280px",
                    "width": 22,
                    "height": 22,
                },
                {
                    "id": "trend",
                    "src": "/images/figma-payouts/path/badge-2.svg",
                    "left": "144px",
                    "top": "687px",
                    "width": 19,
                    "height": 19,
                },
                {
                    "id": "pod",
                    "src": "/images/figma-payouts/path/badge-3.svg",
                    "left": "857px",
                    "top": "311px",
                    "width": 21,
                    "height": 21,
                },
                {
                    "id": "route",
                    "src": "/images/figma-payouts/path/badge-4.svg",
                    "left": "1008px",
                    "top": "521px",
                    "width": 21,
                    "height": 21,
                },
            ],
        },
        "control": {
            "title": "Complete Control Over Every Payout",
            "body": (
                "Manage beneficiaries, track transactions, and send funds across multiple "
                "payment channels through one unified payout infrastructure."
            ),
            "cards": [
                {
                    "title": "Beneficiary Payouts",
                "body": (
                        "Send payments to customers, vendors, partners, employees, and other "
                        "beneficiaries through one unified payout flow."
                    ),
                    "image": "/images/figma-payouts/control/beneficiary.png",
                    "image_alt": (
                        "Beneficiary list with initiate payout flow and transfer status"
                    ),
                    "image_width": 765,
                    "image_height": 411,
                },
                {
                    "title": "Payout Tracking",
                "body": (
                        "Monitor every payout from initiation to completion with real-time status "
                        "updates, transaction visibility, and clear operational insights for "
                        "better control."
                    ),
                    "image": "/images/figma-payouts/control/tracking.png",
                    "image_alt": (
                        "Payout tracking stepper and recent payouts table with live statuses"
                    ),
                    "image_width": 704,
                    "image_height": 413,
                },
                {
                    "title": "Multi Channel Disbursement",
                    "body": (
                        "Support payout journeys across different transfer methods through one "
                        "connected infrastructure."
                    ),
                    "image": "/images/figma-payouts/control/multichannel.png",
                    "image_alt": (
                        "Business connected to UPI, cards, bank transfer, and wallets"
                    ),
                    "image_width": 800,
                    "image_height": 269,
                },
            ],
        },
    },
    "risk-fraud-management": {
        "type": "risk-fraud",
        "eyebrow": "risk and fraud management",
        "title": "Stay Ahead of Risk. Protect Every Transaction.",
        "intro": (
            "Build safer payment experiences with intelligent risk monitoring and fraud "
            "management solutions designed to identify suspicious activity, reduce transaction "
            "risk, and protect your business."
        ),
        "cta_label": "Talk to Expert",
        "hero_image_alt": (
            "Risk management shield clearing payment attempts while flagging unusual location, "
            "stolen cards, fake accounts, suspicious transactions, and bot activity"
        ),
        "secure": {
            "title": "Make Every Transaction More Secure and More Predictable",
            "body": (
                "UrbanRupee helps businesses manage payment risk through intelligent monitoring, "
                "configurable controls, and real-time transaction insights. Identify unusual "
                "activity and potential threats before they impact your business."
            ),
            "image": "/images/figma-risk-fraud/platform/diagram-engine.png?v=3",
            "image_alt": (
                "Urbanrupee Risk Management Engine connecting multiple data inputs to "
                "real-time risk outcomes"
            ),
            "image_width": 1291,
            "image_height": 568,
        },
        "growth": {
            "title": "Turn Payment Complexity Into Business Growth",
            "body": (
                "Monitor payment risks, prevent fraud, and make faster, smarter decisions."
            ),
            # Figma 538:5121 — 2×2 grid, row-major
            "cards": [
                {
                    "title": "Fraud Monitoring",
                    "body": (
                        "Identify unusual transaction behavior and suspicious payment "
                        "patterns in real time."
                    ),
                    "icon": "/images/figma-risk-fraud/icons/monitor.svg",
                },
                {
                    "title": "Chargeback Risk Visibility",
                    "body": (
                        "Track dispute exposure with clearer transaction and merchant-level "
                        "risk insights."
                    ),
                    "icon": "/images/figma-risk-fraud/icons/chargeback.svg",
                },
                {
                    "title": "Risk Review Workflows",
                    "body": (
                        "Streamline approve, decline, review, and challenge actions through "
                        "structured workflows."
                    ),
                    "icon": "/images/figma-risk-fraud/icons/workflows.svg",
                },
                {
                    "title": "Operational Risk Insights",
                    "body": (
                        "Gain clear visibility into risk trends, alerts, and operational "
                        "performance for better decisions."
                    ),
                    "icon": "/images/figma-risk-fraud/icons/insights.svg",
                },
            ],
        },
        "detect": {
            "title": "Detect Risk Before It Becomes Fraud",
            "body": (
                "Identify unusual transaction signals in real time with intelligent monitoring "
                "across IP activity, transaction patterns, timing, location, and suspicious "
                "behavior."
            ),
            "cards": [
                {
                    "title": "IP Detection",
                "body": (
                        "Identify unusual or high-risk IP activity to detect potentially "
                        "unauthorized access and suspicious transaction behavior."
                    ),
                    "image": "/images/figma-risk-fraud/illustration-container.svg",
                    "image_width": 436,
                    "image_height": 331,
                },
                {
                    "title": "Transaction Patterns",
                    "body": (
                        "Analyze transaction frequency, value, and behavior to identify "
                        "patterns that differ from established user activity."
                    ),
                    "image": "/images/figma-risk-fraud/Frame%202147226663.svg",
                    "image_width": 403,
                    "image_height": 300,
                },
                {
                    "title": "Suspicious Transactions",
                    "body": (
                        "Flag transactions that match predefined risk conditions or demonstrate "
                        "characteristics associated with potential fraud."
                    ),
                    "image": "/images/figma-risk-fraud/Frame%202147226808.svg",
                    "image_width": 454,
                    "image_height": 308,
                },
                {
                    "title": "Unusual Locations",
                    "body": (
                        "Identify activity from unexpected or inconsistent locations to help "
                        "detect suspicious access and transaction attempts."
                    ),
                    "image": "/images/figma-risk-fraud/Frame%202147226810.svg",
                    "image_width": 382,
                    "image_height": 256,
                },
            ],
        },
        "safer": {
            "title": "Designed for Safer Financial Operations",
            "body": (
                "Create a stronger risk management layer with continuous monitoring, "
                "configurable controls, and greater visibility across your transaction ecosystem."
            ),
            "items": [
                {
                    "num": "01",
                    "title": "Continuous Monitoring",
                "body": (
                        "Keep track of transaction activity and risk signals across connected "
                        "payment flows."
                ),
            },
            {
                    "num": "02",
                    "title": "Minimize Financial Loss",
                "body": (
                        "Prevent avoidable fraud-related losses by identifying risky transactions "
                        "before they become costly incidents."
                    ),
                },
                {
                    "num": "03",
                    "title": "Improve Chargeback Readiness",
                    "body": (
                        "Stay prepared for disputes with better visibility into transaction "
                        "behavior, risk signals, and chargeback triggers."
                    ),
                },
                {
                    "num": "04",
                    "title": "Stay Ahead of Emerging Risks",
                    "body": (
                        "Continuously monitor transaction patterns and changing risk signals to "
                        "respond proactively as new threats emerge."
                    ),
                },
            ],
        },
    },
    "reconciliation": {
        "type": "reconciliation",
        "eyebrow": "RECONCILIATION",
        "title": "One Connected Layer for Reconciliation",
        "intro": (
            "Manage reconciliation through one operational layer that brings together "
            "transaction records, payment data, and financial visibility."
        ),
        "cta_label": "Talk to Expert",
        "hero_image_alt": (
            "Urbanrupee reconciliation hub connecting payment gateways, banks, internal "
            "systems, and settlement outcomes"
        ),
        "clarity": {
            "title": "Bring Clarity to Every Transaction",
            "body": (
                "Urbanrupee helps businesses connect transaction data across payment systems, "
                "orders, and financial records through a centralized operational layer."
            ),
            "image": "/images/figma-reconciliation/Frame%20214722621.svg",
            "image_alt": (
                "Urbanrupee Reconciliation Engine ingesting data sources and producing "
                "matched, exception, and unmatched outcomes"
            ),
            "image_width": 1291,
            "image_height": 627,
        },
        "features": {
            "title": "Everything You Need to Simplify Reconciliation",
            "body": (
                "Power your financial operations with connected capabilities designed to make "
                "transaction matching and exception management more efficient."
                ),
                "cards": [
                {
                    "title": "Reliable",
                    "body": (
                        "Support payment continuity with fallback routing, operational "
                        "visibility, and infrastructure designed for high-volume environments."
                    ),
                    "icon": "/images/figma-reconciliation/icons/reliable.svg",
                },
                {
                    "title": "Merchant Centric",
                    "body": (
                        "Give businesses direct control over checkout, chargebacks, reporting, "
                        "and payment operations through one connected platform."
                    ),
                    "icon": "/images/figma-reconciliation/icons/merchant.svg",
                },
                {
                    "title": "Scalable",
                    "body": (
                        "Support growing transaction volumes, multiple payment methods, and "
                        "expanding business needs without fragmented systems."
                    ),
                    "icon": "/images/figma-reconciliation/icons/scalable.svg",
                },
                {
                    "title": "Actionable",
                    "body": (
                        "Turn transactions, settlements, routing outcomes, and risk signals "
                        "into clear operational visibility for faster decisions."
                    ),
                    "icon": "/images/figma-reconciliation/icons/actionable.svg",
                },
            ],
        },
        "path": {
            "title": "Built for Seamless Reconciliation",
            "body": [
                (
                    "Urbanrupee brings settlement tracking, transaction matching, and "
                    "reconciliation into one connected financial workflow, helping businesses "
                    "maintain greater accuracy and visibility across every payment."
                ),
            ],
            "icons": [
                {
                    "id": "bank",
                    "src": "/images/figma-reconciliation/path/bank.svg",
                    "left": "22px",
                    "top": "280px",
                    "width": 22,
                    "height": 22,
                },
                {
                    "id": "trend",
                    "src": "/images/figma-reconciliation/path/trend.svg",
                    "left": "144px",
                    "top": "687px",
                    "width": 19,
                    "height": 19,
                },
                {
                    "id": "pod",
                    "src": "/images/figma-reconciliation/path/pod.svg",
                    "left": "857px",
                    "top": "311px",
                    "width": 21,
                    "height": 21,
                },
                {
                    "id": "route",
                    "src": "/images/figma-reconciliation/path/route.svg",
                    "left": "1008px",
                    "top": "521px",
                    "width": 21,
                    "height": 21,
                },
            ],
        },
        "showcase": {
            "title": "Everything You Need to Simplify Reconciliation",
                "body": (
                "Power your financial operations with connected capabilities designed to make "
                "transaction matching, and exception management more efficient."
            ),
            "rows": [
                {
                    "title": "Automated Matching",
                    "body": (
                        "Automatically match payment transactions with settlement records to "
                        "improve reconciliation accuracy and reduce manual effort."
                    ),
                    "image": "/images/figma-reconciliation/Frame%202147226717.svg",
                    "image_alt": (
                        "Settlement reconciliation dashboard showing matched transactions and "
                        "an amount mismatch detail"
                    ),
                    "image_width": 642,
                    "image_height": 365,
                    "side": "left",
                },
                {
                    "title": "Exception Visibility",
                "body": (
                        "Identify mismatches, missing transactions, and settlement exceptions "
                        "with clear visibility into issues that need attention."
                    ),
                    "image": "/images/figma-reconciliation/Frame%202147226952.svg?v=2",
                    "image_alt": (
                        "Settlement transactions table highlighting an exception with a "
                        "detected mismatch alert"
                    ),
                    "image_width": 637,
                    "image_height": 372,
                    "side": "right",
                },
                {
                    "title": "Faster Resolution",
                "body": (
                        "Give finance and operations teams the information they need to "
                        "investigate discrepancies and resolve settlement issues faster."
                    ),
                    "image": "/images/figma-reconciliation/Group%201171275349.svg",
                    "image_alt": (
                        "Side-by-side transaction and settlement records with a reconciled "
                        "success state"
                    ),
                    "image_width": 570,
                    "image_height": 373,
                    "side": "left",
                },
            ],
        },
    },
    "financial-operations": {
        "type": "financial-operations",
        "eyebrow": "financial operations infrastructure",
        "title": "Build Smarter Financial Experiences Without Building the Infrastructure",
        "intro": (
            "Power your products with scalable financial infrastructure that simplifies "
            "banking operations, payment flows, account services, and financial workflows "
            "through a connected ecosystem."
        ),
        "cta_label": "Talk to Expert",
        "infra": {
            "title": "The Infrastructure Behind Modern\nFinancial Operations",
            "body": (
                "Build and manage financial workflows through a flexible infrastructure "
                "designed to connect banking capabilities with your existing products and "
                "platforms."
            ),
        },
        "diagram": {
            "image": "/images/figma-financial-ops/baas-diagram.png?v=3",
            "image_alt": (
                "Urbanrupee BAAS platform connecting customers, beneficiaries, and payment "
                "methods through a single integration"
            ),
            "image_width": 1291,
            "image_height": 813,
        },
        "advantages": {
            "title": "Turn Financial Complexity Into Operational Advantage",
            "body": (
                "Simplify financial operations while creating a more connected, scalable, "
                "and efficient infrastructure for your business."
            ),
            "cards": [
                {
                    "title": "Faster Time to Market",
                    "body": (
                        "Launch financial capabilities faster with ready-to-integrate "
                        "infrastructure that eliminates the need to build every component "
                        "from scratch."
                    ),
                },
                {
                    "title": "Reduced Operational Complexity",
                    "body": (
                        "Bring fragmented financial workflows together through a connected "
                        "infrastructure layer that simplifies day-to-day operations."
                    ),
                },
                {
                    "title": "Greater Financial Visibility",
                    "body": (
                        "Gain a centralized view of accounts, transactions, payments, and "
                        "payouts for better operational control and decision-making."
                    ),
                },
                {
                    "title": "Automated Workflows",
                    "body": (
                        "Reduce manual intervention by automating repetitive financial "
                        "processes, from transaction tracking to reconciliation."
                    ),
                },
                {
                    "title": "Scalable Infrastructure",
                    "body": (
                        "Adapt to growing transaction volumes and evolving business "
                        "requirements with flexible infrastructure built for scale."
                    ),
                },
                {
                    "title": "Better Customer Experiences",
                    "body": (
                        "Embed financial capabilities directly into your products to create "
                        "smoother, more connected experiences for your customers."
                    ),
                },
            ],
        },
        "showcase": {
            "title": "One Infrastructure. Every Financial Flow.",
            "body": (
                "Connect collections, payouts, operational insights, and reconciliation "
                "through a unified platform built for seamless financial experiences."
            ),
            "cards": [
                {
                    "id": "visibility",
                    "title": "Operational Visibility",
                    "body": (
                        "Access better insight into transactions, settlements, and service "
                        "activity."
                    ),
                    "image": "/images/figma-financial-ops/showcase/visibility.svg",
                    "image_alt": "Operational visibility dashboard with transaction KPIs",
                    "image_width": 604,
                    "image_height": 576,
                },
                {
                    "id": "collections",
                    "title": "Collections",
                    "body": (
                        "Send payments to customers, vendors, partners, employees, and other "
                        "beneficiaries through one unified payout flow."
                    ),
                    "image": "/images/figma-financial-ops/showcase/collections.svg",
                    "image_alt": "Collections QR scan and pay flow with payment received",
                    "image_width": 576,
                    "image_height": 542,
                },
                {
                    "id": "payout",
                    "title": "Payouts",
                    "body": (
                        "Enable outgoing payment workflows for customers, partners, and "
                        "business operations."
                    ),
                    "image": "/images/figma-financial-ops/showcase/payout.svg?v=2",
                    "image_alt": "Payout workflow distributing funds to multiple recipients",
                    "image_width": 576,
                    "image_height": 505,
                },
                {
                    "id": "reconciliation",
                    "title": "Reconciliation Support",
                    "body": (
                        "Track and manage financial workflows with stronger reporting and "
                        "operational clarity."
                    ),
                    "image": "/images/figma-financial-ops/showcase/reconciliation.svg?v=2",
                    "image_alt": (
                        "Auto reconciliation connecting payouts, payments, and settlements "
                        "to balanced books"
                    ),
                    "image_width": 576,
                    "image_height": 505,
                },
            ],
        },
        "mid_cta": {
            "title": "Build the Financial Infrastructure\nYour Business Needs",
            "body": (
                "Connect your products to scalable financial infrastructure and create "
                "smarter, more connected financial experiences."
            ),
            "cta_label": "Talk to Expert",
            "cards": [
                {
                    "id": "accounts",
                    "label": "Virtual Accounts",
                    "value": "12,480 Active Accounts",
                    "icon": "/images/figma-financial-ops/icons/account.svg",
                },
                {
                    "id": "transactions",
                    "label": "Transactions",
                    "value": "98.7% Success Rate",
                    "icon": "/images/figma-financial-ops/icons/transaction.svg",
                },
                {
                    "id": "dashboard",
                    "title": "Operational Dashboard",
                    "label": "Processed this month",
                    "value": "+18.2%",
                    "icon": "/images/figma-financial-ops/icons/dashboard.svg",
                },
            ],
        },
    },
    "aml-detector": {
        "type": "marketing",
        "title": "AML Detector",
        "intro": (
            "AI-Powered Anti-Money Laundering & Risk Intelligence\n\n"
            "Protect your business with Urbanrupee's advanced AML Detection Platform, designed to "
            "identify, prevent, and manage financial crime risks in real time. Powered by "
            "artificial intelligence, machine learning, and intelligent behavioral analytics, our "
            "solution continuously monitors transactions, detects suspicious activities, and helps "
            "organizations maintain regulatory compliance with confidence."
        ),
        "sections": [
            {
                "title": "Intelligent Risk Monitoring",
                "body": (
                    "Leverage real-time transaction monitoring and AI-driven risk assessment to "
                    "identify unusual behavior, suspicious transaction patterns, and potential "
                    "money laundering activities before they become threats."
                ),
                "bullets_heading": "Key Capabilities",
                "bullets": [
                    "Real-time transaction surveillance",
                    "Intelligent risk scoring and profiling",
                    "Behavioral pattern analysis",
                    "Automated alert generation",
                    "Continuous monitoring across payment channels",
                ],
            },
            {
                "title": "AI-Powered Risk Assessment",
                "body": (
                    "Our machine learning models analyze thousands of risk indicators, customer "
                    "behaviors, and transaction attributes to deliver accurate risk assessments "
                    "while significantly reducing false positives."
                ),
                "bullets_heading": "Key Benefits",
                "bullets": [
                    "Advanced machine learning algorithms",
                    "Dynamic risk scoring engine",
                    "Behavioral intelligence monitoring",
                    "Global sanctions and watchlist screening",
                    "Adaptive threat detection capabilities",
                ],
            },
            {
                "title": "Compliance & Regulatory Management",
                "body": (
                    "Stay ahead of evolving compliance requirements with a comprehensive AML "
                    "framework that supports customer verification, due diligence, transaction "
                    "reporting, and regulatory oversight."
                ),
                "bullets_heading": "Compliance Features",
                "cards": [
                    {
                        "title": "KYC Verification",
                        "body": "Secure and automated identity verification to streamline onboarding and compliance checks.",
                    },
                    {
                        "title": "Customer Due Diligence (CDD/EDD)",
                        "body": "Enhanced customer screening and risk profiling for high-risk entities and transactions.",
                    },
                    {
                        "title": "Regulatory Reporting",
                        "body": "Automated report generation and audit-ready documentation to support regulatory obligations.",
                    },
                ],
            },
            {
                "title": "Real-Time Transaction Monitoring",
                "body": (
                    "Monitor every transaction as it happens with millisecond-level response times "
                    "and intelligent detection capabilities that help mitigate financial crime "
                    "risks before they impact your business."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Pattern Recognition",
                    "Risk Scoring",
                    "Instant Alerts",
                    "Case Management",
                    "Compliance Monitoring",
                ],
            },
            {
                "title": "Performance Highlights",
                "cards": [
                    {
                        "title": "< 50ms Detection Time",
                        "body": "Lightning-fast risk analysis and transaction screening.",
                    },
                    {
                        "title": "Up to 80% Fewer False Positives",
                        "body": "Improve operational efficiency through intelligent risk filtering.",
                    },
                    {
                        "title": "180+ Countries Supported",
                        "body": "Global monitoring capabilities for cross-border compliance and risk management.",
                    },
                    {
                        "title": "24/7 Continuous Monitoring",
                        "body": "Round-the-clock surveillance to detect and respond to emerging threats.",
                    },
                ],
            },
        ],
        "highlights": [
            {
                "title": "Why Choose Urbanrupee AML Detector?",
                "body": "Built for proactive risk intelligence, global compliance, and enterprise-grade protection.",
            },
            {
                "title": "Real-Time Detection",
                "body": "Identify suspicious activities instantly through continuous monitoring and intelligent threat detection.",
            },
            {
                "title": "Reduced False Positives",
                "body": "Advanced AI and machine learning models help reduce false alerts while maintaining high detection accuracy.",
            },
            {
                "title": "Global Compliance Coverage",
                "body": "Monitor transactions across multiple jurisdictions with support for global regulatory standards and compliance frameworks.",
            },
            {
                "title": "Enterprise-Grade Security",
                "body": "Secure infrastructure designed to protect sensitive financial data while ensuring regulatory compliance.",
            },
            {
                "title": "Actionable Risk Intelligence",
                "body": "Transform complex transaction data into meaningful insights that support faster and smarter decision-making.",
            },
        ],
    },
    "automatic-reconciliation": {
        "type": "marketing",
        "title": "Automatic Reconciliation",
        "intro": (
            "Intelligent Reconciliation. Zero Manual Effort.\n\n"
            "Streamline your financial operations with Urbanrupee's Automated Reconciliation "
            "Solution. Designed to eliminate manual intervention, our intelligent reconciliation "
            "engine automatically matches transactions across payment gateways, banks, wallets, "
            "merchant accounts, and internal systems in real time. Achieve greater accuracy, "
            "reduce operational overhead, and gain complete visibility into your financial "
            "ecosystem."
        ),
        "sections": [
            {
                "title": "Automated Transaction Matching",
                "body": (
                    "Leverage intelligent matching algorithms to automatically reconcile "
                    "transactions from multiple sources with speed and precision, ensuring "
                    "financial records remain accurate and up to date."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Real-time transaction matching",
                    "Multi-source reconciliation support",
                    "Intelligent fuzzy matching algorithms",
                    "Duplicate transaction detection",
                    "Automated settlement validation",
                ],
            },
            {
                "title": "Intelligent Discrepancy Management",
                "body": (
                    "Identify, track, and resolve mismatches instantly through automated exception "
                    "handling and advanced discrepancy management workflows."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Automated exception detection",
                    "Smart discrepancy resolution",
                    "Real-time alerts and notifications",
                    "Detailed audit trails",
                    "Comprehensive reconciliation reporting",
                ],
            },
            {
                "title": "Comprehensive Reconciliation Capabilities",
                "body": (
                    "Manage the entire reconciliation lifecycle through a centralized platform "
                    "built for scalability, transparency, and operational efficiency."
                ),
                "cards": [
                    {
                        "title": "Multi-Format Support",
                        "body": (
                            "Seamlessly process and reconcile data across CSV, Excel, XML, JSON, "
                            "and other standard formats."
                        ),
                    },
                    {
                        "title": "Bank Integrations",
                        "body": (
                            "Connect directly with banking partners and payment providers through "
                            "secure APIs for real-time reconciliation."
                        ),
                    },
                    {
                        "title": "Custom Matching Rules",
                        "body": (
                            "Configure business-specific reconciliation logic and workflows "
                            "tailored to your operational requirements."
                        ),
                    },
                ],
            },
            {
                "title": "Performance Highlights",
                "cards": [
                    {
                        "title": "95% Time Savings",
                        "body": (
                            "Reduce manual reconciliation efforts and operational costs through "
                            "intelligent automation."
                        ),
                    },
                    {
                        "title": "99.9% Matching Accuracy",
                        "body": (
                            "Ensure accurate financial records with advanced reconciliation "
                            "algorithms."
                        ),
                    },
                    {
                        "title": "Live Reconciliation Dashboard",
                        "body": (
                            "Monitor transaction status, exceptions, settlements, and "
                            "reconciliation performance in real time."
                        ),
                    },
                    {
                        "title": "End-to-End Visibility",
                        "body": (
                            "Track every transaction from payment initiation to settlement with "
                            "complete transparency."
                        ),
                    },
                ],
            },
        ],
        "highlights": [
            {
                "title": "Why Choose Urbanrupee Reconciliation?",
                "body": (
                    "Purpose-built to automate finance operations while delivering accuracy, "
                    "visibility, and compliance at scale."
                ),
            },
            {
                "title": "Save Up to 95% of Reconciliation Time",
                "body": (
                    "Automate repetitive manual processes and significantly improve operational "
                    "efficiency."
                ),
            },
            {
                "title": "99.9% Matching Accuracy",
                "body": (
                    "Advanced algorithms ensure highly accurate transaction matching with minimal "
                    "intervention."
                ),
            },
            {
                "title": "Complete Financial Visibility",
                "body": (
                    "Access real-time dashboards, transaction insights, reconciliation reports, "
                    "and audit-ready records from a single interface."
                ),
            },
            {
                "title": "Real-Time Processing",
                "body": (
                    "Monitor transaction matching and exception handling as events occur, enabling "
                    "faster financial decision-making."
                ),
            },
            {
                "title": "Secure & Compliant Operations",
                "body": (
                    "Built on enterprise-grade security standards with robust controls, audit "
                    "logs, and compliance-ready reporting."
                ),
            },
        ],
    },
    "white-label-platform": {
        "type": "white-label",
        "eyebrow": "White label solution",
        "title": "Launch Your Own Branded Payment Experience",
        "intro": (
            "Take control of your customer experience with a platform designed around your brand, "
            "supported by reliable technology and centralized management tools."
        ),
        "cta_label": "Talk to Expert",
        "metrics": [
            {"value": "100%", "label": "Your Branding"},
            {"value": "3x", "label": "Faster Product Launch"},
            {"value": "24/7", "label": "Platform Support"},
            {"value": "99.99%", "label": "Server Uptime"},
        ],
        "platform": {
            "title": "Your Brand. Your payment Platform. Our Technology.",
                "body": (
                "Deliver a seamless experience under your own brand with a customizable platform "
                "powered by reliable technology."
            ),
        },
        "steps": {
            "title": "Launch in 3 Simple Steps",
                "body": (
                "Payment orchestration acts as a centralized layer between your business and "
                "payment providers, helping you connect, manage, route, and optimize payments "
                "through a single integration."
            ),
            "items": [
                {
                    "number": "01.",
                    "title": "Customize Your Brand",
                "body": (
                        "Add your logo, brand colors to create a consistent platform experience "
                        "that reflects your unique brand identity."
                    ),
                    "image": "/images/figma-white-label/Frame%202147225861.svg?v=2",
                    "image_width": 375,
                    "image_height": 242,
                },
                {
                    "number": "02.",
                    "title": "Configure Your Platform",
                "body": (
                        "Choose the features, settings, and workflows that best match your "
                        "business requirements and operational needs."
                    ),
                    "image": "/images/figma-white-label/Frame%202147225859.svg?v=3",
                    "image_width": 498,
                    "image_height": 249,
                },
                {
                    "number": "03.",
                    "title": "Launch Under Your Brand",
                "body": (
                        "Deliver a fully branded platform experience to your customers while "
                        "managing everything through one centralized solution."
                    ),
                    "image": "/images/figma-white-label/Frame%202147225873.svg?v=2",
                    "image_width": 319,
                    "image_height": 269,
                },
            ],
        },
        "benefits": {
            "title": "Why Choose White Label?",
                "body": (
                "Build a payment experience that strengthens your business without "
                "adding operational complexity."
                ),
            "cards": [
            {
                    "title": "Lower Overhead",
                "body": (
                        "Reduce the need for multiple payment systems and simplify how "
                        "your business manages its payment ecosystem."
                ),
                    "icon": "/images/figma-white-label/icon-overhead.svg",
                    "icon_framed": True,
            },
            {
                    "title": "Stronger Trust",
                "body": (
                        "Deliver a consistent, professional payment experience that builds "
                        "confidence at every customer touchpoint."
                ),
                    "icon": "/images/figma-white-label/icon-trust.svg",
                    "icon_framed": False,
            },
            {
                    "title": "Business Focus",
                "body": (
                        "Let your team focus on customers and growth while the underlying "
                        "payment infrastructure is handled for you."
                ),
                    "icon": "/images/figma-white-label/icon-business.svg",
                    "icon_framed": False,
            },
            {
                    "title": "Ready to Scale",
                "body": (
                        "Support growing transaction volumes and evolving business needs "
                        "without rebuilding your payment operations."
                ),
                    "icon": "/images/figma-white-label/icon-scale-ready.svg",
                    "icon_framed": False,
            },
        ],
        },
    },
    "custom-checkout": {
        "type": "custom-checkout",
        "eyebrow": "Hosted & Branded Checkout",
        "title": "Own every step from cart to payment with a branded checkout",
        "intro": (
            "Design a checkout experience that matches your brand and gives you the flexibility "
            "to create a smooth, simple, and seamless payment journey for your customers."
        ),
        "cta_label": "Talk to Expert",
        "showcase": {
            "title": "One Checkout. Built Around Your Customers.",
                "body": (
                "Customize payment methods, checkout flows, and the overall experience from one place."
            ),
            "image": "/images/figma-custom-checkout/platform-visual.png",
            "image_width": 1291,
            "image_height": 813,
        },
        "features": {
            "title": "Customize Every Step of Checkout",
                        "body": (
                "Payment orchestration acts as a centralized layer between your business and "
                "payment providers, helping you connect, manage, route, and optimize payments "
                "through a single integration."
                        ),
            "items": [
                    {
                    "title": "Your Branding and Logo",
                        "body": (
                        "Show your logo and brand identity throughout checkout, so every payment "
                        "step feels like part of your product, not a third-party redirect."
                        ),
                    "graphic": "branding",
                    "image": "/images/figma-custom-checkout/feature-branding.png",
                    "image_width": 637,
                    "image_height": 349,
                    "reverse": False,
                    },
                    {
                    "title": "Configure Payment Methods",
                        "body": (
                        "Choose and manage the payment methods you want to offer, giving customers "
                        "more flexibility to pay using their preferred option."
                        ),
                    "graphic": "methods",
                    "image": "/images/figma-custom-checkout/feature-methods.png",
                    "image_width": 616,
                    "image_height": 351,
                    "reverse": True,
                    },
                    {
                    "title": "Design Your Experience",
                        "body": (
                        "Customize every detail of your checkout, from the layout and visual "
                        "elements to branding, ensuring it feels consistent with your business identity."
                    ),
                    "graphic": "design",
                    "image": "/images/figma-custom-checkout/feature-design.png",
                    "image_width": 586,
                    "image_height": 427,
                    "reverse": False,
                    },
                ],
            },
        "benefits": {
            "title": "Custom Checkout built for your brand",
                "body": (
                "Deliver a seamless experience under your own brand while managing your platform "
                "with greater flexibility, customization, and centralized control."
            ),
            "cards": [
                {
                    "title": "Your Brand, Your Checkout",
                    "body": "Customize the checkout experience to match your brand identity.",
                    "icon": "/images/figma-custom-checkout/icon-brand.svg",
                },
                {
                    "title": "Flexible Payment Options",
                    "body": "Offer customers the payment methods that work best for them.",
                    "icon": "/images/figma-custom-checkout/icon-flexible.svg",
                },
                {
                    "title": "Smooth Payment Experience",
                    "body": "Create a simple and seamless journey from checkout to payment.",
                    "icon": "/images/figma-custom-checkout/icon-smooth.svg",
                },
                {
                    "title": "Built for Your Business",
                    "body": "Configure checkout flows based on your business requirements.",
                    "icon": "/images/figma-custom-checkout/icon-business.svg",
                    },
                ],
            },
    },
    "hyper-checkout": {
        "type": "hyper-checkout",
        "eyebrow": "Hyper Checkout experience",
        "title": "Turn every checkout into a conversion opportunity",
        "intro": (
            "Create faster, smoother and more intuitive payment experiences that help customers "
            "complete their purchases with confidence."
        ),
        "cta_label": "Talk to Expert",
        "showcase": {
            "title": "Designed for less friction. Built for more conversions.",
                "body": (
                "Every interaction at checkout matters. Give your customers a payment experience "
                "that feels simple from the first click to the final confirmation."
                ),
            "image": "/images/figma-hyper-checkout/showcase-adaptive.png",
            "image_alt": "Adaptive Hyper Checkout with smart routing and payment modes",
            "image_width": 1291,
            "image_height": 638,
            },
        "smarter": {
            "title": "A Smarter Checkout, Built for Every Customer",
                "body": (
                "Deliver a seamless payment experience with intelligent payment selection, "
                "flexible payment options, and frictionless checkout."
            ),
            "image": "/images/figma-hyper-checkout/smarter-phone.svg",
            "image_alt": "Mobile Hyper Checkout with payment method logos",
            "image_width": 531,
            "image_height": 702,
            "cards": [
                {
                    "title": "Smart Payment Selection",
                "body": (
                        "Offer the right payment options based on customer preferences. "
                        "Make checkout faster and easier to complete."
                ),
                    "icon": "/images/figma-hyper-checkout/icons/smart-pay.svg",
            },
            {
                    "title": "Outage",
                "body": (
                        "Real-time alerts in the event of payment downtimes. "
                        "Stay ahead of disruptions and keep transactions flowing."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/quick-flow.svg",
                },
                {
                    "title": "Responsive Interface",
                "body": (
                        "Deliver a seamless checkout experience across all devices. "
                        "Keep the interface simple, clear, and easy to use."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/responsive.svg",
                },
                {
                    "title": "Seamless Experience",
                "body": (
                        "Create a smooth and consistent payment journey across every touchpoint. "
                        "Make every interaction simple, fast, and effortless."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/seamless.svg",
                },
            ],
        },
        "journey": {
            "title": "Turn a complex payment journey into a simple one",
                "body": (
                "Make every step of the payment journey simpler, faster and more relevant with an "
                "intelligent checkout built around customer preferences and payment behavior."
                ),
                "cards": [
                    {
                    "title": "Intelligent Payment Selection",
                        "body": (
                        "Present customers with relevant payment options, making it easier to find "
                        "their preferred way to pay and complete the transaction."
                        ),
                    "icon": "/images/figma-hyper-checkout/icons/payment.svg",
                    },
                    {
                    "title": "Streamlined Payment Flow",
                        "body": (
                        "Reduce unnecessary steps and interactions across the checkout journey, "
                        "helping customers move from payment selection to confirmation with ease."
                        ),
                    "icon": "/images/figma-hyper-checkout/icons/flow.svg",
                    },
                    {
                    "title": "Smart Failure Recovery",
                        "body": (
                        "When a payment attempt fails, guide customers toward relevant alternatives "
                        "instead of making them restart the entire checkout process."
                        ),
                    "icon": "/images/figma-hyper-checkout/icons/failure.svg",
            },
            {
                    "title": "Personalized Experience",
                "body": (
                        "Create a more intuitive checkout by adapting the payment journey to "
                        "different devices, payment methods and customer preferences."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/chart.svg",
                },
                {
                    "title": "One-Tap Repeat Payments",
                "body": (
                        "Enable customers to complete repeat purchases with fewer steps by "
                        "reducing unnecessary input across subsequent transactions."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/repeat.svg",
                },
            ],
        },
        "trust": {
            "title": "Everything you need to build a better checkout",
                "body": (
                "Give customers a faster, more flexible and reliable payment journey with "
                "capabilities designed to simplify every stage of checkout."
            ),
            "image": "/images/figma-hyper-checkout/Frame%202147226308.svg",
            "image_alt": "Multi-device Hyper Checkout experience",
            "image_width": 706,
            "image_height": 644,
            "cards": [
                {
                    "title": "Adaptive Checkout Experience",
                "body": (
                        "Adapt the checkout across devices and customer journeys for a seamless, "
                        "intuitive payment experience."
                ),
                    "icon": "/images/figma-hyper-checkout/icons/trust-payment.svg",
                    "image": "/images/figma-hyper-checkout/Frame%202147226308.svg",
                    "image_alt": "Multi-device Hyper Checkout experience",
            },
            {
                    "title": "Multi-Mode Payment Support",
                "body": (
                        "Offer multiple payment methods in one unified checkout, giving customers "
                        "the flexibility to pay their way."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/trust-modes.svg",
                    "image": "/images/figma-hyper-checkout/trust-modes.png",
                    "image_alt": (
                        "UPI, cards, wallets and netbanking connected to a single checkout"
                ),
            },
            {
                    "title": "Intelligent Routing Support",
                "body": (
                        "Route transactions through the most suitable payment path to improve "
                        "reliability and payment success."
                    ),
                    "icon": "/images/figma-hyper-checkout/icons/trust-routing.svg",
                    "image": "/images/figma-hyper-checkout/trust-routing.png",
                    "image_alt": (
                        "A payment routed across providers with successful and fallback outcomes"
                ),
            },
        ],
        },
    },
    "payment-orchestration": {
        "type": "orchestration",
        "eyebrow": "Payment Orchestration",
        "title": "Simplify and optimize your payments with your rules.",
        "intro": (
            "Connect multiple payment providers, intelligently route transactions, improve "
            "approval rates, and manage your entire payment ecosystem from one powerful platform."
        ),
        "cta_label": "Talk to Expert",
        "stats": [
            {"value": "95%", "label": "Payment Success Rate"},
            {"value": "80%", "label": "Reduced Failovers"},
            {"value": "92%", "label": "Reduced Ops Effort"},
            {"value": "50%", "label": "Reduced Latency"},
        ],
        "layer": {
            "title": "One Layer to Manage Every Payment",
                "body": (
                "Payment orchestration acts as a centralized layer between your business and "
                "payment providers, helping you connect, manage, route, and optimize payments "
                "through a single integration."
            ),
            "image": "/images/figma-orchestration/layer.svg",
            "image_alt": (
                "Payment methods flowing into a business rule engine that routes across gateways"
            ),
            "image_width": 1240,
            "image_height": 782,
        },
        "growth": {
            "title": "Turn Payment Complexity Into Business Growth",
                "body": (
                "Payment orchestration acts as a centralized layer between your business and "
                "payment providers, helping you connect, manage, route, and optimize payments "
                "through a single integration."
            ),
            "cards": [
                {
                    "title": "↑ Higher Approval Rates",
                    "body": "Increase successful transactions through smarter routing.",
                    "icon": "/images/figma-orchestration/growth/higher-approval.svg",
                    "icon_width": 53,
                    "icon_height": 55,
                    "framed": True,
                },
                {
                    "title": "↑ More Revenue Recovered",
                    "body": "Recover transactions that might otherwise fail.",
                    "icon": "/images/figma-orchestration/growth/more-revenue.svg",
                    "icon_width": 26,
                    "icon_height": 26,
                },
                {
                    "title": "↓ Lower Payment Costs",
                    "body": "Optimize provider selection and processing costs.",
                    "icon": "/images/figma-orchestration/growth/lower-costs.svg",
                    "icon_width": 26,
                    "icon_height": 26,
                },
                {
                    "title": "↓ Less Operational Complexity",
                    "body": "Centralize payment operations in one platform.",
                    "icon": "/images/figma-orchestration/growth/less-complexity.svg",
                    "icon_width": 26,
                    "icon_height": 26,
                },
            ],
        },
        "routing": {
            "title": "Smarter Routing for Better Payments",
            "body": (
                "Route every transaction intelligently with flexible rules designed to improve "
                "success, reduce costs, and optimize payment performance."
            ),
                "cards": [
                    {
                    "title": "Least Cost Routing",
                        "body": (
                        "Adapt the checkout across devices and customer journeys for a seamless, "
                        "intuitive payment experience."
                    ),
                    "image": "/images/figma-orchestration/routing/least-cost.svg",
                    "image_alt": (
                        "A payment routed to the lowest-cost gateway among three providers"
                        ),
                    },
                    {
                    "title": "Priority Based Routing",
                        "body": (
                        "Handle growing transaction volumes with infrastructure designed for "
                        "high-throughput payment environments."
                    ),
                    "image": "/images/figma-orchestration/routing/priority-based.svg",
                    "image_alt": (
                        "A payment request of 25000 rupees routed by gateway priority"
                        ),
                    },
                    {
                    "title": "MID Cascading",
                        "body": (
                        "Monitor transaction activity and payment performance through a "
                        "centralized view."
                    ),
                    "image": "/images/figma-orchestration/routing/mid-cascading.svg",
                    "image_alt": (
                        "A payment cascading across merchant IDs until one succeeds"
                        ),
                    },
                    {
                    "title": "Rule Based Routing",
                        "body": (
                        "Direct transactions through configured routes to support better payment "
                        "performance."
                    ),
                    "image": "/images/figma-orchestration/routing/rule-based.svg",
                    "image_alt": (
                        "A cost rule sending a payment to a fallback gateway after a failure"
                        ),
                    },
                ],
            },
        "control": {
            "title": "More Control Over Every Transaction",
                "body": (
                "Payment orchestration acts as a centralized layer between your business and "
                "payment providers, helping you connect, manage, route, and optimize payments "
                "through a single integration."
                ),
            "steps": [
            {
                    "num": "01",
                    "title": "Increase Payment Success Rates",
                "body": (
                        "Route transactions intelligently to improve authorization and approval "
                        "rates."
                ),
            },
            {
                    "num": "02",
                    "title": "One Unified Payment Platform",
                "body": (
                        "Manage multiple providers and payment methods through one integration, "
                        "giving you greater control."
                ),
            },
            {
                    "num": "03",
                    "title": "Simplify Your Payment Infrastructure",
                "body": (
                        "Connect and manage multiple payment providers through a centralized "
                        "orchestration layer."
                ),
            },
            {
                    "num": "04",
                    "title": "Smarter Payment Gateway Routing",
                "body": (
                        "Route every transaction through the most suitable gateway based on "
                        "performance and business rules."
                ),
            },
        ],
        },
    },
    "payout-portal": {
        "type": "marketing",
        "title": "Payouts",
        "intro": (
            "Simplify Disbursements. Accelerate Business Operations.\n\n"
            "Urbanrupee's Payout Portal is a powerful and secure disbursement platform designed to "
            "help businesses move money efficiently to vendors, partners, merchants, employees, and "
            "customers. Whether processing individual transfers or managing high-volume payout "
            "operations, our platform provides complete control, visibility, and automation from a "
            "single unified dashboard.\n\n"
            "Built for speed, reliability, and scalability, the Payout Portal streamlines outbound "
            "payments while reducing operational complexity and ensuring a seamless payout "
            "experience."
        ),
        "sections": [
            {
                "title": "Smart Beneficiary & Bulk Payout Management",
                "body": (
                    "Manage beneficiaries effortlessly through a centralized directory and execute "
                    "payouts individually or in bulk with maximum efficiency."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Centralized beneficiary management",
                    "Single and bulk payout processing",
                    "API-driven disbursements",
                    "Reusable payout templates",
                    "Secure beneficiary verification",
                ],
            },
            {
                "title": "Advanced Controls & Approval Workflows",
                "body": (
                    "Strengthen operational governance with intelligent approval mechanisms, "
                    "role-based permissions, and complete audit visibility."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Maker-checker approval workflows",
                    "Role-based access controls",
                    "Comprehensive audit trails",
                    "Configurable payout policies",
                    "Enhanced operational security",
                ],
            },
            {
                "title": "Real-Time Tracking & Visibility",
                "body": (
                    "Monitor every payout with complete transparency through live status updates, "
                    "detailed reporting, and actionable insights."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Real-time payout tracking",
                    "Transaction status monitoring",
                    "Detailed payout reporting",
                    "Batch-level visibility",
                    "Beneficiary-level insights",
                ],
            },
            {
                "title": "Flexible Payment Scheduling",
                "body": (
                    "Execute payouts instantly or automate disbursements according to your "
                    "preferred schedule and business requirements."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "Instant payouts",
                    "Scheduled disbursements",
                    "Automated payout cycles",
                    "Flexible settlement workflows",
                    "Smart payout orchestration",
                ],
            },
            {
                "title": "Seamless Integrations & Automation",
                "body": (
                    "Connect your existing financial ecosystem through robust APIs and automated "
                    "workflows designed to simplify operations."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "API-first architecture",
                    "ERP and accounting integrations",
                    "Automated reconciliation support",
                    "Ledger exports and reporting",
                    "Scalable payout infrastructure",
                ],
            },
            {
                "title": "Performance Highlights",
                "cards": [
                    {
                        "title": "Real-Time Payout Processing",
                        "body": (
                            "Execute and monitor payouts with speed, accuracy, and complete "
                            "visibility."
                        ),
                    },
                    {
                        "title": "Intelligent Approval Workflows",
                        "body": (
                            "Maintain governance and control through configurable approval "
                            "hierarchies."
                        ),
                    },
                    {
                        "title": "Bulk Disbursement Capabilities",
                        "body": (
                            "Process thousands of payouts efficiently through automated batch "
                            "operations."
                        ),
                    },
                    {
                        "title": "Unified Payout Dashboard",
                        "body": (
                            "Manage beneficiaries, transactions, settlements, and reports from one "
                            "centralized platform."
                        ),
                    },
                ],
            },
        ],
        "highlights": [
            {
                "title": "Why Choose Urbanrupee Payout Portal?",
                "body": (
                    "Built to automate disbursement operations with speed, visibility, control, and "
                    "reliability at scale."
                ),
            },
            {
                "title": "Faster Settlement Cycles",
                "body": (
                    "Automate payout operations and reduce manual intervention to accelerate fund "
                    "disbursement."
                ),
            },
            {
                "title": "Reduced Payout Failures",
                "body": (
                    "Built-in validation, intelligent processing, and retry mechanisms help improve "
                    "payout success rates."
                ),
            },
            {
                "title": "Complete Operational Visibility",
                "body": (
                    "Access a unified view of payouts, settlements, fees, statuses, and beneficiary "
                    "activity in real time."
                ),
            },
            {
                "title": "Secure & Compliant Infrastructure",
                "body": (
                    "Enterprise-grade security controls, audit logs, and compliance-focused "
                    "processes protect every transaction."
                ),
            },
            {
                "title": "Built for Scale",
                "body": (
                    "Handle growing payout volumes seamlessly through a resilient and "
                    "high-performance infrastructure."
                ),
            },
        ],
    },
    "unified-dashboard": {
        "type": "unified-dashboard",
        "eyebrow": "Unified Dashboard",
        "title": "One Dashboard. Complete Payment Visibility.",
        "intro": (
            "Manage transactions, settlements, payment performance, and merchant operations "
            "from one intelligent dashboard built for complete control."
        ),
        "cta_label": "Talk to Expert",
        "platform": {
            "title": "Everything You Need, All in One View",
            "body": (
                "Centralize transactions, payments, settlements, and insights in one dashboard."
            ),
            "image": "/images/figma-unified-dashboard/platform-diagram.png?v=4",
            "image_alt": (
                "Unified merchant dashboard connected to payment gateways and merchants"
            ),
            "image_width": 1291,
            "image_height": 523,
        },
        "control": {
            "title": "Built for Complete Payment Control",
            "body": (
                "Manage every aspect of your payment operations from one centralized dashboard."
            ),
            "cards": [
                {
                    "title": "Unified Visibility",
                    "body": (
                        "Get a centralized view of payment activity, transaction status, "
                        "settlements, providers, MIDs, and chargeback exposure in one place."
                    ),
                    "icon": "/images/figma-unified-dashboard/icons/api.svg",
                    "icon_width": 28,
                    "icon_height": 28,
                },
                {
                    "title": "Simplified Operations",
                    "body": (
                        "Manage day to day payment operations through a single interface "
                        "instead of switching between gateways, reports, and support workflows."
                    ),
                    "icon": "/images/figma-unified-dashboard/icons/graph.svg",
                    "icon_width": 24,
                    "icon_height": 24,
                },
                {
                    "title": "Smarter Routing Control",
                    "body": (
                        "Track provider performance, MID usage, fallback routes, and cascading "
                        "activity to improve payment continuity and success rates."
                    ),
                    "icon": "/images/figma-unified-dashboard/icons/routing.svg",
                    "icon_width": 24,
                    "icon_height": 24,
                },
                {
                    "title": "Chargeback Readiness",
                    "body": (
                        "Monitor dispute status, held funds, response timelines, and evidence "
                        "handling so teams can act faster and stay fully in control."
                    ),
                    "icon": "/images/figma-unified-dashboard/icons/cube.svg",
                    "icon_width": 24,
                    "icon_height": 24,
                },
            ],
        },
        "features": {
            "title": "Complete Visibility. Smarter Operations.",
            "body": (
                "Gain centralized control over payments, chargebacks, MIDs, and performance "
                "from one platform."
            ),
            "rows": [
                {
                    "title": "Centralized Visibility",
                    "body": (
                        "Access transaction activity, settlements, reports, and payment "
                        "operations from one dashboard."
                    ),
                    "image": "/images/figma-unified-dashboard/features/visibility-graphic.png",
                    "image_alt": (
                        "Payment overview dashboard with methods, volume, and settlements"
                    ),
                    "image_width": 571,
                    "image_height": 332,
                },
                {
                    "title": "MID Cascading Visibility",
                    "body": (
                        "See how traffic is routed across providers and MIDs, where fallback "
                        "happens, and how cascading improves continuity."
                    ),
                    "image": "/images/figma-unified-dashboard/features/cascading-graphic.svg",
                    "image_alt": (
                        "Parent and child MID hierarchy with transaction volume drill-down"
                    ),
                    "image_width": 709,
                    "image_height": 357,
                },
                {
                    "title": "Performance Insights",
                    "body": (
                        "Monitor payment trends, transaction outcomes, provider performance, "
                        "and operational patterns to identify improvement opportunities."
                    ),
                    "image": "/images/figma-unified-dashboard/features/insights-graphic.png",
                    "image_alt": (
                        "Revenue by payment method and transaction volume trend charts"
                    ),
                    "image_width": 600,
                    "image_height": 304,
                },
            ],
        },
        "path": {
            "title": "Built for Payment Operations at Scale",
            "body": [
                (
                    "Urbanrupee’s Unified Merchant Dashboard brings your payment operations "
                    "into one place. Track transactions, monitor performance, manage "
                    "settlements, and gain actionable insights all from a single, intuitive "
                    "platform."
                ),
            ],
            "icons": [
                {
                    "id": "bank",
                    "src": "/images/figma-unified-dashboard/path/icon-bank.svg",
                    "left": "22px",
                    "top": "280px",
                    "width": 22,
                    "height": 22,
                },
                {
                    "id": "trend",
                    "src": "/images/figma-unified-dashboard/path/icon-trend.svg",
                    "left": "144px",
                    "top": "687px",
                    "width": 19,
                    "height": 19,
                },
                {
                    "id": "pod",
                    "src": "/images/figma-unified-dashboard/path/icon-pod.svg",
                    "left": "857px",
                    "top": "311px",
                    "width": 21,
                    "height": 21,
                },
                {
                    "id": "route",
                    "src": "/images/figma-unified-dashboard/path/icon-routing.svg",
                    "left": "1008px",
                    "top": "521px",
                    "width": 21,
                    "height": 21,
                },
            ],
        },
    },
    "close-route-wallet": {
        "type": "marketing",
        "title": "Close Route Wallet",
        "intro": (
            "Controlled Value Movement. Complete Operational Visibility.\n\n"
            "Urbanrupee's Close Route Wallet enables businesses to create secure, controlled, and "
            "compliant wallet ecosystems where funds move only through approved channels. Built on "
            "a powerful ledger-based architecture, the platform provides complete control over how "
            "value is stored, transferred, and utilized while maintaining transparency, governance, "
            "and security at every stage.\n\n"
            "Whether you're building loyalty programs, fintech applications, merchant ecosystems, "
            "employee benefit solutions, or prepaid programs, Close Route Wallet delivers the "
            "flexibility and control enterprises demand."
        ),
        "sections": [
            {
                "title": "Controlled Wallet Ecosystem",
                "body": (
                    "Create secure wallet programs where funds circulate only within authorized "
                    "participants, merchants, and approved transaction routes."
                ),
                "bullets_heading": "Features",
                "bullets": [
                    "Approved funding source management",
                    "Wallet-to-wallet transfers",
                    "Wallet-to-merchant transactions",
                    "Controlled spending environments",
                    "Real-time treasury visibility",
                ],
            },
            {
                "title": "Governance, Risk & Compliance",
                "body": (
                    "Built for enterprises that require complete accountability, regulatory "
                    "alignment, and operational control over every movement of value."
                ),
                "bullets_heading": "Features",
                "bullets": [
                    "KYC-based user tiers",
                    "Configurable spending limits",
                    "Transaction control policies",
                    "Route-specific permissions",
                    "Immutable ledger records",
                    "Complete audit history",
                ],
            },
            {
                "title": "Connect Payments, Wallets & Payouts",
                "body": (
                    "Integrate Close Route Wallet seamlessly with Urbanrupee's payment "
                    "infrastructure to create a unified financial ecosystem."
                ),
                "cards": [
                    {
                        "title": "In-App Wallet Experience",
                        "body": (
                            "Deliver branded wallet functionality directly within your "
                            "applications, allowing users to load, manage, transfer, and spend "
                            "funds effortlessly."
                        ),
                    },
                    {
                        "title": "Webhooks & Real-Time Events",
                        "body": (
                            "Automate notifications, operational workflows, and backend processes "
                            "through powerful event-driven integrations."
                        ),
                    },
                    {
                        "title": "Finance & Operational Reporting",
                        "body": (
                            "Access comprehensive statements, transaction exports, reconciliation "
                            "reports, and audit-ready records whenever needed."
                        ),
                    },
                ],
            },
        ],
        "highlights": [
            {
                "title": "Why Businesses Choose Close Route Wallet",
                "body": (
                    "Purpose-built for secure closed-loop programs with ledger-grade control "
                    "and enterprise-scale operations."
                ),
            },
            {
                "title": "Closed-Loop Confidence",
                "body": (
                    "Ensure funds move only within approved networks, participants, and business "
                    "rules."
                ),
            },
            {
                "title": "Accelerated Time-to-Market",
                "body": (
                    "Launch wallet-led products without investing in complex ledger, treasury, "
                    "and compliance infrastructure."
                ),
            },
            {
                "title": "Complete Financial Visibility",
                "body": (
                    "Track balances, liabilities, transactions, and operational performance "
                    "through centralized dashboards."
                ),
            },
            {
                "title": "Enterprise Security & Governance",
                "body": (
                    "Protect value with robust controls, monitoring systems, audit trails, and "
                    "compliance-focused architecture."
                ),
            },
            {
                "title": "Built for Scale",
                "body": (
                    "Support growing transaction volumes, expanding user bases, and evolving "
                    "business models through flexible, API-driven infrastructure."
                ),
            },
        ],
    },
    "faq": {
        "type": "faq",
        "title": "Frequently Asked Questions",
        "intro": "Find answers to common questions about Urbanrupee's payment solutions and services.",
        "items": [
            {
                "question": "What is Urbanrupee Hyper Checkout?",
                "answer": (
                    "Hyper Checkout delivers faster UPI, card, net banking, wallet, and EMI payments "
                    "with smart routing and one-click flows for higher conversion rates."
                ),
                "links": [
                    {"label": "Explore Hyper Checkout", "href": "/products/hyper-checkout"},
                ],
            },
            {
                "question": "What is payment orchestration?",
                "answer": (
                    "Payment orchestration intelligently routes transactions across PSPs and banks "
                    "to maximize success rates, uptime, and performance."
                ),
                "links": [
                    {"label": "Payment Orchestration Platform", "href": "/products/orchestration"},
                ],
            },
            {
                "question": "How do I create my Urbanrupee account?",
                "answer": (
                    "Download our mobile app or visit our website. Click 'Sign Up' or 'Register', "
                    "provide your mobile number, verify with OTP, and set a secure password."
                ),
            },
            {
                "question": "How can I add money to my Urbanrupee wallet?",
                "answer": (
                    "Use UPI, Net Banking, Debit Cards, or Credit Cards. Navigate to 'Wallet', "
                    "select 'Add Money', enter the amount, and follow the secure steps."
                ),
            },
            {
                "question": "How can I view my transaction history?",
                "answer": (
                    "Go to 'Transaction History' or 'My Orders' in the app or website to see all "
                    "past payments and recharges."
                ),
            },
            {
                "question": "Is it safe to make payments online with Urbanrupee?",
                "answer": (
                    "Yes. We use SSL encryption, PCI DSS compliance, and robust fraud detection. "
                    "Keep your credentials confidential and use secure networks."
                ),
            },
            {
                "question": "Can I make payments using my phone through Urbanrupee?",
                "answer": (
                    "Yes. Use the Urbanrupee mobile app to pay with wallet balance, UPI, linked "
                    "bank accounts, or saved cards."
                ),
            },
        ],
        "product_links": {
            "title": "Popular Urbanrupee products",
            "intro": "Explore product pages for checkout, orchestration, UPI, and payouts.",
            "items": [
                {"label": "Unified Dashboard", "href": "/products/unified-dashboard"},
                {"label": "Hyper Checkout", "href": "/products/hyper-checkout"},
                {"label": "Custom Checkout", "href": "/products/custom-checkout"},
                {"label": "Payment Orchestration", "href": "/products/orchestration"},
                {"label": "UPI Switch", "href": "/products/upi-switch"},
                {"label": "Payouts", "href": "/services/payouts"},
                {"label": "Affordability (EMI & BNPL)", "href": "/products/affordability"},
            ],
        },
        "cta": {
            "title": "Still have questions?",
            "body": "Can't find the answer you're looking for? Reach out to our support team.",
            "button": "Contact Us",
            "href": "/contact",
        },
    },
    "blog": {
        "type": "blog",
        "title": "Urbanrupee Blog",
        "intro": (
            "Insights on payments, orchestration, compliance, and building resilient fintech "
            "products with Urbanrupee."
        ),
        "posts": [
            {
                "category": "Payment Orchestration",
                "date": "Jan 17, 2025",
                "title": "Payment Orchestration: Maximizing Acceptance Rates for Global Merchants",
                "slug": "orchestration-acceptance-rates",
                "href": "/products/orchestration",
            },
            {
                "category": "Fintech Innovation",
                "date": "Jan 22, 2025",
                "title": "How to Build a Scalable Payment Infrastructure for Growing Businesses",
                "slug": "scalable-payment-infrastructure",
                "href": "/products/hyper-checkout",
            },
            {
                "category": "Global Payments",
                "date": "Jan 23, 2025",
                "title": "Understanding TSP/PSP Solutions: A Complete Guide for Enterprises",
                "slug": "tsp-psp-guide",
                "href": "/products/upi-switch",
            },
            {
                "category": "E-Commerce Payments",
                "date": "Jan 25, 2025",
                "title": "E-Commerce Enablement: Transforming Online Payment Experiences",
                "slug": "ecommerce-enablement",
                "href": "/products/custom-checkout",
            },
        ],
    },
    "privacy-policy": {
        "type": "privacy",
        "title": "Privacy Policy",
        "intro": "Last Updated: 28 September 2026",
        "sections": [
            {
                "id": "scope",
                "title": "Scope",
                "body": (
                    "This Privacy Policy explains how Urbanrupee Techsolution Private Limited "
                    "(\u201cUrbanrupee\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d) collects, uses, "
                    "stores, and protects information when you visit our website, use our services, "
                    "communicate with us, or otherwise interact with Urbanrupee.\n\n"
                    "This Privacy Policy applies to our website, products, services, merchant onboarding "
                    "processes, payment and financial technology solutions, and related business "
                    "interactions.\n\n"
                    "By accessing or using our website or services, you acknowledge that you have read "
                    "and understood this Privacy Policy."
                ),
            },
            {
                "id": "information-we-collect",
                "title": "Information We Collect",
                "body": (
                    "Urbanrupee may collect information that is necessary to provide our services, "
                    "establish and maintain merchant relationships, comply with applicable legal and "
                    "regulatory requirements, and maintain the security of our platform."
                ),
                "subsections": [
                    {
                        "title": "Personal and Contact Information",
                        "body": (
                            "We may collect information such as your name, business email address, phone "
                            "number, designation, communication details, and other information you "
                            "voluntarily provide when you contact us, register with us, or communicate "
                            "with our team."
                        ),
                    },
                    {
                        "title": "Merchant and Business Information",
                        "body": (
                            "For merchants and business users, we may collect information such as business "
                            "or company name, registered address, business type, website or application "
                            "details, business registration information, nature of business, ownership or "
                            "authorised representative details, and other information required to "
                            "understand and support the merchant relationship."
                        ),
                    },
                    {
                        "title": "KYC and Compliance Information",
                        "body": (
                            "Where required for onboarding, verification, risk management, or regulatory "
                            "compliance, we may collect KYC, business verification, beneficial ownership, "
                            "identification, financial, and other compliance-related information and "
                            "documents."
                        ),
                    },
                    {
                        "title": "Transaction and Payment Information",
                        "body": (
                            "Depending on the services used, we may process information related to "
                            "transactions, payment activity, settlement details, payment status, refunds, "
                            "reconciliation, and other information required to provide and manage our "
                            "services."
                        ),
                    },
                    {
                        "title": "Technical and Website Information",
                        "body": (
                            "When you use our website, we may automatically collect technical information "
                            "such as IP address, browser type, device information, operating system, pages "
                            "visited, access times, and other usage information. This information helps us "
                            "maintain website functionality, security, and performance."
                        ),
                    },
                ],
            },
            {
                "id": "how-we-use",
                "title": "How Urbanrupee Uses Personal Information",
                "body": (
                    "Urbanrupee may use personal and business information to provide and manage our "
                    "services, onboard and verify merchants, communicate with users and merchants, "
                    "process and support transactions, manage settlements and reconciliation, conduct "
                    "risk and fraud monitoring, meet applicable KYC and compliance requirements, maintain "
                    "platform security, respond to enquiries, improve our services, and comply with "
                    "applicable legal and regulatory obligations.\n\n"
                    "We use information only for legitimate business, service, security, compliance, and "
                    "operational purposes connected with our relationship with you."
                ),
            },
            {
                "id": "merchant-information",
                "title": "Protection of Merchant and Business Information",
                "body": (
                    "Urbanrupee respects the confidentiality of merchant and business information. We do "
                    "not sell, rent, or commercially exploit merchant information, and we do not disclose "
                    "merchant information to unrelated third parties for their independent commercial "
                    "purposes.\n\n"
                    "Access to merchant information is limited to authorised personnel, systems, and "
                    "service providers who require access for legitimate business, operational, security, "
                    "compliance, or service-related purposes.\n\n"
                    "Merchant information may be processed or disclosed where necessary to provide "
                    "requested services, meet legal or regulatory requirements, prevent fraud or security "
                    "incidents, or comply with a lawful request."
                ),
            },
            {
                "id": "data-security",
                "title": "Data Security",
                "body": (
                    "Urbanrupee uses appropriate technical, organisational, and administrative safeguards "
                    "to protect information against unauthorised access, use, alteration, disclosure, "
                    "loss, or destruction.\n\n"
                    "Our security practices may include access controls, authentication mechanisms, "
                    "encryption, monitoring, vulnerability management, security testing, system "
                    "segregation, and other appropriate security measures.\n\n"
                    "While we take reasonable measures to protect information, no method of transmission "
                    "or electronic storage can be guaranteed to be completely secure."
                ),
            },
            {
                "id": "pci-dss",
                "title": "PCI DSS and Information Security",
                "body": (
                    "Urbanrupee follows applicable information security and payment security practices "
                    "and maintains controls aligned with relevant industry and regulatory requirements.\n\n"
                    "Urbanrupee maintains PCI DSS and ISO 27001-related security controls applicable to "
                    "its operations and scope. Our security environment is designed to protect sensitive "
                    "information and support the confidentiality, integrity, and availability of our "
                    "systems and services.\n\n"
                    "Where hosted or redirected payment interfaces are used, payment information is "
                    "handled according to the applicable service architecture and security controls."
                ),
            },
            {
                "id": "data-retention",
                "title": "Data Retention",
                "body": (
                    "Urbanrupee generally follows a 90-day data retention period for standard operational "
                    "data.\n\n"
                    "Certain information may also remain stored in backend systems for a minimum period "
                    "of one year as part of system and service operations."
                ),
            },
            {
                "id": "cookies",
                "title": "Cookies and Similar Technologies",
                "body": (
                    "Urbanrupee may use cookies and similar technologies to improve website "
                    "functionality, remember preferences, maintain security, and understand how visitors "
                    "use our website.\n\n"
                    "Cookies may be session-based or may remain on your device for a certain period. You "
                    "may manage or disable cookies through your browser settings. Disabling certain "
                    "cookies may affect some website functionality."
                ),
            },
            {
                "id": "analytics",
                "title": "Analytics and Website Usage",
                "body": (
                    "Urbanrupee may use analytics and website usage information to understand how "
                    "visitors interact with our website, monitor performance, identify technical issues, "
                    "improve user experience, and maintain security and functionality.\n\n"
                    "Where analytics tools are used, the information collected will be handled in "
                    "accordance with applicable privacy and security requirements."
                ),
            },
            {
                "id": "your-rights",
                "title": "Users\u2019 Rights and Requests",
                "body": (
                    "Subject to applicable laws and regulatory requirements, you may contact Urbanrupee to "
                    "request access to, correction of, or updates to your personal information. Where "
                    "applicable, you may also request deletion of your personal information or withdrawal "
                    "of consent.\n\n"
                    "Certain information may need to be retained for legal, regulatory, security, "
                    "contractual, or other legitimate purposes. We may require reasonable verification "
                    "before processing your request."
                ),
            },
            {
                "id": "merchant-responsibility",
                "title": "Merchant Responsibility",
                "body": (
                    "Merchants are responsible for ensuring that the information they provide to "
                    "Urbanrupee is accurate, complete, lawful, and up to date.\n\n"
                    "Merchants are also responsible for obtaining any necessary permissions or consents "
                    "before providing personal information of their customers, employees, "
                    "representatives, beneficial owners, or other individuals to Urbanrupee."
                ),
            },
            {
                "id": "data-accuracy",
                "title": "Data Accuracy",
                "body": (
                    "We rely on information provided by users and merchants to provide our services "
                    "effectively. You are responsible for ensuring that the information you provide "
                    "remains accurate and updated.\n\n"
                    "If your information changes, you should notify Urbanrupee or update the information "
                    "through the applicable service or communication channel."
                ),
            },
            {
                "id": "security-incidents",
                "title": "Data Breach and Security Incidents",
                "body": (
                    "Urbanrupee maintains security measures designed to identify, prevent, investigate, "
                    "and respond to security incidents.\n\n"
                    "If Urbanrupee becomes aware of a security incident involving personal information, "
                    "we will take appropriate steps to investigate, contain, and address the incident and "
                    "make any notifications required under applicable laws or regulations."
                ),
            },
            {
                "id": "confidentiality",
                "title": "Confidentiality",
                "body": (
                    "Urbanrupee treats confidential business and personal information with appropriate "
                    "care. Access to such information is restricted to authorised personnel and service "
                    "providers who require it for legitimate business or service-related purposes.\n\n"
                    "We expect our employees, representatives, contractors, and relevant service providers "
                    "to maintain the confidentiality of information accessed in connection with their work."
                ),
            },
            {
                "id": "changes",
                "title": "Changes to This Privacy Policy",
                "body": (
                    "Urbanrupee may update this Privacy Policy from time to time to reflect changes in our "
                    "services, technology, business practices, legal requirements, or regulatory "
                    "requirements.\n\n"
                    "Any updated version will be published on our website with the revised \u201cLast "
                    "Updated\u201d date. We encourage users and merchants to review this Privacy Policy "
                    "periodically."
                ),
            },
            {
                "id": "contact-us",
                "title": "Grievance and Privacy Contact",
                "body": (
                    "If you have any questions, concerns, requests, or complaints regarding this Privacy "
                    "Policy or the handling of your personal information, you may contact us using the "
                    "details below:\n\n"
                    "Urbanrupee Techsolution Private Limited\n"
                    "Registered Office: A01 & A03, UG, Tower 3, NX-One, Techzone 4, Greater Noida, "
                    "Uttar Pradesh, India\n"
                    "Website: urbanrupee.com\n"
                    "Email: it.support@urbanrupee.com\n"
                    "Phone: +91 9305697870"
                ),
            },
            {
                "id": "governing-law",
                "title": "Governing Law",
                "body": (
                    "This Privacy Policy shall be governed by and interpreted in accordance with the laws "
                    "of India. Any disputes arising in connection with this Privacy Policy shall be "
                    "subject to the jurisdiction of the competent courts in India."
                ),
            },
        ],
        "cta": {
            "title": "Need help with privacy or data requests?",
            "body": "Talk to the Urbanrupee team for privacy, compliance, or account-related questions.",
            "button": "Contact Us",
            "href": "/contact",
        },
    },
    "terms-and-conditions": {
        "type": "privacy",
        "title": "Terms and Conditions",
        "intro": (
            "These Terms and Conditions govern your access to and use of Urbanrupee's website, "
            "platform, payment infrastructure, merchant tools, checkout services, payout services, "
            "reconciliation services, APIs, dashboards, and related offerings."
        ),
        "sections": [
            {
                "id": "acceptance",
                "title": "Acceptance of Terms",
                "body": (
                    "By accessing or using Urbanrupee's services, you agree to be bound by these "
                    "Terms and Conditions."
                ),
            },
            {
                "id": "definitions",
                "title": "Definitions",
                "bullets": [
                    "Urbanrupee refers to the company, website, platform, products, and services.",
                    "User refers to any individual or entity accessing or using the services.",
                    (
                        "Merchant refers to any business or organization using Urbanrupee's payment "
                        "or operational services."
                    ),
                    (
                        "Services refers to all software, products, APIs, payment solutions, "
                        "dashboards, integrations, and related offerings provided by Urbanrupee."
                    ),
                ],
            },
            {
                "id": "eligibility",
                "title": "Eligibility",
                "body": (
                    "You may use Urbanrupee only if you are legally capable of entering into "
                    "binding contracts and are authorized to act on behalf of the business or "
                    "entity you represent."
                ),
            },
            {
                "id": "use-of-services",
                "title": "Use of Services",
                "body": "Users agree to use Urbanrupee's services only for lawful and authorized business purposes. You agree not to:",
                "bullets": [
                    "Use the services for fraudulent, unlawful, misleading, or abusive activities.",
                    "Violate applicable payment, financial, data protection, or consumer laws.",
                    "Interfere with platform security, infrastructure, or service availability.",
                    "Attempt unauthorized access to data, systems, APIs, or accounts.",
                    (
                        "Use the services in any manner that could harm Urbanrupee, its partners, "
                        "merchants, or end users."
                    ),
                ],
            },
            {
                "id": "merchant-responsibilities",
                "title": "Merchant Responsibilities",
                "body": "Merchants using Urbanrupee are responsible for:",
                "bullets": [
                    "Providing accurate onboarding and business information.",
                    "Maintaining the confidentiality of account credentials and API keys.",
                    "Complying with applicable laws, regulations, and network requirements.",
                    "Ensuring lawful use of checkout, collections, payouts, and related services.",
                    "Maintaining appropriate customer support, refund, and dispute handling practices.",
                    (
                        "Ensuring any content, branding, and customer communications used through "
                        "the platform are accurate and lawful."
                    ),
                ],
            },
            {
                "id": "service-availability",
                "title": "Service Availability",
                "body": (
                    "Urbanrupee strives to maintain reliable service availability. However, we do "
                    "not guarantee uninterrupted or error-free access at all times. Service may be "
                    "affected by maintenance, technical failures, third-party partner downtime, "
                    "regulatory actions, or events beyond our reasonable control."
                ),
            },
            {
                "id": "third-party-providers",
                "title": "Third-Party Providers",
                        "body": (
                    "Certain services may depend on banks, payment gateways, acquiring institutions, "
                    "UPI partners, technology vendors, or other third-party providers. Urbanrupee "
                    "is not liable for failures, delays, or interruptions caused solely by such "
                    "third-party systems."
                        ),
                    },
                    {
                "id": "fees",
                "title": "Fees and Commercial Terms",
                        "body": (
                    "Use of certain Urbanrupee services may be subject to separate commercial "
                    "agreements, pricing schedules, onboarding documents, or service orders. Users "
                    "and merchants agree to pay all applicable fees, charges, taxes, and levies "
                    "associated with the use of the services."
                        ),
                    },
                    {
                "id": "compliance",
                "title": "Compliance and Verification",
                        "body": (
                    "Urbanrupee may request documents, KYC details, business verification records, "
                    "and related compliance information as required by law, internal risk controls, "
                    "or partner obligations. Urbanrupee may suspend or restrict services if required "
                    "information is not provided or if suspicious or prohibited activity is identified."
                        ),
                    },
                    {
                "id": "intellectual-property",
                "title": "Intellectual Property",
                        "body": (
                    "All content, software, branding, trademarks, designs, interfaces, technology, "
                    "and materials made available by Urbanrupee are the intellectual property of "
                    "Urbanrupee or its licensors. Users may not copy, reproduce, modify, distribute, "
                    "reverse engineer, or exploit any part of the services without prior written permission."
                        ),
                    },
                    {
                "id": "data-and-privacy",
                "title": "Data and Privacy",
                        "body": (
                    "Use of Urbanrupee is also governed by our Privacy Policy. By using the services, "
                    "you acknowledge that Urbanrupee may collect, process, and use information in "
                    "accordance with that policy."
                ),
            },
            {
                "id": "suspension",
                "title": "Suspension and Termination",
                "body": "Urbanrupee may suspend, restrict, or terminate access to services where necessary to:",
                "bullets": [
                    "Prevent fraud or misuse.",
                    "Comply with legal or regulatory obligations.",
                    "Protect platform security.",
                    "Investigate suspicious or prohibited activity.",
                    "Enforce these Terms and Conditions.",
                ],
                "closing": (
                    "Users may stop using the services at any time, subject to any obligations in "
                    "separate commercial agreements."
                ),
            },
            {
                "id": "disclaimers",
                "title": "Disclaimers",
                "body": (
                    "Urbanrupee provides the website and services on an as-available and "
                    "as-applicable basis. To the fullest extent permitted by law, we disclaim all "
                    "warranties, whether express or implied, including merchantability, fitness for "
                    "a particular purpose, and non-infringement."
                ),
            },
            {
                "id": "liability",
                "title": "Limitation of Liability",
                        "body": (
                    "To the maximum extent permitted by law, Urbanrupee shall not be liable for any "
                    "indirect, incidental, special, punitive, or consequential damages, including "
                    "loss of profits, revenue, business, goodwill, or data, arising out of or "
                    "related to the use of the services."
                ),
                "closing": (
                    "Urbanrupee's aggregate liability shall be limited to the amount paid by the "
                    "user or merchant for the specific services giving rise to the claim, subject "
                    "to applicable law and any separate contractual agreement."
                        ),
                    },
                    {
                "id": "indemnity",
                "title": "Indemnity",
                        "body": (
                    "You agree to indemnify and hold harmless Urbanrupee, its affiliates, officers, "
                    "employees, partners, and service providers from any claims, damages, liabilities, "
                    "losses, or expenses arising from your misuse of the services, violation of "
                    "these Terms, breach of law, or infringement of any third-party rights."
                        ),
                    },
                    {
                "id": "governing-law",
                "title": "Governing Law and Jurisdiction",
                        "body": (
                    "These Terms and Conditions shall be governed by the laws of India. Any disputes "
                    "arising out of or relating to these Terms shall be subject to the exclusive "
                    "jurisdiction of the courts located in Greater Noida, Uttar Pradesh."
                ),
            },
            {
                "id": "changes",
                "title": "Changes to These Terms",
                "body": (
                    "Urbanrupee may update these Terms and Conditions from time to time. Revised "
                    "versions will be posted on this page with an updated effective date."
                ),
            },
            {
                "id": "contact-us",
                "title": "Contact Us",
                "body": (
                    "For any questions regarding these Terms and Conditions, please contact us:\n\n"
                    "Urbanrupee Techsolution Private Limited\n"
                    "Email: it.support@urbanrupee.com\n"
                    "Website: www.urbanrupee.com\n"
                    "Address: A01 & A03, UG, Tower 3, NX-One, Techzone 4, Greater Noida, "
                    "Uttar Pradesh, India, 201301"
                ),
            },
        ],
        "cta": {
            "title": "Questions about using Urbanrupee services?",
            "body": "Reach out to our team for clarifications on platform access, merchant onboarding, or service terms.",
            "button": "Contact Us",
            "href": "/contact",
        },
    },
    "upi-switch": {
        "type": "upi-switch",
        "eyebrow": "seamless upi switch",
        "title": "Power every UPI transaction with smarter switching",
        "intro": (
            "Connect, route and manage UPI payments through a reliable switching "
            "infrastructure built for speed, scale and higher payment success."
        ),
        "cta_label": "Talk to Expert",
        "architecture": {
            "title": "One switching layer. Multiple payment connections.",
            "body": (
                "Connect your merchant ecosystem to the UPI network through a centralized "
                "transaction management layer."
            ),
            "image": "/images/figma-upi/architecture.png?v=3",
            "image_alt": (
                "Urbanrupee Seamless UPI Switch connecting payment initiation, UPI network, "
                "bank pipes, and settlement"
            ),
            "image_width": 1291,
            "image_height": 813,
        },
        "features": {
            "title": "Everything you need to manage UPI at scale",
            "body": (
                "Power your UPI payment ecosystem with flexible routing, centralized "
                "connectivity and real-time transaction visibility."
            ),
            "cards": [
                {
                    "title": "Unified UPI API",
                "body": (
                        "Connect merchant payment flows to UPI acceptance through one "
                        "simplified integration layer."
                ),
                    "icon": "/images/figma-upi/icons/api.svg",
                    "icon_width": 28,
                    "icon_height": 28,
            },
            {
                    "title": "Routing Engine",
                "body": (
                        "Apply business rules and routing intelligence to guide UPI "
                        "transactions through the most suitable path."
                ),
                    "icon": "/images/figma-upi/icons/routing.svg",
                    "icon_width": 28,
                    "icon_height": 28,
            },
            {
                    "title": "Intent & QR Support",
                "body": (
                        "Support different UPI payment experiences through seamless intent "
                        "and QR based journeys."
                ),
                    "icon": "/images/figma-upi/icons/qr.svg",
                    "icon_width": 28,
                    "icon_height": 28,
            },
            {
                    "title": "Reconciliation Support",
                "body": (
                        "Improve operational control with better visibility into settlement "
                        "and transaction outcome status."
                    ),
                    "icon": "/images/figma-upi/icons/support.svg",
                    "icon_width": 28,
                    "icon_height": 28,
                },
            ],
        },
        "path": {
            "title": "Where every UPI transaction finds its path.",
            "body": [
                (
                    "Urbanrupee’s Seamless UPI Switch connects your business with the wider "
                    "UPI ecosystem through a unified switching layer. It simplifies payment "
                    "connectivity and gives you greater control over how transactions are "
                    "processed and routed."
                ),
                (
                    "With intelligent routing, real-time visibility and reliable transaction "
                    "management, businesses can deliver smoother UPI payment experiences while "
                    "staying ready to scale."
                ),
            ],
            "icons": [
                {
                    "id": "bank",
                    "src": "/images/figma-upi/icons/bank.svg",
                    "left": "22px",
                    "top": "280px",
                    "width": 22,
                    "height": 22,
                },
                {
                    "id": "trend",
                    "src": "/images/figma-upi/icons/trend.svg",
                    "left": "144px",
                    "top": "687px",
                    "width": 19,
                    "height": 19,
                },
                {
                    "id": "pod",
                    "src": "/images/figma-upi/icons/pod.svg",
                    "left": "857px",
                    "top": "311px",
                    "width": 21,
                    "height": 21,
                },
                {
                    "id": "route",
                    "src": "/images/figma-upi/icons/path-route.svg",
                    "left": "1008px",
                    "top": "521px",
                    "width": 21,
                    "height": 21,
                },
            ],
        },
        "capabilities": {
            "title": "Built to keep every UPI payment moving",
                "body": (
                "Simplify UPI connectivity and intelligently manage transaction flows "
                "through a single switching layer."
            ),
            "cards": [
                {
                    "title": "Reliable Connectivity",
                    "body": (
                        "Connect your payment ecosystem through a centralized UPI switching "
                        "infrastructure."
                    ),
                    "image": "/images/figma-upi/Frame 214722634.png?v=3",
                    "image_alt": (
                        "Primary and backup servers staying always connected through UPI switch"
                    ),
                    "image_width": 530,
                    "image_height": 488,
                },
                {
                    "title": "Intelligent Routing",
                "body": (
                        "Direct transactions through configured routes to support better "
                        "payment performance."
                    ),
                    "image": "/images/figma-upi/Group 1171275350.svg",
                    "image_alt": (
                        "Payment request routed to the optimal gateway among available options"
                    ),
                    "image_width": 466,
                    "image_height": 373,
                },
                {
                    "title": "Real-Time Visibility",
                    "body": (
                        "Monitor transaction activity and payment performance through a "
                        "centralized view."
                    ),
                    "image": "/images/figma-upi/Frame 2147226346.svg",
                    "image_alt": "Live transactions dashboard with success rate and latency",
                    "image_width": 466,
                    "image_height": 373,
                },
                {
                    "title": "Built to Scale",
                    "body": (
                        "Handle growing transaction volumes with infrastructure designed for "
                        "high-throughput payment environments."
                    ),
                    "image": "/images/figma-upi/Frame 2147226365.svg",
                    "image_alt": "Transaction volume scaling from 10K to 1M+ transactions per minute",
                    "image_width": 466,
                    "image_height": 373,
                },
            ],
        },
    },
    "affordability": {
        "type": "marketing",
        "title": "Affordability Solutions",
        "intro": (
            "Empower Purchases. Increase Conversions.\n\n"
            "Urbanrupee's Affordability Solutions help businesses unlock higher sales and improve "
            "customer satisfaction by offering flexible payment options directly within the checkout "
            "experience. Through EMI, Cardless EMI, and Buy Now Pay Later (BNPL) solutions, customers "
            "gain the flexibility to purchase with confidence while businesses benefit from increased "
            "conversions, larger basket sizes, and stronger customer loyalty.\n\n"
            "By seamlessly integrating affordability into the payment journey, Urbanrupee removes "
            "financial barriers and transforms high-value purchases into accessible opportunities."
        ),
        "sections": [
            {
                "title": "Flexible Payment Options for Every Customer",
                "body": (
                    "Give customers the freedom to choose how they pay through a range of "
                    "affordability solutions designed to fit different financial needs and "
                    "purchasing preferences."
                ),
                "bullets_heading": "Available Options",
                "bullets": [
                    "Credit Card EMI",
                    "Debit Card EMI",
                    "Cardless EMI",
                    "Buy Now Pay Later (BNPL)",
                    "No-Cost EMI Programs",
                    "Flexible Tenure Options",
                ],
            },
            {
                "title": "Increase Purchasing Power",
                "body": (
                    "Enable customers to spread payments over manageable installments, making premium "
                    "products and higher-value purchases more accessible."
                ),
                "bullets_heading": "Key Benefits",
                "bullets": [
                    "Improved purchase affordability",
                    "Flexible repayment plans",
                    "Reduced payment hesitation",
                    "Enhanced customer confidence",
                    "Higher purchase completion rates",
                ],
            },
            {
                "title": "Seamless Checkout Integration",
                "body": (
                    "Affordability options are embedded directly into the payment journey, ensuring "
                    "a smooth and frictionless customer experience without additional redirects or "
                    "complex application processes."
                ),
                "bullets_heading": "Key Features",
                "bullets": [
                    "In-line EMI options",
                    "One-click affordability selection",
                    "Real-time eligibility checks",
                    "Transparent repayment breakdowns",
                    "Optimized mobile experiences",
                ],
            },
            {
                "title": "Performance Highlights",
                "cards": [
                    {
                        "title": "Higher Basket Sizes",
                        "body": (
                            "Enable customers to comfortably purchase more through flexible "
                            "payment plans."
                        ),
                    },
                    {
                        "title": "Better Customer Retention",
                        "body": (
                            "Increase repeat purchases by providing payment flexibility customers value."
                        ),
                    },
                    {
                        "title": "Faster Purchase Decisions",
                        "body": (
                            "Reduce payment-related hesitation with clear, transparent affordability "
                            "options."
                        ),
                    },
                    {
                        "title": "Seamless Approval Experience",
                        "body": (
                            "Provide quick eligibility checks and simplified payment plan selection "
                            "within checkout."
                        ),
                    },
                ],
            },
            {
                "title": "Affordability That Drives Growth",
                "cards": [
                    {
                        "title": "Higher AOV",
                        "body": (
                            "Turn larger purchases into achievable decisions with flexible EMI and "
                            "Pay Later options."
                        ),
                    },
                    {
                        "title": "Seamless Checkout",
                        "body": (
                            "Offer affordability solutions directly within the payment flow without "
                            "adding friction or complexity."
                        ),
                    },
                    {
                        "title": "Stronger Customer Loyalty",
                        "body": (
                            "Create positive payment experiences that encourage repeat business and "
                            "long-term customer engagement."
                        ),
                    },
                ],
            },
        ],
        "highlights": [
            {
                "title": "Why Businesses Choose Urbanrupee Affordability",
                "body": (
                    "Flexible payment options built to lift conversions, basket size, and customer "
                    "loyalty at checkout."
                ),
            },
            {
                "title": "Higher Average Order Value (AOV)",
                "body": (
                    "Encourage customers to purchase higher-ticket products by making payments more "
                    "manageable through flexible installment options."
                ),
            },
            {
                "title": "Increased Conversion Rates",
                "body": (
                    "Reduce purchase barriers and improve checkout completion rates by providing "
                    "customers with more payment choices."
                ),
            },
            {
                "title": "Flexible EMI & BNPL Options",
                "body": (
                    "Offer multiple affordability solutions tailored to diverse customer needs and "
                    "spending behaviors."
                ),
            },
            {
                "title": "Frictionless Customer Experience",
                "body": (
                    "Embed affordability directly into checkout without disrupting the purchase journey."
                ),
            },
            {
                "title": "Improved Customer Retention",
                "body": (
                    "Build long-term customer relationships by offering convenient and flexible "
                    "payment experiences."
                ),
            },
        ],
    },
    "products-index": {
        "type": "hub",
        "title": "Urbanrupee Payment Products",
        "intro": (
            "Urbanrupee is a payment solutions platform that enables businesses to accept, process, "
            "route, and manage payments across UPI, cards, net banking, wallets, and EMI, with "
            "orchestration, checkout, payouts, and analytics in one suite."
        ),
        "sections": [
            {
                "heading": "Accept & Route Payments",
                "items": [
                    {
                        "title": "Collections",
                        "body": (
                            "Accept, track, reconcile, and manage payments across channels from a "
                            "single API built for high-volume businesses."
                        ),
                        "href": "/services/collections",
                    },
                    {
                        "title": "Payment Orchestration",
                        "body": (
                            "Route transactions intelligently across PSPs and banks to maximize success "
                            "rates, uptime, and performance at scale."
                        ),
                        "href": "/products/orchestration",
                    },
                    {
                        "title": "Hyper Checkout",
                        "body": (
                            "Fast UPI, card, net banking, wallet, and EMI checkout with smart routing "
                            "and conversion-focused flows."
                        ),
                        "href": "/products/hyper-checkout",
                    },
                    {
                        "title": "Custom Checkout",
                        "body": (
                            "Branded on-site checkout with UPI, cards, net banking, wallets, and EMI, "
                            "designed to reduce drop-offs."
                        ),
                        "href": "/products/custom-checkout",
                    },
                    {
                        "title": "UPI Switch",
                        "body": (
                            "High-volume UPI routing with multi-bank connectivity, low latency, and "
                            "enterprise-grade reliability."
                        ),
                        "href": "/products/upi-switch",
                    },
                    {
                        "title": "Affordability (EMI & Pay Later)",
                        "body": (
                            "Offer EMI, cardless EMI, and BNPL at checkout to lift AOV and conversions."
                        ),
                        "href": "/products/affordability",
                    },
                ],
            },
            {
                "heading": "Platform & Disbursements",
                "alt": True,
                "items": [
                    {
                        "title": "White Label Platform",
                        "body": (
                            "Launch payments under your own brand with customizable UI, APIs, and "
                            "scalable infrastructure."
                        ),
                        "href": "/products/white-label",
                    },
                    {
                        "title": "Payouts",
                        "body": (
                            "Automated vendor, merchant, and customer disbursements with bulk payouts "
                            "and real-time tracking."
                        ),
                        "href": "/services/payouts",
                    },
                    {
                        "title": "Unified Dashboard",
                        "body": (
                            "Centralize transactions, settlements, MID cascading, chargebacks, and "
                            "payment performance in one merchant control plane."
                        ),
                        "href": "/products/unified-dashboard",
                    },
                    {
                        "title": "Close Route Wallet",
                        "body": (
                            "Secure closed-loop wallet infrastructure with real-time visibility and "
                            "operational control."
                        ),
                        "href": "/products/wallet",
                    },
                ],
            },
        ],
        "cta": {"label": "Contact Sales", "href": "/contact"},
    },
    "resources-index": {
        "type": "hub",
        "title": "Urbanrupee Resources",
        "intro": (
            "Guides, FAQs, and insights on payment gateways, UPI, checkout optimization, "
            "orchestration, and fintech for Indian businesses."
        ),
        "sections": [
            {
                "heading": "Learn & Explore",
                "items": [
                    {
                        "title": "FAQ",
                        "body": (
                            "Answers about Urbanrupee products, UPI, checkout, orchestration, "
                            "security, and onboarding."
                        ),
                        "href": "/faq",
                    },
                    {
                        "title": "Blog",
                        "body": (
                            "Payment and fintech insights on gateways, UPI, compliance, and growth "
                            "strategies."
                        ),
                        "href": "/blog",
                    },
                    {
                        "title": "Privacy Policy",
                        "body": (
                            "How Urbanrupee collects, uses, and protects your data across our "
                            "website and services."
                        ),
                        "href": "/privacy-policy",
                    },
                    {
                        "title": "Contact Us",
                        "body": (
                            "Talk to our team for demos, merchant onboarding, and payment "
                            "infrastructure support."
                        ),
                        "href": "/contact",
                    },
                ],
            },
        ],
        "cta": {"label": "Get Started", "href": "/contact"},
    },
    "contact": {
        "type": "contact",
        "title": "Let’s Start a Conversation",
        "intro": (
            "Have a question or need more information? We’re here to help. "
            "Reach out to our team and we’ll get back to you shortly."
        ),
        "company": "Urbanrupee Techsolution Private Limited",
        "phone": "+91 9305697870",
        "email": "it.support@urbanrupee.com",
        "address": (
            "A01 & A03, UG, Tower 3, NX-One, Techzone 4, Greater Noida, "
            "Uttar Pradesh, India, 201301"
        ),
        "faq_title": "Got any questions? We've got you covered.",
        "faq_intro": (
            "Find clear answers about Urbanrupee products, payment orchestration, checkout, "
            "and how our platform helps businesses scale with better visibility and control."
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
            "unified platform, built to scale with your business."
        ),
        "cta_label": "Talk to an Expert",
        "catalogue_note": "As listed in the Urbanrupee Product Catalogue: NX-One, Gaur City.",
    },
}

# Vue route path -> API slug
ROUTE_SLUGS = {
    "/products": "products-index",
    "/resources": "resources-index",
    "/about": "about",
    "/services/payment": "collections",
    "/services/collections": "collections",
    "/services/payouts": "payouts",
    "/services/financial-operations": "financial-operations",
    "/services/risk-fraud-management": "risk-fraud-management",
    "/services/reconciliation": "reconciliation",
    "/products/white-label": "white-label-platform",
    "/products/custom-checkout": "custom-checkout",
    "/products/hyper-checkout": "hyper-checkout",
    "/products/orchestration": "payment-orchestration",
    "/products/upi-switch": "upi-switch",
    "/products/affordability": "affordability",
    "/products/unified-dashboard": "unified-dashboard",
    "/products/wallet": "close-route-wallet",
    "/faq": "faq",
    "/blog": "blog",
    "/privacy-policy": "privacy-policy",
    "/terms-and-conditions": "terms-and-conditions",
    "/contact": "contact",
}

SLUG_TO_ROUTE = {v: k for k, v in ROUTE_SLUGS.items()}
