<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import BrandLogo from "./BrandLogo.vue";

const emit = defineEmits(["method-change"]);

const props = defineProps({
  checkout: { type: Object, required: true },
  tilted: { type: Boolean, default: false },
  autoRotate: { type: Boolean, default: undefined },
  /** Show “your logo” placeholder instead of Urbanrupee mark */
  logoPlaceholder: { type: Boolean, default: false },
  /** Cycle accent/background colors with a slow breathing animation */
  themeBreathe: { type: Boolean, default: false },
});

const ROTATE_MS = props.checkout.rotate_interval_ms || 5000;

const methods = computed(() => {
  const raw = props.checkout.payment_methods;
  if (raw.length && typeof raw[0] === "object") return raw;
  return raw.map((label) => ({
    id: label.toLowerCase().replace(/\s+/g, ""),
    label,
    icon: "card",
  }));
});

const shouldAutoRotate = computed(
  () => props.autoRotate ?? !props.tilted,
);

const activeMethod = ref(methods.value[0]?.id || "upi");
const saveCard = ref(true);
const cardNumber = ref("");
const expiry = ref("");
const cvv = ref("");
const cardholder = ref("");
const cardType = ref("debit");
const upiId = ref("");

const timerSeconds = ref(14 * 60 + 19);
let timerHandle = null;
let rotateTimer = null;
let resumeTimer = null;
let userPaused = false;

const payLabel = computed(() => `Pay ${props.checkout.amount}`);

const activeMethodLabel = computed(
  () => methods.value.find((m) => m.id === activeMethod.value)?.label || "method",
);

function nextMethodId(currentId) {
  const ids = methods.value.map((m) => m.id);
  if (!ids.length) return currentId;
  return ids[(ids.indexOf(currentId) + 1) % ids.length];
}

function setMethod(id, { manual = false } = {}) {
  if (!methods.value.some((m) => m.id === id) || id === activeMethod.value) return;
  activeMethod.value = id;
  if (manual) scheduleRotation();
}

watch(
  activeMethod,
  (id) => emit("method-change", id),
  { immediate: true },
);

function scheduleRotation() {
  clearInterval(rotateTimer);
  if (!shouldAutoRotate.value || userPaused || methods.value.length < 2) return;
  rotateTimer = window.setInterval(() => {
    if (userPaused) return;
    setMethod(nextMethodId(activeMethod.value));
  }, ROTATE_MS);
}

function selectMethod(id) {
  setMethod(id, { manual: true });
}

function onPointerEnter() {
  if (!shouldAutoRotate.value) return;
  userPaused = true;
  clearInterval(rotateTimer);
}

function onPointerLeave() {
  if (!shouldAutoRotate.value) return;
  userPaused = false;
  clearTimeout(resumeTimer);
  resumeTimer = window.setTimeout(scheduleRotation, 400);
}

onMounted(() => {
  timerHandle = window.setInterval(() => {
    if (timerSeconds.value > 0) timerSeconds.value -= 1;
  }, 1000);

  if (
    shouldAutoRotate.value &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    scheduleRotation();
  }
});

onUnmounted(() => {
  if (timerHandle) window.clearInterval(timerHandle);
  clearInterval(rotateTimer);
  clearTimeout(resumeTimer);
});

const timerDisplay = computed(() => {
  const m = Math.floor(timerSeconds.value / 60);
  const s = timerSeconds.value % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
});
</script>

<template>
  <article
    class="checkout"
    :class="{
      'checkout--tilted': tilted,
      'checkout--theme-breathe': themeBreathe,
    }"
    role="region"
    aria-label="Secure checkout preview"
    @pointerenter="onPointerEnter"
    @pointerleave="onPointerLeave"
  >
    <div v-if="themeBreathe" class="checkout__mesh" aria-hidden="true">
      <span class="checkout__orb checkout__orb--cyan" />
      <span class="checkout__orb checkout__orb--violet" />
      <span class="checkout__orb checkout__orb--pink" />
      <span class="checkout__orb checkout__orb--amber" />
      <span class="checkout__orb checkout__orb--blue" />
    </div>
    <!-- Header -->
    <header class="checkout__top">
      <div class="checkout__brand">
        <span
          v-if="logoPlaceholder"
          class="checkout__logo-placeholder"
        >your logo</span>
        <BrandLogo
          v-else
          variant="on-dark"
          alt="Urbanrupee"
          class="checkout__brand-logo"
        />
        <span class="checkout__secure">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" />
          </svg>
          Secure checkout
        </span>
      </div>
      <div class="checkout__timer" aria-label="Session timer">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <circle cx="12" cy="12" r="9" />
          <path d="M12 7v5l3 2" />
        </svg>
        {{ timerDisplay }}
      </div>
    </header>

    <!-- Amount summary strip -->
    <div class="checkout__summary">
      <p class="checkout__summary-amount">{{ checkout.amount }}</p>
      <p class="checkout__summary-note">{{ checkout.payment_note || "Secure payment" }}</p>
      <dl class="checkout__meta">
        <div>
          <dt>Order ID</dt>
          <dd>{{ checkout.order_id || checkout.invoice_no }}</dd>
        </div>
        <div>
          <dt>Merchant</dt>
          <dd>{{ checkout.merchant_id || "UR72" }}</dd>
        </div>
      </dl>
    </div>

    <!-- Payment tabs -->
    <div class="checkout__tabs" role="tablist" aria-label="Payment method">
      <button
        v-for="method in methods"
        :key="method.id"
        type="button"
        role="tab"
        class="checkout__tab"
        :class="{ 'checkout__tab--active': activeMethod === method.id }"
        :aria-selected="activeMethod === method.id"
        @click="selectMethod(method.id)"
      >
        <span class="checkout__tab-icon" :data-icon="method.icon" aria-hidden="true" />
        <span>{{ method.label }}</span>
      </button>
    </div>

    <div class="checkout__panel-host" aria-live="polite">
      <Transition name="checkout-panel" mode="out-in">
        <div v-if="activeMethod === 'upi'" key="upi" class="checkout__panel">
      <label class="checkout__field">
        <span>UPI ID</span>
        <input v-model="upiId" type="text" placeholder="yourname@upi" autocomplete="off" />
      </label>
      <p class="checkout__hint">Pay instantly with any UPI app</p>
        </div>

        <div
          v-else-if="activeMethod === 'cards' || activeMethod === 'card'"
          key="cards"
          class="checkout__panel"
        >
      <label class="checkout__field checkout__field--card">
        <span>Card number</span>
        <input
          v-model="cardNumber"
          type="text"
          inputmode="numeric"
          placeholder="0000 0000 0000 0000"
          maxlength="19"
        />
        <span class="checkout__visa" aria-hidden="true">VISA</span>
      </label>
      <div class="checkout__row-2">
        <label class="checkout__field">
          <span>Expiry</span>
          <input v-model="expiry" type="text" placeholder="MM / YY" maxlength="7" />
        </label>
        <label class="checkout__field">
          <span>CVV</span>
          <input v-model="cvv" type="password" placeholder="•••" maxlength="4" />
        </label>
      </div>
      <label class="checkout__field">
        <span>Cardholder name</span>
        <input v-model="cardholder" type="text" placeholder="Name on card" />
      </label>
      <label class="checkout__field">
        <span>Card type</span>
        <select v-model="cardType">
          <option value="debit">Debit (DC)</option>
          <option value="credit">Credit (CC)</option>
        </select>
      </label>
      <div class="checkout__save">
        <button
          type="button"
          class="checkout__toggle"
          :class="{ 'checkout__toggle--on': saveCard }"
          role="switch"
          :aria-checked="saveCard"
          @click="saveCard = !saveCard"
        >
          <span class="checkout__toggle-knob" />
        </button>
        <div>
          <strong>Save card</strong>
          <span>Faster checkout next time</span>
        </div>
        <span class="checkout__token">Tokenized</span>
      </div>
        </div>

        <div
          v-else
          :key="activeMethod"
          class="checkout__panel checkout__panel--placeholder"
        >
          <p class="checkout__hint">
            Select your {{ activeMethodLabel }} provider to complete payment securely.
          </p>
          <div class="checkout__chips-row">
            <button
              v-for="n in 4"
              :key="n"
              type="button"
              class="checkout__bank-chip"
            >
              {{
                activeMethod === "wallets"
                  ? "Wallet"
                  : activeMethod === "emi"
                    ? "EMI"
                    : "Bank"
              }}
              {{ n }}
            </button>
          </div>
        </div>
      </Transition>
    </div>

    <!-- Pay CTA -->
    <button type="button" class="checkout__pay">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" />
      </svg>
      {{ payLabel }}
    </button>

    <!-- Footer -->
    <footer class="checkout__footer">
      <span>PCI-DSS</span>
      <span>SSL Secure</span>
      <span>RBI Safe</span>
      <span class="checkout__powered">Powered by Urbanrupee</span>
    </footer>

    <div v-if="!themeBreathe" class="checkout__glow" aria-hidden="true" />
  </article>
</template>

<style scoped>
.checkout {
  --checkout-bg: #0b1220;
  --checkout-surface: #111b2e;
  --checkout-border: rgba(255, 255, 255, 0.08);
  --checkout-text: #e8eef7;
  --checkout-muted: #8b9cb3;
  --checkout-cyan: #06b6d4;
  --checkout-cyan-dim: rgba(6, 182, 212, 0.15);

  position: relative;
  width: min(100%, 400px);
  padding: 20px;
  border-radius: 16px;
  background: var(--checkout-bg);
  border: 1px solid var(--checkout-border);
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.35),
    0 0 0 1px rgba(6, 182, 212, 0.08);
  color: var(--checkout-text);
  overflow: hidden;
}

.checkout--tilted {
  transform: rotate(-3deg);
  box-shadow:
    0 28px 56px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(6, 182, 212, 0.12);
}

.checkout__glow {
  position: absolute;
  bottom: -40%;
  right: -30%;
  width: 70%;
  height: 70%;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.25), transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* Subtle ambient color drift behind checkout */
.checkout--theme-breathe {
  --checkout-bg: #0b1220;
  --checkout-surface: rgba(17, 27, 46, 0.85);
  --checkout-border: rgba(255, 255, 255, 0.08);
  border: 1px solid transparent;
  background-image:
    linear-gradient(rgba(11, 18, 32, 0.94), rgba(11, 18, 32, 0.94)),
    linear-gradient(
      90deg,
      rgba(6, 182, 212, 0.45),
      rgba(129, 140, 248, 0.35),
      rgba(167, 139, 250, 0.3),
      rgba(6, 182, 212, 0.45)
    );
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    280% 100%;
  animation: checkout-border-flow 14s linear infinite;
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.38),
    0 0 24px rgba(6, 182, 212, 0.06);
}

@keyframes checkout-border-flow {
  0% {
    background-position:
      0 0,
      0% 50%;
  }

  100% {
    background-position:
      0 0,
      200% 50%;
  }
}

.checkout__mesh {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.checkout__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(52px);
  opacity: 0.28;
  mix-blend-mode: screen;
  will-change: transform;
}

.checkout__orb--cyan {
  width: 52%;
  height: 44%;
  background: #06b6d4;
  top: -14%;
  left: -18%;
  animation: checkout-orb-a 16s ease-in-out infinite;
}

.checkout__orb--violet {
  width: 48%;
  height: 46%;
  background: #818cf8;
  top: 30%;
  right: -22%;
  animation: checkout-orb-b 18s ease-in-out infinite;
}

.checkout__orb--pink {
  width: 42%;
  height: 38%;
  background: #a78bfa;
  bottom: -6%;
  left: 12%;
  animation: checkout-orb-c 17s ease-in-out infinite;
}

.checkout__orb--amber {
  width: 34%;
  height: 32%;
  background: #22d3ee;
  top: 12%;
  right: 20%;
  animation: checkout-orb-d 20s ease-in-out infinite;
  opacity: 0.2;
}

.checkout__orb--blue {
  width: 38%;
  height: 36%;
  background: #6366f1;
  bottom: 24%;
  right: -6%;
  animation: checkout-orb-e 19s ease-in-out infinite;
  opacity: 0.22;
}

@keyframes checkout-orb-a {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(12%, 10%);
  }
}

@keyframes checkout-orb-b {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(-14%, 8%);
  }
}

@keyframes checkout-orb-c {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(10%, -12%);
  }
}

@keyframes checkout-orb-d {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(-10%, 12%);
  }
}

@keyframes checkout-orb-e {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(-12%, -8%);
  }
}

@keyframes checkout-gradient-flow {
  0% {
    background-position: 0% 50%;
  }

  100% {
    background-position: 200% 50%;
  }
}

.checkout__top,
.checkout__summary,
.checkout__tabs,
.checkout__panel,
.checkout__pay,
.checkout__footer {
  position: relative;
  z-index: 1;
}

.checkout__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.checkout__brand {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.checkout__brand-logo :deep(.brand-logo--on-dark) {
  height: 22px;
  max-width: 140px;
}

.checkout__logo-placeholder {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.03em;
  color: rgba(255, 255, 255, 0.72);
  padding: 6px 14px;
  border: 1.5px dashed rgba(255, 255, 255, 0.22);
  border-radius: 8px;
  line-height: 1.2;
  white-space: nowrap;
}

.checkout--theme-breathe .checkout__logo-placeholder {
  border: 1.5px dashed rgba(6, 182, 212, 0.28);
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.55);
  animation: none;
  box-shadow: none;
}

.checkout__secure {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #4ade80;
  background: rgba(74, 222, 128, 0.12);
  padding: 4px 8px;
  border-radius: var(--radius-pill);
}

.checkout--theme-breathe .checkout__secure {
  box-shadow: none;
}

.checkout__timer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--checkout-cyan);
  background: var(--checkout-cyan-dim);
  padding: 6px 10px;
  border-radius: 8px;
  flex-shrink: 0;
}

.checkout--theme-breathe .checkout__timer {
  color: var(--checkout-cyan);
  background: var(--checkout-cyan-dim);
  animation: none;
  box-shadow: none;
}

.checkout__summary {
  margin-bottom: 16px;
  padding: 14px;
  background: var(--checkout-surface);
  border: 1px solid var(--checkout-border);
  border-radius: 12px;
}

.checkout--theme-breathe .checkout__summary {
  backdrop-filter: blur(6px);
  border-color: rgba(6, 182, 212, 0.12);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.checkout__summary-amount {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.checkout__summary-note {
  margin: 2px 0 12px;
  font-size: 12px;
  color: var(--checkout-muted);
}

.checkout__meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin: 0;
  font-size: 11px;
}

.checkout__meta dt {
  color: var(--checkout-muted);
  margin-bottom: 2px;
}

.checkout__meta dd {
  margin: 0;
  font-weight: 600;
  word-break: break-all;
}

.checkout__tabs {
  display: flex;
  gap: 2px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--checkout-border);
  overflow-x: auto;
  scrollbar-width: none;
}

.checkout__tabs::-webkit-scrollbar {
  display: none;
}

.checkout__tab {
  position: relative;
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 6px;
  border: none;
  background: transparent;
  color: var(--checkout-muted);
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition:
    color 0.25s ease,
    border-color 0.25s ease,
    transform 0.2s ease;
}

.checkout__tab--active {
  color: var(--checkout-cyan);
  border-bottom-color: var(--checkout-cyan);
  transform: translateY(-1px);
}

.checkout--theme-breathe .checkout__tab--active {
  color: var(--checkout-cyan);
  border-bottom-color: var(--checkout-cyan);
}

.checkout--theme-breathe .checkout__tab--active::after {
  display: none;
}

.checkout--theme-breathe .checkout__tab--active .checkout__tab-icon {
  background: var(--checkout-cyan);
  box-shadow: none;
}

.checkout__panel-host {
  min-height: 220px;
  margin-bottom: 16px;
}

.checkout-panel-enter-active,
.checkout-panel-leave-active {
  transition:
    opacity 0.32s ease,
    transform 0.32s ease;
}

.checkout-panel-enter-from {
  opacity: 0;
  transform: translateX(14px);
}

.checkout-panel-leave-to {
  opacity: 0;
  transform: translateX(-14px);
}

@media (prefers-reduced-motion: reduce) {
  .checkout--theme-breathe {
    animation: none;
    background-image: linear-gradient(rgba(8, 13, 22, 0.92), rgba(8, 13, 22, 0.92));
    border-color: rgba(34, 211, 238, 0.35);
  }

  .checkout--theme-breathe .checkout__orb,
  .checkout--theme-breathe .checkout__logo-placeholder,
  .checkout--theme-breathe .checkout__timer,
  .checkout--theme-breathe .checkout__tab--active::after,
  .checkout--theme-breathe .checkout__pay {
    animation: none;
  }

  .checkout-panel-enter-active,
  .checkout-panel-leave-active {
    transition: opacity 0.15s ease;
  }

  .checkout-panel-enter-from,
  .checkout-panel-leave-to {
    transform: none;
  }

  .checkout__tab--active {
    transform: none;
  }
}

.checkout__tab-icon {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  background: currentColor;
  opacity: 0.35;
}

.checkout__tab--active .checkout__tab-icon {
  opacity: 1;
  background: var(--checkout-cyan);
}

.checkout__panel {
  margin-bottom: 16px;
}

.checkout__field {
  display: block;
  margin-bottom: 12px;
}

.checkout__field span {
  display: block;
  font-size: 11px;
  color: var(--checkout-muted);
  margin-bottom: 6px;
}

.checkout__field input,
.checkout__field select {
  width: 100%;
  padding: 11px 12px;
  font-size: 13px;
  font-family: inherit;
  color: var(--checkout-text);
  background: var(--checkout-surface);
  border: 1px solid var(--checkout-border);
  border-radius: 10px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.checkout__field input:focus,
.checkout__field select:focus {
  border-color: var(--checkout-cyan);
  box-shadow: 0 0 0 3px var(--checkout-cyan-dim);
}

.checkout--theme-breathe .checkout__field input,
.checkout--theme-breathe .checkout__field select {
  backdrop-filter: blur(6px);
}

.checkout--theme-breathe .checkout__field input:focus,
.checkout--theme-breathe .checkout__field select:focus {
  border-color: var(--checkout-cyan);
  box-shadow: 0 0 0 3px var(--checkout-cyan-dim);
}

.checkout__field--card {
  position: relative;
}

.checkout__field--card input {
  padding-right: 52px;
}

.checkout__visa {
  position: absolute;
  right: 12px;
  bottom: 11px;
  font-size: 10px;
  font-weight: 800;
  color: var(--checkout-muted);
  letter-spacing: 0.05em;
}

.checkout__row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.checkout__save {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 4px;
}

.checkout__save strong {
  display: block;
  font-size: 12px;
}

.checkout__save span {
  font-size: 11px;
  color: var(--checkout-muted);
}

.checkout__toggle {
  width: 40px;
  height: 22px;
  border: none;
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.15);
  padding: 2px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s;
}

.checkout__toggle--on {
  background: var(--checkout-cyan);
}

.checkout__toggle-knob {
  display: block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  transition: transform 0.2s;
}

.checkout__toggle--on .checkout__toggle-knob {
  transform: translateX(18px);
}

.checkout__token {
  margin-left: auto;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--checkout-muted);
  padding: 4px 8px;
  border: 1px solid var(--checkout-border);
  border-radius: 6px;
}

.checkout__hint {
  margin: 0 0 12px;
  font-size: 12px;
  color: var(--checkout-muted);
}

.checkout__chips-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.checkout__bank-chip {
  padding: 10px;
  font-size: 12px;
  font-weight: 600;
  color: var(--checkout-text);
  background: var(--checkout-surface);
  border: 1px solid var(--checkout-border);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.15s;
}

.checkout__bank-chip:hover {
  border-color: var(--checkout-cyan);
}

.checkout__pay {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  font-size: 15px;
  font-weight: 700;
  font-family: inherit;
  color: #0b1220;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  background: linear-gradient(135deg, #22d3ee, var(--checkout-cyan));
  box-shadow:
    0 0 20px rgba(6, 182, 212, 0.5),
    0 4px 16px rgba(6, 182, 212, 0.35);
  transition: transform 0.15s, box-shadow 0.15s;
}

.checkout--theme-breathe .checkout__pay {
  background: linear-gradient(135deg, #22d3ee, #06b6d4);
  animation: none;
  box-shadow:
    0 0 14px rgba(6, 182, 212, 0.28),
    0 4px 14px rgba(6, 182, 212, 0.2);
}

.checkout__pay:hover {
  transform: translateY(-1px);
  box-shadow:
    0 0 28px rgba(6, 182, 212, 0.65),
    0 6px 20px rgba(6, 182, 212, 0.4);
}

.checkout--theme-breathe .checkout__pay:hover {
  box-shadow:
    0 0 20px rgba(6, 182, 212, 0.38),
    0 6px 18px rgba(6, 182, 212, 0.28);
}

.checkout__footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px 14px;
  margin-top: 14px;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--checkout-muted);
}

.checkout__powered {
  margin-left: auto;
  text-transform: none;
  letter-spacing: 0;
  font-weight: 500;
}
</style>
