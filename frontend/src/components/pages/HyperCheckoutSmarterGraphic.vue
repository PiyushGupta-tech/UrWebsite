<script setup>
import { nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: { type: String, default: "Mobile Hyper Checkout with payment method logos" },
});

/**
 * Figma 744:8011 / 744:8012 — Smarter Checkout phone storyboard
 * Loop: cursor → UPI → Pay → Processing morph → Success → reset
 * Drawn at 2× then scaled to fit the 471×621 visual slot.
 */
const ASSET = "/images/figma-hyper-checkout/smarter";
const ART_W = 942; // 471 × 2
const ART_H = 1242; // 621 × 2

const METHODS = [
  {
    id: "upi",
    title: "UPI",
    sub: "Pay with any UPI app",
    icon: "icon-upi.svg",
    selected: true,
  },
  {
    id: "cards",
    title: "Cards",
    sub: "Credit & Debit cards",
    icon: "icon-card.svg",
  },
  {
    id: "net",
    title: "Net Banking",
    sub: "All major banks",
    icon: "icon-bank.svg",
  },
  {
    id: "wallets",
    title: "Wallets",
    sub: "Paytm, PhonePe, Amazon Pay",
    icon: "icon-wallet.svg",
  },
  {
    id: "emi",
    title: "EMI",
    sub: "No cost EMI available",
    icon: "icon-emi.svg",
  },
];

const LOGOS = [
  { id: "upi", rot: -14, top: 145, left: 101 },
  { id: "visa", rot: -10, top: 290, left: 34 },
  { id: "mc", rot: -6, top: 436, left: 0 },
  { id: "paytm", rot: -2, top: 581, left: 8 },
  { id: "phonepe", rot: 2, top: 721, left: 47 },
  { id: "gpay", rot: 7, top: 847, left: 104 },
  { id: "more", rot: 11, top: 964, left: 189 },
];

const reduceMotion = ref(false);
const screen = ref("checkout"); // checkout | success
const buttonPhase = ref("pay"); // pay | circle | arrow | processing
const upiPulse = ref(false);
const clicking = ref(false);
const cursor = reactive({ x: 800, y: 464 });

const rootRef = ref(null);
const stageRef = ref(null);
const upiRef = ref(null);
const payRef = ref(null);
const scale = ref(0.5);
const offsetX = ref(0);
const offsetY = ref(0);

let timers = [];
let loopTimer = null;
let resizeObserver = null;

function clearTimers() {
  timers.forEach((id) => clearTimeout(id));
  timers = [];
  if (loopTimer) {
    clearTimeout(loopTimer);
    loopTimer = null;
  }
}

function wait(ms) {
  return new Promise((resolve) => {
    timers.push(setTimeout(resolve, ms));
  });
}

function setUpiRef(el) {
  upiRef.value = el || null;
}

function aimAt(el) {
  const stage = stageRef.value;
  if (!stage || !el) return;
  const s = stage.getBoundingClientRect();
  const r = el.getBoundingClientRect();
  const sc = scale.value || 1;
  cursor.x = (r.left + r.width / 2 - s.left) / sc;
  cursor.y = (r.top + r.height / 2 - s.top) / sc;
}

async function clickEl(el, holdMs = 160) {
  if (!el) return;
  aimAt(el);
  await wait(380);
  clicking.value = true;
  await wait(holdMs);
  clicking.value = false;
  await wait(100);
}

function updateScale() {
  const root = rootRef.value;
  if (!root) return;
  const sx = root.clientWidth / ART_W;
  const sy = root.clientHeight / ART_H;
  const next = Math.min(sx, sy);
  scale.value = next;
  offsetX.value = (root.clientWidth - ART_W * next) / 2;
  offsetY.value = (root.clientHeight - ART_H * next) / 2;
}

function resetState() {
  screen.value = "checkout";
  buttonPhase.value = "pay";
  upiPulse.value = false;
  clicking.value = false;
}

async function runSequence() {
  if (reduceMotion.value) return;
  clearTimers();
  resetState();
  await nextTick();

  // Start near UPI
  aimAt(upiRef.value);
  await wait(500);

  // Click UPI
  await clickEl(upiRef.value, 180);
  upiPulse.value = true;
  await wait(350);
  upiPulse.value = false;
  await wait(250);

  // Move to Pay → click
  await clickEl(payRef.value, 180);
  await wait(120);

  // Button morph → Figma Processing Button Animation (777:2575)
  buttonPhase.value = "circle";
  await wait(280);
  buttonPhase.value = "arrow";
  await wait(320);
  buttonPhase.value = "processing";
  // Figma 5s timeline: expand+text through ~0.84 → success before collapse
  await wait(4200);

  // Success
  screen.value = "success";
  await wait(2400);

  resetState();
  await wait(400);
  loopTimer = setTimeout(() => runSequence(), 120);
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  nextTick(() => {
    updateScale();
    if (typeof ResizeObserver !== "undefined" && rootRef.value) {
      resizeObserver = new ResizeObserver(updateScale);
      resizeObserver.observe(rootRef.value);
    }
    if (!reduceMotion.value) runSequence();
  });
});

onBeforeUnmount(() => {
  clearTimers();
  resizeObserver?.disconnect();
});
</script>

<template>
  <div
    ref="rootRef"
    class="hc-smart"
    :class="{ 'hc-smart--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div
      ref="stageRef"
      class="hc-smart__artboard"
      aria-hidden="true"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
      }"
    >
      <!-- Floating logos + arc -->
      <div class="hc-smart__logos">
        <img
          class="hc-smart__arc"
          :src="`${ASSET}/circle-x.svg`"
          alt=""
          width="402"
          height="1006"
          draggable="false"
        />
        <div
          v-for="logo in LOGOS"
          :key="logo.id"
          class="hc-smart__logo"
          :class="`hc-smart__logo--${logo.id}`"
          :style="{
            top: `${logo.top}px`,
            left: `${logo.left}px`,
            transform: `rotate(${logo.rot}deg)`,
          }"
        >
          <template v-if="logo.id === 'upi'">
            <span class="hc-smart__logo-upi">UPI</span>
            <img :src="`${ASSET}/bhim.png`" alt="" width="38" height="38" />
          </template>
          <template v-else-if="logo.id === 'visa'">
            <span class="hc-smart__logo-visa">VISA</span>
          </template>
          <template v-else-if="logo.id === 'mc'">
            <img
              :src="`${ASSET}/mastercard.svg`"
              alt=""
              width="67"
              height="40"
            />
          </template>
          <template v-else-if="logo.id === 'paytm'">
            <span class="hc-smart__logo-paytm"
              ><span>pay</span><span>tm</span></span
            >
          </template>
          <template v-else-if="logo.id === 'phonepe'">
            <span class="hc-smart__logo-ppe">पे</span>
          </template>
          <template v-else-if="logo.id === 'gpay'">
            <span class="hc-smart__logo-g">G</span>
            <span class="hc-smart__logo-pay">Pay</span>
          </template>
          <template v-else>
            <span class="hc-smart__logo-more">+ More</span>
          </template>
        </div>
      </div>

      <!-- Phone -->
      <div class="hc-smart__phone">
        <div class="hc-smart__screen">
          <!-- Status -->
          <div class="hc-smart__status">
            <span class="hc-smart__time">9:41</span>
            <span class="hc-smart__island" />
            <span class="hc-smart__status-icons">
              <img :src="`${ASSET}/ios-signal.svg`" alt="" width="24" height="17" />
              <img :src="`${ASSET}/ios-wifi.svg`" alt="" width="24" height="17" />
              <img :src="`${ASSET}/ios-battery.svg`" alt="" width="30" height="17" />
            </span>
          </div>

          <!-- Checkout -->
          <div v-show="screen === 'checkout'" class="hc-smart__checkout">
            <div class="hc-smart__nav">
              <img :src="`${ASSET}/arrow-left.svg`" alt="" width="30" height="30" />
            </div>

            <div class="hc-smart__intro">
              <p class="hc-smart__title">Checkout</p>
              <p class="hc-smart__subtitle">Choose your payment method</p>
            </div>

            <div class="hc-smart__product">
              <div class="hc-smart__thumb">
                <img
                  :src="`${ASSET}/headphones.png`"
                  alt=""
                  width="74"
                  height="74"
                />
              </div>
              <div class="hc-smart__product-meta">
                <p class="hc-smart__product-name">Wireless Headphones</p>
                <p class="hc-smart__product-price">₹2,499</p>
                <p class="hc-smart__product-qty">Qty: <span>1</span></p>
              </div>
            </div>

            <div class="hc-smart__methods">
              <div
                v-for="m in METHODS"
                :key="m.id"
                :ref="m.id === 'upi' ? setUpiRef : undefined"
                class="hc-smart__method"
                :class="{
                  'hc-smart__method--selected': m.selected,
                  'hc-smart__method--pulse': m.id === 'upi' && upiPulse,
                }"
              >
                <span class="hc-smart__method-icon">
                  <img :src="`${ASSET}/${m.icon}`" alt="" width="28" height="28" />
                </span>
                <span class="hc-smart__method-text">
                  <span class="hc-smart__method-title">{{ m.title }}</span>
                  <span class="hc-smart__method-sub">{{ m.sub }}</span>
                </span>
                <img
                  class="hc-smart__method-chevron"
                  :src="`${ASSET}/chevron.svg`"
                  alt=""
                  width="24"
                  height="24"
                />
              </div>
            </div>

            <div class="hc-smart__secure">
              <img :src="`${ASSET}/shield.svg`" alt="" width="24" height="24" />
              <span>100% Secure Checkout</span>
            </div>

            <div class="hc-smart__spacer" />

            <!-- Pay / Processing button (Figma 777:2575 processing) -->
            <div
              ref="payRef"
              class="hc-smart__pay"
              :class="`hc-smart__pay--${buttonPhase}`"
            >
              <template v-if="buttonPhase === 'pay'">
                <span>Pay ₹2,499</span>
                <img
                  :src="`${ASSET}/arrow-right.svg`"
                  alt=""
                  width="24"
                  height="24"
                />
              </template>
              <template v-else-if="buttonPhase === 'processing'">
                <!-- Track + text reveal (777:2576 / 786:2897) -->
                <div class="hc-smart__pay-track">
                  <div class="hc-smart__pay-text-clip">
                    <span class="hc-smart__pay-processing-text">Processing</span>
                  </div>
                </div>
                <!-- Circular pay control (777:2578) -->
                <div class="hc-smart__pay-btn">
                  <span class="hc-smart__pay-orb">
                    <img
                      class="hc-smart__pay-proc-arrow"
                      :src="`${ASSET}/processing-arrow.svg`"
                      alt=""
                      width="48"
                      height="48"
                    />
                  </span>
                </div>
              </template>
              <template v-else>
                <span class="hc-smart__pay-orb">
                  <img
                    v-if="buttonPhase === 'arrow'"
                    :src="`${ASSET}/processing-arrow.svg`"
                    alt=""
                    width="48"
                    height="48"
                  />
                </span>
              </template>
            </div>
          </div>

          <!-- Success -->
          <div v-show="screen === 'success'" class="hc-smart__success">
            <div class="hc-smart__success-icon">
              <img
                :src="`${ASSET}/success-bg.svg`"
                alt=""
                width="146"
                height="146"
              />
            </div>
            <p class="hc-smart__success-text">Payment Successful</p>
          </div>

          <div class="hc-smart__homebar" />
        </div>
      </div>

      <!-- Cursor -->
      <div
        v-show="!reduceMotion && screen === 'checkout'"
        class="hc-smart__cursor"
        :class="{ 'hc-smart__cursor--click': clicking }"
        :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
      >
        <img :src="`${ASSET}/cursor.svg`" alt="" width="36" height="36" />
        <span v-show="clicking" class="hc-smart__click-ring" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.hc-smart {
  position: relative;
  width: 100%;
  aspect-ratio: 471 / 621;
  margin-inline: auto;
  overflow: visible;
  line-height: normal;
  background: transparent;
}

.hc-smart__artboard {
  position: absolute;
  left: 0;
  top: 0;
  width: 942px;
  height: 1242px;
  transform-origin: top left;
}

.hc-smart__logos {
  position: absolute;
  left: 0;
  top: 115px;
  width: 402px;
  height: 1006px;
  z-index: 1;
  pointer-events: none;
}

.hc-smart__arc {
  position: absolute;
  left: 106px;
  top: 0;
  width: 402px;
  height: auto;
  opacity: 0.9;
}

.hc-smart__logo {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  width: 161px;
  height: 107px;
  box-sizing: border-box;
  padding: 20px;
  border: 1.7px solid #eef2f6;
  border-radius: 27px;
  background: #ffffff;
  box-shadow: 0 20px 20px rgba(13, 23, 48, 0.05);
  transform-origin: center;
}

.hc-smart__logo--more {
  width: auto;
  height: auto;
  padding: 17px 34px;
  border-radius: 168px;
  box-shadow: 0 13px 13px rgba(13, 23, 48, 0.05);
}

.hc-smart--motion .hc-smart__logo {
  animation: hc-smart-float 4.2s ease-in-out infinite;
}

.hc-smart--motion .hc-smart__logo--visa {
  animation-delay: 0.3s;
}
.hc-smart--motion .hc-smart__logo--mc {
  animation-delay: 0.55s;
}
.hc-smart--motion .hc-smart__logo--paytm {
  animation-delay: 0.8s;
}
.hc-smart--motion .hc-smart__logo--phonepe {
  animation-delay: 1.05s;
}
.hc-smart--motion .hc-smart__logo--gpay {
  animation-delay: 1.3s;
}
.hc-smart--motion .hc-smart__logo--more {
  animation-delay: 1.55s;
}

@keyframes hc-smart-float {
  0%,
  100% {
    translate: 0 0;
  }
  50% {
    translate: 0 -6px;
  }
}

.hc-smart__logo-upi {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 27px;
  font-weight: 800;
  color: #1e293b;
}

.hc-smart__logo img {
  display: block;
  width: 38px;
  height: 38px;
  object-fit: contain;
}

.hc-smart__logo-visa {
  font-family: Montserrat, Manrope, system-ui, sans-serif;
  font-size: 30px;
  font-weight: 900;
  font-style: italic;
  letter-spacing: -0.8px;
  color: #1a1f71;
}

.hc-smart__logo-paytm {
  font-family: Arimo, Arial, sans-serif;
  font-size: 27px;
  font-weight: 700;
}

.hc-smart__logo-paytm span:first-child {
  color: #002e6e;
}

.hc-smart__logo-paytm span:last-child {
  color: #00baf2;
}

.hc-smart__logo-ppe {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 27px;
  background: #5f259f;
  font-family: Arimo, Arial, sans-serif;
  font-size: 30px;
  font-weight: 700;
  font-style: italic;
  color: #ffffff;
}

.hc-smart__logo-g {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 27px;
  font-weight: 800;
  color: #4285f4;
}

.hc-smart__logo-pay {
  font-family: Arimo, Arial, sans-serif;
  font-size: 23px;
  font-weight: 700;
  color: #5f6368;
}

.hc-smart__logo-more {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.hc-smart__phone {
  position: absolute;
  left: 339px;
  top: 0;
  width: 604px;
  height: 1241px;
  z-index: 2;
  box-sizing: border-box;
  padding: 13px;
  border-radius: 74px;
  background: #0e1e2f;
  box-shadow: 0 40px 40px rgba(9, 29, 52, 0.15);
}

.hc-smart__screen {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 64px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  padding: 20px 27px 27px;
  box-sizing: border-box;
}

.hc-smart__status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  flex-shrink: 0;
}

.hc-smart__time {
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: #1e293b;
}

.hc-smart__island {
  width: 134px;
  height: 30px;
  border-radius: 17px;
  background: #000000;
}

.hc-smart__status-icons {
  display: flex;
  align-items: center;
  gap: 7px;
}

.hc-smart__status-icons img {
  display: block;
  height: 17px;
  width: auto;
}

.hc-smart__checkout {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  width: 100%;
}

.hc-smart__nav {
  display: flex;
  align-items: center;
  padding: 20px 0;
}

.hc-smart__nav img {
  display: block;
  width: 30px;
  height: 30px;
}

.hc-smart__intro {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 10px;
}

.hc-smart__title {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 34px;
  font-weight: 800;
  color: #252b37;
}

.hc-smart__subtitle {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 18px;
  font-weight: 400;
  color: #535862;
}

.hc-smart__product {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border: 1.7px solid #f1f5f9;
  border-radius: 23px;
  background: #ffffff;
}

.hc-smart__thumb {
  display: grid;
  place-items: center;
  width: 94px;
  height: 94px;
  flex-shrink: 0;
  border: 1.7px solid #eef2f6;
  border-radius: 17px;
  background: #f8fafc;
  overflow: hidden;
}

.hc-smart__thumb img {
  display: block;
  width: 74px;
  height: 74px;
  object-fit: cover;
  border-radius: 10px;
}

.hc-smart__product-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.hc-smart__product-name,
.hc-smart__product-price {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
}

.hc-smart__product-name {
  font-size: 20px;
}

.hc-smart__product-price {
  font-size: 22px;
}

.hc-smart__product-qty {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 16px;
  color: #64748b;
}

.hc-smart__product-qty span {
  color: #535862;
}

.hc-smart__methods {
  display: flex;
  flex-direction: column;
  gap: 13px;
  padding-top: 27px;
  width: 100%;
}

.hc-smart__method {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
  padding: 23px;
  box-sizing: border-box;
  border: 1.7px solid #eef2f6;
  border-radius: 20px;
  background: #ffffff;
  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.hc-smart__method--selected {
  border-color: #0292b8;
  background: #f0f9ff;
}

.hc-smart__method--pulse {
  transform: scale(1.02);
}

.hc-smart__method-icon {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  flex-shrink: 0;
  border: 1.7px solid #d5d7da;
  border-radius: 13px;
  background: #ffffff;
}

.hc-smart__method--selected .hc-smart__method-icon {
  background: #ffffff;
}

.hc-smart__method-icon img {
  display: block;
  width: 28px;
  height: 28px;
}

.hc-smart__method-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.hc-smart__method-title {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
}

.hc-smart__method-sub {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 18px;
  font-weight: 400;
  color: #535862;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hc-smart__method-chevron {
  display: block;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.hc-smart__secure {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding-top: 27px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.hc-smart__secure img {
  display: block;
  width: 24px;
  height: 24px;
}

.hc-smart__spacer {
  flex: 1;
  min-height: 16px;
}

.hc-smart__pay {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 13px;
  width: 100%;
  height: 74px;
  box-sizing: border-box;
  border-radius: 20px;
  background: #097495;
  color: #ffffff;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 23px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  transition:
    width 0.35s cubic-bezier(0.45, 0, 0.2, 1),
    border-radius 0.35s cubic-bezier(0.45, 0, 0.2, 1),
    padding 0.35s ease,
    gap 0.25s ease,
    background 0.2s ease;
}

.hc-smart__pay img {
  display: block;
  width: 24px;
  height: 24px;
}

.hc-smart__pay--circle,
.hc-smart__pay--arrow {
  width: 100px;
  height: 92px;
  margin-inline: auto;
  padding: 6px 10px;
  border-radius: 1000px;
  justify-content: flex-start;
}

/* Figma 777:2575 — Processing Button Animation @ 2× */
.hc-smart__pay--processing {
  position: relative;
  width: 350px;
  height: 92px;
  margin-inline: auto;
  padding: 0;
  border-radius: 0;
  background: transparent;
  overflow: visible;
  justify-content: flex-start;
  gap: 0;
  transition: none;
}

.hc-smart__pay-track {
  position: absolute;
  left: 38px;
  top: 11px;
  width: 0.2px;
  height: 70px;
  box-sizing: border-box;
  border-radius: 20.126px;
  background: #097495;
  overflow: hidden;
  opacity: 0;
  animation: hc-smart-pay-track 5s linear forwards;
}

.hc-smart__pay-text-clip {
  position: absolute;
  left: 88px;
  top: 19px;
  width: 0.2px;
  height: 32px;
  overflow: hidden;
  opacity: 0;
  animation: hc-smart-pay-text 5s linear forwards;
}

.hc-smart__pay-processing-text {
  display: block;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 23.48px;
  font-weight: 700;
  line-height: normal;
  color: #ffffff;
  white-space: nowrap;
}

.hc-smart__pay-btn {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  width: 100px;
  height: 92px;
  padding: 6px 10px;
  border-radius: 1000px;
  background: #097495;
}

.hc-smart__pay-orb {
  display: grid;
  place-items: center;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border: 2px solid #ffffff;
  border-radius: 100px;
  box-sizing: border-box;
}

.hc-smart__pay-orb img,
.hc-smart__pay .hc-smart__pay-proc-arrow {
  display: block;
  width: 48px;
  height: 48px;
  filter: none;
}

.hc-smart__pay-proc-arrow {
  opacity: 0;
  transform: translateX(-40px);
  animation: hc-smart-pay-arrow 5s linear forwards;
}

/* Rectangle 777:2576 — width + opacity (Figma 5s) */
@keyframes hc-smart-pay-track {
  0%,
  19% {
    width: 0.2px;
    opacity: 0;
  }
  20% {
    width: 0.2px;
    opacity: 0;
    animation-timing-function: ease-out;
  }
  30% {
    width: 312px;
    opacity: 1;
    animation-timing-function: linear;
  }
  84% {
    width: 312px;
    opacity: 1;
    animation-timing-function: ease-in-out;
  }
  90%,
  100% {
    width: 0.2px;
    opacity: 0;
  }
}

/* text-reveal-clip 786:2897 — stepped width reveal */
@keyframes hc-smart-pay-text {
  0%,
  29.8% {
    width: 0.2px;
    opacity: 0;
  }
  30% {
    width: 18px;
    opacity: 1;
  }
  34.8% {
    width: 18px;
  }
  35% {
    width: 28px;
  }
  39.8% {
    width: 28px;
  }
  40% {
    width: 42px;
  }
  44.8% {
    width: 42px;
  }
  45% {
    width: 56px;
  }
  49.8% {
    width: 56px;
  }
  50% {
    width: 68px;
  }
  54.8% {
    width: 68px;
  }
  55% {
    width: 82px;
  }
  59.8% {
    width: 82px;
  }
  60% {
    width: 94px;
  }
  64.8% {
    width: 94px;
  }
  65% {
    width: 100px;
  }
  69.8% {
    width: 100px;
  }
  70% {
    width: 116px;
  }
  74.8% {
    width: 116px;
  }
  75% {
    width: 130px;
  }
  84% {
    width: 130px;
    opacity: 1;
  }
  87%,
  100% {
    width: 0.2px;
    opacity: 0;
  }
}

/* arrow-right 777:2580 */
@keyframes hc-smart-pay-arrow {
  0%,
  10% {
    opacity: 0;
    transform: translateX(-40px);
  }
  15% {
    opacity: 1;
    transform: translateX(0);
  }
  84% {
    opacity: 1;
    transform: translateX(0);
  }
  89%,
  100% {
    opacity: 0;
    transform: translateX(-40px);
  }
}

.hc-smart__success {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  animation: hc-smart-success-in 0.45s ease-out;
}

@keyframes hc-smart-success-in {
  from {
    opacity: 0;
    transform: scale(0.92);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.hc-smart__success-icon {
  width: 200px;
  height: 200px;
  display: grid;
  place-items: center;
}

.hc-smart__success-icon img {
  display: block;
  width: 146px;
  height: 146px;
}

.hc-smart--motion .hc-smart__success-icon {
  animation: hc-smart-success-pulse 2s ease-in-out infinite;
}

@keyframes hc-smart-success-pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.04);
  }
}

.hc-smart__success-text {
  margin: 0;
  width: 280px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 48px;
  font-weight: 600;
  line-height: 1.15;
  text-align: center;
  color: #252b37;
}

.hc-smart__homebar {
  width: 201px;
  height: 7px;
  margin: 13px auto 0;
  border-radius: 3px;
  background: #1e2937;
  flex-shrink: 0;
}

.hc-smart__cursor {
  position: absolute;
  z-index: 8;
  width: 36px;
  height: 36px;
  margin-left: -4px;
  margin-top: -4px;
  pointer-events: none;
  transition:
    left 0.55s cubic-bezier(0.45, 0, 0.2, 1),
    top 0.55s cubic-bezier(0.45, 0, 0.2, 1),
    transform 0.12s ease;
  filter: drop-shadow(0 3px 4px rgba(0, 0, 0, 0.35));
}

.hc-smart__cursor img {
  display: block;
  width: 36px;
  height: 36px;
}

.hc-smart__cursor--click {
  transform: scale(0.82);
  transform-origin: 2px 2px;
}

.hc-smart__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid rgba(9, 116, 149, 0.85);
  animation: hc-smart-ring 0.28s ease-out forwards;
}

@keyframes hc-smart-ring {
  from {
    transform: scale(0.4);
    opacity: 0.95;
  }
  to {
    transform: scale(1.7);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hc-smart__cursor,
  .hc-smart__method,
  .hc-smart__pay,
  .hc-smart__logo,
  .hc-smart__success,
  .hc-smart__success-icon,
  .hc-smart__pay-track,
  .hc-smart__pay-text-clip,
  .hc-smart__pay-proc-arrow {
    transition: none;
    animation: none;
  }

  .hc-smart__pay--processing .hc-smart__pay-track {
    width: 312px;
    opacity: 1;
  }

  .hc-smart__pay--processing .hc-smart__pay-text-clip {
    width: 130px;
    opacity: 1;
  }

  .hc-smart__pay--processing .hc-smart__pay-proc-arrow {
    opacity: 1;
    transform: none;
  }
}
</style>
