<script setup>
import { onMounted, ref } from "vue";

defineProps({
  alt: { type: String, default: "Built to Scale" },
});

/**
 * Figma 786:2929 Growth Chart Animation — 6s infinite loop.
 * Absolute artboard 466×373; keyframes from get_motion_context.
 */
const ASSET = "/images/figma-upi/caps/scale";
const ART_W = 466;
const ART_H = 373;

/** Bars left→right with Figma appear times (fraction of 6s). */
const BARS = [
  { id: "2944", left: 65.81, top: 320.52, w: 25.476, h: 45.464, anim: 1 },
  { id: "2945", left: 101.91, top: 306.88, w: 33.968, h: 59.103, anim: 2 },
  { id: "2946", left: 146.49, top: 288.7, w: 33.968, h: 77.289, anim: 3 },
  { id: "2947", left: 192.13, top: 270.51, w: 33.968, h: 95.474, anim: 4 },
  { id: "2948", left: 237.78, top: 240.96, w: 33.968, h: 125.026, anim: 5 },
  { id: "2931", left: 283, top: 207.5, w: 35, h: 158, anim: 6 },
  { id: "2932", left: 329.07, top: 134.12, w: 36.091, h: 231.866, anim: 7 },
  { id: "2933", left: 376, top: 110.5, w: 36, h: 255, anim: 8 },
];

const CALLOUTS = [
  {
    label: "10K",
    left: 15,
    top: 169.48,
    w: 102,
    h: 100.956,
    valueSize: 22.578,
    anim: 1,
  },
  {
    label: "100K",
    left: 182,
    top: 62.5,
    w: 101.574,
    h: 97.265,
    valueSize: 21.752,
    anim: 2,
  },
  {
    label: "1M+",
    left: 340,
    top: 0.5,
    w: 104.579,
    h: 95.484,
    valueSize: 21.354,
    anim: 3,
  },
];

const reduceMotion = ref(false);

function pct(n, base) {
  return `${(n / base) * 100}%`;
}

function barStyle(bar) {
  return {
    left: pct(bar.left, ART_W),
    top: pct(bar.top, ART_H),
    width: pct(bar.w, ART_W),
    height: pct(bar.h, ART_H),
  };
}

function calloutStyle(c) {
  return {
    left: pct(c.left, ART_W),
    top: pct(c.top, ART_H),
    width: pct(c.w, ART_W),
    height: pct(c.h, ART_H),
    "--value-size": `${c.valueSize}px`,
  };
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});
</script>

<template>
  <div
    class="upi-scale"
    :class="{ 'upi-scale--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div class="upi-scale__art" aria-hidden="true">
      <div class="upi-scale__glow-wrap">
        <img class="upi-scale__glow" :src="`${ASSET}/glow.svg`" alt="" />
      </div>

      <span
        v-for="bar in BARS"
        :key="bar.id"
        class="upi-scale__bar"
        :class="`upi-scale__bar--${bar.anim}`"
        :style="barStyle(bar)"
      />

      <div class="upi-scale__curve-wrap">
        <svg
          class="upi-scale__curve"
          viewBox="0 0 287.098 212.332"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            class="upi-scale__curve-path"
            d="M0 212.332C108.768 204.166 202.36 146.999 287.098 0"
            pathLength="1"
            stroke="#2D6A4F"
            stroke-width="6.21354"
            stroke-linecap="round"
          />
        </svg>
      </div>

      <div class="upi-scale__arrow-wrap">
        <img class="upi-scale__arrow" :src="`${ASSET}/arrow.svg`" alt="" />
      </div>

      <div
        v-for="c in CALLOUTS"
        :key="c.label"
        class="upi-scale__callout"
        :class="`upi-scale__callout--${c.anim}`"
        :style="calloutStyle(c)"
      >
        <p class="upi-scale__callout-value">{{ c.label }}</p>
        <p class="upi-scale__callout-label">Transactions/min</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upi-scale {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
}

.upi-scale__art {
  position: absolute;
  inset: 0;
}

.upi-scale__glow-wrap {
  position: absolute;
  left: calc(56 / 466 * 100%);
  top: calc(18.48 / 373 * 100%);
  width: calc(347.561 / 466 * 100%);
  height: calc(347.775 / 373 * 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.upi-scale__glow {
  width: calc(315.014 / 347.561 * 100%);
  height: auto;
  transform: rotate(6.62deg) skewX(0.27deg);
  opacity: 0.9;
}

.upi-scale__bar {
  position: absolute;
  border-radius: 10.874px 10.874px 0 0;
  background: linear-gradient(180deg, #bde7ff 0%, #79c8ff 100%);
  opacity: 0;
  transform: translateY(-15px);
  will-change: opacity, transform;
}

.upi-scale__curve-wrap {
  position: absolute;
  left: calc(65 / 466 * 100%);
  top: calc(101.66 / 373 * 100%);
  width: calc(297 / 466 * 100%);
  height: calc(225.925 / 373 * 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.upi-scale__curve {
  width: calc(287.098 / 297 * 100%);
  height: auto;
  overflow: visible;
  transform: rotate(2.76deg);
}

.upi-scale__curve-path {
  fill: none;
  stroke-dasharray: 0 1;
  opacity: 0;
}

.upi-scale__arrow-wrap {
  position: absolute;
  left: calc(349 / 466 * 100%);
  top: calc(92.5 / 373 * 100%);
  width: calc(33.845 / 466 * 100%);
  height: calc(33.845 / 373 * 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.3);
  transform-origin: center center;
}

.upi-scale__arrow {
  display: block;
  width: calc(24 / 33.845 * 100%);
  height: auto;
  transform: rotate(-139.32deg);
}

.upi-scale__callout {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  border: 1.2px solid #e8f1fa;
  border-radius: 15.7px;
  background: #ffffff;
  box-shadow: 0 6.27px 20.07px rgba(123, 185, 229, 0.1);
  opacity: 0;
  transform: translateY(10px) scale(0.7);
  transform-origin: center center;
  will-change: opacity, transform;
}

.upi-scale__callout-value {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: var(--value-size, 22px);
  font-weight: 700;
  line-height: 1.1;
  color: #252b37;
  white-space: nowrap;
}

.upi-scale__callout-label {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 400;
  line-height: 16px;
  color: #252b37;
  white-space: nowrap;
}

/* —— Motion: 6s loop, Figma times —— */
.upi-scale--motion .upi-scale__bar {
  animation: upi-scale-bar-1 6s linear infinite;
}
.upi-scale--motion .upi-scale__bar--1 {
  animation-name: upi-scale-bar-1;
}
.upi-scale--motion .upi-scale__bar--2 {
  animation-name: upi-scale-bar-2;
}
.upi-scale--motion .upi-scale__bar--3 {
  animation-name: upi-scale-bar-3;
}
.upi-scale--motion .upi-scale__bar--4 {
  animation-name: upi-scale-bar-4;
}
.upi-scale--motion .upi-scale__bar--5 {
  animation-name: upi-scale-bar-5;
}
.upi-scale--motion .upi-scale__bar--6 {
  animation-name: upi-scale-bar-6;
}
.upi-scale--motion .upi-scale__bar--7 {
  animation-name: upi-scale-bar-7;
}
.upi-scale--motion .upi-scale__bar--8 {
  animation-name: upi-scale-bar-8;
}

.upi-scale--motion .upi-scale__curve-path {
  animation:
    upi-scale-curve-opacity 6s linear infinite,
    upi-scale-curve-draw 6s linear infinite;
}

.upi-scale--motion .upi-scale__arrow-wrap {
  animation: upi-scale-arrow 6s linear infinite;
}

.upi-scale--motion .upi-scale__callout--1 {
  animation: upi-scale-callout-1 6s linear infinite;
}
.upi-scale--motion .upi-scale__callout--2 {
  animation: upi-scale-callout-2 6s linear infinite;
}
.upi-scale--motion .upi-scale__callout--3 {
  animation: upi-scale-callout-3 6s linear infinite;
}

/* Bar times from motion: [0, tIn, tSet, 0.9167, 0.9667, 1] */
@keyframes upi-scale-bar-1 {
  0%,
  3.33% {
    opacity: 0;
    transform: translateY(-15px);
  }
  8.33%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-2 {
  0%,
  8% {
    opacity: 0;
    transform: translateY(-15px);
  }
  13%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-3 {
  0%,
  12.67% {
    opacity: 0;
    transform: translateY(-15px);
  }
  17.67%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-4 {
  0%,
  17.33% {
    opacity: 0;
    transform: translateY(-15px);
  }
  22.33%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-5 {
  0%,
  22% {
    opacity: 0;
    transform: translateY(-15px);
  }
  27%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-6 {
  0%,
  26.67% {
    opacity: 0;
    transform: translateY(-15px);
  }
  31.67%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-7 {
  0%,
  31.33% {
    opacity: 0;
    transform: translateY(-15px);
  }
  36.33%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}
@keyframes upi-scale-bar-8 {
  0%,
  36% {
    opacity: 0;
    transform: translateY(-15px);
  }
  41%,
  91.67% {
    opacity: 1;
    transform: translateY(0);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(-15px);
  }
}

@keyframes upi-scale-curve-opacity {
  0%,
  31.67% {
    opacity: 0;
  }
  33.33%,
  91.67% {
    opacity: 1;
  }
  96.67%,
  100% {
    opacity: 0;
  }
}

@keyframes upi-scale-curve-draw {
  0%,
  33.3% {
    stroke-dasharray: 0 1;
  }
  58.3%,
  91.7% {
    stroke-dasharray: 1 1;
  }
  96.7%,
  100% {
    stroke-dasharray: 0 1;
  }
}

@keyframes upi-scale-arrow {
  0%,
  55% {
    opacity: 0;
    transform: scale(0.3);
  }
  58.33%,
  91.67% {
    opacity: 1;
    transform: scale(1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: scale(0.3);
  }
}

@keyframes upi-scale-callout-1 {
  0%,
  58.33% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
  63.33%,
  91.67% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
}
@keyframes upi-scale-callout-2 {
  0%,
  64.17% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
  69.17%,
  91.67% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
}
@keyframes upi-scale-callout-3 {
  0%,
  70% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
  75%,
  91.67% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(10px) scale(0.7);
  }
}

.upi-scale:not(.upi-scale--motion) .upi-scale__bar,
.upi-scale:not(.upi-scale--motion) .upi-scale__curve-path,
.upi-scale:not(.upi-scale--motion) .upi-scale__arrow-wrap,
.upi-scale:not(.upi-scale--motion) .upi-scale__callout {
  opacity: 1;
  transform: none;
}
.upi-scale:not(.upi-scale--motion) .upi-scale__curve-path {
  stroke-dasharray: 1 1;
}
.upi-scale:not(.upi-scale--motion) .upi-scale__arrow-wrap {
  transform: scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .upi-scale__bar,
  .upi-scale__curve-path,
  .upi-scale__arrow-wrap,
  .upi-scale__callout {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
  .upi-scale__curve-path {
    stroke-dasharray: 1 1 !important;
  }
  .upi-scale__arrow-wrap {
    transform: scale(1) !important;
  }
}
</style>
