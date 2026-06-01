<script setup>
import { onMounted, ref } from "vue";
import { fetchSite } from "@/api/client";
import SiteNav from "@/components/SiteNav.vue";
import SiteFooter from "@/components/SiteFooter.vue";
import ChatWidget from "@/components/ChatWidget.vue";

const site = ref(null);
const nav = ref(null);
const footer = ref(null);
const error = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const data = await fetchSite();
    site.value = data.site;
    nav.value = data.nav;
    footer.value = data.footer;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
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

  <div v-else>
    <SiteNav :nav="nav" :site="site" />
    <RouterView v-slot="{ Component }">
      <component :is="Component" :site="site" :footer="footer" />
    </RouterView>
    <SiteFooter :footer="footer" :site="site" />
    <ChatWidget />
  </div>
</template>

<style scoped>
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
