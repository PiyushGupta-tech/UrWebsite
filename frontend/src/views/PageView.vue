<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { fetchPage } from "@/api/client";
import AboutPage from "@/components/pages/AboutPage.vue";
import MarketingPage from "@/components/pages/MarketingPage.vue";
import FaqPage from "@/components/pages/FaqPage.vue";
import BlogPage from "@/components/pages/BlogPage.vue";
import PrivacyPage from "@/components/pages/PrivacyPage.vue";
import ContactPage from "@/components/pages/ContactPage.vue";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

const route = useRoute();
const payload = ref(null);
const error = ref(null);
const loading = ref(true);

const slug = computed(() => route.meta.slug);

const pageComponent = computed(() => {
  const type = payload.value?.page?.type;
  const map = {
    about: AboutPage,
    marketing: MarketingPage,
    faq: FaqPage,
    blog: BlogPage,
    privacy: PrivacyPage,
    contact: ContactPage,
  };
  return map[type] || MarketingPage;
});

async function loadPage() {
  loading.value = true;
  error.value = null;
  try {
    payload.value = await fetchPage(slug.value);
    document.title = `${payload.value.page.title} — Urbanrupee`;
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

  <component
    :is="pageComponent"
    v-else
    :page="payload.page"
    :site="payload.site"
    :checkout="payload.checkout_demo"
    :dashboard="payload.dashboard_preview"
  />
</template>

<style scoped>
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
