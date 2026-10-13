<script setup>
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { fetchPage } from "@/api/client";
import { applySeo } from "@/utils/seo";
import { scheduleScrollRestore } from "@/utils/scrollRestoration.js";
import HomeClosing from "@/components/HomeClosing.vue";
import AboutPage from "@/components/pages/AboutPage.vue";
import MarketingPage from "@/components/pages/MarketingPage.vue";
import WhiteLabelPage from "@/components/pages/WhiteLabelPage.vue";
import CustomCheckoutPage from "@/components/pages/CustomCheckoutPage.vue";
import HyperCheckoutPage from "@/components/pages/HyperCheckoutPage.vue";
import OrchestrationPage from "@/components/pages/OrchestrationPage.vue";
import CollectionsPage from "@/components/pages/CollectionsPage.vue";
import UpiSwitchPage from "@/components/pages/UpiSwitchPage.vue";
import PayoutsPage from "@/components/pages/PayoutsPage.vue";
import RiskFraudPage from "@/components/pages/RiskFraudPage.vue";
import ReconciliationPage from "@/components/pages/ReconciliationPage.vue";
import FinancialOperationsPage from "@/components/pages/FinancialOperationsPage.vue";
import UnifiedDashboardPage from "@/components/pages/UnifiedDashboardPage.vue";
import FaqPage from "@/components/pages/FaqPage.vue";
import BlogPage from "@/components/pages/BlogPage.vue";
import PrivacyPage from "@/components/pages/PrivacyPage.vue";
import ContactPage from "@/components/pages/ContactPage.vue";
import HubPage from "@/components/pages/HubPage.vue";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

const route = useRoute();
const payload = ref(null);
const error = ref(null);
const loading = ref(true);

const slug = computed(() => route.meta.slug);
const usesSolutionsTypography = computed(
  () => route.path.startsWith("/services") || route.path.startsWith("/products"),
);

const pageComponent = computed(() => {
  const type = payload.value?.page?.type;
  const map = {
    about: AboutPage,
    marketing: MarketingPage,
    "white-label": WhiteLabelPage,
    "custom-checkout": CustomCheckoutPage,
    "hyper-checkout": HyperCheckoutPage,
    orchestration: OrchestrationPage,
    collections: CollectionsPage,
    "upi-switch": UpiSwitchPage,
    payouts: PayoutsPage,
    "risk-fraud": RiskFraudPage,
    reconciliation: ReconciliationPage,
    "financial-operations": FinancialOperationsPage,
    "unified-dashboard": UnifiedDashboardPage,
    faq: FaqPage,
    blog: BlogPage,
    privacy: PrivacyPage,
    contact: ContactPage,
    hub: HubPage,
  };
  return map[type] || MarketingPage;
});

function pageCacheKey(pageSlug) {
  return `ur:page-bootstrap:${pageSlug}`;
}

function readEmbeddedPage(pageSlug) {
  const el = document.getElementById("page-bootstrap");
  if (!el?.textContent) return null;
  try {
    const data = JSON.parse(el.textContent);
    return data?.slug === pageSlug ? data : null;
  } catch {
    return null;
  }
}

function readPageCache(pageSlug) {
  try {
    return JSON.parse(sessionStorage.getItem(pageCacheKey(pageSlug)) || "null");
  } catch {
    return null;
  }
}

function writePageCache(pageSlug, data) {
  try {
    sessionStorage.setItem(pageCacheKey(pageSlug), JSON.stringify(data));
  } catch {
    /* ignore */
  }
}

async function loadPage() {
  const pageSlug = slug.value;
  const cached = readEmbeddedPage(pageSlug) || readPageCache(pageSlug);
  error.value = null;

  if (cached) {
    payload.value = cached;
    loading.value = false;
    applySeo(cached.seo, cached.structured_data);
    await nextTick();
    scheduleScrollRestore(route.fullPath);
  } else {
    loading.value = true;
  }

  try {
    const data = await fetchPage(pageSlug);
    payload.value = data;
    writePageCache(pageSlug, data);
    applySeo(data.seo, data.structured_data);
  } catch (e) {
    if (!cached) {
      error.value = e.status === 404 ? "Page not found." : e.message;
      payload.value = null;
    }
  } finally {
    loading.value = false;
    await nextTick();
    scheduleScrollRestore(route.fullPath);
  }
}

onMounted(loadPage);
watch(() => route.path, loadPage);
</script>

<template>
  <div v-if="loading" class="page-loading">
    <div class="loading-screen__spinner" />
  </div>

  <div v-else-if="error" class="page-loading page-loading--error">
    <p>{{ error }}</p>
    <RouterLink to="/" class="btn btn--primary">Back to home</RouterLink>
  </div>

  <div
    v-else
    class="page-view"
    :class="{ 'page-view--solutions': usesSolutionsTypography }"
  >
    <component
      :is="pageComponent"
      :page="payload.page"
      :site="payload.site"
      :checkout="payload.checkout_demo"
      :dashboard="payload.dashboard_preview"
      :related-links="payload.related_links"
    />
    <HomeClosing
      v-if="payload.common_closing"
      :section="payload.common_closing"
      :show-india-growth="false"
      :show-audiences="false"
      :show-faq="slug !== 'faq'"
      :show-cta="slug !== 'contact'"
    />
  </div>
</template>

<style scoped>
.page-view {
  --page-nav-offset: 129px;
  margin-top: calc(-1 * var(--page-nav-offset));
  padding-top: var(--page-nav-offset);
  overflow-x: clip;
  max-width: 100%;
  background: #ffffff;
}

.page-view > .site-closing {
  margin-top: 100px;
}

/* Tablet (Figma 931:18733): 86px between the page body and each closing section */
@media (min-width: 768px) and (max-width: 1024px) {
  .page-view > .site-closing {
    --ur-section-gap: 86px;
    margin-top: var(--ur-section-gap);
  }
}

.page-view--solutions {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.page-loading {
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.page-loading--error {
  color: var(--text-secondary);
}

.loading-screen__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@media (max-width: 1280px) {
  .page-view {
    --page-nav-offset: 113px;
  }
}

@media (max-width: 1200px) {
  .page-view {
    --page-nav-offset: 82px;
  }
}

@media (max-width: 700px) {
  .page-view {
    --page-nav-offset: 88px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
