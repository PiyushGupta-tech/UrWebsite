<script setup>
import { reactive } from "vue";

/** Figma 283:8852 — Configure Payment Methods graphic */
const ASSET = "/images/figma-custom-checkout/showcase";
const LOGO = "/images/figma-custom-checkout/features";

const methods = [
  {
    id: "cards",
    label: "Cards",
    icon: `${ASSET}/cards-icon.svg`,
  },
  {
    id: "upi",
    label: "UPI",
    icon: `${ASSET}/upi-icon.svg`,
    tall: true,
  },
  {
    id: "netbanking",
    label: "Net Banking",
    icon: `${ASSET}/building.svg`,
  },
  {
    id: "wallets",
    label: "Wallets",
    icon: `${ASSET}/wallet.svg`,
  },
  {
    id: "emi",
    label: "EMI",
    icon: `${ASSET}/calendar.svg`,
  },
];

const enabled = reactive({
  cards: true,
  upi: true,
  netbanking: true,
  wallets: true,
  emi: true,
});

const badges = [
  { id: "visa", src: `${LOGO}/logo-visa.png`, side: "left", top: "2%", method: "cards" },
  {
    id: "mastercard",
    src: `${LOGO}/logo-mastercard.png`,
    side: "left",
    top: "32%",
    method: "cards",
  },
  { id: "upi", src: `${LOGO}/logo-upi.png`, side: "left", top: "62%", method: "upi" },
  { id: "gpay", src: `${LOGO}/logo-gpay.png`, side: "right", top: "2%", method: "upi" },
  {
    id: "phonepe",
    src: `${LOGO}/logo-phonepe.png`,
    side: "right",
    top: "32%",
    method: "upi",
  },
  {
    id: "paytm",
    src: `${LOGO}/logo-paytm.png`,
    side: "right",
    top: "62%",
    method: "wallets",
  },
];

function toggle(id) {
  enabled[id] = !enabled[id];
}

function isOn(id) {
  return !!enabled[id];
}
</script>

<template>
  <div class="cfm">
    <div class="cfm__screen">
      <div class="cfm__grid" />
      <div class="cfm__pulse cfm__pulse--a cfm__pulse--lg"><span /><span /><span /></div>
      <div class="cfm__pulse cfm__pulse--b"><span /><span /><span /></div>
      <div class="cfm__pulse cfm__pulse--c"><span /><span /></div>
      <div class="cfm__pulse cfm__pulse--d cfm__pulse--lg"><span /><span /><span /></div>
      <div class="cfm__pulse cfm__pulse--e"><span /><span /></div>
      <div class="cfm__pulse cfm__pulse--f cfm__pulse--xl"><span /><span /><span /></div>
    </div>

    <div class="cfm__stage">
      <svg class="cfm__wires" viewBox="0 0 616 333" fill="none" aria-hidden="true">
        <!-- Left branch -->
        <g :class="{ 'cfm__wire-group--off': !isOn('cards') && !isOn('upi') }">
          <path
            class="cfm__wire"
            d="M118 42 C150 42, 168 120, 188 158"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            class="cfm__wire"
            d="M118 140 C148 140, 168 155, 188 165"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            class="cfm__wire"
            d="M118 238 C148 220, 168 185, 188 172"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <circle cx="118" cy="42" r="4" fill="#7ec8d9" />
          <circle cx="118" cy="140" r="4" fill="#7ec8d9" />
          <circle cx="118" cy="238" r="4" fill="#7ec8d9" />
        </g>
        <!-- Right branch -->
        <g :class="{ 'cfm__wire-group--off': !isOn('upi') && !isOn('wallets') }">
          <path
            class="cfm__wire"
            d="M498 42 C468 42, 450 120, 430 158"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            class="cfm__wire"
            d="M498 140 C468 140, 450 155, 430 168"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            class="cfm__wire"
            d="M498 238 C468 220, 450 185, 430 175"
            stroke="#7ec8d9"
            stroke-width="2"
            stroke-linecap="round"
          />
          <circle cx="498" cy="42" r="4" fill="#7ec8d9" />
          <circle cx="498" cy="140" r="4" fill="#7ec8d9" />
          <circle cx="498" cy="238" r="4" fill="#7ec8d9" />
        </g>
      </svg>

      <article
        v-for="badge in badges"
        :key="badge.id"
        class="cfm__badge"
        :class="[
          `cfm__badge--${badge.side}`,
          { 'cfm__badge--off': !isOn(badge.method) },
        ]"
        :style="{ top: badge.top }"
      >
        <img :src="badge.src" :alt="badge.id" decoding="async" />
      </article>

      <article class="cfm__card">
        <p class="cfm__title">Payment Methods</p>
        <ul class="cfm__list">
          <li v-for="method in methods" :key="method.id" class="cfm__row">
            <div class="cfm__left">
              <img
                class="cfm__icon"
                :class="{ 'cfm__icon--tall': method.tall }"
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
              class="cfm__toggle"
              :class="{ 'cfm__toggle--off': !isOn(method.id) }"
              :aria-pressed="isOn(method.id)"
              :aria-label="`${isOn(method.id) ? 'Disable' : 'Enable'} ${method.label}`"
              @click="toggle(method.id)"
            >
              <span class="cfm__knob" />
            </button>
          </li>
        </ul>
      </article>
    </div>
  </div>
</template>

<style scoped>
.cfm {
  position: relative;
  width: 100%;
  aspect-ratio: 616 / 351;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.cfm__screen {
  position: absolute;
  left: 15.06%;
  right: 23.37%;
  top: 0;
  bottom: 24.28%;
  overflow: hidden;
  border-radius: 14px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.cfm__grid {
  position: absolute;
  inset: -30%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 26px 26px;
}

.cfm__pulse {
  position: absolute;
}

.cfm__pulse--a {
  left: 58%;
  top: 38%;
}

.cfm__pulse--b {
  left: 22%;
  top: 30%;
}

.cfm__pulse--c {
  left: 40%;
  top: 62%;
}

.cfm__pulse--d {
  left: 78%;
  top: 22%;
}

.cfm__pulse--e {
  left: 12%;
  top: 58%;
}

.cfm__pulse--f {
  left: 68%;
  top: 72%;
}

.cfm__pulse--lg {
  transform: scale(1.45);
  transform-origin: center;
}

.cfm__pulse--xl {
  transform: scale(1.85);
  transform-origin: center;
}

.cfm__pulse--lg span:not(:nth-child(1)) {
  animation-name: cfm-ring-lg;
}

.cfm__pulse--xl span:not(:nth-child(1)) {
  animation-name: cfm-ring-xl;
}

.cfm__pulse span {
  position: absolute;
  border: 1.5px solid rgba(180, 230, 255, 0.35);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: cfm-ring 3s ease-out infinite;
}

.cfm__pulse--a span:nth-child(1),
.cfm__pulse--b span:nth-child(1),
.cfm__pulse--c span:nth-child(1),
.cfm__pulse--d span:nth-child(1),
.cfm__pulse--e span:nth-child(1),
.cfm__pulse--f span:nth-child(1) {
  width: 18px;
  height: 18px;
  background: radial-gradient(
    circle,
    rgba(220, 245, 255, 0.95) 0%,
    rgba(180, 230, 255, 0.55) 45%,
    rgba(180, 230, 255, 0) 72%
  );
  border: none;
  animation: none;
  filter: blur(5px);
  box-shadow: 0 0 14px 5px rgba(180, 230, 255, 0.35);
}

.cfm__pulse--lg span:nth-child(1) {
  width: 24px;
  height: 24px;
  filter: blur(6px);
  box-shadow: 0 0 18px 6px rgba(180, 230, 255, 0.4);
}

.cfm__pulse--xl span:nth-child(1) {
  width: 28px;
  height: 28px;
  filter: blur(7px);
  box-shadow: 0 0 22px 8px rgba(180, 230, 255, 0.45);
}

.cfm__pulse span:nth-child(2) {
  animation-delay: 0.5s;
}

.cfm__pulse span:nth-child(3) {
  animation-delay: 1.1s;
}

.cfm__pulse--d span:nth-child(2) {
  animation-delay: 0.9s;
}

.cfm__pulse--d span:nth-child(3) {
  animation-delay: 1.5s;
}

.cfm__pulse--e span:nth-child(2) {
  animation-delay: 1.2s;
}

.cfm__pulse--f span:nth-child(2) {
  animation-delay: 0.3s;
}

.cfm__pulse--f span:nth-child(3) {
  animation-delay: 0.8s;
}

.cfm__stage {
  position: absolute;
  inset: 5.2% 0 0;
  width: 100%;
  height: 94.8%;
}

.cfm__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cfm__wire {
  stroke-dasharray: 5 6;
  animation: cfm-dash 0.95s linear infinite;
}

.cfm__wire-group--off {
  opacity: 0.25;
  transition: opacity 0.3s ease;
}

.cfm__card {
  position: absolute;
  z-index: 3;
  left: 29.2%;
  top: 12%;
  width: 39%;
  padding: 16px 18px;
  box-sizing: border-box;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  background: #ffffff;
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.02),
    0 8px 12px rgba(0, 0, 0, 0.05);
  animation: cfm-float 5.2s ease-in-out infinite;
}

.cfm__title {
  margin: 0 0 14px;
  text-align: center;
  font-size: clamp(12px, 2vw, 15px);
  font-weight: 600;
  color: #1a1a2e;
}

.cfm__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cfm__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.cfm__left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: clamp(9px, 1.5vw, 11px);
  font-weight: 600;
  color: #252b37;
  white-space: nowrap;
}

.cfm__icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
  flex-shrink: 0;
}

.cfm__icon--tall {
  height: 20px;
}

.cfm__toggle {
  position: relative;
  width: 34px;
  height: 18px;
  padding: 0;
  border: none;
  border-radius: 999px;
  background: #097495;
  cursor: pointer;
  transition: background 0.25s ease;
  flex-shrink: 0;
}

.cfm__toggle--off {
  background: #cbd5e1;
}

.cfm__knob {
  position: absolute;
  top: 2px;
  left: 16px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #fff;
  transition: left 0.25s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
}

.cfm__toggle--off .cfm__knob {
  left: 2px;
}

.cfm__badge {
  position: absolute;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14%;
  height: 15%;
  padding: 0 8px;
  box-sizing: border-box;
  border: 1px solid #e2e6ef;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition:
    opacity 0.3s ease,
    filter 0.3s ease;
  animation: cfm-float 4.6s ease-in-out infinite;
}

.cfm__badge--left {
  left: 2%;
}

.cfm__badge--right {
  right: 1.5%;
}

.cfm__badge:nth-child(odd) {
  animation-delay: 0.35s;
}

.cfm__badge img {
  display: block;
  max-width: 70px;
  max-height: 22px;
  width: auto;
  height: auto;
  object-fit: contain;
}

.cfm__badge--off {
  opacity: 0.28;
  filter: grayscale(1);
}

@keyframes cfm-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes cfm-dash {
  to {
    stroke-dashoffset: -22;
  }
}

@keyframes cfm-ring {
  0% {
    width: 12px;
    height: 12px;
    opacity: 0.65;
  }
  100% {
    width: 140px;
    height: 140px;
    opacity: 0;
  }
}

@keyframes cfm-ring-lg {
  0% {
    width: 16px;
    height: 16px;
    opacity: 0.65;
  }
  100% {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}

@keyframes cfm-ring-xl {
  0% {
    width: 18px;
    height: 18px;
    opacity: 0.7;
  }
  100% {
    width: 260px;
    height: 260px;
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cfm__card,
  .cfm__badge,
  .cfm__wire,
  .cfm__pulse span {
    animation: none;
  }
}
</style>
