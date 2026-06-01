<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import BrandLogo from "../BrandLogo.vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const periods = ["Daily", "Weekly", "Monthly", "Yearly"];
const activePeriod = ref("Monthly");
const sidebarOpen = ref(true);

const metrics = [
  { label: "Total Payouts", value: "0", tone: "blue", sub: "All transactions" },
  { label: "Successful", value: "0", tone: "green", sub: "Settled" },
  { label: "Pending", value: "0", tone: "orange", sub: "In queue" },
  { label: "Failed", value: "0", tone: "red", sub: "Unsuccessful" },
];

const wallets = [
  { label: "Main Wallet", value: "₹0.00", sub: "Available balance" },
  { label: "Total amount processed", value: "₹0.00", sub: "Volume" },
  { label: "Success rate", value: "0%", sub: "Successful share" },
];

const nav = [
  { label: "Dashboard", active: true },
  { label: "Main Wallet", active: false },
  { label: "Request Payout", active: false, indent: true },
  { label: "Bank Accounts", active: false, indent: true },
  { label: "Transaction History", active: false, indent: true },
];

let periodTimer = null;

function startCycle() {
  stopCycle();
  periodTimer = setInterval(() => {
    if (!props.ready) return;
    const i = periods.indexOf(activePeriod.value);
    activePeriod.value = periods[(i + 1) % periods.length];
  }, 4000);
}

function stopCycle() {
  clearInterval(periodTimer);
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
    class="payout"
    :class="{ 'payout--ready': ready }"
    role="img"
    aria-label="Payout portal dashboard preview"
  >
    <div class="payout__mesh" aria-hidden="true">
      <span class="payout__orb payout__orb--a" />
      <span class="payout__orb payout__orb--b" />
    </div>

    <article class="payout__frame">
      <header class="payout__bar">
        <BrandLogo variant="on-dark" alt="Urbanrupee" class="payout__logo" />
        <div class="payout__user">
          <span class="payout__avatar" aria-hidden="true" />
          <div>
            <strong>Testing</strong>
            <span>Member</span>
          </div>
        </div>
      </header>

      <div class="payout__body">
        <aside v-show="sidebarOpen" class="payout__side">
          <nav>
            <button
              v-for="item in nav"
              :key="item.label"
              type="button"
              class="payout__nav"
              :class="{
                'payout__nav--active': item.active,
                'payout__nav--indent': item.indent,
              }"
            >
              {{ item.label }}
            </button>
          </nav>
        </aside>

        <main class="payout__main">
          <div class="payout__title-row">
            <div>
              <h3>Payout Dashboard</h3>
              <p>Welcome back! Here's your payout activity overview.</p>
            </div>
            <button type="button" class="payout__cta">Request Payout</button>
          </div>

          <div class="payout__metrics">
            <div
              v-for="m in metrics"
              :key="m.label"
              class="payout__metric"
              :class="`payout__metric--${m.tone}`"
            >
              <span>{{ m.label }}</span>
              <strong>{{ m.value }}</strong>
              <em>{{ m.sub }}</em>
            </div>
          </div>

          <div class="payout__wallets">
            <div v-for="w in wallets" :key="w.label" class="payout__wallet">
              <span>{{ w.label }}</span>
              <strong>{{ w.value }}</strong>
              <em>{{ w.sub }}</em>
            </div>
          </div>

          <section class="payout__chart">
            <div class="payout__chart-head">
              <span>Payout Activity</span>
              <div class="payout__periods">
                <button
                  v-for="p in periods"
                  :key="p"
                  type="button"
                  class="payout__period"
                  :class="{ 'payout__period--active': activePeriod === p }"
                  @click="activePeriod = p"
                >
                  {{ p }}
                </button>
              </div>
            </div>
            <div class="payout__chart-area">
              <svg viewBox="0 0 280 80" preserveAspectRatio="none" aria-hidden="true">
                <defs>
                  <linearGradient id="payoutLine" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#ef4444" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#ef4444" stop-opacity="0" />
                  </linearGradient>
                </defs>
                <path
                  fill="url(#payoutLine)"
                  d="M0,70 L40,65 L80,68 L120,55 L160,58 L200,48 L240,52 L280,45 L280,80 L0,80 Z"
                />
                <polyline
                  fill="none"
                  stroke="#ef4444"
                  stroke-width="2"
                  points="0,68 40,63 80,66 120,53 160,56 200,46 240,50 280,43"
                  class="payout__line"
                />
              </svg>
              <span class="payout__legend">Payout Amount (₹)</span>
            </div>
          </section>
        </main>
      </div>
    </article>
  </div>
</template>

<style scoped>
.payout {
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

.payout--ready {
  opacity: 1;
  transform: translateY(0);
}

.payout__mesh {
  position: absolute;
  inset: -5%;
  pointer-events: none;
}

.payout__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(48px);
  opacity: 0.4;
}

.payout__orb--a {
  width: 45%;
  height: 40%;
  background: #0d9488;
  top: 0;
  left: 20%;
  animation: payout-orb 9s ease-in-out infinite;
}

.payout__orb--b {
  width: 40%;
  height: 38%;
  background: #3b82f6;
  bottom: 5%;
  right: 0;
  animation: payout-orb 11s ease-in-out infinite reverse;
}

@keyframes payout-orb {
  50% {
    transform: translate(12%, -10%);
  }
}

.payout__frame {
  position: relative;
  z-index: 1;
  border-radius: 14px;
  overflow: hidden;
  background: #f1f5f9;
  border: 2px solid transparent;
  background-image:
    linear-gradient(#f1f5f9, #f1f5f9),
    linear-gradient(90deg, #0d9488, #3b82f6, #22c55e, #0d9488);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    300% 100%;
  animation: payout-border 6s linear infinite;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.2);
  font-size: 10px;
}

@keyframes payout-border {
  to {
    background-position:
      0 0,
      200% 50%;
  }
}

.payout__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: linear-gradient(120deg, #0f766e, #0e7490, #1d4ed8, #0f766e);
  background-size: 280% 280%;
  animation: payout-bar 8s ease infinite;
  color: #fff;
}

@keyframes payout-bar {
  50% {
    background-position: 100% 50%;
  }
}

.payout__logo :deep(.brand-logo--on-dark) {
  height: 14px;
}

.payout__user {
  display: flex;
  align-items: center;
  gap: 8px;
}

.payout__user strong {
  display: block;
  font-size: 11px;
}

.payout__user span {
  font-size: 9px;
  opacity: 0.85;
}

.payout__avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #94a3b8, #e2e8f0);
}

.payout__body {
  display: flex;
  min-height: 320px;
}

.payout__side {
  width: 108px;
  flex-shrink: 0;
  background: #0f172a;
  padding: 10px 6px;
}

.payout__nav {
  display: block;
  width: 100%;
  text-align: left;
  padding: 7px 8px;
  margin-bottom: 2px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #94a3b8;
  font-size: 9px;
  font-weight: 500;
  cursor: pointer;
}

.payout__nav--indent {
  padding-left: 16px;
  font-size: 8px;
}

.payout__nav--active {
  background: rgba(13, 148, 136, 0.35);
  color: #fff;
}

.payout__main {
  flex: 1;
  padding: 12px;
  min-width: 0;
}

.payout__title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 10px;
}

.payout__title-row h3 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.payout__title-row p {
  margin: 0;
  font-size: 9px;
  color: #64748b;
  max-width: 200px;
}

.payout__cta {
  flex-shrink: 0;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  font-size: 9px;
  font-weight: 700;
  color: #fff;
  cursor: pointer;
  background: linear-gradient(135deg, #0d9488, #06b6d4);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35);
}

.payout__metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-bottom: 8px;
}

.payout__metric {
  padding: 8px 6px;
  border-radius: 8px;
  color: #fff;
}

.payout__metric span {
  display: block;
  font-size: 8px;
  opacity: 0.9;
}

.payout__metric strong {
  display: block;
  font-size: 16px;
  margin: 4px 0;
}

.payout__metric em {
  font-size: 7px;
  font-style: normal;
  opacity: 0.85;
}

.payout__metric--blue {
  background: linear-gradient(145deg, #2563eb, #3b82f6);
}

.payout__metric--green {
  background: linear-gradient(145deg, #059669, #22c55e);
}

.payout__metric--orange {
  background: linear-gradient(145deg, #d97706, #f59e0b);
}

.payout__metric--red {
  background: linear-gradient(145deg, #dc2626, #ef4444);
}

.payout__wallets {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 8px;
}

.payout__wallet {
  padding: 10px 8px;
  border-radius: 8px;
  background: linear-gradient(145deg, #1e293b, #334155);
  color: #fff;
}

.payout__wallet span {
  display: block;
  font-size: 8px;
  color: #94a3b8;
}

.payout__wallet strong {
  display: block;
  font-size: 13px;
  margin: 4px 0 2px;
}

.payout__wallet em {
  font-size: 7px;
  font-style: normal;
  color: #94a3b8;
}

.payout__chart {
  background: #fff;
  border-radius: 8px;
  padding: 10px;
  border: 1px solid #e2e8f0;
}

.payout__chart-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 600;
  color: #0f172a;
}

.payout__periods {
  display: flex;
  gap: 4px;
}

.payout__period {
  padding: 3px 8px;
  border: none;
  border-radius: 6px;
  background: #f1f5f9;
  font-size: 8px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
}

.payout__period--active {
  background: linear-gradient(90deg, #0d9488, #06b6d4);
  color: #fff;
}

.payout__chart-area {
  height: 72px;
  position: relative;
}

.payout__chart-area svg {
  width: 100%;
  height: 100%;
}

.payout__line {
  stroke-dasharray: 320;
  stroke-dashoffset: 320;
  animation: payout-draw 2.5s ease forwards infinite alternate;
}

@keyframes payout-draw {
  to {
    stroke-dashoffset: 0;
  }
}

.payout__legend {
  position: absolute;
  bottom: 0;
  right: 0;
  font-size: 8px;
  color: #ef4444;
}

@media (prefers-reduced-motion: reduce) {
  .payout,
  .payout__frame,
  .payout__bar,
  .payout__orb,
  .payout__line {
    animation: none;
    transition: none;
  }

  .payout__line {
    stroke-dashoffset: 0;
  }
}
</style>
