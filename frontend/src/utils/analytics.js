/**
 * Google Analytics 4, loaded only after the visitor accepts analytics cookies.
 * The Measurement ID comes from <meta name="ga-measurement-id"> (injected by Django from
 * GA_MEASUREMENT_ID); without it analytics and the cookie banner stay off.
 */
import { ref } from "vue";

const CONSENT_KEY = "ur:cookie-consent";
const CONSENT_VERSION = 1;
const ID_PATTERN = /^G-[A-Z0-9]{4,20}$/;

function readMeasurementId() {
  if (typeof document === "undefined") return "";
  const id = document.querySelector('meta[name="ga-measurement-id"]')?.getAttribute("content");
  const trimmed = String(id || "").trim();
  return ID_PATTERN.test(trimmed) ? trimmed : "";
}

function readConsent() {
  try {
    const stored = JSON.parse(localStorage.getItem(CONSENT_KEY) || "null");
    if (stored?.v !== CONSENT_VERSION) return null;
    return stored.analytics === "granted" || stored.analytics === "denied" ? stored.analytics : null;
  } catch {
    return null;
  }
}

export const measurementId = readMeasurementId();
export const analyticsAvailable = measurementId !== "";
/** "granted" | "denied" | null (not asked yet) */
export const analyticsConsent = ref(analyticsAvailable ? readConsent() : null);
export const consentSettingsOpen = ref(false);

let tagLoaded = false;

function gtag() {
  // gtag.js expects the arguments object itself, not an array.
  window.dataLayer.push(arguments);
}

function setOptOut(disabled) {
  window[`ga-disable-${measurementId}`] = disabled;
}

function loadTag() {
  setOptOut(false);
  if (tagLoaded) {
    gtag("consent", "update", { analytics_storage: "granted" });
    return;
  }
  tagLoaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = gtag;
  gtag("consent", "default", {
    analytics_storage: "granted",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
  });
  gtag("js", new Date());
  gtag("config", measurementId);
  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
  document.head.appendChild(script);
}

function clearAnalyticsCookies() {
  const host = window.location.hostname;
  const domains = ["", host, `.${host}`, `.${host.replace(/^www\./, "")}`];
  document.cookie
    .split(";")
    .map((part) => part.split("=")[0].trim())
    .filter((name) => name === "_ga" || name.startsWith("_ga_") || name === "_gid")
    .forEach((name) => {
      domains.forEach((domain) => {
        document.cookie = `${name}=; Max-Age=0; path=/${domain ? `; domain=${domain}` : ""}`;
      });
    });
}

/** Load analytics on page start when the visitor already accepted. */
export function initAnalytics() {
  if (analyticsAvailable && analyticsConsent.value === "granted") loadTag();
}

export function setAnalyticsConsent(value) {
  if (!analyticsAvailable || (value !== "granted" && value !== "denied")) return;
  analyticsConsent.value = value;
  consentSettingsOpen.value = false;
  try {
    localStorage.setItem(
      CONSENT_KEY,
      JSON.stringify({ v: CONSENT_VERSION, analytics: value, ts: Date.now() }),
    );
  } catch {
    /* private mode: the choice lasts for this page view only */
  }
  if (value === "granted") {
    loadTag();
    return;
  }
  setOptOut(true);
  if (tagLoaded) gtag("consent", "update", { analytics_storage: "denied" });
  clearAnalyticsCookies();
}

export function openConsentSettings() {
  if (analyticsAvailable) consentSettingsOpen.value = true;
}

export function trackEvent(name, params = {}) {
  if (!tagLoaded || analyticsConsent.value !== "granted") return;
  gtag("event", name, params);
}
