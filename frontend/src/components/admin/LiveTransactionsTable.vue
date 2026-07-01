<script setup>
import { computed, ref, watch } from "vue";
import { formatInr, formatTime } from "@/utils/adminFormat";

const props = defineProps({
  transactions: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

const highlighted = ref(false);

const latest = computed(() => props.transactions[0] || null);

function statusClass(status) {
  const value = String(status || "").toLowerCase();
  if (value.includes("success")) return "status--success";
  if (value.includes("pending")) return "status--pending";
  if (value.includes("fail")) return "status--failed";
  return "status--neutral";
}

watch(
  () => props.transactions[0]?.id || props.transactions[0]?.transaction_id,
  (next, prev) => {
    if (!prev || !next || next === prev) return;
    highlighted.value = true;
    window.setTimeout(() => {
      highlighted.value = false;
    }, 1800);
  },
);
</script>

<template>
  <article class="admin-card tx-card">
    <h2 class="tx-card__title">Latest transaction</h2>

    <div v-if="loading" class="tx-card__shimmer shimmer-block" />

    <div v-else-if="latest" class="tx-card__table">
      <div class="tx-card__labels" aria-hidden="true">
        <span>Time</span>
        <span>Merchant</span>
        <span>City</span>
        <span>Amount</span>
        <span>Mode</span>
        <span>Status</span>
      </div>
      <div
        class="tx-card__row"
        :class="{ 'tx-card__row--new': highlighted }"
      >
      <span class="tx-card__cell tx-card__time">{{ formatTime(latest.created_at) }}</span>
      <span class="tx-card__cell tx-card__merchant">{{ latest.merchant?.name || latest.userid || "—" }}</span>
      <span class="tx-card__cell">{{ latest.merchant?.location?.city || latest.merchant?.city || latest.city || "—" }}</span>
      <span class="tx-card__cell tx-card__amount">{{ formatInr(latest.amount) }}</span>
      <span class="tx-card__cell">{{ latest.mode || "—" }}</span>
      <span class="tx-card__cell">
        <span class="status-pill" :class="statusClass(latest.status)">{{ latest.status || "—" }}</span>
      </span>
      </div>
    </div>

    <p v-else class="tx-card__empty">No transaction yet today.</p>
  </article>
</template>

<style scoped>
.tx-card {
  width: 100%;
  min-width: 0;
  flex-shrink: 0;
}

.tx-card__title {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--ur-text);
}

.tx-card__table {
  width: 100%;
  min-width: 0;
}

.tx-card__labels,
.tx-card__row {
  display: grid;
  grid-template-columns: 72px minmax(0, 1.4fr) minmax(0, 1fr) minmax(0, 1fr) 56px auto;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.tx-card__labels {
  margin-bottom: 4px;
  padding: 0 8px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--ur-muted);
}

.tx-card__row {
  padding: 6px 8px;
  border-radius: 8px;
  background: var(--ur-surface-raised);
  border: 1px solid var(--ur-card-border);
  font-size: 11px;
  color: var(--ur-text);
}

.tx-card__cell {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tx-card__time {
  color: var(--ur-muted);
  font-variant-numeric: tabular-nums;
}

.tx-card__merchant {
  font-weight: 600;
}

.tx-card__amount {
  font-weight: 700;
  color: var(--ur-text);
}

.tx-card__row--new {
  animation: rowFlash 1.6s ease;
}

.status-pill {
  display: inline-flex;
  padding: 2px 7px;
  border-radius: 999px;
  font-size: 9px;
  font-weight: 700;
  text-transform: capitalize;
}

.status--success {
  background: rgba(5, 163, 74, 0.15);
  color: var(--ur-success);
}

.status--pending {
  background: rgba(251, 188, 6, 0.15);
  color: var(--ur-warning);
}

.status--failed {
  background: rgba(255, 51, 102, 0.15);
  color: var(--ur-danger);
}

.status--neutral {
  background: rgba(255, 255, 255, 0.08);
  color: var(--ur-muted);
}

.tx-card__empty {
  margin: 0;
  padding: 4px 0;
  font-size: 11px;
  color: var(--ur-muted);
}

.tx-card__shimmer {
  height: 34px;
}

.shimmer-block {
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
    background-position: -200% 0;
  }
}

@keyframes rowFlash {
  0% {
    background: rgba(255, 255, 255, 0.08);
  }

  100% {
    background: var(--ur-surface-raised);
  }
}

@media (max-width: 900px) {
  .tx-card__row {
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
}
</style>
