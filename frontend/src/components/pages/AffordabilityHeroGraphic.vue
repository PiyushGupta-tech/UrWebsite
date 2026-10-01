<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const plans = [
  { id: "3", months: 3, emi: "₹8,400", rate: "0%", badge: "No cost" },
  { id: "6", months: 6, emi: "₹4,250", rate: "6%", badge: "Popular" },
  { id: "9", months: 9, emi: "₹2,890", rate: "9%", badge: null },
  { id: "12", months: 12, emi: "₹2,210", rate: "12%", badge: "Low EMI" },
];

const amount = "₹24,999";
const activeId = ref("6");
let cycleTimer = null;

const active = computed(
  () => plans.find((p) => p.id === activeId.value) ?? plans[1],
);

function select(id) {
  activeId.value = id;
}

function startCycle() {
  stopCycle();
  cycleTimer = setInterval(() => {
    if (!props.ready) return;
    const i = plans.findIndex((p) => p.id === activeId.value);
    activeId.value = plans[(i + 1) % plans.length].id;
  }, 3500);
}

function stopCycle() {
  clearInterval(cycleTimer);
}

watch(
  () => props.ready,
  (r) => (r ? startCycle() : stopCycle()),
  { immediate: true },
);

onMounted(() => {
  if (props.ready) startCycle();
});

onUnmounted(stopCycle);
</script>

<template>
  <div
    class="afford"
    :class="{ 'afford--ready': ready }"
    role="img"
    aria-label="Affordability and EMI preview"
  >
    <div class="afford__mesh" aria-hidden="true">
      <span class="afford__orb afford__orb--a" />
      <span class="afford__orb afford__orb--b" />
    </div>

    <article class="afford__card">
      <header class="afford__head">
        <span class="afford__title">EMI &amp; BNPL</span>
        <span class="afford__amount">{{ amount }}</span>
      </header>

      <p class="afford__lead">Split checkout: cardless &amp; card EMI</p>

      <div class="afford__plans" role="tablist">
        <button
          v-for="plan in plans"
          :key="plan.id"
          type="button"
          role="tab"
          class="afford__plan"
          :class="{ 'afford__plan--active': activeId === plan.id }"
          :aria-selected="activeId === plan.id"
          @click="select(plan.id)"
        >
          <span class="afford__plan-months">{{ plan.months }} mo</span>
          <span class="afford__plan-emi">{{ plan.emi }}</span>
          <span v-if="plan.badge" class="afford__plan-badge">{{ plan.badge }}</span>
        </button>
      </div>

      <div class="afford__detail">
        <div class="afford__detail-row">
          <span>Monthly EMI</span>
          <strong>{{ active.emi }}</strong>
        </div>
        <div class="afford__detail-row">
          <span>Interest</span>
          <strong>{{ active.rate }}</strong>
        </div>
        <div class="afford__detail-row">
          <span>Tenure</span>
          <strong>{{ active.months }} months</strong>
        </div>
      </div>

      <button type="button" class="afford__cta">Continue with {{ active.months }}-month EMI</button>

      <div class="afford__tags">
        <span>Cardless EMI</span>
        <span>Credit EMI</span>
        <span>Pay later</span>
      </div>
    </article>
  </div>
</template>

<style scoped>
.afford {
  width: 100%;
  max-width: 400px;
  margin-inline: auto;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.55s ease,
    transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.afford--ready {
  opacity: 1;
  transform: translateY(0);
}

.afford__mesh {
  position: absolute;
  inset: -6%;
  pointer-events: none;
}

.afford__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(44px);
  opacity: 0.55;
}

.afford__orb--a {
  width: 50%;
  height: 45%;
  background: #f472b6;
  top: -5%;
  right: -5%;
  animation: afford-orb 10s ease-in-out infinite;
}

.afford__orb--b {
  width: 48%;
  height: 42%;
  background: #fbbf24;
  bottom: -8%;
  left: -10%;
  animation: afford-orb 12s ease-in-out infinite reverse;
}

@keyframes afford-orb {
  50% {
    transform: translate(-16%, 14%);
  }
}

.afford__card {
  position: relative;
  z-index: 1;
  padding: 18px;
  border-radius: 16px;
  background: #fff;
  border: 2px solid transparent;
  background-image:
    linear-gradient(#fff, #fff),
    linear-gradient(90deg, #f472b6, #fb923c, #facc15, #a78bfa, #f472b6);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    320% 100%;
  animation: afford-border 5s linear infinite;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.15);
  color: #0f172a;
}

@keyframes afford-border {
  to {
    background-position:
      0 0,
      200% 50%;
  }
}

.afford__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 6px;
}

.afford__title {
  font-size: 15px;
  font-weight: 700;
}

.afford__amount {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(90deg, #db2777, #ea580c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.afford__lead {
  margin: 0 0 14px;
  font-size: 12px;
  color: #64748b;
}

.afford__plans {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-bottom: 14px;
}

.afford__plan {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 10px 4px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #f8fafc;
  cursor: pointer;
  transition:
    border-color 0.2s,
    transform 0.2s,
    box-shadow 0.2s;
}

.afford__plan--active {
  border-color: #ec4899;
  background: linear-gradient(160deg, #fdf2f8, #fff7ed);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(236, 72, 153, 0.2);
}

.afford__plan-months {
  font-size: 10px;
  font-weight: 700;
  color: #64748b;
}

.afford__plan--active .afford__plan-months {
  color: #db2777;
}

.afford__plan-emi {
  font-size: 11px;
  font-weight: 800;
}

.afford__plan-badge {
  position: absolute;
  top: -6px;
  font-size: 7px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 4px;
  background: linear-gradient(90deg, #ec4899, #f97316);
  color: #fff;
}

.afford__detail {
  padding: 12px;
  border-radius: 10px;
  background: #f1f5f9;
  margin-bottom: 12px;
}

.afford__detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  padding: 4px 0;
}

.afford__detail-row span {
  color: #64748b;
}

.afford__detail-row strong {
  font-weight: 700;
}

.afford__cta {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  font-family: inherit;
  color: #fff;
  cursor: pointer;
  background: linear-gradient(90deg, #ec4899, #f97316, #facc15, #ec4899);
  background-size: 280% 100%;
  animation: afford-border 4s linear infinite;
  margin-bottom: 10px;
}

.afford__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.afford__tags span {
  font-size: 9px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  background: #ede9fe;
  color: #6d28d9;
}

@media (prefers-reduced-motion: reduce) {
  .afford,
  .afford__card,
  .afford__cta,
  .afford__orb {
    animation: none;
    transition: none;
  }
}
</style>
