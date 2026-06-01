<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const banks = [
  { id: "sbi", label: "SBI", color: "#2563eb" },
  { id: "hdfc", label: "HDFC", color: "#1d4ed8" },
  { id: "icici", label: "ICICI", color: "#ea580c" },
  { id: "axis", label: "Axis", color: "#7c3aed" },
  { id: "kotak", label: "Kotak", color: "#dc2626" },
];

const flows = [
  { id: "intent", label: "UPI Intent", amount: "₹12,450", meta: "pay@merchant · 0.3s" },
  { id: "collect", label: "Collect", amount: "₹8,200", meta: "VPA verified · 0.4s" },
  { id: "qr", label: "QR", amount: "₹24,999", meta: "Dynamic QR · 0.2s" },
];

const activeFlow = ref("intent");
const pulse = ref(false);
let cycleTimer = null;
let pulseTimer = null;

const active = computed(
  () => flows.find((f) => f.id === activeFlow.value) ?? flows[0],
);

function selectFlow(id) {
  activeFlow.value = id;
}

function startCycle() {
  stopCycle();
  cycleTimer = setInterval(() => {
    if (!props.ready) return;
    const i = flows.findIndex((f) => f.id === activeFlow.value);
    activeFlow.value = flows[(i + 1) % flows.length].id;
    pulse.value = true;
    clearTimeout(pulseTimer);
    pulseTimer = setTimeout(() => {
      pulse.value = false;
    }, 600);
  }, 3800);
}

function stopCycle() {
  clearInterval(cycleTimer);
  clearTimeout(pulseTimer);
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
    class="upi"
    :class="{ 'upi--ready': ready, 'upi--pulse': pulse }"
    role="img"
    aria-label="UPI switch routing preview"
  >
    <div class="upi__mesh" aria-hidden="true">
      <span class="upi__orb upi__orb--a" />
      <span class="upi__orb upi__orb--b" />
    </div>

    <article class="upi__card">
      <header class="upi__head">
        <span class="upi__title">UPI Switch</span>
        <span class="upi__live">
          <span class="upi__dot" aria-hidden="true" />
          Live routing
        </span>
      </header>

      <div class="upi__qr" :class="{ 'upi__qr--pulse': pulse }">
        <div class="upi__qr-grid" aria-hidden="true" />
        <span class="upi__qr-label">Scan &amp; pay</span>
      </div>

      <div class="upi__flows" role="tablist">
        <button
          v-for="flow in flows"
          :key="flow.id"
          type="button"
          role="tab"
          class="upi__flow"
          :class="{ 'upi__flow--active': activeFlow === flow.id }"
          :aria-selected="activeFlow === flow.id"
          @click="selectFlow(flow.id)"
        >
          {{ flow.label }}
        </button>
      </div>

      <div class="upi__txn">
        <p class="upi__amount">{{ active.amount }}</p>
        <p class="upi__meta">{{ active.meta }}</p>
        <div class="upi__route">
          <span>Merchant</span>
          <span class="upi__route-line" aria-hidden="true" />
          <span class="upi__route-hub">UR Switch</span>
          <span class="upi__route-line" aria-hidden="true" />
          <span>PSP</span>
        </div>
      </div>

      <div class="upi__banks">
        <span
          v-for="bank in banks"
          :key="bank.id"
          class="upi__bank"
          :style="{ '--bank': bank.color }"
        >{{ bank.label }}</span>
      </div>

      <div class="upi__stats">
        <div><strong>99.2%</strong><span>Success</span></div>
        <div><strong>&lt;400ms</strong><span>Route</span></div>
        <div><strong>5+</strong><span>Banks</span></div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.upi {
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

.upi--ready {
  opacity: 1;
  transform: translateY(0);
}

.upi__mesh {
  position: absolute;
  inset: -8%;
  pointer-events: none;
  z-index: 0;
}

.upi__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.5;
}

.upi__orb--a {
  width: 55%;
  height: 50%;
  background: #22d3ee;
  top: 0;
  left: -10%;
  animation: upi-orb 9s ease-in-out infinite;
}

.upi__orb--b {
  width: 50%;
  height: 45%;
  background: #34d399;
  bottom: 0;
  right: -8%;
  animation: upi-orb 11s ease-in-out infinite reverse;
}

@keyframes upi-orb {
  50% {
    transform: translate(18%, -12%);
  }
}

.upi__card {
  position: relative;
  z-index: 1;
  padding: 18px;
  border-radius: 16px;
  background: rgba(8, 13, 22, 0.92);
  border: 2px solid transparent;
  background-image:
    linear-gradient(rgba(8, 13, 22, 0.94), rgba(8, 13, 22, 0.94)),
    linear-gradient(90deg, #22d3ee, #34d399, #818cf8, #22d3ee);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    300% 100%;
  animation: upi-border 5s linear infinite;
  color: #e8eef7;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
}

@keyframes upi-border {
  to {
    background-position:
      0 0,
      200% 50%;
  }
}

.upi__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.upi__title {
  font-size: 14px;
  font-weight: 700;
}

.upi__live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  color: #4ade80;
  text-transform: uppercase;
}

.upi__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4ade80;
  animation: upi-blink 1.2s ease infinite;
}

@keyframes upi-blink {
  50% {
    opacity: 0.35;
  }
}

.upi__qr {
  display: grid;
  place-items: center;
  width: 88px;
  height: 88px;
  margin: 0 auto 14px;
  border-radius: 12px;
  background: #fff;
  position: relative;
  transition: transform 0.35s ease;
}

.upi--pulse .upi__qr,
.upi__qr--pulse {
  transform: scale(1.04);
  box-shadow: 0 0 24px rgba(34, 211, 238, 0.5);
}

.upi__qr-grid {
  width: 62px;
  height: 62px;
  background:
    linear-gradient(90deg, #0f172a 2px, transparent 2px) 0 0 / 8px 8px,
    linear-gradient(#0f172a 2px, transparent 2px) 0 0 / 8px 8px;
  opacity: 0.85;
}

.upi__qr-label {
  position: absolute;
  bottom: 6px;
  font-size: 8px;
  font-weight: 700;
  color: #0f172a;
}

.upi__flows {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
}

.upi__flow {
  flex: 1;
  padding: 8px 6px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
  color: #8b9cb3;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.2s,
    color 0.2s;
}

.upi__flow--active {
  color: #fff;
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
}

.upi__amount {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
}

.upi__meta {
  margin: 2px 0 10px;
  font-size: 11px;
  color: #8b9cb3;
}

.upi__route {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 9px;
  font-weight: 600;
  color: #8b9cb3;
  margin-bottom: 12px;
}

.upi__route-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, #22d3ee, #34d399);
  border-radius: 2px;
  animation: upi-line 1.5s ease-in-out infinite;
}

@keyframes upi-line {
  50% {
    opacity: 0.45;
  }
}

.upi__route-hub {
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.upi__banks {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.upi__bank {
  font-size: 9px;
  font-weight: 700;
  padding: 5px 8px;
  border-radius: 6px;
  background: color-mix(in srgb, var(--bank) 22%, transparent);
  color: #fff;
  border: 1px solid color-mix(in srgb, var(--bank) 45%, transparent);
}

.upi__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  text-align: center;
}

.upi__stats strong {
  display: block;
  font-size: 14px;
  color: #22d3ee;
}

.upi__stats span {
  font-size: 9px;
  color: #8b9cb3;
}

@media (prefers-reduced-motion: reduce) {
  .upi,
  .upi__card,
  .upi__orb,
  .upi__dot,
  .upi__route-line {
    animation: none;
    transition: none;
  }
}
</style>
