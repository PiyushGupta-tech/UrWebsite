<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import HomeHeroConversionCard from "@/components/HomeHeroConversionCard.vue";
import HomeHeroDashboard from "@/components/HomeHeroDashboard.vue";
import HomeHeroPhone from "@/components/HomeHeroPhone.vue";
import HomeHeroRoutingCard from "@/components/HomeHeroRoutingCard.vue";

/* Figma 1001:8597 — fixed 1180×512 composition, scaled to the available width. */
const STAGE_W = 1180;
const ASSET = "/images/figma-home/hero-v2";
const LOGO_MARK = "/logos/favicon.svg";

/*
 * PCB-style traces: straight runs with 45° bends, drawn over the core as SVG and reused
 * as the dots' motion paths. Each starts where the core's old connector left it (the two
 * upward runs fork out of the core's back corner) and runs out to a terminal just outside
 * its node, so dots flow core → node. The banks share one
 * trace into the left bank; the dashed diamond joins them to each other.
 */
const FLOW_PATHS = {
  phone: { length: 262, d: "M445 366 L380 366 L349 397 L196 397" },
  conversion: {
    length: 135,
    d: "M497.8 288.3 L454 288.3 L434 268.3 L434 247.4 L414 227.4 L400 227.4",
  },
  routing: { length: 230, d: "M580 241 L580 150 L497 67 L476 67" },
  dash: { length: 229, d: "M605 241.4 L605 150 L688 67 L708 67" },
  bank: { length: 141, d: "M737 393.5 L826 393.5 L855.5 364 L866 364" },
};

/* Solder pad on each trace's terminal (its last point). */
const TRACE_PADS = Object.values(FLOW_PATHS).map(({ d }) => {
  const [x, y] = d.slice(d.lastIndexOf("L") + 1).trim().split(" ").map(Number);
  return { x, y };
});

/* Stage px per second, so every connector moves at the same speed. */
const FLOW_SPEED = 80;

/* left/top are the resting spots (reduced motion); phase is how far along the path that spot is. */
const RING_DOTS = [
  { left: 361.2, top: 366.4, path: "phone", phase: 0.3 },
  { left: 414.1, top: 227.5, path: "conversion", phase: 0.8 },
  { left: 595.8, top: 163.6, path: "dash", phase: 0.3 },
];

const DOTS = [
  { left: 550.2, top: 120.2, tone: "dark", path: "routing", phase: 0.55 },
  { left: 802.6, top: 388.5, tone: "dark", path: "bank", phase: 0.5 },
];

const BANK_LINES = [
  { id: "644", left: 918, top: 254, w: 89, h: 67, angle: -36.97, length: 111.4 },
  { id: "645", left: 1055, top: 373, w: 69, h: 58, angle: -40.05, length: 90.139 },
  { id: "646", left: 931, top: 381, w: 71, h: 57, angle: 38.76, length: 91.049 },
  { id: "647", left: 1067, top: 267, w: 65, h: 47, angle: 35.87, length: 80.212 },
];

const BANKS = [
  { left: 987, top: 208, w: 87, h: 86.298 },
  { left: 983, top: 412.3, w: 87, h: 86.298 },
  { left: 870, top: 311, w: 84, h: 83 },
  { left: 1096, top: 311, w: 84, h: 83 },
];

/*
 * Chip on top of the core: its top face corners in stage px (it rises CHIP_DEPTH px off the core).
 * A CHIP_GRID × CHIP_GRID dot matrix lies flat on that face through an SVG matrix, so the dots
 * and the favicon they spell take the core's isometric perspective.
 */
const CHIP = { left: [536.5, 321.1], back: [592.9, 287.8], front: [592.9, 354.4] };
const CHIP_DEPTH = 4.8;
const CHIP_GRID = 15;

/* Favicon sampled onto an 11×13 grid: "a" = outer frame, "b" = inner swoosh, "." = unlit. */
const CHIP_LOGO = [
  "aaaaaaaaaaa",
  "aaaaaaaaaaa",
  ".......aaaa",
  "bbbbbb..aaa",
  "bbbbbbb..aa",
  "bbbbbbb..aa",
  "bbbbbb...aa",
  "bbb.....aaa",
  "bbbb..aaaaa",
  "bbbbb..aaaa",
  ".bbbb...aa.",
  "..bbbb..a..",
  "...bbbb....",
];
const CHIP_LOGO_COL = (CHIP_GRID - CHIP_LOGO[0].length) >> 1;
const CHIP_LOGO_ROW = (CHIP_GRID - CHIP_LOGO.length) >> 1;

function chipPoints(points) {
  return points.map(([x, y]) => `${x},${y}`).join(" ");
}

const CHIP_RIGHT = [
  CHIP.back[0] + CHIP.front[0] - CHIP.left[0],
  CHIP.back[1] + CHIP.front[1] - CHIP.left[1],
];
const drop = ([x, y]) => [x, y + CHIP_DEPTH];
const CHIP_FACES = {
  top: chipPoints([CHIP.left, CHIP.back, CHIP_RIGHT, CHIP.front]),
  left: chipPoints([CHIP.left, CHIP.front, drop(CHIP.front), drop(CHIP.left)]),
  right: chipPoints([CHIP.front, CHIP_RIGHT, drop(CHIP_RIGHT), drop(CHIP.front)]),
};

/* Grid x runs left → back corner, grid y runs left → front corner; one unit = one dot cell. */
const CHIP_MATRIX = `matrix(${[
  (CHIP.back[0] - CHIP.left[0]) / CHIP_GRID,
  (CHIP.back[1] - CHIP.left[1]) / CHIP_GRID,
  (CHIP.front[0] - CHIP.left[0]) / CHIP_GRID,
  (CHIP.front[1] - CHIP.left[1]) / CHIP_GRID,
  CHIP.left[0],
  CHIP.left[1],
]
  .map((n) => +n.toFixed(4))
  .join(" ")})`;

const CHIP_DOTS = [];
for (let row = 0; row < CHIP_GRID; row += 1) {
  for (let col = 0; col < CHIP_GRID; col += 1) {
    const mark = CHIP_LOGO[row - CHIP_LOGO_ROW]?.[col - CHIP_LOGO_COL];
    const tone = mark === "a" ? "frame" : mark === "b" ? "swoosh" : null;
    CHIP_DOTS.push({
      x: col + 0.5,
      y: row + 0.5,
      tone,
      /* Sweeps from the chip's left corner to its right corner. */
      delay: tone ? `${((col + row) * 0.07).toFixed(2)}s` : null,
    });
  }
}

/* Faces sit at ±2px; these solid silhouettes fill the gap so the spinning shield reads as ~4px thick. */
const SHIELD_RIM_DEPTHS = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5];

const rootRef = ref(null);
const scale = ref(1);
let resizeObserver = null;

function updateScale() {
  const width = rootRef.value?.clientWidth || STAGE_W;
  scale.value = Math.min(1, width / STAGE_W);
}

function px(value) {
  return `${value}px`;
}

function flowStyle(dot) {
  const { d, length } = FLOW_PATHS[dot.path];
  const duration = length / FLOW_SPEED;
  return {
    "--dot-x": px(dot.left),
    "--dot-y": px(dot.top),
    "--flow-path": `path("${d}")`,
    animationDuration: `${duration.toFixed(2)}s`,
    animationDelay: `${(-dot.phase * duration).toFixed(2)}s`,
  };
}

onMounted(() => {
  updateScale();
  if (typeof ResizeObserver !== "undefined") {
    resizeObserver = new ResizeObserver(updateScale);
    resizeObserver.observe(rootRef.value);
  }
});

onBeforeUnmount(() => {
  resizeObserver?.disconnect();
});
</script>

<template>
  <div
    ref="rootRef"
    class="hero-graphic"
    role="img"
    aria-label="Urbanrupee connects checkout, smart routing, analytics, and banks through one payment infrastructure"
  >
    <div class="hero-graphic__stage" :style="{ transform: `scale(${scale})` }" aria-hidden="true">
      <!-- Core, its traces and the dots share one float so they never drift apart.
           Before the cards/devices so traces and dots slip under them. -->
      <div class="hg-flow">
        <!-- Core stack 990:8005 -->
        <div class="hg-core">
          <img :src="`${ASSET}/core-stack.png`" alt="" width="1774" height="887" decoding="async" />
        </div>

        <!-- Chip with the favicon spelt out in lit dots, lying flat on its top face -->
        <svg class="hg-chip" viewBox="0 0 1180 512" width="1180" height="512">
          <polygon class="hg-chip__side hg-chip__side--left" :points="CHIP_FACES.left" />
          <polygon class="hg-chip__side hg-chip__side--right" :points="CHIP_FACES.right" />
          <polygon class="hg-chip__top" :points="CHIP_FACES.top" />
          <g :transform="CHIP_MATRIX">
            <rect
              class="hg-chip__inset"
              x="0.6"
              y="0.6"
              :width="CHIP_GRID - 1.2"
              :height="CHIP_GRID - 1.2"
            />
            <circle
              v-for="(dot, i) in CHIP_DOTS"
              :key="i"
              class="hg-chip__dot"
              :class="dot.tone && `hg-chip__dot--lit hg-chip__dot--${dot.tone}`"
              :cx="dot.x"
              :cy="dot.y"
              :r="dot.tone ? 0.34 : 0.22"
              :style="dot.delay && { animationDelay: dot.delay }"
            />
          </g>
        </svg>

        <svg class="hg-traces" viewBox="0 0 1180 512" width="1180" height="512">
          <path v-for="(trace, name) in FLOW_PATHS" :key="name" class="hg-traces__line" :d="trace.d" />
          <circle
            v-for="(pad, i) in TRACE_PADS"
            :key="`pad-${i}`"
            class="hg-traces__pad"
            :cx="pad.x"
            :cy="pad.y"
            r="3.5"
          />
        </svg>

        <span v-for="(dot, i) in RING_DOTS" :key="`ring-${i}`" class="hg-ring-dot" :style="flowStyle(dot)">
          <img :src="`${ASSET}/ring-dot.svg`" alt="" width="18" height="18" />
        </span>

        <span v-for="(dot, i) in DOTS" :key="`dot-${i}`" class="hg-dot" :style="flowStyle(dot)">
          <img :src="`${ASSET}/dot-${dot.tone}.svg`" alt="" width="10" height="10" />
        </span>
      </div>

      <div
        v-for="line in BANK_LINES"
        :key="line.id"
        class="hg-bank-line"
        :style="{ left: px(line.left), top: px(line.top), width: px(line.w), height: px(line.h) }"
      >
        <div :style="{ transform: `rotate(${line.angle}deg)` }">
          <div class="hg-bank-line__track" :style="{ width: px(line.length) }">
            <img :src="`${ASSET}/line-${line.id}.svg`" alt="" />
          </div>
        </div>
      </div>

      <HomeHeroConversionCard />
      <HomeHeroRoutingCard />

      <div
        v-for="(bank, i) in BANKS"
        :key="`bank-${i}`"
        class="hg-bank"
        :style="{ left: px(bank.left), top: px(bank.top), width: px(bank.w), height: px(bank.h) }"
      >
        <img :src="`${ASSET}/bank.png`" alt="" width="320" height="299" decoding="async" />
      </div>

      <div class="hg-shield" :style="{ '--shield-src': `url(${ASSET}/shield.png)` }">
        <div class="hg-shield__body">
          <span class="hg-shield__face hg-shield__face--front">
            <img :src="`${ASSET}/shield.png`" alt="" width="192" height="176" decoding="async" />
          </span>
          <span
            v-for="z in SHIELD_RIM_DEPTHS"
            :key="z"
            class="hg-shield__rim"
            :style="{ transform: `translateZ(${z}px)` }"
          />
          <span class="hg-shield__side" />
          <span class="hg-shield__face hg-shield__face--back">
            <img :src="`${ASSET}/shield-blank.png`" alt="" width="192" height="176" decoding="async" />
            <img
              class="hg-shield__logo"
              :src="LOGO_MARK"
              alt=""
              width="31"
              height="37"
              decoding="async"
            />
          </span>
        </div>
      </div>

      <HomeHeroPhone />
      <HomeHeroDashboard />
    </div>
  </div>
</template>

<style scoped>
.hero-graphic {
  position: relative;
  width: 100%;
  max-width: 1180px;
  aspect-ratio: 1180 / 512;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.hero-graphic__stage {
  position: absolute;
  left: 0;
  top: 0;
  width: 1180px;
  height: 512px;
  transform-origin: 0 0;
}

.hero-graphic__stage *,
.hero-graphic__stage *::before,
.hero-graphic__stage *::after {
  box-sizing: border-box;
}

.hero-graphic__stage > * {
  position: absolute;
}

.hero-graphic__stage img {
  display: block;
  max-width: none;
}

/* —— Core stack + flowing layer —— */
.hg-flow {
  inset: 0;
  pointer-events: none;
}

.hg-flow > * {
  position: absolute;
}

.hg-core {
  left: 177px;
  top: 2px;
  width: 828px;
  height: 510px;
  overflow: hidden;
  pointer-events: none;
}

.hg-core img {
  position: absolute;
  left: -17.88%;
  top: -3.35%;
  width: 135.92%;
  height: 110.39%;
}

/* —— Traces —— */
.hg-traces {
  left: 0;
  top: 0;
  overflow: visible;
}

.hg-traces__line {
  fill: none;
  stroke: #45b6da;
  stroke-width: 2;
  stroke-linejoin: miter;
  filter: drop-shadow(0 0 2px rgba(56, 183, 211, 0.45));
}

.hg-traces__pad {
  fill: #ffffff;
  stroke: #45b6da;
  stroke-width: 2;
}

/* —— Chip —— */
.hg-chip {
  left: 0;
  top: 0;
  overflow: visible;
}

.hg-chip__top {
  fill: #0b2a52;
  stroke: #45b6da;
  stroke-width: 1;
  stroke-linejoin: round;
}

.hg-chip__side {
  stroke: #45b6da;
  stroke-width: 0.6;
  stroke-opacity: 0.55;
  stroke-linejoin: round;
}

.hg-chip__side--left {
  fill: #071a36;
}

.hg-chip__side--right {
  fill: #0a2244;
}

.hg-chip__inset {
  fill: none;
  stroke: #45b6da;
  stroke-opacity: 0.35;
  stroke-width: 0.6;
  vector-effect: non-scaling-stroke;
}

.hg-chip__dot {
  fill: #45b6da;
  opacity: 0.3;
}

.hg-chip__dot--lit {
  opacity: 1;
}

.hg-chip__dot--frame {
  fill: #18d4f5;
}

.hg-chip__dot--swoosh {
  fill: #c8f7ff;
}

/* —— Dots —— */
.hg-ring-dot,
.hg-dot {
  left: var(--dot-x);
  top: var(--dot-y);
}

.hg-ring-dot {
  width: 18px;
  height: 18px;
  transform: scaleY(-1);
}

.hg-ring-dot img {
  width: 18px;
  height: 18px;
}

.hg-dot {
  width: 10px;
  height: 10px;
  transform: scaleY(-1);
}

.hg-dot img {
  width: 10px;
  height: 10px;
}

/* —— Bank connectors —— */
.hg-bank-line {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hg-bank-line > div {
  flex: none;
}

.hg-bank-line__track {
  position: relative;
  height: 0;
}

.hg-bank-line__track img {
  position: absolute;
  inset: -1px 0 0 0;
  width: 100%;
  height: 1px;
}

/* —— Banks + shield —— */
.hg-bank {
  overflow: hidden;
}

.hg-bank,
.hg-shield {
  pointer-events: none;
}

.hg-bank img {
  position: absolute;
  left: -9.68%;
  top: -6.57%;
  width: 120.97%;
  height: 113.96%;
}

.hg-shield {
  left: 1009px;
  top: 331.5px;
  width: 36px;
  height: 42px;
  perspective: 160px;
}

.hg-shield__body {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.hg-shield__face,
.hg-shield__rim {
  position: absolute;
  inset: 0;
}

.hg-shield__face {
  overflow: hidden;
  backface-visibility: hidden;
}

.hg-shield__face--front {
  transform: translateZ(2px);
}

/* Its own face turned 180°, so the logo reads correctly from behind instead of mirrored. */
.hg-shield__face--back {
  transform: rotateY(180deg) translateZ(2px);
}

.hg-shield img {
  position: absolute;
  left: -36.36%;
  top: -15.72%;
  width: 175.76%;
  height: 136.56%;
}

/* Centred on the shield's inner face (~27×32 px, centre 17.3, 21.3). */
.hg-shield .hg-shield__logo {
  left: 11.43px;
  top: 14.3px;
  width: 11.73px;
  height: 14px;
}

/* Same crop as the img above, in px, so the silhouette lines up with the faces. */
.hg-shield__rim {
  background: #22324d;
  -webkit-mask: var(--shield-src) -13.09px -6.6px / 63.27px 57.36px no-repeat;
  mask: var(--shield-src) -13.09px -6.6px / 63.27px 57.36px no-repeat;
}

/* Parallel layers vanish when exactly edge-on; this strip is the side wall at 90°. */
.hg-shield__side {
  position: absolute;
  left: calc(50% - 2px);
  top: 1.2px;
  bottom: 1.3px;
  width: 4px;
  border-radius: 2px 2px 2px 2px / 2px 2px 6px 6px;
  background: linear-gradient(#34496b, #1c2a42);
  transform: rotateY(90deg);
}

/* —— Motion —— */
@media (prefers-reduced-motion: no-preference) {
  .hg-flow {
    animation: hg-float 5s ease-in-out infinite;
  }

  .hg-ring-dot img {
    animation: hg-ring-pulse 1.8s ease-in-out infinite;
  }

  .hg-shield {
    animation: hg-shield-bounce 1.2s infinite;
  }

  .hg-shield__body {
    animation: hg-shield-spin 4s linear infinite;
  }

  /* Delay comes inline, so a light sweep runs across the logo's dots. */
  .hg-chip__dot--lit {
    animation: hg-chip-sweep 3.6s ease-in-out infinite;
  }

  /* Duration and delay come inline from each path's length and the dot's phase. */
  @supports (offset-path: path("M 0 0")) {
    .hg-ring-dot,
    .hg-dot {
      left: 0;
      top: 0;
      offset-path: var(--flow-path);
      offset-anchor: center;
      offset-rotate: 0deg;
      animation-name: hg-dot-flow;
      animation-timing-function: linear;
      animation-iteration-count: infinite;
    }
  }

  .hg-routing,
  .hg-conv,
  .hg-dash {
    animation: hg-card-bob 4.8s ease-in-out infinite;
  }

  .hg-conv {
    animation-delay: 0.8s;
  }

  .hg-dash {
    animation-delay: 1.6s;
  }
}

@keyframes hg-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@keyframes hg-ring-pulse {
  0%,
  100% {
    transform: scale(1);
    filter: none;
  }
  50% {
    transform: scale(1.18);
    filter: drop-shadow(0 0 4px rgba(56, 183, 211, 0.75));
  }
}

@keyframes hg-shield-spin {
  from {
    transform: rotateY(0deg);
  }
  to {
    transform: rotateY(360deg);
  }
}

@keyframes hg-chip-sweep {
  0%,
  30%,
  100% {
    opacity: 1;
  }
  15% {
    opacity: 0.45;
  }
}

/* Ease-out on the way up, ease-in on the way down, so it lands like a bounce. */
@keyframes hg-shield-bounce {
  0%,
  100% {
    translate: 0 0;
    animation-timing-function: cubic-bezier(0.33, 1, 0.68, 1);
  }
  50% {
    translate: 0 -5px;
    animation-timing-function: cubic-bezier(0.32, 0, 0.67, 0);
  }
}

@keyframes hg-dot-flow {
  0% {
    offset-distance: 0%;
    opacity: 0;
  }
  8%,
  92% {
    opacity: 1;
  }
  100% {
    offset-distance: 100%;
    opacity: 0;
  }
}

@keyframes hg-card-bob {
  0%,
  100% {
    translate: 0 0;
  }
  50% {
    translate: 0 -3px;
  }
}
</style>
