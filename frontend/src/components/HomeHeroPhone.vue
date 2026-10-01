<script setup>
import { nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

/*
 * Figma 990:8203 — checkout phone mockup, running the Hyper Checkout "Smarter" storyboard
 * (HyperCheckoutSmarterGraphic): cursor → UPI → Pay → processing morph → success → reset.
 * Motion sizes are that graphic's 2× artboard values × 0.26, the ratio between the two phones.
 */
const ASSET = "/images/figma-home/hero-v2";
const SMARTER_ASSET = "/images/figma-hyper-checkout/smarter";

const METHODS = [
  { name: "UPI", note: "Pay with any UPI app", icon: "pay-upi.svg", active: true },
  { name: "Cards", note: "Credit & Debit cards", icon: "pay-card.svg" },
  { name: "Net Banking", note: "All major banks", icon: "pay-bank.svg" },
  { name: "Wallets", note: "Paytm, PhonePe, Amazon Pay", icon: "pay-wallet.svg" },
  { name: "EMI", note: "No cost EMI available", icon: "pay-emi.svg" },
];

const reduceMotion = ref(false);
const screen = ref("checkout"); // checkout | success
const buttonPhase = ref("pay"); // pay | circle | arrow | processing
const upiPulse = ref(false);
const clicking = ref(false);
const cursor = reactive({ x: 120.7, y: 121.5 });

const phoneRef = ref(null);
const upiRef = ref(null);
const payRef = ref(null);

let timers = [];
let loopTimer = null;

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

/* The hero stage is CSS-scaled, so convert viewport px back to phone px. */
function aimAt(el) {
  const phone = phoneRef.value;
  if (!phone || !el) return;
  const p = phone.getBoundingClientRect();
  const r = el.getBoundingClientRect();
  const sc = p.width / phone.offsetWidth || 1;
  cursor.x = (r.left + r.width / 2 - p.left) / sc;
  cursor.y = (r.top + r.height / 2 - p.top) / sc;
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

  aimAt(upiRef.value);
  await wait(500);

  await clickEl(upiRef.value, 180);
  upiPulse.value = true;
  await wait(350);
  upiPulse.value = false;
  await wait(250);

  await clickEl(payRef.value, 180);
  await wait(120);

  buttonPhase.value = "circle";
  await wait(280);
  buttonPhase.value = "arrow";
  await wait(320);
  buttonPhase.value = "processing";
  await wait(4200);

  screen.value = "success";
  await wait(2400);

  resetState();
  await wait(400);
  loopTimer = setTimeout(() => runSequence(), 120);
}

onMounted(() => {
  reduceMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduceMotion.value) nextTick(runSequence);
});

onBeforeUnmount(clearTimers);
</script>

<template>
  <div ref="phoneRef" class="hg-phone">
    <div class="hg-phone__screen">
      <div class="hg-phone__status">
        <span class="hg-phone__time">9:41</span>
        <span class="hg-phone__notch" />
        <span class="hg-phone__signals">
          <img :src="`${ASSET}/phone-signal.svg`" alt="" width="6.149" height="4.392" />
          <img :src="`${ASSET}/phone-wifi.svg`" alt="" width="6.149" height="4.392" />
          <img :src="`${ASSET}/phone-battery.svg`" alt="" width="7.905" height="4.392" />
        </span>
      </div>

      <div v-show="screen === 'checkout'" class="hg-phone__checkout">
        <div class="hg-phone__header">
          <img :src="`${ASSET}/phone-arrow-left.svg`" alt="" width="7.905" height="7.905" />
        </div>

        <div class="hg-phone__intro">
          <div class="hg-phone__heading">
            <p class="hg-phone__title">Checkout</p>
            <p class="hg-phone__subtitle">Choose your payment method</p>
          </div>
          <div class="hg-phone__product">
            <span class="hg-phone__thumb">
              <img :src="`${ASSET}/product-headphones.png`" alt="" width="80" height="80" decoding="async" />
            </span>
            <span class="hg-phone__product-text">
              <span class="hg-phone__product-name">Wireless Headphones</span>
              <span class="hg-phone__product-price">₹2,499</span>
              <span class="hg-phone__product-qty">Qty: <span>1</span></span>
            </span>
          </div>
        </div>

        <div class="hg-phone__methods">
          <div
            v-for="method in METHODS"
            :key="method.name"
            :ref="method.active ? setUpiRef : undefined"
            class="hg-phone__method"
            :class="{
              'hg-phone__method--active': method.active,
              'hg-phone__method--pulse': method.active && upiPulse,
            }"
          >
            <span class="hg-phone__method-main">
              <span class="hg-phone__method-icon">
                <img :src="`${ASSET}/${method.icon}`" alt="" width="7.332" height="7.332" />
              </span>
              <span class="hg-phone__method-text">
                <span class="hg-phone__method-name">{{ method.name }}</span>
                <span class="hg-phone__method-note">{{ method.note }}</span>
              </span>
            </span>
            <img
              class="hg-phone__chevron"
              :src="`${ASSET}/${method.active ? 'chevron-right-active' : 'chevron-right'}.svg`"
              alt=""
              width="6.149"
              height="6.149"
            />
          </div>
        </div>

        <div class="hg-phone__secure">
          <img :src="`${ASSET}/shield-check.svg`" alt="" width="6.149" height="6.149" />
          <span>100% Secure Checkout</span>
        </div>

        <div ref="payRef" class="hg-phone__pay" :class="`hg-phone__pay--${buttonPhase}`">
          <template v-if="buttonPhase === 'pay'">
            <span>Pay ₹2,499</span>
            <img :src="`${ASSET}/arrow-right.svg`" alt="" width="6.149" height="6.149" />
          </template>
          <template v-else-if="buttonPhase === 'processing'">
            <div class="hg-phone__pay-track">
              <div class="hg-phone__pay-text-clip">
                <span class="hg-phone__pay-text">Processing</span>
              </div>
            </div>
            <div class="hg-phone__pay-btn">
              <span class="hg-phone__pay-orb">
                <img
                  class="hg-phone__pay-proc-arrow"
                  :src="`${SMARTER_ASSET}/processing-arrow.svg`"
                  alt=""
                  width="48"
                  height="48"
                />
              </span>
            </div>
          </template>
          <span v-else class="hg-phone__pay-orb">
            <img
              v-if="buttonPhase === 'arrow'"
              :src="`${SMARTER_ASSET}/processing-arrow.svg`"
              alt=""
              width="48"
              height="48"
            />
          </span>
        </div>
      </div>

      <div v-show="screen === 'success'" class="hg-phone__success">
        <div class="hg-phone__success-icon">
          <img :src="`${SMARTER_ASSET}/success-bg.svg`" alt="" width="146" height="146" />
        </div>
        <p class="hg-phone__success-text">Payment Successful</p>
      </div>

      <div class="hg-phone__home">
        <span />
      </div>
    </div>

    <div
      v-show="!reduceMotion && screen === 'checkout'"
      class="hg-phone__cursor"
      :class="{ 'hg-phone__cursor--click': clicking }"
      :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
    >
      <img :src="`${SMARTER_ASSET}/cursor.svg`" alt="" width="36" height="36" />
      <span v-show="clicking" class="hg-phone__click-ring" />
    </div>
  </div>
</template>

<style scoped>
/* Sized 1.2× via scale so the Figma px inside stay as-is; aimAt() reads the scaled rect. */
.hg-phone {
  left: 0;
  top: 105.5px;
  scale: 1.2;
  transform-origin: 0 0;
  display: flex;
  width: 158.108px;
  height: 325px;
  padding: 3.514px;
  border-radius: 19.324px;
  background: #0e1e2f;
  filter: drop-shadow(0 10.541px 10.541px rgba(9, 29, 52, 0.15));
  line-height: normal;
  color: #252b37;
}

.hg-phone,
.hg-phone *,
.hg-phone *::before,
.hg-phone *::after {
  box-sizing: border-box;
}

.hg-phone img {
  display: block;
  max-width: none;
}

.hg-phone p {
  margin: 0;
}

.hg-phone__screen {
  display: flex;
  flex: 1 0 0;
  flex-direction: column;
  min-width: 1px;
  height: 100%;
  overflow: hidden;
  padding: 5.27px 7.027px 7.027px;
  border-radius: 16.689px;
  background: #f8fafc;
}

.hg-phone__status {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: space-between;
  height: 10.541px;
}

.hg-phone__time {
  font-size: 5.27px;
  font-weight: 800;
  color: #1e293b;
}

.hg-phone__notch {
  width: 35.135px;
  height: 7.905px;
  border-radius: 4.392px;
  background: #000000;
}

.hg-phone__signals {
  display: flex;
  align-items: center;
  gap: 1.757px;
}

.hg-phone__signals img {
  height: 4.392px;
}

.hg-phone__signals img:not(:last-child) {
  width: 6.149px;
}

.hg-phone__signals img:last-child {
  width: 7.905px;
}

.hg-phone__header {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  height: 18.446px;
}

.hg-phone__header img {
  width: 7.905px;
  height: 7.905px;
}

.hg-phone__intro {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  gap: 2.619px;
  width: 136.697px;
  height: 57.088px;
}

.hg-phone__heading {
  display: flex;
  flex-direction: column;
  gap: 0.878px;
}

.hg-phone__title {
  font-size: 8.784px;
  font-weight: 800;
}

.hg-phone__subtitle {
  font-size: 4.831px;
  font-weight: 400;
  color: #535862;
}

.hg-phone__product {
  display: flex;
  align-items: center;
  gap: 5.27px;
  height: 35.135px;
  padding: 5.27px;
  border: 0.439px solid #f1f5f9;
  border-radius: 6.149px;
  background: #ffffff;
}

.hg-phone__thumb {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 24.595px;
  height: 24.595px;
  border: 0.439px solid #eef2f6;
  border-radius: 4.392px;
  background: #f8fafc;
}

.hg-phone__thumb img {
  width: 19.324px;
  height: 19.324px;
  border-radius: 2.635px;
  object-fit: cover;
}

.hg-phone__product-text {
  display: flex;
  flex: 1 0 0;
  flex-direction: column;
  gap: 0.878px;
  min-width: 1px;
  font-weight: 700;
}

.hg-phone__product-name {
  font-size: 5.27px;
}

.hg-phone__product-price {
  font-size: 5.709px;
}

.hg-phone__product-qty {
  font-size: 4.19px;
  font-weight: 400;
  color: #64748b;
}

.hg-phone__product-qty span {
  color: #535862;
}

.hg-phone__methods {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  gap: 3.514px;
  padding-top: 7.027px;
}

/* Figma strokes don't add size; fixed heights stop the CSS borders pushing rows apart. */
.hg-phone__method {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 28.176px;
  padding: 6.149px;
  border: 0.439px solid #eef2f6;
  border-radius: 5.27px;
  background: #ffffff;
}

.hg-phone__method--active {
  border-color: #0292b8;
  background: #f0f9ff;
}

.hg-phone__method-main {
  display: flex;
  flex: 1 0 0;
  align-items: center;
  gap: 5.27px;
  min-width: 1px;
}

.hg-phone__method-icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 14.054px;
  height: 14.054px;
  border: 0.439px solid #d5d7da;
  border-radius: 3.514px;
  background: #fafbfa;
}

.hg-phone__method--active .hg-phone__method-icon {
  background: #ffffff;
}

.hg-phone__method-icon img {
  width: 7.332px;
  height: 7.332px;
}

.hg-phone__method-text {
  display: flex;
  flex: 1 0 0;
  flex-direction: column;
  gap: 0.878px;
  min-width: 1px;
  white-space: nowrap;
}

.hg-phone__method-name {
  font-size: 5.709px;
  font-weight: 700;
}

.hg-phone__method-note {
  overflow: hidden;
  font-size: 4.831px;
  font-weight: 400;
  color: #535862;
  text-overflow: ellipsis;
}

.hg-phone__chevron {
  flex-shrink: 0;
  width: 6.149px;
  height: 6.149px;
}

.hg-phone__secure {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 2.635px;
  padding-top: 7.027px;
  font-size: 4.831px;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.hg-phone__secure img {
  width: 6.149px;
  height: 6.149px;
}

.hg-phone__pay {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 3.514px;
  width: 100%;
  height: 22.054px;
  margin-top: auto;
  padding: 7.027px;
  overflow: hidden;
  border-radius: 5.27px;
  background: #097495;
  font-size: 6.149px;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  transition:
    width 0.35s cubic-bezier(0.45, 0, 0.2, 1),
    border-radius 0.35s cubic-bezier(0.45, 0, 0.2, 1),
    padding 0.35s ease,
    gap 0.25s ease,
    background 0.2s ease;
}

.hg-phone__pay img {
  width: 6.149px;
  height: 6.149px;
}

.hg-phone__checkout {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.hg-phone__method {
  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.hg-phone__method--pulse {
  transform: scale(1.02);
}

.hg-phone__pay--circle,
.hg-phone__pay--arrow {
  justify-content: flex-start;
  width: 26.18px;
  height: 24.086px;
  margin-inline: auto;
  padding: 1.571px 2.618px;
  border-radius: 1000px;
}

/* Figma 777:2575 — Processing Button Animation */
.hg-phone__pay--processing {
  position: relative;
  justify-content: flex-start;
  gap: 0;
  width: 91.63px;
  height: 24.086px;
  margin-inline: auto;
  padding: 0;
  overflow: visible;
  border-radius: 0;
  background: transparent;
  transition: none;
}

.hg-phone__pay-track {
  position: absolute;
  left: 9.948px;
  top: 2.88px;
  width: 0.2px;
  height: 18.326px;
  overflow: hidden;
  border-radius: 5.269px;
  background: #097495;
  opacity: 0;
  animation: hg-phone-pay-track 5s linear forwards;
}

.hg-phone__pay-text-clip {
  position: absolute;
  left: 23.04px;
  top: 4.974px;
  width: 0.2px;
  height: 8.378px;
  overflow: hidden;
  opacity: 0;
  animation: hg-phone-pay-text 5s linear forwards;
}

.hg-phone__pay-text {
  display: block;
  font-size: 6.149px;
  font-weight: 700;
  line-height: normal;
  color: #ffffff;
  white-space: nowrap;
}

.hg-phone__pay-btn {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  width: 26.18px;
  height: 24.086px;
  padding: 1.571px 2.618px;
  border-radius: 1000px;
  background: #097495;
}

.hg-phone__pay-orb {
  display: grid;
  flex-shrink: 0;
  place-items: center;
  width: 20.944px;
  height: 20.944px;
  border: 0.524px solid #ffffff;
  border-radius: 100px;
}

.hg-phone__pay .hg-phone__pay-orb img {
  width: 12.566px;
  height: 12.566px;
}

.hg-phone__pay-proc-arrow {
  opacity: 0;
  transform: translateX(-10.472px);
  animation: hg-phone-pay-arrow 5s linear forwards;
}

@keyframes hg-phone-pay-track {
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
    width: 81.68px;
    opacity: 1;
    animation-timing-function: linear;
  }
  84% {
    width: 81.68px;
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
@keyframes hg-phone-pay-text {
  0%,
  29.8% {
    width: 0.2px;
    opacity: 0;
  }
  30% {
    width: 4.712px;
    opacity: 1;
  }
  34.8% {
    width: 4.712px;
  }
  35% {
    width: 7.33px;
  }
  39.8% {
    width: 7.33px;
  }
  40% {
    width: 10.996px;
  }
  44.8% {
    width: 10.996px;
  }
  45% {
    width: 14.661px;
  }
  49.8% {
    width: 14.661px;
  }
  50% {
    width: 17.802px;
  }
  54.8% {
    width: 17.802px;
  }
  55% {
    width: 21.468px;
  }
  59.8% {
    width: 21.468px;
  }
  60% {
    width: 24.609px;
  }
  64.8% {
    width: 24.609px;
  }
  65% {
    width: 26.18px;
  }
  69.8% {
    width: 26.18px;
  }
  70% {
    width: 30.369px;
  }
  74.8% {
    width: 30.369px;
  }
  75% {
    width: 34.034px;
  }
  84% {
    width: 34.034px;
    opacity: 1;
  }
  87%,
  100% {
    width: 0.2px;
    opacity: 0;
  }
}

@keyframes hg-phone-pay-arrow {
  0%,
  10% {
    opacity: 0;
    transform: translateX(-10.472px);
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
    transform: translateX(-10.472px);
  }
}

.hg-phone__success {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2.094px;
  animation: hg-phone-success-in 0.45s ease-out;
}

@keyframes hg-phone-success-in {
  from {
    opacity: 0;
    transform: scale(0.92);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.hg-phone__success-icon {
  display: grid;
  place-items: center;
  width: 52.36px;
  height: 52.36px;
  animation: hg-phone-success-pulse 2s ease-in-out infinite;
}

.hg-phone__success-icon img {
  width: 38.223px;
  height: 38.223px;
}

@keyframes hg-phone-success-pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.04);
  }
}

.hg-phone__success-text {
  width: 73.304px;
  font-size: 12.566px;
  font-weight: 600;
  line-height: 1.15;
  text-align: center;
  color: #252b37;
}

.hg-phone__cursor {
  position: absolute;
  z-index: 8;
  width: 9.425px;
  height: 9.425px;
  margin-left: -1.047px;
  margin-top: -1.047px;
  pointer-events: none;
  filter: drop-shadow(0 0.785px 1.047px rgba(0, 0, 0, 0.35));
  transition:
    left 0.55s cubic-bezier(0.45, 0, 0.2, 1),
    top 0.55s cubic-bezier(0.45, 0, 0.2, 1),
    transform 0.12s ease;
}

.hg-phone__cursor img {
  width: 9.425px;
  height: 9.425px;
}

.hg-phone__cursor--click {
  transform: scale(0.82);
  transform-origin: 0.524px 0.524px;
}

.hg-phone__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 9.425px;
  height: 9.425px;
  border: 0.524px solid rgba(9, 116, 149, 0.85);
  border-radius: 50%;
  animation: hg-phone-ring 0.28s ease-out forwards;
}

@keyframes hg-phone-ring {
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
  .hg-phone__cursor,
  .hg-phone__method,
  .hg-phone__pay,
  .hg-phone__success,
  .hg-phone__success-icon,
  .hg-phone__pay-track,
  .hg-phone__pay-text-clip,
  .hg-phone__pay-proc-arrow {
    transition: none;
    animation: none;
  }
}

.hg-phone__home {
  display: flex;
  flex-shrink: 0;
  justify-content: center;
  padding-top: 3.514px;
}

.hg-phone__home span {
  width: 52.703px;
  height: 1.757px;
  border-radius: 0.878px;
  background: #1e2937;
}
</style>
