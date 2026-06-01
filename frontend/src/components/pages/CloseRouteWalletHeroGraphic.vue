<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import BrandLogo from "../BrandLogo.vue";

const emit = defineEmits(["metric-change"]);

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const metrics = [
  { id: "users", label: "Users", value: "4", sub: "Registered accounts", icon: "👥" },
  { id: "wallets", label: "Wallets", value: "2", sub: "All currencies", icon: "💳" },
  { id: "journals", label: "Journal entries", value: "6", sub: "Immutable postings", icon: "📒" },
  { id: "liability", label: "INR liability", value: "₹53,000", sub: "Sum of INR balances", icon: "₹" },
  { id: "posted", label: "Posted today", value: "0", sub: "New rows today", icon: "🕐" },
  { id: "topups", label: "PG top-ups", value: "0", sub: "Via settlement API", icon: "🛒" },
];

const nav = [
  { label: "Dashboard", active: true },
  { label: "Reconciliation Center", active: false },
  { section: "Ledger" },
  { label: "Ledger accounts", active: false },
  { label: "Wallets", active: false },
  { label: "Journal entries", active: false },
  { section: "People" },
  { label: "Users", active: false },
];

const highlight = ref(0);
let cycleTimer = null;

const activeMetricId = computed(
  () => metrics[highlight.value]?.id ?? "wallets",
);

function emitMetric() {
  emit("metric-change", activeMetricId.value);
}

function startCycle() {
  stopCycle();
  cycleTimer = setInterval(() => {
    if (!props.ready) return;
    highlight.value = (highlight.value + 1) % metrics.length;
  }, 3200);
}

function stopCycle() {
  clearInterval(cycleTimer);
}

watch(
  () => props.ready,
  (r) => (r ? startCycle() : stopCycle()),
  { immediate: true },
);

watch(activeMetricId, () => emitMetric(), { immediate: true });

onMounted(() => {
  if (props.ready) startCycle();
});

onUnmounted(stopCycle);
</script>

<template>
  <div
    class="wallet-dash"
    :class="{ 'wallet-dash--ready': ready }"
    role="img"
    aria-label="Closed-loop wallet command center preview"
  >
    <div class="wallet-dash__mesh" aria-hidden="true">
      <span class="wallet-dash__orb wallet-dash__orb--a" />
      <span class="wallet-dash__orb wallet-dash__orb--b" />
    </div>

    <article class="wallet-dash__frame">
      <header class="wallet-dash__bar">
        <BrandLogo variant="on-dark" alt="Urbanrupee" class="wallet-dash__logo" />
        <input
          class="wallet-dash__search"
          type="text"
          placeholder="Search…"
          readonly
          aria-hidden="true"
        />
        <span class="wallet-dash__avatar" aria-hidden="true">OA</span>
      </header>

      <div class="wallet-dash__body">
        <aside class="wallet-dash__side">
          <template v-for="(item, i) in nav" :key="`${item.label || item.section}-${i}`">
            <p v-if="item.section" class="wallet-dash__section">{{ item.section }}</p>
            <button
              v-else
              type="button"
              class="wallet-dash__nav"
              :class="{ 'wallet-dash__nav--active': item.active }"
            >
              {{ item.label }}
            </button>
          </template>
        </aside>

        <main class="wallet-dash__main">
          <div class="wallet-dash__welcome">
            <span class="wallet-dash__welcome-avatar" aria-hidden="true">OA</span>
            <div>
              <strong>Welcome Operations Admin</strong>
              <button type="button" class="wallet-dash__signout">Sign out</button>
            </div>
          </div>

          <h3 class="wallet-dash__title">Command center</h3>
          <p class="wallet-dash__sub">Closed-loop wallet &amp; ledger snapshot</p>

          <div class="wallet-dash__grid">
            <div
              v-for="(m, idx) in metrics"
              :key="m.label"
              class="wallet-dash__card"
              :class="{ 'wallet-dash__card--pulse': highlight === idx }"
            >
              <span class="wallet-dash__card-icon" aria-hidden="true">{{ m.icon }}</span>
              <span class="wallet-dash__card-label">{{ m.label }}</span>
              <strong>{{ m.value }}</strong>
              <em>{{ m.sub }}</em>
            </div>
          </div>

          <section class="wallet-dash__chart">
            <h4>Journal volume</h4>
            <p>Posted entries per day (last 14 days)</p>
            <div class="wallet-dash__chart-area">
              <svg viewBox="0 0 300 60" preserveAspectRatio="none" aria-hidden="true">
                <polyline
                  fill="none"
                  stroke="#0d9488"
                  stroke-width="2"
                  points="0,50 30,48 60,45 90,42 120,40 150,38 180,35 210,32 240,30 270,28 300,25"
                  class="wallet-dash__line"
                />
              </svg>
            </div>
          </section>
        </main>
      </div>
    </article>
  </div>
</template>

<style scoped>
.wallet-dash {
  width: 100%;
  max-width: 520px;
  margin-inline: auto;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.55s ease,
    transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.wallet-dash--ready {
  opacity: 1;
  transform: translateY(0);
}

.wallet-dash__mesh {
  position: absolute;
  inset: -5%;
  pointer-events: none;
}

.wallet-dash__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(48px);
  opacity: 0.45;
}

.wallet-dash__orb--a {
  width: 48%;
  height: 42%;
  background: #6366f1;
  top: 5%;
  right: 10%;
  animation: wallet-orb 10s ease-in-out infinite;
}

.wallet-dash__orb--b {
  width: 42%;
  height: 40%;
  background: #0d9488;
  bottom: 0;
  left: 5%;
  animation: wallet-orb 12s ease-in-out infinite reverse;
}

@keyframes wallet-orb {
  50% {
    transform: translate(-14%, 12%);
  }
}

.wallet-dash__frame {
  position: relative;
  z-index: 1;
  border-radius: 14px;
  overflow: hidden;
  background: #f8fafc;
  border: 2px solid transparent;
  background-image:
    linear-gradient(#f8fafc, #f8fafc),
    linear-gradient(90deg, #6366f1, #0d9488, #22d3ee, #6366f1);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    300% 100%;
  animation: wallet-border 6s linear infinite;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.18);
  font-size: 10px;
}

@keyframes wallet-border {
  to {
    background-position:
      0 0,
      200% 50%;
  }
}

.wallet-dash__bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: linear-gradient(120deg, #0f766e, #0891b2, #4f46e5, #0f766e);
  background-size: 280% 280%;
  animation: wallet-bar 8s ease infinite;
  color: #fff;
}

@keyframes wallet-bar {
  50% {
    background-position: 100% 50%;
  }
}

.wallet-dash__logo :deep(.brand-logo--on-dark) {
  height: 14px;
  flex-shrink: 0;
}

.wallet-dash__search {
  flex: 1;
  max-width: 140px;
  margin-left: auto;
  padding: 6px 10px;
  border: none;
  border-radius: 8px;
  font-size: 9px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.wallet-dash__avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #fff;
  color: #0f766e;
  font-size: 10px;
  font-weight: 800;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.wallet-dash__body {
  display: flex;
  min-height: 340px;
}

.wallet-dash__side {
  width: 118px;
  flex-shrink: 0;
  background: #0f172a;
  padding: 10px 8px;
  color: #94a3b8;
}

.wallet-dash__section {
  margin: 10px 0 4px;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #64748b;
}

.wallet-dash__nav {
  display: block;
  width: 100%;
  text-align: left;
  padding: 7px 8px;
  margin-bottom: 2px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #cbd5e1;
  font-size: 9px;
  cursor: pointer;
}

.wallet-dash__nav--active {
  background: #fff;
  color: #0f172a;
  font-weight: 600;
}

.wallet-dash__main {
  flex: 1;
  padding: 12px;
  min-width: 0;
}

.wallet-dash__welcome {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  margin-bottom: 10px;
}

.wallet-dash__welcome-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d9488, #6366f1);
  color: #fff;
  font-size: 10px;
  font-weight: 800;
  display: grid;
  place-items: center;
}

.wallet-dash__welcome strong {
  display: block;
  font-size: 11px;
  color: #0f172a;
}

.wallet-dash__signout {
  margin-top: 2px;
  padding: 0;
  border: none;
  background: none;
  font-size: 9px;
  color: #64748b;
  cursor: pointer;
}

.wallet-dash__title {
  margin: 0 0 4px;
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
}

.wallet-dash__sub {
  margin: 0 0 10px;
  font-size: 9px;
  color: #64748b;
}

.wallet-dash__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 10px;
}

.wallet-dash__card {
  padding: 10px 8px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e2e8f0;
  transition:
    box-shadow 0.35s ease,
    transform 0.35s ease,
    border-color 0.35s ease;
}

.wallet-dash__card--pulse {
  border-color: #0d9488;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.2);
}

.wallet-dash__card-icon {
  font-size: 12px;
}

.wallet-dash__card-label {
  display: block;
  font-size: 8px;
  color: #64748b;
  margin-top: 4px;
}

.wallet-dash__card strong {
  display: block;
  font-size: 14px;
  color: #0f172a;
  margin: 2px 0;
}

.wallet-dash__card em {
  font-size: 7px;
  font-style: normal;
  color: #94a3b8;
}

.wallet-dash__chart {
  padding: 10px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.wallet-dash__chart h4 {
  margin: 0 0 2px;
  font-size: 11px;
  color: #0f172a;
}

.wallet-dash__chart p {
  margin: 0 0 8px;
  font-size: 8px;
  color: #64748b;
}

.wallet-dash__chart-area {
  height: 56px;
}

.wallet-dash__chart-area svg {
  width: 100%;
  height: 100%;
}

.wallet-dash__line {
  stroke-dasharray: 400;
  animation: wallet-line 3s ease-in-out infinite alternate;
}

@keyframes wallet-line {
  from {
    stroke-dashoffset: 80;
  }

  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .wallet-dash,
  .wallet-dash__frame,
  .wallet-dash__bar,
  .wallet-dash__orb,
  .wallet-dash__line {
    animation: none;
    transition: none;
  }
}
</style>
