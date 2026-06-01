/** Hero copy synced to Close Route Wallet dashboard metric highlight. */
export const WALLET_METRIC_HERO = {
  users: {
    headline: "Users — who can hold and move value",
    body:
      "Onboard programme participants with KYC tiers, roles, and eligibility rules so only approved identities access wallet balances.",
    bullets: [
      "Registered accounts with audit trail",
      "Tiered limits per user profile",
      "Ops admin & member roles",
    ],
  },
  wallets: {
    headline: "Wallets — balances inside your route",
    body:
      "Issue INR and multi-currency wallets that stay inside programme boundaries—loads, spends, and transfers only on rails you allow.",
    bullets: [
      "Per-user & programme wallets",
      "Currency-aware balances",
      "Real-time available balance",
    ],
  },
  journals: {
    headline: "Journal entries — immutable ledger postings",
    body:
      "Every credit and debit becomes an immutable journal row finance and compliance teams can reconcile without spreadsheet glue.",
    bullets: [
      "Double-entry style postings",
      "Reference IDs on every movement",
      "Export-ready activity history",
    ],
  },
  liability: {
    headline: "INR liability — treasury visibility",
    body:
      "See aggregate INR wallet balances as live liability so treasury knows float in circulation and can fund loads with confidence.",
    bullets: [
      "Sum of INR wallet balances",
      "Float vs. funding source tracking",
      "Daily liability snapshots",
    ],
  },
  posted: {
    headline: "Posted today — live programme pulse",
    body:
      "Track new journal activity as it lands so operations spots unusual volume, stuck flows, or batch jobs that need attention.",
    bullets: [
      "New rows since midnight",
      "Alerting on spikes & anomalies",
      "Same-day ops dashboards",
    ],
  },
  topups: {
    headline: "PG top-ups — loads via settlement API",
    body:
      "Fund wallets from approved payment-gateway settlements and bank loads—value enters the closed route only through whitelisted sources.",
    bullets: [
      "Settlement API integration",
      "Load confirmation webhooks",
      "No off-route funding paths",
    ],
  },
};

export function walletMetricHeroFor(id) {
  return WALLET_METRIC_HERO[id] || WALLET_METRIC_HERO.wallets;
}
