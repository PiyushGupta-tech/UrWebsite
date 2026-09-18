<script setup>
import { nextTick, onMounted, onUnmounted, ref } from "vue";
import { fetchSite } from "@/api/client";
import SiteNav from "@/components/SiteNav.vue";
import SiteFooter from "@/components/SiteFooter.vue";
import ChatWidget from "@/components/ChatWidget.vue";
import { startResponsiveBand } from "@/composables/useResponsiveBand.js";
import { scheduleScrollRestore } from "@/utils/scrollRestoration.js";

const SITE_CACHE_KEY = "ur:site-bootstrap";

function readSiteCache() {
  try {
    return JSON.parse(sessionStorage.getItem(SITE_CACHE_KEY) || "null");
  } catch {
    return null;
  }
}

function writeSiteCache(data) {
  try {
    sessionStorage.setItem(SITE_CACHE_KEY, JSON.stringify(data));
  } catch {
    /* ignore */
  }
}

const cached = readSiteCache();
const site = ref(cached?.site ?? null);
const nav = ref(cached?.nav ?? null);
const footer = ref(cached?.footer ?? null);
const error = ref(null);
const loading = ref(!cached);

let stopBand = null;

onMounted(async () => {
  stopBand = startResponsiveBand();
  try {
    const data = await fetchSite();
    site.value = data.site;
    nav.value = data.nav;
    footer.value = data.footer;
    writeSiteCache(data);
  } catch (e) {
    if (!cached) error.value = e.message;
  } finally {
    loading.value = false;
    await nextTick();
    scheduleScrollRestore();
  }
});

onUnmounted(() => {
  stopBand?.();
});
</script>

<template>
  <div v-if="loading" class="loading-screen">
    <div class="loading-screen__spinner" />
    <p>Loading Urbanrupee…</p>
  </div>

  <div v-else-if="error" class="loading-screen loading-screen--error">
    <p>Could not load site. Is the Django API running?</p>
    <code>{{ error }}</code>
  </div>

  <div v-else class="app-shell">
    <SiteNav :nav="nav" :site="site" />
    <RouterView v-slot="{ Component }">
      <component :is="Component" :site="site" :footer="footer" />
    </RouterView>
    <SiteFooter :footer="footer" :site="site" />
    <ChatWidget />
  </div>
</template>

<style scoped>
.app-shell {
  overflow-x: clip;
  max-width: 100%;
}
.loading-screen {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: var(--text-secondary);
}

.loading-screen--error code {
  font-size: 13px;
  color: #c0392b;
}

.loading-screen__spinner {
  width: 36px;
  height: 36px;
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
