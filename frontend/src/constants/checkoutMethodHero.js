/** Hero copy synced to CheckoutCard payment tab (custom / hyper checkout). */
export const CHECKOUT_METHOD_HERO = {
  upi: {
    headline: "UPI — Instant, Familiar & High-Converting",
    body:
      "Enable customers to pay instantly through their preferred UPI apps with optimized payment flows and intelligent routing designed to maximize success rates.",
    bullets_heading: "Key Features",
    bullets: [
      "Dynamic QR codes and deep-link experiences",
      "Smart PSP routing for higher success rates",
      "VPA validation before payment initiation",
      "Real-time transaction status updates",
      "Instant payment confirmations",
    ],
  },
  cards: {
    headline: "Cards — Secure & Frictionless",
    body:
      "Deliver a modern card payment experience with tokenization, secure authentication, and optimized checkout journeys that improve customer confidence.",
    bullets_heading: "Key Features",
    bullets: [
      "Network tokenization support",
      "Credit and debit card acceptance",
      "PCI DSS compliant payment flows",
      "Secure authentication protocols",
      "Branded checkout experiences",
    ],
  },
  card: {
    headline: "Cards — Secure & Frictionless",
    body:
      "Deliver a modern card payment experience with tokenization, secure authentication, and optimized checkout journeys that improve customer confidence.",
    bullets_heading: "Key Features",
    bullets: [
      "Network tokenization support",
      "Credit and debit card acceptance",
      "PCI DSS compliant payment flows",
      "Secure authentication protocols",
      "Branded checkout experiences",
    ],
  },
  netbanking: {
    headline: "Net Banking — Trusted Banking Experience",
    body:
      "Provide customers with secure access to major banking networks through optimized redirects and seamless transaction processing.",
    bullets_heading: "Key Features",
    bullets: [
      "Broad banking coverage",
      "Secure bank authentication",
      "Intelligent session management",
      "Retry and recovery mechanisms",
      "Real-time payment status updates",
    ],
  },
  wallets: {
    headline: "Wallets — Faster Payments for Returning Customers",
    body:
      "Offer convenient wallet-based payments that reduce checkout time and improve repeat purchase experiences.",
    bullets_heading: "Key Features",
    bullets: [
      "Popular wallet integrations",
      "One-tap payment experiences",
      "Unified reconciliation framework",
      "Faster customer checkout",
      "Optimized mobile journeys",
    ],
  },
  emi: {
    headline: "EMI — Increase Affordability & Conversions",
    body:
      "Enable flexible payment options through EMI solutions that improve purchasing power and increase average transaction values.",
    bullets_heading: "Key Features",
    bullets: [
      "Multiple repayment tenures",
      "Card and cardless EMI options",
      "Transparent installment breakdowns",
      "Integrated affordability solutions",
      "Enhanced customer purchasing flexibility",
    ],
  },
};

export function checkoutMethodHeroFor(id) {
  return CHECKOUT_METHOD_HERO[id] || CHECKOUT_METHOD_HERO.upi;
}
