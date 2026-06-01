<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const phases = [
  {
    id: "match",
    label: "Matching",
    hint: "Match transactions across gateways, banks, wallets, and ledgers in real time.",
    matched: 847,
    exceptions: 3,
    progress: 96,
    txn: { id: "PAY-2041", source: "Gateway", amount: "₹18,400", status: "matched", statusLabel: "Matched" },
  },
  {
    id: "discrepancy",
    label: "Exceptions",
    hint: "Flag unmatched items and resolve discrepancies with automated alerts.",
    matched: 812,
    exceptions: 38,
    progress: 88,
    txn: { id: "LED-5502", source: "Ledger", amount: "₹9,800", status: "exception", statusLabel: "Exception" },
  },
  {
    id: "report",
    label: "Reports",
    hint: "Live dashboards and exportable reports for full reconciliation visibility.",
    matched: 850,
    exceptions: 0,
    progress: 100,
    txn: { id: "BNK-8820", source: "Bank", amount: "₹42,100", status: "matched", statusLabel: "Matched" },
  },
];

const stats = [
  { value: "95%", label: "Time saved" },
  { value: "99.9%", label: "Accuracy" },
  { value: "Live", label: "Dashboard" },
];

const activeId = ref("match");
let cycleTimer = null;

const active = computed(
  () => phases.find((p) => p.id === activeId.value) ?? phases[0],
);

function select(id) {
  activeId.value = id;
}

function startCycle() {
  stopCycle();
  cycleTimer = setInterval(() => {
    if (!props.ready) return;
    const i = phases.findIndex((p) => p.id === activeId.value);
    activeId.value = phases[(i + 1) % phases.length].id;
  }, 4000);
}

function stopCycle() {
  if (cycleTimer) {
    clearInterval(cycleTimer);
    cycleTimer = null;
  }
}

watch(
  () => props.ready,
  (ready) => (ready ? startCycle() : stopCycle()),
  { immediate: true },
);

onMounted(() => {
  if (props.ready) startCycle();
});

onUnmounted(stopCycle);
</script>

<template>
  <div
    class="recon"
    :class="{ 'recon--ready': ready }"
    role="img"
    aria-label="Automatic reconciliation preview"
  >
    <div class="recon__card">
      <div class="recon__top">
        <span class="recon__title">Reconciliation</span>
        <span class="recon__live">
          <span class="recon__live-dot" aria-hidden="true" />
          Live
        </span>
      </div>

      <div class="recon__tabs" role="tablist">
        <button
          v-for="phase in phases"
          :key="phase.id"
          type="button"
          role="tab"
          class="recon__tab"
          :class="{ 'recon__tab--active': activeId === phase.id }"
          :aria-selected="activeId === phase.id"
          @click="select(phase.id)"
        >
          {{ phase.label }}
        </button>
      </div>

      <div class="recon__summary">
        <div class="recon__counts">
          <span class="recon__matched-num">{{ active.matched }}</span>
          <span class="recon__matched-label">matched</span>
          <span class="recon__sep">·</span>
          <span class="recon__exc-num">{{ active.exceptions }}</span>
          <span class="recon__exc-label">exceptions</span>
        </div>
        <span class="recon__pct">{{ active.progress }}%</span>
      </div>

      <div class="recon__bar">
        <span class="recon__bar-fill" :style="{ width: `${active.progress}%` }" />
      </div>

      <Transition name="recon-fade" mode="out-in">
        <div :key="active.id" class="recon__txn">
          <span class="recon__txn-id">{{ active.txn.id }}</span>
          <span class="recon__txn-meta">{{ active.txn.source }} · {{ active.txn.amount }}</span>
          <span
            class="recon__txn-badge"
            :class="`recon__txn-badge--${active.txn.status}`"
          >
            {{ active.txn.statusLabel }}
          </span>
        </div>
      </Transition>

      <p class="recon__hint">{{ active.hint }}</p>

      <div class="recon__stats">
        <div v-for="s in stats" :key="s.label" class="recon__stat">
          <span class="recon__stat-value">{{ s.value }}</span>
          <span class="recon__stat-label">{{ s.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recon {
  width: 100%;
  max-width: 360px;
  margin-inline: auto;
}

.recon__card {
  padding: 18px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 12px 32px rgba(26, 54, 93, 0.08);
  transition: box-shadow 0.3s ease;
}

.recon--ready .recon__card:hover {
  box-shadow: 0 16px 40px rgba(6, 182, 212, 0.12);
}

.recon__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.recon__title {
  font-size: 14px;
  font-weight: 700;
  color: #1a365d;
}

.recon__live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #06b6d4;
}

.recon__live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #06b6d4;
}

.recon--ready .recon__live-dot {
  animation: recon-pulse 1.5s ease-in-out infinite;
}

@keyframes recon-pulse {
  50% {
    opacity: 0.4;
  }
}

.recon__tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 14px;
}

.recon__tab {
  flex: 1;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  padding: 8px 6px;
  border-radius: 8px;
  cursor: pointer;
  transition:
    color 0.2s,
    border-color 0.2s,
    background 0.2s;
}

.recon__tab--active {
  color: #1a365d;
  border-color: #06b6d4;
  background: #ecfeff;
}

.recon__summary {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 8px;
}

.recon__counts {
  display: flex;
  align-items: baseline;
  gap: 4px;
  flex-wrap: wrap;
  font-size: 12px;
  color: #64748b;
}

.recon__matched-num {
  font-size: 22px;
  font-weight: 800;
  color: #1a365d;
}

.recon__matched-label,
.recon__exc-label {
  font-weight: 600;
}

.recon__sep {
  color: #cbd5e1;
  margin: 0 2px;
}

.recon__exc-num {
  font-size: 18px;
  font-weight: 700;
  color: #d97706;
}

.recon__pct {
  font-size: 14px;
  font-weight: 800;
  color: #06b6d4;
}

.recon__bar {
  height: 6px;
  border-radius: 6px;
  background: #e8eef3;
  overflow: hidden;
  margin-bottom: 14px;
}

.recon__bar-fill {
  display: block;
  height: 100%;
  border-radius: 6px;
  background: linear-gradient(90deg, #1a365d, #06b6d4);
  transition: width 0.45s ease;
}

.recon__txn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  margin-bottom: 10px;
}

.recon__txn-id {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  font-family: ui-monospace, monospace;
}

.recon__txn-meta {
  flex: 1;
  font-size: 12px;
  font-weight: 600;
  color: #1a365d;
}

.recon__txn-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.recon__txn-badge--matched {
  background: #ecfdf5;
  color: #059669;
}

.recon__txn-badge--exception {
  background: #fffbeb;
  color: #d97706;
}

.recon__hint {
  margin: 0 0 14px;
  font-size: 12px;
  line-height: 1.45;
  color: #64748b;
}

.recon__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #e8eef3;
}

.recon__stat {
  text-align: center;
}

.recon__stat-value {
  display: block;
  font-size: 13px;
  font-weight: 800;
  color: #1a365d;
}

.recon__stat-label {
  display: block;
  font-size: 9px;
  color: #94a3b8;
  margin-top: 2px;
}

.recon-fade-enter-active,
.recon-fade-leave-active {
  transition: opacity 0.25s ease;
}

.recon-fade-enter-from,
.recon-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .recon--ready .recon__live-dot {
    animation: none;
  }
}
</style>
