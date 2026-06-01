/** Hero copy synced to CheckoutCard payment tab (custom / hyper checkout). */
export const CHECKOUT_METHOD_HERO = {
  upi: {
    headline: "UPI — instant, familiar, high success",
    body:
      "Offer intent, collect, and QR flows with smart routing across PSPs so customers pay in one tap from any UPI app.",
    bullets: [
      "Dynamic QR & deep links",
      "VPA validation before pay",
      "Real-time success webhooks",
    ],
  },
  cards: {
    headline: "Cards — tokenized, compliant checkout",
    body:
      "Accept debit and credit with saved-card tokens, 3DS when required, and a form layout that matches your brand.",
    bullets: [
      "Network tokenization",
      "Debit & credit (DC / CC)",
      "PCI-DSS hosted fields option",
    ],
  },
  card: {
    headline: "Cards — tokenized, compliant checkout",
    body:
      "Accept debit and credit with saved-card tokens, 3DS when required, and a form layout that matches your brand.",
    bullets: [
      "Network tokenization",
      "Debit & credit (DC / CC)",
      "PCI-DSS hosted fields option",
    ],
  },
  netbanking: {
    headline: "Net banking — trusted bank redirects",
    body:
      "Let shoppers pick their bank, complete a secure redirect, and return to your site with status surfaced instantly.",
    bullets: [
      "Major bank coverage",
      "Session & retry handling",
      "Settlement-ready callbacks",
    ],
  },
  wallets: {
    headline: "Wallets — one-tap for repeat buyers",
    body:
      "Connect popular Indian wallets so returning users pay faster without re-entering card or UPI details.",
    bullets: [
      "Leading wallet brands",
      "Balance & redirect flows",
      "Unified reconciliation",
    ],
  },
  emi: {
    headline: "EMI — higher ticket, smoother yes",
    body:
      "Surface cardless and card EMI plans at checkout to lift average order value without a separate affordability page.",
    bullets: [
      "Multiple tenures in-line",
      "Issuer & NBFC partners",
      "Transparent installment breakdown",
    ],
  },
};

export function checkoutMethodHeroFor(id) {
  return (
    CHECKOUT_METHOD_HERO[id] ||
    CHECKOUT_METHOD_HERO.upi
  );
}
