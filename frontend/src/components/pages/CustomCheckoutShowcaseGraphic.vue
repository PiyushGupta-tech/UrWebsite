<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const ASSET = "/images/figma-custom-checkout/showcase";

/** Figma colors-row 283:8787 */
const THEME_COLORS = [
  { id: "blue", hex: "#0A54E9" },
  { id: "teal", hex: "#00D2C4" },
  { id: "purple", hex: "#8854D0" },
  { id: "pink", hex: "#FF4DFF" },
  { id: "orange", hex: "#FF9F43" },
  { id: "dark", hex: "#2C3E50" },
];

const STAGE = { w: 1291, h: 813 };

const activeIndex = ref(0);
const paused = ref(false);
let cycleTimer = null;
let reduceMotion = false;

const accent = computed(() => THEME_COLORS[activeIndex.value].hex);
const accentSoft = computed(() => `${accent.value}1A`);

const paymentMethods = [
  { id: "cards", rowId: "card", label: "Cards", icon: `${ASSET}/cards-icon.svg` },
  { id: "upi", rowId: "upi", label: "UPI", icon: `${ASSET}/upi-icon.svg`, tall: true },
  {
    id: "netbanking",
    rowId: "netbanking",
    label: "Net Banking",
    icon: `${ASSET}/building.svg`,
  },
  { id: "wallets", rowId: "wallet", label: "Wallets", icon: `${ASSET}/wallet.svg` },
  { id: "emi", rowId: "emi", label: "EMI", icon: `${ASSET}/calendar.svg` },
];

const checkoutMethods = [
  {
    id: "card",
    label: "Card",
    icon: `${ASSET}/credit-card.svg`,
    brands: "visa-mc",
  },
  {
    id: "upi",
    label: "UPI",
    icon: `${ASSET}/phone.svg`,
    brands: "upi",
  },
  {
    id: "netbanking",
    label: "Net Banking",
    icon: `${ASSET}/building.svg`,
    brands: "chevron",
  },
  {
    id: "wallet",
    label: "Wallet",
    icon: `${ASSET}/wallet.svg`,
    brands: "paytm",
  },
  {
    id: "emi",
    label: "EMI",
    icon: `${ASSET}/calendar.svg`,
    brands: "chevron",
  },
];

/** Checkout rows enabled by the Payment Methods toggles (all on by default). */
const enabledRows = ref({
  card: true,
  upi: true,
  netbanking: true,
  wallet: true,
  emi: true,
});

function isRowEnabled(rowId) {
  return !!enabledRows.value[rowId];
}

function toggleMethod(rowId) {
  enabledRows.value = {
    ...enabledRows.value,
    [rowId]: !enabledRows.value[rowId],
  };
}

/** Connector paths in stage space — shaped like Figma Line 614 / 618. */
const wires = [
  {
    id: "tl",
    d: "M340 254 C358 252, 376 238, 392 230 C400 226, 406 224, 414 224",
  },
  {
    id: "bl",
    d: "M340 523 C358 521, 376 507, 392 499 C400 495, 406 493, 414 493",
  },
  {
    id: "tr",
    d: "M964 327 C946 318, 920 300, 900 288 C890 282, 885 281, 880 281",
  },
  {
    id: "br",
    d: "M965 616 C947 607, 921 589, 901 577 C891 571, 886 570, 881 570",
  },
];

function selectColor(index) {
  activeIndex.value = index;
  restartCycle();
}

function nextColor() {
  activeIndex.value = (activeIndex.value + 1) % THEME_COLORS.length;
}

function restartCycle() {
  stopCycle();
  if (reduceMotion || paused.value) return;
  cycleTimer = window.setInterval(nextColor, 2200);
}

function stopCycle() {
  if (cycleTimer) {
    clearInterval(cycleTimer);
    cycleTimer = null;
  }
}

function onEnter() {
  paused.value = true;
  stopCycle();
}

function onLeave() {
  paused.value = false;
  restartCycle();
}

onMounted(() => {
  reduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  restartCycle();
});

onBeforeUnmount(stopCycle);
</script>

<template>
  <div
    class="cc-stage"
    :style="{
      '--cc-accent': accent,
      '--cc-accent-soft': accentSoft,
      aspectRatio: `${STAGE.w} / ${STAGE.h}`,
    }"
    @mouseenter="onEnter"
    @mouseleave="onLeave"
    @focusin="onEnter"
    @focusout="onLeave"
  >
    <!-- Brand card — top left -->
    <article class="cc-stage__card cc-stage__card--brand">
      <div class="cc-stage__card-icon">
        <img
          :src="`${ASSET}/briefcase.svg`"
          alt=""
          width="16"
          height="16"
          decoding="async"
        />
      </div>
      <div class="cc-stage__card-copy">
        <p class="cc-stage__card-title">Your Brand Name, Your Logo</p>
        <p class="cc-stage__card-sub">Smart Payments. Smarter Business</p>
      </div>
    </article>

    <!-- Design card — bottom left -->
    <article class="cc-stage__card cc-stage__card--design">
      <p class="cc-stage__design-title">Design Your Experience</p>
      <div class="cc-stage__swatches" role="listbox" aria-label="Theme colors">
        <button
          v-for="(color, index) in THEME_COLORS"
          :key="color.id"
          type="button"
          class="cc-stage__swatch"
          :class="{ 'cc-stage__swatch--active': index === activeIndex }"
          :style="{ '--swatch': color.hex }"
          :aria-selected="index === activeIndex"
          :aria-label="`Select ${color.id} theme`"
          role="option"
          @click="selectColor(index)"
        />
      </div>
      <div class="cc-stage__typo">
        <span class="cc-stage__typo-aa">Aa</span>
        <span class="cc-stage__typo-label">Typography</span>
        <img
          class="cc-stage__typo-chevron"
          :src="`${ASSET}/chevron-down.svg`"
          alt=""
          width="12"
          height="12"
          decoding="async"
        />
      </div>
    </article>

    <!-- Payment methods config — top right -->
    <article class="cc-stage__card cc-stage__card--methods">
      <p class="cc-stage__methods-title">Payment Methods</p>
      <ul class="cc-stage__toggles">
        <li v-for="method in paymentMethods" :key="method.id" class="cc-stage__toggle-row">
          <div class="cc-stage__toggle-left">
            <img
              class="cc-stage__toggle-icon"
              :class="{ 'cc-stage__toggle-icon--tall': method.tall }"
              :src="method.icon"
              alt=""
              width="16"
              :height="method.tall ? 23 : 16"
              decoding="async"
            />
            <span>{{ method.label }}</span>
          </div>
          <button
            type="button"
            class="cc-stage__toggle"
            :class="{ 'cc-stage__toggle--off': !isRowEnabled(method.rowId) }"
            :aria-pressed="isRowEnabled(method.rowId)"
            :aria-label="`${isRowEnabled(method.rowId) ? 'Disable' : 'Enable'} ${method.label}`"
            @click="toggleMethod(method.rowId)"
          >
            <span class="cc-stage__toggle-knob" />
          </button>
        </li>
      </ul>
    </article>

    <!-- Conversions card — bottom right -->
    <article class="cc-stage__card cc-stage__card--conv">
      <div class="cc-stage__card-icon">
        <img
          :src="`${ASSET}/shield-teal.svg`"
          alt=""
          width="16"
          height="16"
          decoding="async"
        />
      </div>
      <div class="cc-stage__card-copy">
        <p class="cc-stage__card-title cc-stage__card-title--sm">Better Experience</p>
        <p class="cc-stage__card-sub">Higher Conversions</p>
      </div>
    </article>

    <!-- Link badges -->
    <div class="cc-stage__badge cc-stage__badge--edit" aria-hidden="true">
      <img :src="`${ASSET}/edit.svg`" alt="" width="18" height="18" decoding="async" />
    </div>
    <div class="cc-stage__badge cc-stage__badge--trend" aria-hidden="true">
      <img :src="`${ASSET}/trending.svg`" alt="" width="18" height="18" decoding="async" />
    </div>
    <div class="cc-stage__badge cc-stage__badge--settings" aria-hidden="true">
      <img :src="`${ASSET}/settings.svg`" alt="" width="18" height="18" decoding="async" />
    </div>
    <div class="cc-stage__badge cc-stage__badge--users" aria-hidden="true">
      <img :src="`${ASSET}/users.svg`" alt="" width="18" height="18" decoding="async" />
    </div>

    <!-- Animated dotted connectors -->
    <svg
      class="cc-stage__wires"
      :viewBox="`0 0 ${STAGE.w} ${STAGE.h}`"
      preserveAspectRatio="xMidYMid meet"
      aria-hidden="true"
    >
      <path
        v-for="wire in wires"
        :key="wire.id"
        :d="wire.d"
        class="cc-stage__wire"
        fill="none"
        stroke="rgba(255,255,255,0.85)"
        stroke-width="2"
        stroke-linecap="round"
      />
      <circle cx="340" cy="254" r="4.5" fill="#fff" />
      <circle cx="340" cy="523" r="4.5" fill="#fff" />
      <circle cx="880" cy="281" r="4.5" fill="#fff" />
      <circle cx="881" cy="570" r="4.5" fill="#fff" />
      <circle
        cx="414"
        cy="224"
        r="4"
        fill="none"
        stroke="var(--cc-accent)"
        stroke-width="1.5"
      />
      <circle
        cx="414"
        cy="493"
        r="4"
        fill="none"
        stroke="var(--cc-accent)"
        stroke-width="1.5"
      />
      <circle
        cx="964"
        cy="327"
        r="4"
        fill="none"
        stroke="var(--cc-accent)"
        stroke-width="1.5"
      />
      <circle
        cx="965"
        cy="616"
        r="4"
        fill="none"
        stroke="var(--cc-accent)"
        stroke-width="1.5"
      />
    </svg>

    <!-- Browser checkout mockup -->
    <div class="cc-stage__browser">
      <div class="cc-stage__browser-chrome">
        <img
          class="cc-stage__browser-dots"
          :src="`${ASSET}/browser-dots.svg`"
          alt=""
          width="36"
          height="8"
          decoding="async"
        />
        <div class="cc-stage__address">
          <img :src="`${ASSET}/lock.svg`" alt="" width="12" height="12" decoding="async" />
          <span>yourbrand.com/checkout</span>
        </div>
        <span class="cc-stage__chrome-spacer" />
      </div>

      <div class="cc-stage__checkout">
        <div class="cc-stage__checkout-head">
          <div class="cc-stage__brand">
            <span class="cc-stage__brand-mark">M</span>
            <span class="cc-stage__brand-name">Your Brand</span>
          </div>
          <div class="cc-stage__secure">
            <img :src="`${ASSET}/shield.svg`" alt="" width="12" height="12" decoding="async" />
            <span>Secure Checkout</span>
          </div>
        </div>

        <div class="cc-stage__stepper">
          <div class="cc-stage__step cc-stage__step--done">
            <span class="cc-stage__step-num">
              <img :src="`${ASSET}/check.svg`" alt="" width="10" height="10" decoding="async" />
            </span>
            <span class="cc-stage__step-label">Cart</span>
          </div>
          <span class="cc-stage__step-line" />
          <div class="cc-stage__step cc-stage__step--active">
            <span class="cc-stage__step-num">2</span>
            <span class="cc-stage__step-label">Details</span>
          </div>
          <span class="cc-stage__step-line cc-stage__step-line--muted" />
          <div class="cc-stage__step cc-stage__step--pending">
            <span class="cc-stage__step-num">3</span>
            <span class="cc-stage__step-label">Payment</span>
          </div>
        </div>

        <div class="cc-stage__skeletons">
          <span class="cc-stage__skel cc-stage__skel--lg" />
          <span class="cc-stage__skel cc-stage__skel--sm" />
        </div>

        <div class="cc-stage__pay-section">
          <p class="cc-stage__pay-heading">Payment Methods</p>
          <div class="cc-stage__pay-table">
            <div
              v-for="row in checkoutMethods"
              :key="row.id"
              class="cc-stage__pay-row"
              :class="{ 'cc-stage__pay-row--disabled': !isRowEnabled(row.id) }"
              :aria-disabled="!isRowEnabled(row.id) ? 'true' : undefined"
            >
              <div class="cc-stage__pay-left">
                <span
                  class="cc-stage__mask-icon cc-stage__mask-icon--sm"
                  :style="{ WebkitMaskImage: `url(${row.icon})`, maskImage: `url(${row.icon})` }"
                />
                <span>{{ row.label }}</span>
              </div>
              <div class="cc-stage__pay-right">
                <template v-if="row.brands === 'visa-mc'">
                  <span class="cc-stage__visa">VISA</span>
                  <img
                    :src="`${ASSET}/mastercard.png`"
                    alt=""
                    width="19"
                    height="12"
                    decoding="async"
                  />
                </template>
                <template v-else-if="row.brands === 'upi'">
                  <img :src="`${ASSET}/gpay.png`" alt="" width="39" height="16" decoding="async" />
                  <img :src="`${ASSET}/phonepe.png`" alt="" width="19" height="18" decoding="async" />
                </template>
                <template v-else-if="row.brands === 'chevron'">
                  <img
                    :src="`${ASSET}/chevron-right.svg`"
                    alt=""
                    width="12"
                    height="12"
                    decoding="async"
                  />
                </template>
                <template v-else-if="row.brands === 'paytm'">
                  <img :src="`${ASSET}/paytm.png`" alt="" width="45" height="23" decoding="async" />
                </template>
              </div>
            </div>
          </div>
        </div>

        <button type="button" class="cc-stage__pay-btn" tabindex="-1">
          Pay Securely
        </button>

        <div class="cc-stage__trust">
          <img :src="`${ASSET}/lock-trust.svg`" alt="" width="14" height="14" decoding="async" />
          <span>100% Secure Payments</span>
        </div>
      </div>
    </div>

    <span class="visually-hidden">
      Interactive branded checkout preview. Theme color cycles through design swatches.
    </span>
  </div>
</template>

<style scoped>
.cc-stage {
  --cc-accent: #0a54e9;
  --cc-accent-soft: rgba(10, 84, 233, 0.1);
  position: relative;
  width: 100%;
  border-radius: 14.141px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
  user-select: none;
}

/* —— Floating cards —— */
.cc-stage__card {
  position: absolute;
  z-index: 3;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #eef2f6;
}

.cc-stage__card--brand {
  left: 2.52%;
  top: 27.43%;
  width: 22%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  filter: drop-shadow(0 8px 8px rgba(13, 23, 48, 0.02));
}

.cc-stage__card--design {
  left: 2.83%;
  top: 53.14%;
  width: 21.69%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px;
  border-radius: 16px;
  filter: drop-shadow(0 12px 12px rgba(13, 23, 48, 0.03));
}

.cc-stage__card--methods {
  left: 77.3%;
  top: 29.27%;
  width: 18.59%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  border-color: #e5e7eb;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.02)) drop-shadow(0 8px 12px rgba(0, 0, 0, 0.05));
}

.cc-stage__card--conv {
  left: 77.69%;
  top: 71.96%;
  width: 17.82%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  filter: drop-shadow(0 8px 8px rgba(13, 23, 48, 0.02));
}

.cc-stage__card-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 16px;
  background: rgba(16, 148, 185, 0.1);
}

.cc-stage__card-icon img {
  display: block;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.cc-stage__card-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cc-stage__card-title {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  line-height: normal;
  color: #252b37;
}

.cc-stage__card-title--sm {
  font-size: 14px;
}

.cc-stage__card-sub {
  margin: 0;
  font-size: 10px;
  font-weight: 500;
  line-height: normal;
  color: #252b37;
}

.cc-stage__design-title {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  line-height: normal;
  color: #252b37;
}

.cc-stage__swatches {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 28px;
}

.cc-stage__swatch {
  position: relative;
  width: 18px;
  height: 18px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: var(--swatch);
  cursor: pointer;
  transition:
    transform 0.35s ease,
    box-shadow 0.35s ease;
}

.cc-stage__swatch::after {
  content: "";
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  border: 1.5px solid transparent;
  transition: border-color 0.35s ease, transform 0.35s ease;
}

.cc-stage__swatch--active {
  transform: scale(1.05);
}

.cc-stage__swatch--active::after {
  border-color: var(--swatch);
}

.cc-stage__swatch:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 3px;
}

.cc-stage__typo {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 14px;
  box-sizing: border-box;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fafbfd;
}

.cc-stage__typo-aa {
  font-size: 14px;
  font-weight: 700;
  color: #252b37;
}

.cc-stage__typo-label {
  margin-left: 8px;
  margin-right: auto;
  font-size: 13px;
  font-weight: 500;
  color: #535862;
}

.cc-stage__typo-chevron {
  display: block;
  width: 12px;
  height: 12px;
}

.cc-stage__methods-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  text-align: center;
  color: #1a1a2e;
}

.cc-stage__toggles {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
}

.cc-stage__toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.cc-stage__toggle-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 600;
  color: #252b37;
  white-space: nowrap;
}

.cc-stage__toggle-icon {
  display: block;
  width: 16px;
  height: 16px;
  object-fit: contain;
  flex-shrink: 0;
}

.cc-stage__toggle-icon--tall {
  height: 23px;
}

.cc-stage__toggle {
  position: relative;
  flex-shrink: 0;
  width: 36px;
  height: 20px;
  padding: 0;
  border: none;
  border-radius: 10px;
  background: #097495;
  cursor: pointer;
  transition: background 0.25s ease;
}

.cc-stage__toggle:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}

.cc-stage__toggle--off {
  background: #cbd5e1;
}

.cc-stage__toggle-knob {
  position: absolute;
  top: 2px;
  left: 18px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
  transition: left 0.25s ease;
}

.cc-stage__toggle--off .cc-stage__toggle-knob {
  left: 2px;
}

/* —— Masked icons (themeable) —— */
.cc-stage__mask-icon {
  display: block;
  width: 16px;
  height: 16px;
  background: var(--cc-accent);
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
  mask-mode: alpha;
  -webkit-mask-mode: alpha;
  transition: background 0.45s ease;
}

.cc-stage__mask-icon--sm {
  width: 16px;
  height: 16px;
}

.cc-stage__mask-icon--tall {
  height: 23px;
}

/* —— Link badges —— */
.cc-stage__badge {
  position: absolute;
  z-index: 4;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background: #1094b9;
  filter: drop-shadow(0 4px 4px rgba(0, 0, 0, 0.1));
}

.cc-stage__badge img {
  display: block;
  width: 18px;
  height: 18px;
  filter: brightness(0) invert(1);
}

.cc-stage__badge--edit {
  left: 23.39%;
  top: 29.27%;
}

.cc-stage__badge--trend {
  left: 23.39%;
  top: 61.99%;
}

.cc-stage__badge--settings {
  left: 75.13%;
  top: 38.25%;
}

.cc-stage__badge--users {
  left: 75.13%;
  top: 74.05%;
}

/* —— Wires —— */
.cc-stage__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

.cc-stage__wire {
  stroke-dasharray: 5 6;
  animation: cc-wire-march 0.9s linear infinite;
}

@keyframes cc-wire-march {
  to {
    stroke-dashoffset: -22;
  }
}

/* —— Browser —— */
.cc-stage__browser {
  position: absolute;
  z-index: 5;
  left: 50%;
  top: 50%;
  width: 38.73%;
  max-width: 500px;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  background: #ffffff;
  box-shadow: 0 16px 40px rgba(13, 23, 48, 0.06);
}

.cc-stage__browser-chrome {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #eef2f6;
}

.cc-stage__browser-dots {
  display: block;
  width: 36px;
  height: 8px;
  flex-shrink: 0;
}

.cc-stage__address {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: min(240px, 100%);
  padding: 4px 14px;
  border: 1px solid #eef2f6;
  border-radius: 6px;
  background: #ffffff;
  font-size: 11px;
  font-weight: 500;
  color: #5e6a82;
  white-space: nowrap;
}

.cc-stage__address img {
  width: 12px;
  height: 12px;
}

.cc-stage__chrome-spacer {
  width: 32px;
  flex-shrink: 0;
}

.cc-stage__checkout {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px 24px 18px;
}

.cc-stage__checkout-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.cc-stage__brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cc-stage__brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #0d1730;
  color: #ffffff;
  font-size: 14px;
  font-weight: 800;
}

.cc-stage__brand-name {
  font-size: 14px;
  font-weight: 700;
  color: #252b37;
}

.cc-stage__secure {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
}

.cc-stage__secure img {
  width: 12px;
  height: 12px;
}

.cc-stage__stepper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.cc-stage__step {
  display: flex;
  align-items: center;
  gap: 6px;
}

.cc-stage__step-num {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  transition: background 0.45s ease, color 0.45s ease, border-color 0.45s ease;
}

.cc-stage__step-label {
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  transition: color 0.45s ease;
}

.cc-stage__step--done .cc-stage__step-num,
.cc-stage__step--active .cc-stage__step-num {
  background: var(--cc-accent);
  color: #ffffff;
}

.cc-stage__step--done .cc-stage__step-label,
.cc-stage__step--active .cc-stage__step-label {
  color: var(--cc-accent);
}

.cc-stage__step--pending .cc-stage__step-num {
  background: #eef2f6;
  border: 1px solid #e2e8f0;
  color: #94a3b8;
}

.cc-stage__step--pending .cc-stage__step-label {
  font-weight: 600;
  color: #94a3b8;
}

.cc-stage__step-line {
  width: 40px;
  height: 0;
  border-top: 1px solid var(--cc-accent);
  opacity: 0.55;
  transition: border-color 0.45s ease;
}

.cc-stage__step-line--muted {
  border-top-color: #e2e8f0;
  opacity: 1;
}

.cc-stage__skeletons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cc-stage__skel {
  display: block;
  border-radius: 6px;
  background: #eef2f6;
}

.cc-stage__skel--lg {
  width: 68.8%;
  height: 10px;
}

.cc-stage__skel--sm {
  width: 41.3%;
  height: 8px;
  opacity: 0.6;
  border-radius: 5px;
}

.cc-stage__pay-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cc-stage__pay-heading {
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  color: #0d1730;
}

.cc-stage__pay-table {
  overflow: hidden;
  border: 1px solid #eef2f6;
  border-radius: 12px;
}

.cc-stage__pay-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 44px;
  min-height: 44px;
  max-height: 44px;
  padding: 0 14px;
  box-sizing: border-box;
  border-bottom: 1px solid #eef2f6;
  transition:
    opacity 0.25s ease,
    filter 0.25s ease,
    background 0.25s ease;
}

.cc-stage__pay-row:last-child {
  border-bottom: none;
}

.cc-stage__pay-row--disabled {
  opacity: 0.45;
  filter: grayscale(1);
  background: #f8fafc;
  pointer-events: none;
}

.cc-stage__pay-row--disabled .cc-stage__mask-icon {
  background: #94a3b8;
}

.cc-stage__pay-row--disabled .cc-stage__pay-left {
  color: #94a3b8;
}

.cc-stage__pay-row--disabled .cc-stage__visa {
  color: #94a3b8;
}

.cc-stage__pay-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
}

.cc-stage__pay-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  height: 18px;
  min-width: 0;
}

.cc-stage__visa {
  font-size: 11px;
  font-weight: 800;
  color: #1434cb;
  line-height: 1;
}

.cc-stage__pay-right img {
  display: block;
  max-height: 16px;
  width: auto;
  object-fit: contain;
}

.cc-stage__pay-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: var(--cc-accent);
  color: #ffffff;
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: default;
  transition: background 0.45s ease, transform 0.35s ease;
}

.cc-stage__trust {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
}

.cc-stage__trust img {
  width: 14px;
  height: 14px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (prefers-reduced-motion: reduce) {
  .cc-stage__wire {
    animation: none;
  }

  .cc-stage__mask-icon,
  .cc-stage__pay-btn,
  .cc-stage__step-num,
  .cc-stage__step-label,
  .cc-stage__step-line,
  .cc-stage__swatch,
  .cc-stage__swatch::after {
    transition: none;
  }
}

@media (max-width: 900px) {
  .cc-stage__card--brand,
  .cc-stage__card--design,
  .cc-stage__card--methods,
  .cc-stage__card--conv,
  .cc-stage__badge,
  .cc-stage__wires {
    display: none;
  }

  .cc-stage__browser {
    width: min(500px, 92%);
  }

  .cc-stage {
    min-height: 560px;
    aspect-ratio: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 16px;
  }

  .cc-stage__browser {
    position: relative;
    left: auto;
    top: auto;
    transform: none;
  }
}
</style>
