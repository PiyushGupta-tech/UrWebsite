<script setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import AdminTopBar from "@/components/admin/AdminTopBar.vue";
import IndiaTransactionMap from "@/components/admin/IndiaTransactionMap.vue";
import LiveTransactionsTable from "@/components/admin/LiveTransactionsTable.vue";
import PayinPlaceholderSection from "@/components/admin/PayinPlaceholderSection.vue";
import PayoutSection from "@/components/admin/PayoutSection.vue";
import { useAdminAuth } from "@/composables/useAdminAuth";
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

const mapCitiesToday = computed(() => summary.value?.map_cities_today || []);
const latestTransactions = computed(() => summary.value?.latest_transactions || []);
const topProviders = computed(() => summary.value?.top_providers_today || []);

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
      :refreshing="refreshing"
      @logout="onLogout"
    />

    <main class="admin-main">
      <p v-if="error" class="admin-main__error" role="alert">{{ error }}</p>

      <div class="admin-grid">
        <section class="admin-grid__left">
          <IndiaTransactionMap
            :map-cities="mapCitiesToday"
            :loading="loading || authLoading"
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
            <PayinPlaceholderSection />
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-shell {
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: #000;
  color: var(--ur-text);
}

.admin-main {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  padding: 12px 16px 16px;
  background: #000;
}

.admin-main__error {
  margin: 0 0 8px;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(255, 51, 102, 0.12);
  color: var(--ur-danger);
  font-size: 12px;
}

.admin-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(300px, 1fr);
  gap: 12px;
  height: 100%;
  align-items: stretch;
}

.admin-grid__left {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 10px;
  min-height: 0;
  overflow: hidden;
}

.admin-grid__left > * {
  min-width: 0;
}

.admin-grid__right {
  min-height: 0;
  overflow: hidden;
}

.metrics-panel {
  display: grid;
  grid-template-rows: 1fr 1fr;
  height: 100%;
  min-height: 0;
  overflow: hidden;
}

.metrics-panel :deep(.payout-section) {
  min-height: 0;
  overflow: hidden;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--ur-card-border);
}

.metrics-panel :deep(.payin-section) {
  min-height: 0;
  overflow: hidden;
  padding-top: 6px;
}

@media (max-width: 1100px) {
  .admin-grid {
    grid-template-columns: 1fr;
  }

  .admin-grid__left {
    grid-template-rows: minmax(0, 1fr) auto;
  }
}
</style>

<style>
html:has(.admin-shell),
body:has(.admin-shell),
#app:has(.admin-shell) {
  height: 100%;
  overflow: hidden;
}
</style>
