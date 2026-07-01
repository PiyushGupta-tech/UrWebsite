<script setup>
import { computed } from "vue";
import { formatInr } from "@/utils/adminFormat";

const props = defineProps({
  summary: { type: Object, default: null },
  providers: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

const todaySuccess = computed(() => props.summary?.today_success_with_fees ?? 0);
const earningsToday = computed(() => props.summary?.today_earnings?.today ?? 0);
const earningsTotal = computed(() => props.summary?.today_earnings?.total ?? 0);
const pendingCount = computed(() => props.summary?.today_pending?.count ?? 0);
const pendingAmount = computed(() => props.summary?.today_pending?.amount ?? 0);
const overall = computed(() => props.summary?.overall_successful_amount ?? 0);

function providerLocation(provider) {
  const loc = provider.location;
  if (loc?.city) {
    return [loc.city, loc.state].filter(Boolean).join(", ");
  }
  return [provider.city, provider.state].filter(Boolean).join(", ") || "—";
}
</script>

<template>
  <div class="payout-section">
    <div class="payout-section__header">
      <h2 class="payout-section__title">Payout</h2>
      <span class="payout-section__badge">LIVE</span>
    </div>

    <div class="payout-grid">
      <article class="payout-card">
        <p class="payout-card__label">Today success</p>
        <p v-if="loading" class="payout-card__value shimmer" />
        <p v-else class="payout-card__value payout-card__value--success">{{ formatInr(todaySuccess) }}</p>
      </article>

      <article class="payout-card">
        <p class="payout-card__label">Earnings</p>
        <template v-if="loading">
          <p class="payout-card__value shimmer" />
        </template>
        <div v-else class="payout-card__dual">
          <div class="payout-card__metric">
            <p class="payout-card__sub-label">Today</p>
            <p class="payout-card__value payout-card__value--success">{{ formatInr(earningsToday) }}</p>
          </div>
          <span class="payout-card__sep" aria-hidden="true">/</span>
          <div class="payout-card__metric">
            <p class="payout-card__sub-label">Total</p>
            <p class="payout-card__value payout-card__value--success">{{ formatInr(earningsTotal) }}</p>
          </div>
        </div>
      </article>

      <article class="payout-card payout-card--warning">
        <p class="payout-card__label">Pending today</p>
        <template v-if="loading">
          <p class="payout-card__value shimmer" />
        </template>
        <div v-else class="payout-card__dual">
          <div class="payout-card__metric">
            <p class="payout-card__sub-label">Txns</p>
            <p class="payout-card__value">{{ pendingCount }} txns</p>
          </div>
          <span class="payout-card__sep" aria-hidden="true">/</span>
          <div class="payout-card__metric">
            <p class="payout-card__sub-label">Amount</p>
            <p class="payout-card__value">{{ formatInr(pendingAmount) }}</p>
          </div>
        </div>
      </article>

      <article class="payout-card">
        <p class="payout-card__label">Overall successful amount</p>
        <p v-if="loading" class="payout-card__value shimmer" />
        <p v-else class="payout-card__value payout-card__value--success">{{ formatInr(overall) }}</p>
      </article>
    </div>

    <div class="payout-providers">
      <h3 class="payout-providers__title">Top providers today</h3>

      <div v-if="loading" class="payout-providers__shimmer shimmer" />

      <ul v-else-if="providers.length" class="payout-providers__list">
        <li v-for="(provider, index) in providers" :key="provider.userid || index" class="payout-provider">
          <span class="payout-provider__rank">{{ index + 1 }}</span>
          <div class="payout-provider__meta">
            <p class="payout-provider__name">{{ provider.name || provider.userid || "—" }}</p>
            <p class="payout-provider__loc">{{ providerLocation(provider) }}</p>
          </div>
          <div class="payout-provider__stats">
            <p class="payout-provider__txns">{{ provider.txn_count }} txn{{ provider.txn_count === 1 ? "" : "s" }}</p>
            <p class="payout-provider__amount">{{ formatInr(provider.amount_with_fees ?? provider.amount) }}</p>
          </div>
        </li>
      </ul>

      <p v-else class="payout-providers__empty">No successful payouts today yet.</p>
    </div>
  </div>
</template>

<style scoped>
.payout-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.payout-section__title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #fff;
  text-transform: uppercase;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.55),
    0 0 18px rgba(240, 250, 251, 0.28);
}

.payout-section__badge {
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(34, 197, 94, 0.15);
  color: var(--ur-success);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.payout-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.payout-card__label {
  margin: 0 0 6px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #fff;
  text-transform: uppercase;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.55),
    0 0 18px rgba(240, 250, 251, 0.28);
}

.payout-card__value {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--ur-text);
}

.payout-card__value--success {
  color: var(--ur-success);
}

.payout-card__dual {
  display: flex;
  align-items: flex-end;
  gap: 6px;
}

.payout-card__metric {
  flex: 1;
  min-width: 0;
}

.payout-card__sub-label {
  margin: 0 0 4px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--ur-muted);
  text-transform: uppercase;
}

.payout-card__dual .payout-card__value {
  font-size: 18px;
}

.payout-card__sep {
  flex-shrink: 0;
  padding-bottom: 3px;
  color: var(--ur-muted);
  font-size: 18px;
  font-weight: 400;
}

.payout-card--warning .payout-card__value {
  color: var(--ur-warning);
}

.payout-section {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.payout-grid {
  flex-shrink: 0;
}

.payout-providers {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--ur-card-border);
  flex: 1 1 auto;
  min-height: 0;
  overflow: auto;
}

.payout-providers__title {
  margin: 0 0 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--ur-muted);
}

.payout-providers__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.payout-provider {
  display: grid;
  grid-template-columns: 20px minmax(0, 1fr) auto;
  gap: 8px;
  align-items: center;
  padding: 6px 8px;
  border-radius: 8px;
  background: var(--ur-surface-raised);
  border: 1px solid var(--ur-card-border);
}

.payout-provider__rank {
  font-size: 11px;
  font-weight: 700;
  color: var(--ur-muted);
}

.payout-provider__name {
  margin: 0;
  font-size: 11px;
  font-weight: 600;
  color: var(--ur-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.payout-provider__loc {
  margin: 2px 0 0;
  font-size: 10px;
  color: var(--ur-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.payout-provider__stats {
  text-align: right;
}

.payout-provider__txns {
  margin: 0;
  font-size: 10px;
  color: var(--ur-muted);
}

.payout-provider__amount {
  margin: 2px 0 0;
  font-size: 11px;
  font-weight: 700;
  color: var(--ur-text);
}

.payout-providers__shimmer {
  height: 72px;
  border-radius: 8px;
}

.payout-providers__empty {
  margin: 0;
  padding: 8px;
  font-size: 11px;
  color: var(--ur-muted);
  text-align: center;
  border-radius: 8px;
  background: var(--ur-surface-raised);
  border: 1px solid var(--ur-card-border);
}

.shimmer {
  min-height: 24px;
  border-radius: 8px;
  background: linear-gradient(
    90deg,
    var(--ur-card-bg) 25%,
    var(--ur-shimmer-mid) 50%,
    var(--ur-card-bg) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -100% 0;
  }
}
</style>
