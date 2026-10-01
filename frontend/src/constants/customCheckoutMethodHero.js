/** Hero copy synced to CustomCheckoutHeroGraphic payment tabs. */
export const CUSTOM_CHECKOUT_METHOD_HERO = {
  upi: {
    headline: "UPI: Fast, Familiar & Frictionless",
    body:
      "Deliver instant UPI payment experiences through optimized payment flows, smart routing, and seamless user interactions.",
    bullets_heading: "Key Features",
    bullets: [
      "Dynamic QR and deep-link payments",
      "Intelligent PSP routing",
      "VPA validation before payment",
      "Real-time payment confirmation",
      "Optimized mobile experience",
    ],
  },
  cards: {
    headline: "Cards: Branded & Secure",
    body:
      "Offer a premium card payment experience through tokenized transactions, secure authentication, and fully customized interfaces.",
    bullets_heading: "Key Features",
    bullets: [
      "Network tokenization support",
      "Credit and debit card acceptance",
      "PCI DSS compliant architecture",
      "Branded payment forms",
      "Enhanced transaction security",
    ],
  },
  card: {
    headline: "Cards: Branded & Secure",
    body:
      "Offer a premium card payment experience through tokenized transactions, secure authentication, and fully customized interfaces.",
    bullets_heading: "Key Features",
    bullets: [
      "Network tokenization support",
      "Credit and debit card acceptance",
      "PCI DSS compliant architecture",
      "Branded payment forms",
      "Enhanced transaction security",
    ],
  },
  netbanking: {
    headline: "Net Banking: Trusted Banking Payments",
    body:
      "Provide secure bank-based payment options through seamless banking integrations and intelligent transaction handling.",
    bullets_heading: "Key Features",
    bullets: [
      "Extensive banking network coverage",
      "Secure bank authentication",
      "Retry and recovery workflows",
      "Real-time transaction updates",
      "Faster payment confirmations",
    ],
  },
  wallets: {
    headline: "Wallets: Convenient One-Tap Payments",
    body:
      "Enable customers to complete transactions quickly through popular wallet integrations and simplified payment journeys.",
    bullets_heading: "Key Features",
    bullets: [
      "Leading wallet integrations",
      "One-tap payment experiences",
      "Unified reconciliation framework",
      "Faster repeat purchases",
      "Seamless customer convenience",
    ],
  },
  emi: {
    headline: "EMI: Flexible Payment Experiences",
    body:
      "Increase affordability and encourage higher-value purchases through integrated EMI options directly within checkout.",
    bullets_heading: "Key Features",
    bullets: [
      "Multiple repayment tenures",
      "Card and cardless EMI support",
      "Transparent installment visibility",
      "Enhanced purchase flexibility",
      "Improved conversion potential",
    ],
  },
};

export function customCheckoutMethodHeroFor(id) {
  return CUSTOM_CHECKOUT_METHOD_HERO[id] || CUSTOM_CHECKOUT_METHOD_HERO.upi;
}
