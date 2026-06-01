<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const modules = [
  {
    id: "monitor",
    label: "Monitoring",
    hint: "Real-time pattern detection with instant alerts.",
    score: 78,
    alert: "Unusual pattern detected",
    txn: { id: "TXN-8F2A", amount: "₹2.4L", status: "flag", statusLabel: "Flagged" },
  },
  {
    id: "ai",
    label: "AI Risk",
    hint: "ML scoring that cuts false positives by up to 80%.",
    score: 84,
    alert: "Elevated behavioral risk",
    txn: { id: "TXN-1D02", amount: "₹45,000", status: "review", statusLabel: "Review" },
  },
  {
    id: "compliance",
    label: "Compliance",
    hint: "KYC, due diligence, and regulatory reporting.",
    score: 62,
    alert: "Report queued for submission",
    txn: { id: "KYC-4412", amount: "Verified", status: "low", statusLabel: "Clear" },
  },
];

const stats = [
  { value: "<50ms", label: "Detection" },
  { value: "-80%", label: "False positives" },
  { value: "180+", label: "Countries" },
];

const activeId = ref("monitor");
let cycleTimer = null;

const active = computed(
  () => modules.find((m) => m.id === activeId.value) ?? modules[0],
);

const riskClass = computed(() => {
  const s = active.value.score;
  if (s >= 75) return "high";
  if (s >= 55) return "mid";
  return "low";
});

function select(id) {
  activeId.value = id;
}

function startCycle() {
  stopCycle();
  cycleTimer = setInterval(() => {
    if (!props.ready) return;
    const i = modules.findIndex((m) => m.id === activeId.value);
    activeId.value = modules[(i + 1) % modules.length].id;
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
    class="aml"
    :class="{ 'aml--ready': ready }"
    role="img"
    aria-label="AML risk screening preview"
  >
    <div class="aml__card">
      <div class="aml__top">
        <span class="aml__title">AML screening</span>
        <span class="aml__live">
          <span class="aml__live-dot" aria-hidden="true" />
          Live
        </span>
      </div>

      <div class="aml__tabs" role="tablist" aria-label="AML focus">
        <button
          v-for="mod in modules"
          :key="mod.id"
          type="button"
          role="tab"
          class="aml__tab"
          :class="{ 'aml__tab--active': activeId === mod.id }"
          :aria-selected="activeId === mod.id"
          @click="select(mod.id)"
        >
          {{ mod.label }}
        </button>
      </div>

      <div class="aml__score-block">
        <div class="aml__score-head">
          <span class="aml__score-label">Risk score</span>
          <span class="aml__score-num" :class="`aml__score-num--${riskClass}`">
            {{ active.score }}
          </span>
        </div>
        <div class="aml__bar">
          <span
            class="aml__bar-fill"
            :class="`aml__bar-fill--${riskClass}`"
            :style="{ width: `${active.score}%` }"
          />
        </div>
        <p class="aml__alert">{{ active.alert }}</p>
      </div>

      <Transition name="aml-fade" mode="out-in">
        <div :key="active.id" class="aml__txn">
          <span class="aml__txn-id">{{ active.txn.id }}</span>
          <span class="aml__txn-amount">{{ active.txn.amount }}</span>
          <span
            class="aml__txn-badge"
            :class="`aml__txn-badge--${active.txn.status}`"
          >
            {{ active.txn.statusLabel }}
          </span>
        </div>
      </Transition>

      <p class="aml__hint">{{ active.hint }}</p>

      <div class="aml__stats">
        <div v-for="s in stats" :key="s.label" class="aml__stat">
          <span class="aml__stat-value">{{ s.value }}</span>
          <span class="aml__stat-label">{{ s.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.aml {
  width: 100%;
  max-width: 360px;
  margin-inline: auto;
}

.aml__card {
  padding: 18px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 12px 32px rgba(26, 54, 93, 0.08);
  transition:
    transform 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.5s ease;
}

.aml:not(.aml--ready) .aml__card {
  opacity: 0.92;
  transform: translateY(8px);
}

.aml--ready .aml__card {
  transform: translateY(0);
}

.aml--ready .aml__card:hover {
  box-shadow: 0 16px 40px rgba(6, 182, 212, 0.12);
}

.aml__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.aml__title {
  font-size: 14px;
  font-weight: 700;
  color: #1a365d;
}

.aml__live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #059669;
}

.aml__live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #34d399;
}

.aml--ready .aml__live-dot {
  animation: aml-pulse 1.5s ease-in-out infinite;
}

@keyframes aml-pulse {
  50% {
    opacity: 0.45;
  }
}

.aml__tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}

.aml__tab {
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

.aml__tab--active {
  color: #1a365d;
  border-color: #06b6d4;
  background: #ecfeff;
}

.aml__tab:hover {
  border-color: #94a3b8;
}

.aml__score-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 8px;
}

.aml__score-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.aml__score-num {
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
  transition: color 0.3s ease;
}

.aml__score-num--low {
  color: #059669;
}

.aml__score-num--mid {
  color: #d97706;
}

.aml__score-num--high {
  color: #dc2626;
}

.aml__bar {
  height: 6px;
  border-radius: 6px;
  background: #e8eef3;
  overflow: hidden;
  margin-bottom: 8px;
}

.aml__bar-fill {
  display: block;
  height: 100%;
  border-radius: 6px;
  transition: width 0.45s ease;
}

.aml__bar-fill--low {
  background: linear-gradient(90deg, #059669, #34d399);
}

.aml__bar-fill--mid {
  background: linear-gradient(90deg, #d97706, #fbbf24);
}

.aml__bar-fill--high {
  background: linear-gradient(90deg, #dc2626, #f87171);
}

.aml__alert {
  margin: 0 0 14px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
}

.aml__txn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  margin-bottom: 10px;
}

.aml__txn-id {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  font-family: ui-monospace, monospace;
}

.aml__txn-amount {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  color: #1a365d;
}

.aml__txn-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.aml__txn-badge--low {
  background: #ecfdf5;
  color: #059669;
}

.aml__txn-badge--review {
  background: #fffbeb;
  color: #d97706;
}

.aml__txn-badge--flag {
  background: #fef2f2;
  color: #dc2626;
}

.aml__hint {
  margin: 0 0 14px;
  font-size: 12px;
  line-height: 1.45;
  color: #64748b;
}

.aml__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #e8eef3;
}

.aml__stat {
  text-align: center;
}

.aml__stat-value {
  display: block;
  font-size: 13px;
  font-weight: 800;
  color: #06b6d4;
}

.aml__stat-label {
  display: block;
  font-size: 9px;
  color: #94a3b8;
  margin-top: 2px;
}

.aml-fade-enter-active,
.aml-fade-leave-active {
  transition: opacity 0.25s ease;
}

.aml-fade-enter-from,
.aml-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .aml--ready .aml__live-dot {
    animation: none;
  }

  .aml__card {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
