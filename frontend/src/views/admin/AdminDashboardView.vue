<script setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import AdminTopBar from "@/components/admin/AdminTopBar.vue";
import IndiaTransactionMap from "@/components/admin/IndiaTransactionMap.vue";
import LiveTransactionsTable from "@/components/admin/LiveTransactionsTable.vue";
import PayinSection from "@/components/admin/PayinSection.vue";
import PayoutSection from "@/components/admin/PayoutSection.vue";
import { useAdminAuth } from "@/composables/useAdminAuth";
import { usePayinDashboard } from "@/composables/usePayinDashboard";
import { usePayoutDashboard } from "@/composables/usePayoutDashboard";

const router = useRouter();
const { authenticated, loading: authLoading, refresh, logout } = useAdminAuth();

const {
  summary,
  generatedAt,
  loading,
  refreshing,
  error,
} = usePayoutDashboard({
  onUnauthorized: () => router.replace({ name: "admin-login" }),
});

const {
  summary: payinSummary,
  loading: payinLoading,
  refreshing: payinRefreshing,
  error: payinError,
} = usePayinDashboard({
  onUnauthorized: () => router.replace({ name: "admin-login" }),
});

const mapCitiesToday = computed(() => summary.value?.map_cities_today || []);
const payinMapCitiesToday = computed(() => payinSummary.value?.map_cities_today || []);
const latestTransactions = computed(() => summary.value?.latest_transactions || []);
const topProviders = computed(() => summary.value?.top_providers_today || []);
const payinTopProviders = computed(() => payinSummary.value?.top_providers_today || []);
const payinLatestTransactions = computed(() => payinSummary.value?.latest_transactions || []);

onMounted(async () => {
  await refresh();
  if (!authenticated.value) {
    router.replace({ name: "admin-login" });
  }
});

async function onLogout() {
  await logout();
  router.push({ name: "admin-login" });
}
</script>

<template>
  <div class="admin-shell admin-theme">
    <AdminTopBar
      :generated-at="generatedAt"
      :refreshing="refreshing || payinRefreshing"
      @logout="onLogout"
    />

    <main class="admin-main">
      <p v-if="error" class="admin-main__error" role="alert">{{ error }}</p>

      <div class="admin-grid">
        <section class="admin-grid__left">
          <IndiaTransactionMap
            :payout-cities="mapCitiesToday"
            :payin-cities="payinMapCitiesToday"
            :payout-providers="topProviders"
            :payin-providers="payinTopProviders"
            :payout-transactions="latestTransactions"
            :payin-transactions="payinLatestTransactions"
            :loading="loading || payinLoading || authLoading"
          />
          <LiveTransactionsTable
            :transactions="latestTransactions"
            :loading="loading || authLoading"
          />
        </section>

        <aside class="admin-grid__right">
          <div class="admin-card metrics-panel">
            <PayoutSection
              :summary="summary"
              :providers="topProviders"
              :loading="loading || authLoading"
            />
            <PayinSection
              :summary="payinSummary"
              :providers="payinTopProviders"
              :loading="payinLoading || authLoading"
              :error="payinError"
            />
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-shell {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  min-height: 100dvh;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background: #000;
  color: var(--ur-text);
}

.admin-main {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: auto;
  overscroll-behavior: contain;
  padding: clamp(8px, 1.2vh, 12px) clamp(10px, 1.5vw, 16px) clamp(10px, 1.5vh, 16px);
  background: #000;
}

.admin-main__error {
  margin: 0 0 clamp(6px, 0.8vh, 8px);
  padding: clamp(6px, 0.8vh, 8px) clamp(8px, 1vw, 10px);
  border-radius: 10px;
  background: rgba(255, 51, 102, 0.12);
  color: var(--ur-danger);
  font-size: clamp(10px, 1.1vh, 12px);
}

.admin-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr);
  gap: clamp(8px, 1.2vh, 12px);
  flex: 1 1 auto;
  width: 100%;
  min-height: 0;
  align-items: stretch;
}

.admin-grid__left {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: clamp(8px, 1vh, 10px);
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

.admin-grid__left > * {
  min-width: 0;
}

.admin-grid__right {
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

.metrics-panel {
  display: grid;
  grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
  height: 100%;
  min-height: 0;
  overflow: hidden;
}

.metrics-panel :deep(.payout-section) {
  min-height: 0;
  overflow: hidden;
  padding-bottom: clamp(4px, 0.6vh, 6px);
  border-bottom: 1px solid var(--ur-card-border);
}

.metrics-panel :deep(.payin-section) {
  min-height: 0;
  overflow: hidden;
  padding-top: clamp(4px, 0.6vh, 6px);
}

@media (max-width: 1100px) {
  .admin-grid {
    grid-template-columns: 1fr;
    height: auto;
    min-height: min(100%, calc(100dvh - 64px));
  }

  .admin-grid__left {
    grid-template-rows: minmax(clamp(220px, 38vh, 420px), 1fr) auto;
  }

  .admin-grid__right {
    min-height: clamp(320px, 42vh, 480px);
  }
}
</style>

<style>
html:has(.admin-shell),
body:has(.admin-shell),
#app:has(.admin-shell) {
  width: 100%;
  height: 100%;
  min-height: 100vh;
  min-height: 100dvh;
  margin: 0;
  overflow: hidden;
}
</style>
