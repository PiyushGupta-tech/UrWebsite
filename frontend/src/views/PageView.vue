<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { fetchPage } from "@/api/client";
import { applySeo } from "@/utils/seo";
import HomeClosing from "@/components/HomeClosing.vue";
import AboutPage from "@/components/pages/AboutPage.vue";
import MarketingPage from "@/components/pages/MarketingPage.vue";
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
    faq: FaqPage,
    blog: BlogPage,
    privacy: PrivacyPage,
    contact: ContactPage,
    hub: HubPage,
  };
  return map[type] || MarketingPage;
});

async function loadPage() {
  loading.value = true;
  error.value = null;
  try {
    payload.value = await fetchPage(slug.value);
    applySeo(payload.value.seo, payload.value.structured_data);
  } catch (e) {
    error.value = e.status === 404 ? "Page not found." : e.message;
    payload.value = null;
  } finally {
    loading.value = false;
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
  background:
    url("/images/figma-contact/hero-bg@2x.png") center top / max(100%, 1440px) auto no-repeat,
    #ffffff;
}

.page-view > .site-closing {
  margin-top: var(--ur-section-gap);
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
