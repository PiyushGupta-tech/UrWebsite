<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Beneficiary list with initiate payout flow and transfer status",
  },
});

/**
 * Figma 812:2574 — Payout Flow Animation (7s loop).
 * Wires use exact Figma SVG geometry (812:2575 / 2685 / 2688).
 * Draw + card order: Initiate → Scheduled → In Progress → Transfer completed.
 */
const ASSET = "/images/figma-payouts/control";

const VENDORS = [
  {
    name: "Acme Supplies",
    role: "Vendor 1",
    last4: "4321",
    avatar: `${ASSET}/avatar-1.jpg`,
  },
  {
    name: "Brightline Traders",
    role: "Vendor 2",
    last4: "3765",
    avatar: `${ASSET}/avatar-2.png`,
  },
  {
    name: "Nova Retail",
    role: "Vendor 3",
    last4: "7345",
    avatar: `${ASSET}/avatar-3.jpg`,
  },
  {
    name: "Apex Solutions",
    role: "Vendor 4",
    last4: "8734",
    avatar: `${ASSET}/avatar-4.jpg`,
  },
];

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});

onBeforeUnmount(() => {});
</script>

<template>
  <div
    class="po-ben"
    :class="{ 'po-ben--static': reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <!-- Beneficiaries card — always visible -->
    <div class="po-ben__card">
      <div class="po-ben__card-head">
        <p class="po-ben__card-title">Beneficiaries</p>
        <div class="po-ben__add">
          <img
            :src="`${ASSET}/plus.svg`"
            alt=""
            width="24"
            height="24"
          />
          <span>Add Beneficiary</span>
        </div>
      </div>
      <ul class="po-ben__list">
        <li
          v-for="(v, i) in VENDORS"
          :key="v.name"
          class="po-ben__row"
          :class="{ 'po-ben__row--last': i === VENDORS.length - 1 }"
        >
          <div class="po-ben__who">
            <img
              class="po-ben__avatar"
              :src="v.avatar"
              alt=""
              width="24"
              height="24"
            />
            <div class="po-ben__meta">
              <span class="po-ben__name">{{ v.name }}</span>
              <span class="po-ben__role">{{ v.role }}</span>
            </div>
          </div>
          <div class="po-ben__acct">
            <span class="po-ben__dots" aria-hidden="true">
              <i /><i /><i /><i />
            </span>
            <span class="po-ben__last4">{{ v.last4 }}</span>
            <img
              class="po-ben__chevron"
              :src="`${ASSET}/chevron.svg`"
              alt=""
              width="15"
              height="15"
            />
          </div>
        </li>
      </ul>
    </div>

    <!--
      Exact Figma wires (812:2575 connector, 812:2685 arrow1, 812:2688 arrow2).
      Positions match absoluteBoundingBox / node origin in artboard 765×411.
    -->
    <div
      class="po-ben__wire po-ben__wire--connector po-ben__anim po-ben__anim--connector"
      aria-hidden="true"
    >
      <div class="po-ben__wire-rot">
        <img
          class="po-ben__wire-img po-ben__wire-img--connector"
          :src="`${ASSET}/connector.svg`"
          alt=""
          draggable="false"
          decoding="async"
        />
      </div>
    </div>

    <div
      class="po-ben__wire po-ben__wire--arrow1 po-ben__anim po-ben__anim--arrow1"
      aria-hidden="true"
    >
      <img
        class="po-ben__wire-img po-ben__wire-img--arrow1"
        :src="`${ASSET}/arrow1.svg`"
        alt=""
        draggable="false"
        decoding="async"
      />
    </div>

    <!-- arrow2: exact Figma paths; mask draws bottom→mid then mid→top -->
    <svg
      class="po-ben__wire po-ben__wire--arrow2 po-ben__anim po-ben__anim--arrow2"
      viewBox="0 0 39.6479 169.287"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <linearGradient
          id="po-ben-a2-bot"
          x1="32.2153"
          y1="124.33"
          x2="0.380022"
          y2="124.33"
          gradientUnits="userSpaceOnUse"
        >
          <stop stop-color="#0292B8" />
          <stop offset="1" stop-color="#134E66" />
        </linearGradient>
        <linearGradient
          id="po-ben-a2-top"
          x1="32.2153"
          y1="46.4631"
          x2="0.380022"
          y2="46.4631"
          gradientUnits="userSpaceOnUse"
        >
          <stop stop-color="#0292B8" />
          <stop offset="1" stop-color="#134E66" />
        </linearGradient>
        <linearGradient
          id="po-ben-a2-ring"
          x1="6"
          y1="0"
          x2="6"
          y2="12"
          gradientUnits="userSpaceOnUse"
        >
          <stop stop-color="#0292B8" />
          <stop offset="1" stop-color="#134E66" />
        </linearGradient>
        <mask
          id="po-ben-mask-a2-bot"
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="40"
          height="170"
        >
          <path
            class="po-ben__reveal po-ben__reveal--a2-bot"
            pathLength="1"
            d="M32.2153 160.037L17.8621 153.926C10.14 150.638 4.25806 144.116 1.78263 136.096C0.853968 133.088 0.429883 129.946 0.527585 126.799L0.568572 125.479C0.995267 111.734 9.12208 99.4002 21.5831 93.585L32.2153 88.6232"
            stroke="#fff"
            stroke-width="10"
            stroke-linecap="round"
            stroke-linejoin="round"
            fill="none"
          />
        </mask>
        <mask
          id="po-ben-mask-a2-top"
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="40"
          height="170"
        >
          <path
            class="po-ben__reveal po-ben__reveal--a2-top"
            pathLength="1"
            d="M32.2153 87.7628L19.8994 81.5954C10.8647 77.071 4.21561 68.8754 1.6506 59.1021C0.807804 55.8909 0.424486 52.5764 0.512091 49.2575L0.568982 47.1022C1.00444 30.605 9.51053 15.3727 23.3271 6.34793L25.1408 5.16329"
            stroke="#fff"
            stroke-width="10"
            stroke-linecap="round"
            stroke-linejoin="round"
            fill="none"
          />
        </mask>
      </defs>

      <!-- Bottom: Scheduled → In Progress (reversed Line 625) -->
      <path
        d="M32.2153 160.037L17.8621 153.926C10.14 150.638 4.25806 144.116 1.78263 136.096C0.853968 133.088 0.429883 129.946 0.527585 126.799L0.568572 125.479C0.995267 111.734 9.12208 99.4002 21.5831 93.585L32.2153 88.6232"
        stroke="url(#po-ben-a2-bot)"
        stroke-width="1"
        stroke-dasharray="3.4 10"
        stroke-linecap="round"
        stroke-linejoin="round"
        mask="url(#po-ben-mask-a2-bot)"
      />

      <!-- Top: In Progress → Transfer completed (reversed Line 626) -->
      <path
        d="M32.2153 87.7628L19.8994 81.5954C10.8647 77.071 4.21561 68.8754 1.6506 59.1021C0.807804 55.8909 0.424486 52.5764 0.512091 49.2575L0.568982 47.1022C1.00444 30.605 9.51053 15.3727 23.3271 6.34793L25.1408 5.16329"
        stroke="url(#po-ben-a2-top)"
        stroke-width="1"
        stroke-dasharray="3.4 10"
        stroke-linecap="round"
        stroke-linejoin="round"
        mask="url(#po-ben-mask-a2-top)"
      />

      <g class="po-ben__a2-hub po-ben__a2-hub--bot">
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 38.4196 157.061)"
          fill="white"
        />
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 38.4196 157.061)"
          stroke="url(#po-ben-a2-ring)"
        />
        <circle
          cx="4.5"
          cy="4.5"
          r="4.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 37.9397 158.58)"
          fill="#38B7D3"
        />
      </g>
      <g class="po-ben__a2-hub po-ben__a2-hub--mid">
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 37.4196 82.0606)"
          fill="white"
        />
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 37.4196 82.0606)"
          stroke="url(#po-ben-a2-ring)"
        />
        <circle
          cx="4.5"
          cy="4.5"
          r="4.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 36.9397 83.5803)"
          fill="#38B7D3"
        />
      </g>
      <g class="po-ben__a2-hub po-ben__a2-hub--top">
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 36.4197 0.0606099)"
          fill="white"
        />
        <rect
          x="-0.489974"
          y="0.509829"
          width="11"
          height="11"
          rx="5.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 36.4197 0.0606099)"
          stroke="url(#po-ben-a2-ring)"
        />
        <circle
          cx="4.5"
          cy="4.5"
          r="4.5"
          transform="matrix(-0.999803 0.0198545 0.0198545 0.999803 35.9398 1.58027)"
          fill="#38B7D3"
        />
      </g>
    </svg>

    <!-- Initiate payout -->
    <div class="po-ben__initiate po-ben__anim po-ben__anim--initiate">
      <div class="po-ben__initiate-btn">
        <div class="po-ben__initiate-inner">
          <img
            :src="`${ASSET}/paper-plane.svg`"
            alt=""
            width="21"
            height="21"
          />
        </div>
      </div>
      <div class="po-ben__initiate-label">
        <span>Initiate</span>
        <span>Payout</span>
      </div>
    </div>

    <!-- Status toasts: DOM order top→bottom matches Figma; visibility timed bottom→top -->
    <div class="po-ben__toasts">
      <div class="po-ben__toast po-ben__toast--done po-ben__anim po-ben__anim--done">
        <div class="po-ben__toast-icon po-ben__toast-icon--done">
          <img
            :src="`${ASSET}/check-circle.svg`"
            alt=""
            width="17"
            height="17"
          />
        </div>
        <div class="po-ben__toast-copy">
          <strong>Transfer completed</strong>
          <span>$940.00 sent to Acme Ltd.</span>
        </div>
      </div>
      <div class="po-ben__toast po-ben__toast--progress po-ben__anim po-ben__anim--progress">
        <img
          :src="`${ASSET}/clock.svg`"
          alt=""
          width="24"
          height="24"
        />
        <strong>In Progress</strong>
      </div>
      <div class="po-ben__toast po-ben__toast--sched po-ben__anim po-ben__anim--sched">
        <div class="po-ben__toast-icon po-ben__toast-icon--sched">
          <img
            :src="`${ASSET}/three-dots.svg`"
            alt=""
            width="14"
            height="14"
          />
        </div>
        <strong>Scheduled</strong>
      </div>
    </div>

    <!-- Cursor -->
    <div
      class="po-ben__cursor po-ben__anim po-ben__anim--cursor"
      aria-hidden="true"
    >
      <img
        :src="`${ASSET}/cursor.svg`"
        alt=""
        width="24"
        height="24"
      />
    </div>
  </div>
</template>

<style scoped>
.po-ben {
  --po-ben-ink: #252b37;
  --po-ben-muted: #535862;
  --po-ben-brand: #097495;
  position: relative;
  width: 100%;
  max-width: 765px;
  aspect-ratio: 765 / 411;
  container-type: inline-size;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  overflow: hidden;
}

.po-ben__card {
  position: absolute;
  left: 0;
  top: calc(62 / 411 * 100%);
  width: calc(365.4 / 765 * 100%);
  height: calc(281 / 411 * 100%);
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 3cqi, 23px);
  padding: clamp(10px, 2cqi, 15px) clamp(14px, 3cqi, 23px);
  border-radius: clamp(6px, 1cqi, 8px);
  background: #fff;
  box-shadow: 0 3.8px 9.6px rgba(37, 43, 55, 0.12);
  box-sizing: border-box;
}

.po-ben__card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}

.po-ben__card-title {
  margin: 0;
  font-size: clamp(11px, 2.1cqi, 16px);
  font-weight: 600;
  color: var(--po-ben-ink);
  white-space: nowrap;
}

.po-ben__add {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 4px 8px;
  border-radius: 4px;
  background: var(--po-ben-brand);
  color: #fff;
  font-size: clamp(9px, 1.6cqi, 12px);
  font-weight: 500;
  white-space: nowrap;
}

.po-ben__add img {
  width: clamp(14px, 3.1cqi, 24px);
  height: auto;
  display: block;
}

.po-ben__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(6px, 1.5cqi, 12px);
  min-height: 0;
  flex: 1;
}

.po-ben__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(8px, 2cqi, 24px);
  padding-bottom: clamp(4px, 1cqi, 8px);
  border-bottom: 1px solid #e9eaeb;
}

.po-ben__row--last {
  border-bottom: none;
  padding-bottom: 0;
}

.po-ben__who {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1cqi, 8px);
  min-width: 0;
}

.po-ben__avatar {
  width: clamp(18px, 3.1cqi, 24px);
  height: clamp(18px, 3.1cqi, 24px);
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.po-ben__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.po-ben__name {
  font-size: clamp(9px, 1.6cqi, 12px);
  font-weight: 600;
  color: var(--po-ben-ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.po-ben__role {
  font-size: clamp(8px, 1.3cqi, 10px);
  font-weight: 400;
  color: var(--po-ben-muted);
}

.po-ben__acct {
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8cqi, 6px);
  flex-shrink: 0;
}

.po-ben__dots {
  display: flex;
  gap: 2px;
}

.po-ben__dots i {
  width: clamp(5px, 1.1cqi, 8px);
  height: clamp(5px, 1.1cqi, 8px);
  border-radius: 50%;
  background: #252b37;
  display: block;
}

.po-ben__last4 {
  font-size: clamp(9px, 1.6cqi, 12px);
  color: #717680;
}

.po-ben__chevron {
  width: clamp(10px, 2cqi, 15px);
  height: auto;
  transform: rotate(90deg);
  opacity: 0.55;
}

/* —— Exact Figma wire placement —— */
.po-ben__wire {
  position: absolute;
  pointer-events: none;
  overflow: visible;
}

/* 812:2575 — outer fade; inner applies Figma absoluteTransform */
.po-ben__wire--connector {
  left: calc(387.488 / 765 * 100%);
  top: calc(182 / 411 * 100%);
  width: calc(58.2367 / 765 * 100%);
  height: calc(49.5167 / 411 * 100%);
}

.po-ben__wire-rot {
  width: 100%;
  height: 100%;
  transform: matrix(0.717582, 0.696474, -0.696474, 0.717582, 0, 0);
  transform-origin: 0 0;
}

.po-ben__wire-img--connector {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
}

/* 812:2685 arrow1 */
.po-ben__wire--arrow1 {
  left: calc(448.367 / 765 * 100%);
  top: calc(247.781 / 411 * 100%);
  width: calc(116.058 / 765 * 100%);
  height: calc(70.97 / 411 * 100%);
}

.po-ben__wire-img--arrow1 {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
}

/* 812:2688 arrow2 — SVG slightly larger than frame for stroke overflow */
.po-ben__wire--arrow2 {
  left: calc(528.969 / 765 * 100%);
  top: calc(149.949 / 411 * 100%);
  width: calc(39.6479 / 765 * 100%);
  height: calc(169.287 / 411 * 100%);
  overflow: visible;
}

.po-ben__reveal {
  fill: none;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
}

.po-ben__a2-hub {
  opacity: 0;
}

.po-ben__initiate {
  position: absolute;
  left: calc(385.56 / 765 * 100%);
  top: calc(234.57 / 411 * 100%);
  width: calc(75 / 765 * 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.po-ben__initiate-btn {
  width: clamp(40px, 8.9cqi, 68px);
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #fff;
  border: 0.5px solid rgba(226, 232, 240, 0.72);
  box-shadow:
    0 0.86px 0.86px rgba(0, 0, 0, 0.1),
    0 0.86px 1.3px rgba(0, 0, 0, 0.1);
}

.po-ben__initiate-inner {
  width: 70.5%;
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--po-ben-brand);
}

.po-ben__initiate-inner img {
  width: 43%;
  height: auto;
  display: block;
}

.po-ben__initiate-label {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px 8px;
  border-radius: 6px;
  background: #fff;
  box-shadow: 0 0.86px 0.86px rgba(0, 0, 0, 0.08);
  font-size: clamp(9px, 1.6cqi, 12px);
  font-weight: 600;
  color: var(--po-ben-ink);
  line-height: 1.25;
  text-align: center;
}

.po-ben__toasts {
  position: absolute;
  left: calc(568 / 765 * 100%);
  top: calc(127 / 411 * 100%);
  width: calc(200 / 765 * 100%);
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 3.1cqi, 24px);
}

.po-ben__toast {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.8cqi, 14px);
  padding: clamp(8px, 1.8cqi, 14px);
  border-radius: 8px;
  background: #fff;
  border: 1px solid #f1f5f9;
  box-sizing: border-box;
}

.po-ben__toast--done {
  width: 100%;
}

.po-ben__toast--progress,
.po-ben__toast--sched {
  width: fit-content;
  max-width: 100%;
}

.po-ben__toast-icon {
  display: grid;
  place-items: center;
  width: clamp(18px, 3.1cqi, 24px);
  height: clamp(18px, 3.1cqi, 24px);
  border-radius: 50%;
  flex-shrink: 0;
}

.po-ben__toast-icon--done {
  background: #d1fae5;
}

.po-ben__toast-icon--sched {
  border: 1.7px solid #717680;
}

.po-ben__toast-copy {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.po-ben__toast strong {
  font-size: clamp(10px, 1.6cqi, 12px);
  font-weight: 700;
  color: var(--po-ben-ink);
  white-space: nowrap;
}

.po-ben__toast--progress strong,
.po-ben__toast--sched strong {
  font-size: clamp(11px, 2.1cqi, 16px);
  font-weight: 600;
  color: #717680;
}

.po-ben__toast-copy span {
  font-size: clamp(9px, 1.6cqi, 12px);
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.po-ben__cursor {
  position: absolute;
  left: calc(100 / 765 * 100%);
  top: calc(100 / 411 * 100%);
  width: calc(24 / 765 * 100%);
  z-index: 5;
  pointer-events: none;
}

.po-ben__cursor img {
  display: block;
  width: 100%;
  height: auto;
}

/* —— 7s loop —— */
.po-ben__anim {
  animation-duration: 7s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.po-ben__anim--cursor {
  animation-name: po-ben-cursor;
  will-change: transform, opacity;
}

.po-ben__anim--connector {
  animation-name: po-ben-fade-connector;
}

.po-ben__wire-img--connector {
  animation: po-ben-draw-connector 7s linear infinite;
}

.po-ben__anim--initiate {
  animation-name: po-ben-initiate;
  transform-origin: center top;
  will-change: transform, opacity;
}

.po-ben__anim--arrow1 {
  animation-name: po-ben-fade-arrow1;
}

.po-ben__wire-img--arrow1 {
  animation: po-ben-draw-arrow1 7s linear infinite;
}

.po-ben__anim--arrow2 {
  animation-name: po-ben-fade-arrow2;
}

.po-ben__reveal--a2-bot {
  animation: po-ben-draw-a2-bot 7s linear infinite;
}

.po-ben__reveal--a2-top {
  animation: po-ben-draw-a2-top 7s linear infinite;
}

.po-ben__a2-hub--bot {
  animation: po-ben-hub-a2-bot 7s linear infinite;
}

.po-ben__a2-hub--mid {
  animation: po-ben-hub-a2-mid 7s linear infinite;
}

.po-ben__a2-hub--top {
  animation: po-ben-hub-a2-top 7s linear infinite;
}

.po-ben__anim--sched {
  animation-name: po-ben-sched;
  will-change: transform, opacity;
}

.po-ben__anim--progress {
  animation-name: po-ben-progress;
  will-change: transform, opacity;
}

.po-ben__anim--done {
  animation-name: po-ben-done;
  will-change: transform, opacity;
}

@keyframes po-ben-cursor {
  0%,
  4.29% {
    opacity: 0;
    transform: translate(-50px, 0);
  }
  7.14% {
    opacity: 1;
    transform: translate(-50px, 0);
  }
  14.29%,
  78.57% {
    opacity: 1;
    transform: translate(210px, 10px);
  }
  85.71%,
  100% {
    opacity: 0;
    transform: translate(210px, 10px);
  }
}

/*
 * Strict gate: draw segment fully → then show that node’s card → then next segment.
 * 1) connector → Initiate
 * 2) arrow1 → Scheduled
 * 3) a2-bot → In Progress
 * 4) a2-top → Transfer completed
 */
@keyframes po-ben-fade-connector {
  0%,
  15% {
    opacity: 0;
  }
  16%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

/* Card → Initiate hub */
@keyframes po-ben-draw-connector {
  0%,
  16% {
    clip-path: inset(0 100% 0 0);
  }
  24%,
  78.57% {
    clip-path: inset(0 0 0 0);
  }
  85.71%,
  100% {
    clip-path: inset(0 100% 0 0);
  }
}

/* Only after connector arrives */
@keyframes po-ben-initiate {
  0%,
  24% {
    opacity: 0;
    transform: scale(0.5);
  }
  28%,
  78.57% {
    opacity: 1;
    transform: scale(1);
  }
  85.71%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes po-ben-fade-arrow1 {
  0%,
  28% {
    opacity: 0;
  }
  29%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

/* Initiate → Scheduled hub (starts after Initiate is visible) */
@keyframes po-ben-draw-arrow1 {
  0%,
  29% {
    clip-path: inset(0 100% 0 0);
  }
  37%,
  78.57% {
    clip-path: inset(0 0 0 0);
  }
  85.71%,
  100% {
    clip-path: inset(0 100% 0 0);
  }
}

/* arrow2 group on once Scheduled is ready (hubs live here) */
@keyframes po-ben-fade-arrow2 {
  0%,
  36.5% {
    opacity: 0;
  }
  37%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

/* Scheduled → In Progress (starts after Scheduled card) */
@keyframes po-ben-draw-a2-bot {
  0%,
  41% {
    stroke-dashoffset: 1;
  }
  48%,
  78.57% {
    stroke-dashoffset: 0;
  }
  85.71%,
  100% {
    stroke-dashoffset: 1;
  }
}

/* In Progress → Transfer completed (starts after Progress card) */
@keyframes po-ben-draw-a2-top {
  0%,
  52% {
    stroke-dashoffset: 1;
  }
  59%,
  78.57% {
    stroke-dashoffset: 0;
  }
  85.71%,
  100% {
    stroke-dashoffset: 1;
  }
}

/* Hubs appear with their destination card (when line arrives) */
@keyframes po-ben-hub-a2-bot {
  0%,
  36.5% {
    opacity: 0;
  }
  37.5%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

@keyframes po-ben-hub-a2-mid {
  0%,
  47.5% {
    opacity: 0;
  }
  48.5%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

@keyframes po-ben-hub-a2-top {
  0%,
  58.5% {
    opacity: 0;
  }
  59.5%,
  78.57% {
    opacity: 1;
  }
  85.71%,
  100% {
    opacity: 0;
  }
}

/* Cards only after their inbound line finishes */
@keyframes po-ben-sched {
  0%,
  37% {
    opacity: 0;
    transform: translateX(-20px);
  }
  40%,
  78.57% {
    opacity: 1;
    transform: translateX(0);
  }
  85.71%,
  100% {
    opacity: 0;
    transform: translateX(0);
  }
}

@keyframes po-ben-progress {
  0%,
  48% {
    opacity: 0;
    transform: translateX(-20px);
  }
  51%,
  78.57% {
    opacity: 1;
    transform: translateX(0);
  }
  85.71%,
  100% {
    opacity: 0;
    transform: translateX(0);
  }
}

@keyframes po-ben-done {
  0%,
  59% {
    opacity: 0;
    transform: translateX(-20px);
  }
  62%,
  78.57% {
    opacity: 1;
    transform: translateX(0);
  }
  85.71%,
  100% {
    opacity: 0;
    transform: translateX(0);
  }
}

.po-ben--static .po-ben__anim {
  animation: none;
  opacity: 1;
  transform: none;
}

.po-ben--static .po-ben__wire-img--connector,
.po-ben--static .po-ben__wire-img--arrow1 {
  animation: none !important;
  clip-path: none;
}

.po-ben--static .po-ben__reveal {
  animation: none !important;
  stroke-dashoffset: 0;
}

.po-ben--static .po-ben__a2-hub {
  animation: none !important;
  opacity: 1;
}

.po-ben--static .po-ben__cursor {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .po-ben__anim {
    animation: none;
    opacity: 1;
    transform: none;
  }

  .po-ben__wire-img--connector,
  .po-ben__wire-img--arrow1 {
    animation: none !important;
    clip-path: none;
  }

  .po-ben__reveal {
    animation: none !important;
    stroke-dashoffset: 0;
  }

  .po-ben__a2-hub {
    animation: none !important;
    opacity: 1;
  }

  .po-ben__cursor {
    opacity: 0;
  }
}
</style>
