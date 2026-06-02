/** Hero copy synced to Close Route Wallet dashboard metric highlight. */
export const WALLET_METRIC_HERO = {
  wallets: {
    headline: "Wallets — Controlled Digital Value",
    body:
      "Issue and manage digital wallets that operate within clearly defined programme boundaries. Maintain complete control over how funds are loaded, transferred, spent, and tracked.",
    bullets_heading: "Key Benefits",
    bullets: [
      "Programme-specific wallet creation",
      "Multi-currency wallet support",
      "Real-time balance visibility",
      "Controlled fund movement",
      "Secure value storage",
    ],
  },
  users: {
    headline: "Users — Identity-Driven Access Control",
    body:
      "Enable only authorized participants to access and transact within your wallet ecosystem through configurable onboarding, verification, and eligibility frameworks.",
    bullets_heading: "Key Benefits",
    bullets: [
      "KYC-enabled onboarding",
      "Role-based user management",
      "Tiered access permissions",
      "Configurable transaction limits",
      "Complete user lifecycle control",
    ],
  },
  journals: {
    headline: "Journal Entries — Ledger-Grade Transparency",
    body:
      "Every transaction is securely recorded through an immutable ledger, ensuring complete traceability, accountability, and audit readiness.",
    bullets_heading: "Key Benefits",
    bullets: [
      "Immutable transaction records",
      "Complete audit trails",
      "Real-time journal postings",
      "Reference tracking for every transaction",
      "Export-ready financial records",
    ],
  },
  liability: {
    headline: "Treasury & Liability Management",
    body:
      "Gain complete visibility into wallet balances, liabilities, and funding positions through real-time treasury monitoring.",
    bullets_heading: "Key Benefits",
    bullets: [
      "Live liability tracking",
      "Float management visibility",
      "Funding source monitoring",
      "Treasury reporting",
      "Balance reconciliation support",
    ],
  },
  posted: {
    headline: "Live Programme Activity",
    body:
      "Monitor wallet activity as it happens through operational dashboards designed to identify trends, anomalies, and business-critical events.",
    bullets_heading: "Key Benefits",
    bullets: [
      "Real-time activity monitoring",
      "Operational alerts",
      "Volume tracking",
      "Anomaly detection",
      "Performance dashboards",
    ],
  },
  topups: {
    headline: "Controlled Wallet Funding",
    body:
      "Ensure value enters the ecosystem only through approved funding sources, creating a secure and compliant closed-loop environment.",
    bullets_heading: "Key Benefits",
    bullets: [
      "Approved funding channels",
      "Payment gateway integrations",
      "Settlement API connectivity",
      "Secure load mechanisms",
      "Automated funding confirmations",
    ],
  },
};

export function walletMetricHeroFor(id) {
  return WALLET_METRIC_HERO[id] || WALLET_METRIC_HERO.wallets;
}
