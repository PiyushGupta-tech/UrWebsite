<script setup>
import { computed } from "vue";
import {
  analyticsAvailable,
  analyticsConsent,
  consentSettingsOpen,
  setAnalyticsConsent,
} from "@/utils/analytics.js";

const visible = computed(
  () => analyticsAvailable && (analyticsConsent.value === null || consentSettingsOpen.value),
);
</script>

<template>
  <section
    v-if="visible"
    class="cookie-banner"
    role="region"
    aria-labelledby="cookie-banner-title"
  >
    <h2 id="cookie-banner-title" class="cookie-banner__title">Cookies on Urbanrupee</h2>
    <p class="cookie-banner__body">
      We use analytics cookies to understand how visitors use our website and to improve it. They
      are only set if you accept. Read our
      <RouterLink to="/privacy-policy" class="cookie-banner__link">Privacy Policy</RouterLink>.
    </p>
    <div class="cookie-banner__actions">
      <button
        type="button"
        class="cookie-banner__btn cookie-banner__btn--reject"
        @click="setAnalyticsConsent('denied')"
      >
        Reject
      </button>
      <button
        type="button"
        class="cookie-banner__btn cookie-banner__btn--accept"
        @click="setAnalyticsConsent('granted')"
      >
        Accept
      </button>
    </div>
  </section>
</template>

<style scoped>
.cookie-banner {
  position: fixed;
  left: 20px;
  bottom: calc(20px + var(--ur-sticky-cta, 0px));
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: min(400px, calc(100vw - 40px));
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #e9eaeb;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.16);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

.cookie-banner__title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: 22px;
}

.cookie-banner__body {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  color: #535861;
}

.cookie-banner__link {
  color: #097495;
  font-weight: 600;
  text-decoration: underline;
}

.cookie-banner__actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.cookie-banner__btn {
  flex: 1 1 0;
  height: 44px;
  padding: 0 16px;
  border-radius: 8px;
  font: inherit;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.cookie-banner__btn:hover {
  opacity: 0.9;
}

.cookie-banner__btn:focus-visible,
.cookie-banner__link:focus-visible {
  outline: 2px solid #097495;
  outline-offset: 2px;
}

.cookie-banner__btn--reject {
  border: 1px solid #097495;
  background: #ffffff;
  color: #097495;
}

.cookie-banner__btn--accept {
  border: 1px solid #097495;
  background: #097495;
  color: #ffffff;
}

@media (max-width: 767px) {
  .cookie-banner {
    left: 12px;
    right: 12px;
    bottom: calc(12px + var(--ur-sticky-cta, 0px));
    width: auto;
    padding: 16px;
  }
}
</style>
