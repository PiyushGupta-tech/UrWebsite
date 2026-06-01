/** Orchestration hero modes — aligned with payment-orchestration page sections. */
export const ORCHESTRATION_MODES = [
  {
    id: "smart",
    title: "Multi-provider",
    section: "Multi-Provider Routing",
    pickId: "airpay",
    rates: {
      airpay: 98.2,
      "jio-payments": 97.9,
      easebuzz: 98.4,
      cashfree: 98.1,
      unlimit: 99.0,
      payu: 98.5,
    },
  },
  {
    id: "failover",
    title: "Failover",
    section: "Failover Protection",
    downId: "jio-payments",
    pickId: "cashfree",
  },
  {
    id: "balance",
    title: "Load balance",
    section: "Routing rules",
    shares: {
      airpay: 18,
      "jio-payments": 16,
      easebuzz: 22,
      cashfree: 20,
      unlimit: 12,
      payu: 12,
    },
    pickId: "easebuzz",
  },
];
