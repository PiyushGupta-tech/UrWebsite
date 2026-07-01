import { onMounted, onUnmounted, ref } from "vue";
import { fetchPayoutDashboard } from "@/api/client";

const POLL_MS = 10_000;

export function usePayoutDashboard({ onUnauthorized } = {}) {
  const summary = ref(null);
  const generatedAt = ref(null);
  const loading = ref(true);
  const refreshing = ref(false);
  const error = ref("");

  let timer = null;

  async function load({ initial = false } = {}) {
    if (initial) loading.value = true;
    else refreshing.value = true;
    error.value = "";

    try {
      const data = await fetchPayoutDashboard();
      summary.value = data.summary || null;
      generatedAt.value = data.generated_at || null;
    } catch (err) {
      if (err.status === 401) {
        onUnauthorized?.();
        return;
      }
      error.value = err.message || "Failed to load dashboard.";
    } finally {
      loading.value = false;
      refreshing.value = false;
    }
  }

  function startPolling() {
    stopPolling();
    timer = window.setInterval(() => {
      if (document.visibilityState === "hidden") return;
      load();
    }, POLL_MS);
  }

  function stopPolling() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function onVisibilityChange() {
    if (document.visibilityState === "visible") {
      load();
    }
  }

  onMounted(async () => {
    await load({ initial: true });
    startPolling();
    document.addEventListener("visibilitychange", onVisibilityChange);
  });

  onUnmounted(() => {
    stopPolling();
    document.removeEventListener("visibilitychange", onVisibilityChange);
  });

  return { summary, generatedAt, loading, refreshing, error, reload: () => load({ initial: false }) };
}
