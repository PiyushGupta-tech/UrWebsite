<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: { type: String, default: "Reliable Connectivity" },
});

/**
 * Arrow growth matches CustomCheckoutFeatureBranding chart draw:
 * pathLength=1 + strokeDashoffset 1→0 (rAF), origin dots on outer nodes,
 * triangle head follows the drawing tip via getPointAtLength.
 */
const ASSET = "/images/figma-upi/caps/connectivity";
const CYCLE_MS = 2400;
const DRAW_RATIO = 0.45;

/** Centerline of arrow-left.png (174×30), head excluded */
const PATH_LEFT =
  "M1 11 C18 18, 35 28, 52 27 S78 14, 95 5 S125 1, 150 7";
/** Centerline of arrow-right.png flipped to point left toward hub */
const PATH_RIGHT =
  "M170 12 C153 18, 136 26, 119 27 S93 14, 76 5 S46 1, 21 7";

const reduceMotion = ref(false);
const leftOffset = ref(1);
const rightOffset = ref(1);
const leftOpacity = ref(1);
const rightOpacity = ref(1);

const leftHead = reactive({ x: 0, y: 0, angle: 0, show: false });
const rightHead = reactive({ x: 0, y: 0, angle: 0, show: false });

const leftPathEl = ref(null);
const rightPathEl = ref(null);

let rafId = 0;
let cycleStart = 0;

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

function updateHead(pathEl, head, progress) {
  if (!pathEl || progress < 0.04) {
    head.show = false;
    return;
  }
  const len = pathEl.getTotalLength();
  const d = Math.min(len, progress * len);
  const p = pathEl.getPointAtLength(d);
  const p0 = pathEl.getPointAtLength(Math.max(0, d - 3));
  head.x = p.x;
  head.y = p.y;
  head.angle = (Math.atan2(p.y - p0.y, p.x - p0.x) * 180) / Math.PI;
  head.show = true;
}

function phaseOffset(t, delay) {
  const local = (t - delay + 1) % 1;
  if (local < DRAW_RATIO) {
    const p = easeInOut(local / DRAW_RATIO);
    return { offset: 1 - p, opacity: 1, progress: p };
  }
  if (local < 0.72) {
    return { offset: 0, opacity: 1, progress: 1 };
  }
  if (local < 0.88) {
    const fade = 1 - (local - 0.72) / (0.88 - 0.72);
    return { offset: 0, opacity: fade, progress: 1 };
  }
  if (local < 0.9) {
    return { offset: 1, opacity: 0, progress: 0 };
  }
  const show = (local - 0.9) / (1 - 0.9);
  return { offset: 1, opacity: show, progress: 0 };
}

function tick(now) {
  if (!cycleStart) cycleStart = now;
  const t = ((now - cycleStart) % CYCLE_MS) / CYCLE_MS;

  const L = phaseOffset(t, 0);
  const R = phaseOffset(t, 0.12);
  leftOffset.value = L.offset;
  leftOpacity.value = L.opacity;
  rightOffset.value = R.offset;
  rightOpacity.value = R.opacity;

  updateHead(leftPathEl.value, leftHead, L.progress);
  updateHead(rightPathEl.value, rightHead, R.progress);

  rafId = window.requestAnimationFrame(tick);
}

function start() {
  stop();
  if (reduceMotion.value) {
    leftOffset.value = 0;
    rightOffset.value = 0;
    leftOpacity.value = 1;
    rightOpacity.value = 1;
    updateHead(leftPathEl.value, leftHead, 1);
    updateHead(rightPathEl.value, rightHead, 1);
    return;
  }
  cycleStart = 0;
  rafId = window.requestAnimationFrame(tick);
}

function stop() {
  if (rafId) {
    window.cancelAnimationFrame(rafId);
    rafId = 0;
  }
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // next frame so path refs exist for getTotalLength
  requestAnimationFrame(() => start());
});

onBeforeUnmount(stop);
</script>

<template>
  <div
    class="upi-conn"
    :class="{ 'upi-conn--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="upi-conn__glow"
      :src="`${ASSET}/glow.svg`"
      alt=""
      width="380"
      height="340"
    />

    <div class="upi-conn__stage" aria-hidden="true">
      <div class="upi-conn__node upi-conn__node--primary">
        <div class="upi-conn__node-icon">
          <img
            class="upi-conn__server-glow"
            :src="`${ASSET}/server-glow.svg`"
            alt=""
          />
          <img
            class="upi-conn__glyph"
            :src="`${ASSET}/globe.svg`"
            alt=""
            width="38"
            height="38"
          />
        </div>
        <p class="upi-conn__label">Primary<br />Server</p>
      </div>

      <div class="upi-conn__hub">
        <div class="upi-conn__badge">
          <img :src="`${ASSET}/status-dot.svg`" alt="" width="14" height="14" />
          <span>Always Connected</span>
        </div>
        <div class="upi-conn__rings">
          <img
            class="upi-conn__ring upi-conn__ring--outer"
            :src="`${ASSET}/ring-outer.svg`"
            alt=""
          />
          <img
            class="upi-conn__ring upi-conn__ring--mid"
            :src="`${ASSET}/ring-mid.svg`"
            alt=""
          />
          <img
            class="upi-conn__ring upi-conn__ring--inner"
            :src="`${ASSET}/ring-inner.svg`"
            alt=""
          />
          <img class="upi-conn__hub-base" :src="`${ASSET}/hub.svg`" alt="" />
          <img
            class="upi-conn__wifi"
            :src="`${ASSET}/wifi.svg`"
            alt=""
            width="67"
            height="57"
          />
        </div>
      </div>

      <div class="upi-conn__node upi-conn__node--backup">
        <div class="upi-conn__node-icon">
          <img
            class="upi-conn__server-glow"
            :src="`${ASSET}/server-glow.svg`"
            alt=""
          />
          <img
            class="upi-conn__glyph"
            :src="`${ASSET}/tower.svg`"
            alt=""
            width="38"
            height="38"
          />
        </div>
        <p class="upi-conn__label">Backup<br />Server</p>
      </div>

      <!-- Left connector: origin on Primary → grows into hub -->
      <div class="upi-conn__link upi-conn__link--left">
        <img
          class="upi-conn__point"
          :src="`${ASSET}/point-a.svg`"
          alt=""
          width="10"
          height="10"
        />
        <svg
          class="upi-conn__chart"
          viewBox="0 0 174 30"
          preserveAspectRatio="xMidYMid meet"
        >
          <path
            ref="leftPathEl"
            class="upi-conn__chart-path"
            pathLength="1"
            :d="PATH_LEFT"
            fill="none"
            stroke="#2D6A4F"
            stroke-width="2.25"
            stroke-linecap="round"
            stroke-linejoin="round"
            :style="{
              strokeDasharray: 1,
              strokeDashoffset: leftOffset,
              opacity: leftOpacity,
            }"
          />
          <polygon
            class="upi-conn__head"
            points="0,-4.5 9,0 0,4.5"
            fill="#2D6A4F"
            :opacity="leftHead.show ? leftOpacity : 0"
            :transform="`translate(${leftHead.x} ${leftHead.y}) rotate(${leftHead.angle})`"
          />
        </svg>
      </div>

      <!-- Right connector: origin on Backup → grows into hub -->
      <div class="upi-conn__link upi-conn__link--right">
        <svg
          class="upi-conn__chart"
          viewBox="0 0 174 30"
          preserveAspectRatio="xMidYMid meet"
        >
          <path
            ref="rightPathEl"
            class="upi-conn__chart-path"
            pathLength="1"
            :d="PATH_RIGHT"
            fill="none"
            stroke="#2D6A4F"
            stroke-width="2.25"
            stroke-linecap="round"
            stroke-linejoin="round"
            :style="{
              strokeDasharray: 1,
              strokeDashoffset: rightOffset,
              opacity: rightOpacity,
            }"
          />
          <polygon
            class="upi-conn__head"
            points="0,-4.5 9,0 0,4.5"
            fill="#2D6A4F"
            :opacity="rightHead.show ? rightOpacity : 0"
            :transform="`translate(${rightHead.x} ${rightHead.y}) rotate(${rightHead.angle})`"
          />
        </svg>
        <img
          class="upi-conn__point"
          :src="`${ASSET}/point-a.svg`"
          alt=""
          width="10"
          height="10"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.upi-conn {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
}

.upi-conn__glow {
  position: absolute;
  left: 14%;
  top: 18%;
  width: 72%;
  height: auto;
  opacity: 0.9;
  pointer-events: none;
}

.upi-conn__stage {
  position: absolute;
  inset: 8% 2% 6%;
}

.upi-conn__node {
  position: absolute;
  width: 72px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 3;
}

.upi-conn__node--primary {
  left: 2%;
  top: 8%;
}

.upi-conn__node--backup {
  right: 2%;
  top: 48%;
}

.upi-conn__node-icon {
  position: relative;
  width: 67px;
  height: 67px;
}

.upi-conn__server-glow,
.upi-conn__glyph {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.upi-conn__glyph {
  inset: 22%;
  width: 56%;
  height: 56%;
}

.upi-conn__label {
  margin: 0;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 18px;
  text-align: center;
  color: #252b37;
}

.upi-conn__hub {
  position: absolute;
  left: 50%;
  top: 42%;
  width: 228px;
  height: 250px;
  transform: translate(-50%, -50%);
  z-index: 1;
}

.upi-conn__badge {
  position: absolute;
  left: 50%;
  top: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 7px 16px rgba(21, 156, 255, 0.13);
  transform: translateX(-50%);
  white-space: nowrap;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
}

.upi-conn__badge img {
  display: block;
  width: 14px;
  height: 14px;
}

.upi-conn__rings {
  position: absolute;
  left: 50%;
  top: 28px;
  width: 228px;
  height: 228px;
  transform: translateX(-50%);
}

.upi-conn__ring,
.upi-conn__hub-base,
.upi-conn__wifi {
  position: absolute;
  display: block;
  max-width: none;
}

.upi-conn__ring {
  transform-origin: center center;
}

.upi-conn__ring--outer {
  inset: 0;
  width: 100%;
  height: 100%;
}

.upi-conn__ring--mid {
  inset: 10.6%;
  width: 78.8%;
  height: 78.8%;
}

.upi-conn__ring--inner {
  inset: 20%;
  width: 60%;
  height: 60%;
}

.upi-conn__hub-base {
  /* Figma 296:2704 — 99.208 / 227.746 */
  inset: 28%;
  width: 44%;
  height: 44%;
}

.upi-conn__wifi {
  /* Keep Figma aspect 67.29×56.94 — never force a square box */
  left: 50%;
  top: 50%;
  width: 28%;
  height: auto;
  max-height: 28%;
  aspect-ratio: 67.29 / 56.94;
  transform: translate(-50%, -48%);
  object-fit: contain;
}

.upi-conn__link {
  position: absolute;
  z-index: 2;
  display: flex;
  align-items: center;
  pointer-events: none;
  line-height: 0;
}

.upi-conn__link--left {
  left: 14%;
  top: 24%;
  width: 120px;
  transform: rotate(18deg);
  transform-origin: left center;
}

.upi-conn__link--right {
  right: 13%;
  top: 44%;
  width: 120px;
  transform: rotate(-10deg);
  transform-origin: right center;
}

.upi-conn__point {
  position: relative;
  z-index: 2;
  display: block;
  width: 10px;
  height: 10px;
  flex-shrink: 0;
  margin: 0 -3px;
}

.upi-conn__chart {
  flex: 1;
  min-width: 0;
  height: 28px;
  overflow: visible;
}

.upi-conn__chart-path {
  transition: none;
}

.upi-conn__head {
  transition: none;
}

.upi-conn--motion .upi-conn__ring--outer {
  animation: upi-conn-ring-outer 2.4s ease-in-out infinite;
}
.upi-conn--motion .upi-conn__ring--mid {
  animation: upi-conn-ring-mid 2.4s ease-in-out 0.2s infinite;
}
.upi-conn--motion .upi-conn__ring--inner {
  animation: upi-conn-ring-inner 2.4s ease-in-out 0.4s infinite;
}

.upi-conn--motion .upi-conn__badge {
  animation: upi-conn-badge 3.2s ease-in-out infinite;
}

.upi-conn--motion .upi-conn__point {
  animation: upi-conn-point 2.4s ease-in-out infinite;
}
.upi-conn--motion .upi-conn__link--right .upi-conn__point {
  animation-delay: 0.28s;
}

@keyframes upi-conn-ring-outer {
  0%,
  100% {
    transform: scale(0.9);
    opacity: 0.35;
  }
  50% {
    transform: scale(1.08);
    opacity: 0.95;
  }
}

@keyframes upi-conn-ring-mid {
  0%,
  100% {
    transform: scale(0.94);
    opacity: 0.45;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

@keyframes upi-conn-ring-inner {
  0%,
  100% {
    transform: scale(0.96);
    opacity: 0.55;
  }
  50% {
    transform: scale(1.03);
    opacity: 1;
  }
}

@keyframes upi-conn-badge {
  0%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-3px);
  }
}

@keyframes upi-conn-point {
  0%,
  100% {
    opacity: 0.65;
    transform: scale(0.85);
  }
  40%,
  55% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@media (prefers-reduced-motion: reduce) {
  .upi-conn__ring--outer,
  .upi-conn__ring--mid,
  .upi-conn__ring--inner,
  .upi-conn__badge,
  .upi-conn__point {
    animation: none !important;
  }

  .upi-conn__point {
    opacity: 1;
    transform: none;
  }
}
</style>
