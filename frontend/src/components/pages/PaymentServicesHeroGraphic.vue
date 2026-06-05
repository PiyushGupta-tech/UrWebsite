<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const methods = [
  {
    id: "upi",
    label: "UPI",
    hint: "High success UPI routing with real-time fallback across PSPs.",
    amount: "₹12,450",
    meta: "pay@Urbanrupee · Intent",
    latency: "0.3s",
  },
  {
    id: "cards",
    label: "Cards",
    hint: "Debit & credit with tokenization and saved-card checkout.",
    amount: "₹24,999",
    meta: "•••• 4242 · Visa",
    latency: "0.4s",
  },
  {
    id: "netbanking",
    label: "Net Banking",
    hint: "Major bank rails with seamless redirect and retry logic.",
    amount: "₹8,200",
    meta: "HDFC · Redirect",
    latency: "0.6s",
  },
  {
    id: "wallets",
    label: "Wallets",
    hint: "Popular digital wallets supported for Indian customers.",
    amount: "₹3,150",
    meta: "Paytm · One-tap",
    latency: "0.35s",
  },
];

const pipeline = [
  { id: "init", label: "Initiate" },
  { id: "route", label: "Route" },
  { id: "auth", label: "Authorize" },
  { id: "settle", label: "Settle" },
];

const features = [
  { label: "Recurring", icon: "↻" },
  { label: "Split Pay", icon: "⑂" },
  { label: "Refunds", icon: "↩" },
];

const metrics = [
  { stat: "+10%", label: "Conversion lift" },
  { stat: "99.9%", label: "Uptime SLA" },
  { stat: "PCI", label: "DSS compliant" },
];

const activeMethodId = ref("upi");
const hoveredMethod = ref(null);
const lockedMethod = ref(null);
const pipelineStep = ref(0);
const txnStatus = ref("idle"); // idle | processing | success
const feedIndex = ref(0);

const feedLines = [
  "UPI intent created · routed to primary PSP",
  "Card token matched · 3DS skipped (low risk)",
  "Net banking redirect · session verified",
  "Wallet balance confirmed · debited",
  "Split payout queued · 2 beneficiaries",
  "Refund issued · settled to source",
];

const activeMethod = computed(
  () => methods.find((m) => m.id === activeMethodId.value) ?? methods[0],
);

const displayMethodId = computed(() => {
  if (lockedMethod.value) return lockedMethod.value;
  if (hoveredMethod.value) return hoveredMethod.value;
  return activeMethodId.value;
});

const displayMethod = computed(
  () => methods.find((m) => m.id === displayMethodId.value) ?? methods[0],
);

const statusLabel = computed(() => {
  if (txnStatus.value === "processing") return "Processing payment…";
  if (txnStatus.value === "success") return "Payment successful";
  return "Ready to collect";
});

let methodTimer = null;
let pipelineTimer = null;
let feedTimer = null;

function isPaused() {
  return !!lockedMethod.value || !!hoveredMethod.value;
}

function selectMethod(id, { lock = false } = {}) {
  activeMethodId.value = id;
  if (lock) {
    lockedMethod.value = lockedMethod.value === id ? null : id;
  }
}

function onMethodEnter(id) {
  hoveredMethod.value = id;
  if (activeMethodId.value !== id) {
    activeMethodId.value = id;
    runTxnAnimation();
  }
}

function onMethodLeave() {
  hoveredMethod.value = null;
  if (!lockedMethod.value) {
    const idx = methods.findIndex((m) => m.id === activeMethodId.value);
    activeMethodId.value = methods[idx >= 0 ? idx : 0].id;
  } else {
    activeMethodId.value = lockedMethod.value;
  }
}

function onMethodClick(id) {
  selectMethod(id, { lock: true });
  if (activeMethodId.value !== id) activeMethodId.value = id;
  runTxnAnimation();
}

function startMethodCycle() {
  stopMethodCycle();
  methodTimer = setInterval(() => {
    if (!props.ready || isPaused()) return;
    const idx = methods.findIndex((m) => m.id === activeMethodId.value);
    const next = methods[(idx + 1) % methods.length];
    activeMethodId.value = next.id;
    runTxnAnimation();
  }, 4000);
}

function stopMethodCycle() {
  if (methodTimer) {
    clearInterval(methodTimer);
    methodTimer = null;
  }
}

function runTxnAnimation() {
  txnStatus.value = "processing";
  pipelineStep.value = 0;
  clearInterval(pipelineTimer);

  let step = 0;
  pipelineTimer = setInterval(() => {
    if (!props.ready) return;
    step += 1;
    pipelineStep.value = Math.min(step, pipeline.length);
    if (step >= pipeline.length) {
      clearInterval(pipelineTimer);
      pipelineTimer = null;
      txnStatus.value = "success";
      setTimeout(() => {
        if (!props.ready) return;
        txnStatus.value = "idle";
        pipelineStep.value = 0;
      }, 1400);
    }
  }, 420);
}

function startFeedCycle() {
  stopFeedCycle();
  feedTimer = setInterval(() => {
    if (!props.ready) return;
    feedIndex.value = (feedIndex.value + 1) % feedLines.length;
  }, 2800);
}

function stopFeedCycle() {
  if (feedTimer) {
    clearInterval(feedTimer);
    feedTimer = null;
  }
}

function stopPipeline() {
  if (pipelineTimer) {
    clearInterval(pipelineTimer);
    pipelineTimer = null;
  }
}

watch(
  () => props.ready,
  (ready) => {
    if (ready) {
      startMethodCycle();
      startFeedCycle();
      runTxnAnimation();
    } else {
      stopMethodCycle();
      stopFeedCycle();
      stopPipeline();
    }
  },
  { immediate: true },
);

onMounted(() => {
  if (props.ready) {
    startMethodCycle();
    startFeedCycle();
    runTxnAnimation();
  }
});

onUnmounted(() => {
  stopMethodCycle();
  stopFeedCycle();
  stopPipeline();
});
</script>

<template>
  <div
    class="paydash"
    :class="{ 'paydash--ready': ready }"
    role="group"
    aria-label="Payment services live dashboard preview"
  >
    <div class="paydash__frame">
      <header class="paydash__header">
        <span class="paydash__live">
          <span class="paydash__live-dot" aria-hidden="true" />
          Live checkout
        </span>
        <span class="paydash__sla">99.9% uptime</span>
      </header>

      <nav class="paydash__tabs" aria-label="Payment methods">
        <button
          v-for="m in methods"
          :key="m.id"
          type="button"
          class="paydash__tab"
          :class="{
            'paydash__tab--active': displayMethodId === m.id,
            'paydash__tab--locked': lockedMethod === m.id,
          }"
          :aria-pressed="displayMethodId === m.id"
          @mouseenter="onMethodEnter(m.id)"
          @mouseleave="onMethodLeave"
          @click="onMethodClick(m.id)"
        >
          {{ m.label }}
        </button>
      </nav>

      <div class="paydash__body">
        <div class="paydash__checkout">
          <Transition name="paydash-slide" mode="out-in">
            <div :key="displayMethod.id" class="paydash__receipt">
              <p class="paydash__receipt-label">Amount due</p>
              <p class="paydash__receipt-amount">{{ displayMethod.amount }}</p>
              <p class="paydash__receipt-meta">{{ displayMethod.meta }}</p>
              <div
                class="paydash__status"
                :class="`paydash__status--${txnStatus}`"
              >
                <span class="paydash__status-dot" aria-hidden="true" />
                {{ statusLabel }}
              </div>
              <div class="paydash__bar">
                <span
                  class="paydash__bar-fill"
                  :class="{
                    'paydash__bar-fill--go': txnStatus === 'processing',
                    'paydash__bar-fill--done': txnStatus === 'success',
                  }"
                />
              </div>
              <p class="paydash__latency">
                Response <strong>{{ displayMethod.latency }}</strong>
              </p>
            </div>
          </Transition>
        </div>

        <ol class="paydash__pipeline" aria-label="Transaction pipeline">
          <li
            v-for="(step, i) in pipeline"
            :key="step.id"
            class="paydash__step"
            :class="{
              'paydash__step--done': pipelineStep > i,
              'paydash__step--current':
                txnStatus === 'processing' && pipelineStep === i + 1,
              'paydash__step--success': txnStatus === 'success' && pipelineStep >= i + 1,
            }"
          >
            <span class="paydash__step-marker" aria-hidden="true">
              <span v-if="pipelineStep > i || (txnStatus === 'success' && pipelineStep >= i + 1)">✓</span>
              <span v-else>{{ i + 1 }}</span>
            </span>
            <span class="paydash__step-label">{{ step.label }}</span>
          </li>
        </ol>
      </div>

      <div class="paydash__features" aria-hidden="true">
        <span v-for="f in features" :key="f.label" class="paydash__feat">
          <span class="paydash__feat-icon">{{ f.icon }}</span>
          {{ f.label }}
        </span>
      </div>

      <footer class="paydash__metrics">
        <div v-for="m in metrics" :key="m.label" class="paydash__metric">
          <span class="paydash__metric-stat">{{ m.stat }}</span>
          <span class="paydash__metric-label">{{ m.label }}</span>
        </div>
      </footer>

      <div class="paydash__feed" aria-live="polite">
        <Transition name="paydash-feed" mode="out-in">
          <p :key="feedIndex" class="paydash__feed-line">
            <span class="paydash__feed-time">now</span>
            {{ feedLines[feedIndex] }}
          </p>
        </Transition>
      </div>
    </div>

    <p class="paydash__caption" :class="{ 'paydash__caption--ready': ready }">
      {{ displayMethod.hint }}
    </p>
  </div>
</template>

<style scoped>
.paydash {
  width: 100%;
  max-width: 400px;
  margin-inline: auto;
}

.paydash__frame {
  position: relative;
  border-radius: 20px;
  background: #fff;
  border: 1px solid #e2e8f0;
  box-shadow:
    0 4px 6px rgba(26, 54, 93, 0.04),
    0 20px 48px rgba(26, 54, 93, 0.1);
  overflow: hidden;
  opacity: 1;
  transform: perspective(900px) rotateY(-2deg) rotateX(0deg) translateY(0);
  transition:
    opacity 0.55s ease,
    transform 0.65s cubic-bezier(0.22, 1, 0.36, 1);
}

.paydash:not(.paydash--ready) .paydash__frame {
  opacity: 0.85;
  transform: perspective(900px) rotateY(-6deg) rotateX(2deg) translateY(12px);
}

.paydash--ready .paydash__frame {
  opacity: 1;
  transform: perspective(900px) rotateY(-2deg) rotateX(0deg) translateY(0);
}

.paydash--ready .paydash__frame:hover {
  transform: perspective(900px) rotateY(0deg) translateY(-2px);
  box-shadow:
    0 8px 12px rgba(26, 54, 93, 0.06),
    0 28px 56px rgba(6, 182, 212, 0.14);
}

.paydash__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px 10px;
  background: linear-gradient(135deg, #1a365d 0%, #0e7490 55%, #06b6d4 100%);
  color: #fff;
}

.paydash__live {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
}

.paydash__live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.6);
}

.paydash--ready .paydash__live-dot {
  animation: paydash-pulse-dot 1.6s ease-in-out infinite;
}

@keyframes paydash-pulse-dot {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.5);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(52, 211, 153, 0);
  }
}

.paydash__sla {
  font-size: 10px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
}

.paydash__tabs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  padding: 10px 12px 0;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.paydash__tab {
  border: none;
  background: transparent;
  padding: 10px 4px;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  transition:
    color 0.2s,
    background 0.2s,
    transform 0.2s;
  position: relative;
}

.paydash__tab::after {
  content: "";
  position: absolute;
  left: 20%;
  right: 20%;
  bottom: 0;
  height: 2px;
  border-radius: 2px 2px 0 0;
  background: linear-gradient(90deg, #1a365d, #06b6d4);
  transform: scaleX(0);
  transition: transform 0.25s ease;
}

.paydash__tab--active {
  color: #1a365d;
  background: #fff;
}

.paydash__tab--active::after {
  transform: scaleX(1);
}

.paydash__tab:hover {
  color: #06b6d4;
}

.paydash__tab--locked {
  color: #1a365d;
}

.paydash__body {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  padding: 16px;
  align-items: start;
}

.paydash__checkout {
  min-width: 0;
}

.paydash__receipt-label {
  margin: 0 0 4px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
}

.paydash__receipt-amount {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #1a365d;
  line-height: 1.1;
}

.paydash__receipt-meta {
  margin: 4px 0 12px;
  font-size: 12px;
  color: #64748b;
}

.paydash__status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 8px;
}

.paydash__status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #cbd5e1;
}

.paydash__status--processing {
  color: #0e7490;
}

.paydash__status--processing .paydash__status-dot {
  background: #06b6d4;
  animation: paydash-blink 0.7s ease-in-out infinite;
}

.paydash__status--success {
  color: #059669;
}

.paydash__status--success .paydash__status-dot {
  background: #34d399;
}

@keyframes paydash-blink {
  50% {
    opacity: 0.35;
  }
}

.paydash__bar {
  height: 5px;
  border-radius: 5px;
  background: #e8eef3;
  overflow: hidden;
  margin-bottom: 8px;
}

.paydash__bar-fill {
  display: block;
  height: 100%;
  width: 0;
  border-radius: 5px;
  background: linear-gradient(90deg, #1a365d, #06b6d4);
  transition: width 0.5s ease;
}

.paydash__bar-fill--go {
  width: 72%;
  animation: paydash-bar-pulse 0.9s ease-in-out infinite;
}

.paydash__bar-fill--done {
  width: 100%;
}

@keyframes paydash-bar-pulse {
  50% {
    width: 88%;
  }
}

.paydash__latency {
  margin: 0;
  font-size: 10px;
  color: #94a3b8;
}

.paydash__latency strong {
  color: #06b6d4;
  font-weight: 700;
}

/* Pipeline */
.paydash__pipeline {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  position: relative;
}

.paydash__pipeline::before {
  content: "";
  position: absolute;
  left: 11px;
  top: 14px;
  bottom: 14px;
  width: 2px;
  background: #e2e8f0;
  border-radius: 2px;
}

.paydash__step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  position: relative;
  z-index: 1;
}

.paydash__step-marker {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f1f5f9;
  border: 2px solid #e2e8f0;
  display: grid;
  place-items: center;
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
  flex-shrink: 0;
  transition:
    background 0.3s,
    border-color 0.3s,
    color 0.3s,
    transform 0.3s;
}

.paydash__step-label {
  font-size: 10px;
  font-weight: 600;
  color: #94a3b8;
  white-space: nowrap;
  transition: color 0.3s;
}

.paydash__step--current .paydash__step-marker {
  border-color: #06b6d4;
  background: #ecfeff;
  color: #0e7490;
  transform: scale(1.12);
  animation: paydash-step-pulse 0.8s ease-in-out infinite;
}

.paydash__step--done .paydash__step-marker,
.paydash__step--success .paydash__step-marker {
  border-color: #34d399;
  background: #ecfdf5;
  color: #059669;
}

.paydash__step--done .paydash__step-label,
.paydash__step--success .paydash__step-label {
  color: #1a365d;
}

@keyframes paydash-step-pulse {
  50% {
    box-shadow: 0 0 0 6px rgba(6, 182, 212, 0.15);
  }
}

/* Features + metrics */
.paydash__features {
  display: flex;
  gap: 8px;
  padding: 0 16px 12px;
  flex-wrap: wrap;
}

.paydash__feat {
  font-size: 10px;
  font-weight: 600;
  color: #475569;
  padding: 5px 10px;
  border-radius: 999px;
  background: #f1f5f9;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.paydash--ready .paydash__feat {
  animation: paydash-feat-in 0.5s ease backwards;
}

.paydash--ready .paydash__feat:nth-child(2) {
  animation-delay: 0.08s;
}

.paydash--ready .paydash__feat:nth-child(3) {
  animation-delay: 0.16s;
}

@keyframes paydash-feat-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
}

.paydash__feat-icon {
  color: #06b6d4;
  font-size: 11px;
}

.paydash__metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 0 16px 12px;
}

.paydash__metric {
  text-align: center;
  padding: 10px 6px;
  border-radius: 10px;
  background: linear-gradient(180deg, #f8fafc, #fff);
  border: 1px solid #e8eef3;
}

.paydash__metric-stat {
  display: block;
  font-size: 14px;
  font-weight: 800;
  background: linear-gradient(135deg, #1a365d, #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.paydash__metric-label {
  display: block;
  font-size: 9px;
  font-weight: 600;
  color: #64748b;
  margin-top: 2px;
}

.paydash__feed {
  padding: 10px 16px 14px;
  background: #0f172a;
  min-height: 40px;
  display: flex;
  align-items: center;
}

.paydash__feed-line {
  margin: 0;
  font-size: 11px;
  color: #94a3b8;
  line-height: 1.4;
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
}

.paydash__feed-time {
  color: #06b6d4;
  font-weight: 600;
  margin-right: 8px;
}

.paydash__caption {
  margin: 12px 0 0;
  font-size: 13px;
  line-height: 1.5;
  color: #64748b;
  text-align: center;
  opacity: 0;
  transform: translateY(6px);
  transition:
    opacity 0.4s ease 0.25s,
    transform 0.4s ease 0.25s;
  min-height: 2.8em;
}

.paydash__caption--ready {
  opacity: 1;
  transform: translateY(0);
}

/* Transitions */
.paydash-slide-enter-active,
.paydash-slide-leave-active {
  transition:
    opacity 0.28s ease,
    transform 0.28s ease;
}

.paydash-slide-enter-from {
  opacity: 0;
  transform: translateX(12px);
}

.paydash-slide-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

.paydash-feed-enter-active,
.paydash-feed-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.paydash-feed-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.paydash-feed-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 420px) {
  .paydash__body {
    grid-template-columns: 1fr;
  }

  .paydash__pipeline {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 6px;
  }

  .paydash__pipeline::before {
    display: none;
  }

  .paydash__step {
    padding: 4px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .paydash__frame,
  .paydash__caption,
  .paydash__feat {
    opacity: 1;
    transform: none;
    transition: none;
    animation: none;
  }

  .paydash--ready .paydash__live-dot,
  .paydash__status--processing .paydash__status-dot,
  .paydash__bar-fill--go,
  .paydash__step--current .paydash__step-marker {
    animation: none;
  }
}
</style>
