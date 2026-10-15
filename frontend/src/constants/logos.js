/** Shared Urbanrupee logo assets used across the frontend */
export const LOGO_PATHS = {
  /** Full wordmark for dark surfaces */
  onDark: "/images/figma-footer-logo.png",
  /** Full wordmark for light surfaces */
  onLight: "/logos/urbanrupee-nav.svg",
  /** Shield / favicon mark */
  icon: "/logos/favicon.svg",
  /** Chat launcher and assistant avatar */
  chatAssistant: "/logos/favicon.svg",
  /** Legacy alias kept for compatibility */
  glass: "/logos/favicon.svg",
};

/** Footer compliance marks */
export const CERT_LOGOS = [
  { id: "pci-dss", src: "/logos/pcidss.png", alt: "PCI DSS Certified" },
  {
    id: "iso27001",
    src: "/logos/iso27001.png",
    alt: "ISO 27001 Information Security Management System Certified",
  },
];

/** Platform merchants — files in public/logos/merchants/{slug}.png */
export const MERCHANT_LOGOS = {
  bharatCod: "/logos/merchants/bharat-cod.png",
  greenWeb: "/logos/merchants/green-web.png",
  grootsPay: "/logos/merchants/groots.png",
  paidkiya: "/logos/merchants/paidkiya.png",
  bingopay: "/logos/merchants/bingopay.png",
  aaiWallet: "/logos/merchants/aai-wallet.png",
  bbPay: "/logos/merchants/burberrypay.png",
  indyapay: "/logos/merchants/indyapay.png",
  ninePay: "/logos/merchants/9pay.png",
  zipmart: "/logos/merchants/Zipmart.png",
  finyatra: "/logos/merchants/finyatra.png",
  kuxdistro: "/logos/merchants/kuxdistro.png",
  revopay: "/logos/merchants/revopay.png",
  sparkmudra: "/logos/merchants/sparkmudra.png",
};

/** Orchestration hero merchant row (slug → logo path via MERCHANT_LOGOS or convention) */
export const ORCHESTRATION_MERCHANTS = [
  { id: "bharat-cod", label: "Bharat COD", logo: MERCHANT_LOGOS.bharatCod },
  { id: "green-web", label: "Green Web", logo: MERCHANT_LOGOS.greenWeb },
  { id: "groots-pay", label: "Groots Pay", logo: MERCHANT_LOGOS.grootsPay },
  { id: "paidkiya", label: "Paidkiya", logo: MERCHANT_LOGOS.paidkiya },
  { id: "bingopay", label: "BingoPay", logo: MERCHANT_LOGOS.bingopay },
  { id: "aai-wallet", label: "AAI Wallet", logo: MERCHANT_LOGOS.aaiWallet },
];

export function merchantLogoPath(slug) {
  return `/logos/merchants/${slug}.png`;
}

function partnerLogoPath(slug) {
  return `/logos/partners/${slug}.png`;
}

/** Payment gateway marks for orchestration graphic & banking partners strip */
export const PSP_LOGOS = {
  airpay: "/logos/psp/airpay.png",
  jioPayments: "/logos/psp/jio-payments.png",
  easebuzz: "/logos/psp/easebuzz.png",
  cashfree: "/logos/psp/cashfree.png",
  unlimit: "/logos/psp/unlimit.png",
  payu: "/logos/psp/payu.png",
};

/** Home page banking partners marquee (name → logo path) */
export const BANKING_PARTNER_LOGOS = {
  Airpay: PSP_LOGOS.airpay,
  Easebuzz: PSP_LOGOS.easebuzz,
  "Cashfree Payments": PSP_LOGOS.cashfree,
  "Jio Pay": PSP_LOGOS.jioPayments,
  PayU: PSP_LOGOS.payu,
  Unlimit: PSP_LOGOS.unlimit,
  "IDFC First Bank": partnerLogoPath("idfc-first-bank"),
  "Kotak Mahindra Bank": partnerLogoPath("kotak-mahindra-bank"),
};

/** Home page merchant partners marquee */
export const MERCHANT_PARTNER_LOGOS = {
  "Bharat COD": MERCHANT_LOGOS.bharatCod,
  "Green Web Solutions": MERCHANT_LOGOS.greenWeb,
  "Groots Pay": MERCHANT_LOGOS.grootsPay,
  Paidkiya: MERCHANT_LOGOS.paidkiya,
  BingoPay: MERCHANT_LOGOS.bingopay,
  "AAI Wallet": MERCHANT_LOGOS.aaiWallet,
  "BB Pay": MERCHANT_LOGOS.bbPay,
  Indyapay: MERCHANT_LOGOS.indyapay,
  "9Pay": MERCHANT_LOGOS.ninePay,
  Zipmart: MERCHANT_LOGOS.zipmart,
  Finyatra: MERCHANT_LOGOS.finyatra,
  Kuxdistro: MERCHANT_LOGOS.kuxdistro,
  RevoPay: MERCHANT_LOGOS.revopay,
  "Spark Mudra": MERCHANT_LOGOS.sparkmudra,
};

export function getPartnerLogo(name, variant = "banks") {
  const map = variant === "merchants" ? MERCHANT_PARTNER_LOGOS : BANKING_PARTNER_LOGOS;
  return map[name] ?? null;
}

/** Color variant path: `bingopay.png` → `bingopaycolor.png` */
export function getPartnerLogoColor(logoPath) {
  if (!logoPath) return null;
  return logoPath.replace(/\.png$/i, "color.png");
}

/** Marquee logo height (px); merchants default 35, banks 23 */
export const PARTNER_LOGO_HEIGHT = {
  "Jio Pay": 46,
  Indyapay: 44,
};
