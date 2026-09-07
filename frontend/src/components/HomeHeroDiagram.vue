<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const PRODUCTS = [
  {
    id: "orchestration",
    label: "Orchestration",
    pill: { x: 273, y: 8, w: 133 },
    path: "M342.5 34.5V62.5C342.5 65.8137 339.814 68.5 336.5 68.5H298.5C295.186 68.5 292.5 71.1863 292.5 74.5V121.5",
    dot: { cx: 293.5, cy: 118.5 },
  },
  {
    id: "collections",
    label: "Collections",
    pill: { x: 12, y: 95, w: 114 },
    path: "M206 165H161.505C158.192 165 155.505 162.314 155.505 159V119C155.505 115.686 152.819 113 149.505 113H124",
    dot: { cx: 211.5, cy: 164.5 },
  },
  {
    id: "checkout",
    label: "Hyper Checkout",
    pill: { x: 10, y: 272, w: 160 },
    path: "M209 255H164.505C161.192 255 158.505 257.686 158.505 261V282C158.505 285.314 155.819 288 152.505 288H170",
    dot: { cx: 213.5, cy: 253.5 },
  },
  {
    id: "tsp",
    label: "BaaS",
    pill: { x: 462, y: 162, w: 88 },
    path: "M375.5 164.5H418.5C421.814 164.5 424.5 167.186 424.5 170.5V177C424.5 180.314 427.186 183 430.5 183H462",
    dot: { cx: 375.5, cy: 164.5 },
  },
  {
    id: "withdrawls",
    label: "Withdrawls",
    pill: { x: 218, y: 396, w: 115 },
    path: "M296 306V334C296 337.314 293.314 340 290 340H275C271.686 340 269 342.686 269 346V366.5V393",
    dot: { cx: 295.5, cy: 301.5 },
  },
  {
    id: "whitelabel",
    label: "White Label",
    pill: { x: 474, y: 282, w: 118 },
    path: "M474 301H421.5C418.186 301 415.5 298.314 415.5 295V255.5C415.5 252.186 412.814 249.5 409.5 249.5H379",
    dot: { cx: 373.5, cy: 248.934 },
  },
];

const CYCLE_ORDER = [
  "orchestration",
  "tsp",
  "whitelabel",
  "withdrawls",
  "checkout",
  "collections",
];

const CYCLE_MS = 1800;
const activeIndex = ref(0);
const reduceMotion = ref(false);
const paused = ref(false);
let timer = null;
let resumeTimer = null;

const activeId = computed(() => CYCLE_ORDER[activeIndex.value] || CYCLE_ORDER[0]);

function isActive(id) {
  return reduceMotion.value || activeId.value === id;
}

function startCycle() {
  stopCycle();
  if (reduceMotion.value) return;
  timer = window.setInterval(() => {
    if (!paused.value) {
      activeIndex.value = (activeIndex.value + 1) % CYCLE_ORDER.length;
    }
  }, CYCLE_MS);
}

function stopCycle() {
  if (timer != null) {
    window.clearInterval(timer);
    timer = null;
  }
  if (resumeTimer != null) {
    window.clearTimeout(resumeTimer);
    resumeTimer = null;
  }
}

function focusProduct(index) {
  if (reduceMotion.value) return;
  const cycleIndex = CYCLE_ORDER.indexOf(PRODUCTS[index]?.id);
  activeIndex.value = cycleIndex >= 0 ? cycleIndex : 0;
  paused.value = true;
  if (resumeTimer != null) {
    window.clearTimeout(resumeTimer);
  }
  resumeTimer = window.setTimeout(() => {
    paused.value = false;
  }, CYCLE_MS * 2);
}

onMounted(() => {
  reduceMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startCycle();
});

onUnmounted(stopCycle);
</script>

<template>
  <svg
    class="hero-diagram"
    :class="{ 'hero-diagram--static': reduceMotion }"
    width="604"
    height="454"
    viewBox="0 0 604 454"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="Urbanrupee products: Orchestration, Collections, Checkout, TSP, Withdrawls, and White Label"
  >
    <defs>
      <linearGradient id="heroHubGrad" x1="223" y1="139" x2="362" y2="278" gradientUnits="userSpaceOnUse">
        <stop stop-color="#0292B8" />
        <stop offset="1" stop-color="#134E66" />
      </linearGradient>
      <radialGradient id="heroWaveGlowOuter" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#D9F7FF" stop-opacity="0.95" />
        <stop offset="38%" stop-color="#52D7F3" stop-opacity="0.82" />
        <stop offset="70%" stop-color="#0EA1C7" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#0EA1C7" stop-opacity="0" />
      </radialGradient>
      <radialGradient id="heroWaveGlowMid" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#A8F3FF" stop-opacity="0.9" />
        <stop offset="35%" stop-color="#2CD5F6" stop-opacity="0.75" />
        <stop offset="72%" stop-color="#167D9F" stop-opacity="0.25" />
        <stop offset="100%" stop-color="#167D9F" stop-opacity="0" />
      </radialGradient>
      <mask id="heroOuterRingMask">
        <rect width="604" height="454" fill="black" />
        <circle cx="293.5" cy="208.934" r="86.5" fill="white" />
        <circle cx="293.5" cy="208.934" r="69.5" fill="black" />
      </mask>
      <mask id="heroMidRingMask">
        <rect width="604" height="454" fill="black" />
        <circle cx="293.5" cy="208.934" r="69.5" fill="white" />
        <circle cx="293.5" cy="208.934" r="51.5" fill="black" />
      </mask>
      <linearGradient id="heroPillStroke" x1="0" y1="0" x2="0" y2="42" gradientUnits="userSpaceOnUse">
        <stop stop-color="#0292B8" />
        <stop offset="1" stop-color="#134E66" />
      </linearGradient>
      <linearGradient id="heroConnectorGlow" x1="143" y1="35" x2="473" y2="393" gradientUnits="userSpaceOnUse">
        <stop stop-color="#B9E5F2" />
        <stop offset="1" stop-color="#4FA7C3" />
      </linearGradient>
      <filter id="heroPillShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#134E66" flood-opacity="0.12" />
      </filter>
    </defs>

    <g class="hero-diagram__hub" aria-hidden="true">
      <circle class="hero-diagram__ring hero-diagram__ring--outer" cx="293.5" cy="208.934" r="86.5" fill="#58B9D7" />
      <circle class="hero-diagram__ring hero-diagram__ring--mid" cx="293.5" cy="208.934" r="69.5" fill="url(#heroHubGrad)" />
      <g mask="url(#heroOuterRingMask)" class="hero-diagram__ring-wave hero-diagram__ring-wave--outer">
        <circle cx="293.5" cy="208.934" r="86.5" fill="url(#heroWaveGlowOuter)" />
        <circle class="hero-diagram__ring-wave-secondary" cx="293.5" cy="208.934" r="86.5" fill="url(#heroWaveGlowOuter)" />
      </g>
      <g mask="url(#heroMidRingMask)" class="hero-diagram__ring-wave hero-diagram__ring-wave--mid">
        <circle cx="293.5" cy="208.934" r="69.5" fill="url(#heroWaveGlowMid)" />
        <circle class="hero-diagram__ring-wave-secondary" cx="293.5" cy="208.934" r="69.5" fill="url(#heroWaveGlowMid)" />
      </g>
      <circle cx="293.5" cy="208.934" r="51.5" fill="#ffffff" />
      <image
        class="hero-diagram__hub-logo"
        href="/images/figma-home/hero-diagram/logo.svg"
        x="269.75"
        y="180.4"
        width="47.5949"
        height="57.0833"
        preserveAspectRatio="xMidYMid meet"
      />
    </g>

    <g
      v-for="(item, index) in PRODUCTS"
      :key="item.id"
      class="hero-diagram__node"
      :class="{ 'is-active': isActive(item.id), 'is-dim': !isActive(item.id) && !reduceMotion }"
      @mouseenter="focusProduct(index)"
      @focusin="focusProduct(index)"
      tabindex="0"
      role="button"
      :aria-label="item.label"
    >
      <path :d="item.path" class="hero-diagram__connector hero-diagram__connector--base" />
      <path :d="item.path" class="hero-diagram__connector hero-diagram__connector--live" />
      <circle class="hero-diagram__anchor" :cx="item.dot.cx" :cy="item.dot.cy" r="5.5" />

      <g class="hero-diagram__pill" filter="url(#heroPillShadow)">
        <rect
          class="hero-diagram__pill-fill"
          :x="item.pill.x"
          :y="item.pill.y"
          :width="item.pill.w"
          height="42"
          rx="8"
          fill="#ffffff"
        />
        <rect
          class="hero-diagram__pill-stroke"
          :x="item.pill.x + 0.75"
          :y="item.pill.y + 0.75"
          :width="item.pill.w - 1.5"
          height="40.5"
          rx="7.25"
          fill="none"
          stroke="url(#heroPillStroke)"
          stroke-width="1.5"
        />
        <text
          class="hero-diagram__label"
          :x="item.pill.x + item.pill.w / 2"
          :y="item.pill.y + 26"
          text-anchor="middle"
        >
          {{ item.label }}
        </text>
      </g>
    </g>
  </svg>
</template>

<style scoped>
.hero-diagram {
  display: block;
  width: min(100%, 604px);
  height: auto;
  max-height: 454px;
  overflow: visible;
  font-family: Inter, Manrope, "DM Sans", system-ui, sans-serif;
}

.hero-diagram__ring {
  transform-box: fill-box;
  transform-origin: center;
}

.hero-diagram__hub-logo {
  transform-box: fill-box;
  transform-origin: center;
  animation: hero-logo-float 4.2s ease-in-out infinite;
}

.hero-diagram__ring-wave {
  transform-box: fill-box;
  transform-origin: center;
}

.hero-diagram__ring-wave > circle {
  transform-box: fill-box;
  transform-origin: center;
  animation: hero-ring-wave 2.4s ease-out infinite;
}

.hero-diagram__ring-wave-secondary {
  animation-delay: 1.2s !important;
}

.hero-diagram__node {
  cursor: pointer;
  outline: none;
  transition: opacity 0.28s ease;
}

.hero-diagram__connector {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.hero-diagram__connector--base {
  stroke: #0892b1;
  stroke-width: 1.5;
  stroke-dasharray: 4 4;
  opacity: 0.52;
}

.hero-diagram__connector--live {
  stroke: url(#heroConnectorGlow);
  stroke-width: 2.2;
  stroke-dasharray: 12 18;
  stroke-linecap: round;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.hero-diagram__anchor {
  fill: #38b7d3;
  transition:
    fill 0.25s ease,
    transform 0.25s ease,
    opacity 0.25s ease;
  transform-box: fill-box;
  transform-origin: center;
  opacity: 0.56;
}

.hero-diagram__label {
  fill: #134e66;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0;
}

.hero-diagram__pill {
  transform-box: fill-box;
  transform-origin: center;
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.hero-diagram__pill rect,
.hero-diagram__label {
  transition:
    fill 0.25s ease,
    stroke 0.25s ease,
    color 0.25s ease;
}

.hero-diagram__node.is-dim {
  opacity: 0.32;
}

.hero-diagram__node.is-active .hero-diagram__connector--live {
  opacity: 1;
  animation: hero-path-sweep 1.35s linear infinite;
}

.hero-diagram__node.is-active .hero-diagram__anchor {
  fill: #097495;
  opacity: 1;
  animation: hero-anchor-pulse 1.35s ease-in-out infinite;
}

.hero-diagram__node.is-active .hero-diagram__pill {
  animation: hero-pill-pop 0.55s cubic-bezier(0.22, 1, 0.36, 1);
  filter: none;
}

.hero-diagram__node.is-active .hero-diagram__pill-fill {
  stroke: #0892b1 !important;
  stroke-width: 1.5;
}

.hero-diagram__node.is-active .hero-diagram__pill-stroke {
  stroke: #0892b1 !important;
}

.hero-diagram__node.is-active .hero-diagram__label {
  fill: #0892b1;
}

@keyframes hero-logo-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-1.5px);
  }
}

@keyframes hero-ring-wave {
  0% {
    opacity: 0;
    transform: scale(0.18);
  }
  20% {
    opacity: 0.92;
  }
  65% {
    opacity: 0.4;
  }
  100% {
    opacity: 0;
    transform: scale(1.08);
  }
}

@keyframes hero-path-sweep {
  from {
    stroke-dashoffset: 72;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes hero-anchor-pulse {
  0%,
  100% {
    transform: scale(1);
  }
  35% {
    transform: scale(1.45);
  }
  70% {
    transform: scale(1.08);
  }
}

@keyframes hero-card-float {
  0%,
  100% {
    transform: translateY(4px);
  }
  30% {
    transform: translateY(-3px);
  }
  75% {
    transform: translateY(1px);
  }
}

@keyframes hero-pill-pop {
  0%,
  100% {
    transform: scale(1);
  }
  45% {
    transform: scale(1.045);
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-diagram--static .hero-diagram__ring,
  .hero-diagram--static .hero-diagram__hub-logo,
  .hero-diagram--static .hero-diagram__connector--live,
  .hero-diagram--static .hero-diagram__anchor,
  .hero-diagram--static .hero-diagram__pill {
    animation: none;
  }

  .hero-diagram--static .hero-diagram__connector--live,
  .hero-diagram--static .hero-diagram__pill,
  .hero-diagram--static .hero-diagram__anchor {
    opacity: 1;
  }
}
</style>
