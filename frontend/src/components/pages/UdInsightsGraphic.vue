<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Revenue by payment method and transaction volume trend charts",
  },
});

/**
 * Figma 689:3805 — Performance Insights.
 * PNG backdrop + SVG overlays: donut fill + legend count-up,
 * triple sparkline draw (cfb-style), static dotted plot grid.
 */
const ART_W = 600;
const ART_H = 304;

/** Transaction Volume card — Figma 689:3854 */
const VOLUME_CARD = { x: 340, y: 126.5, w: 260, h: 177.28 };

const PLOT = { x: 376.33, y: 166.29, w: 223.67, h: 85.15 };

/** Cover width: full plot up to inside the card border (hides baked area-fill leftover) */
const PLOT_COVER_W = VOLUME_CARD.x + VOLUME_CARD.w - PLOT.x - 2;

/** Graphs must not extend past the dotted grid line end */
const CHART_END = 210;

/** Revenue donut — Figma 689:3956; center calibrated to insights PNG */
const DONUT = {
  cx: 70.48,
  cy: 124.86,
  r: 45.4,
  stroke: 12,
  /** Solid white disc covering the whole baked ring + fringe */
  coverR: 56,
};

const SEGMENTS = [
  { id: "upi", value: 42, color: "#1890ff" },
  { id: "cards", value: 28, color: "#8e52ff" },
  { id: "nb", value: 14, color: "#ff5b5b" },
  { id: "wallets", value: 10, color: "#ffae34" },
  { id: "others", value: 6, color: "#00c48c" },
];

let cum = 0;
const SEGMENT_LAYOUT = SEGMENTS.map((s) => {
  const start = cum;
  cum += s.value;
  return {
    ...s,
    start,
    /** Degrees from 12 o'clock, clockwise */
    rotate: (start / 100) * 360 - 90,
  };
});

/** Legend % column — Figma 689:3965 */
const LEGEND = {
  y: 80.35,
  row: 19.78,
};
/** Right edge of baked % glyphs — text-anchor end */
const PCT_X = 279.67;
const PCT_COVER = { x: 262, y: LEGEND.y - 1, w: 22, h: 5 * LEGEND.row - 4 };

const SERIES = [
  {
    id: "ok",
    stroke: "#00C48C",
    width: 1.5,
    d: "M1.38,56.30L26.36,39.27L52.35,44.86L76.97,33.55L102.82,36.34L127.49,25.03L153.34,27.82L177.98,13.70L203.92,19.32",
    dots: [
      [26.68, 39.74, 1.42],
      [52.23, 45.41, 1.42],
      [77.21, 34.06, 1.42],
      [102.75, 36.9, 1.42],
      [127.73, 25.55, 1.42],
      [153.28, 28.38, 1.42],
      [178.25, 14.19, 1.42],
      [203.8, 19.87, 1.42],
    ],
  },
  {
    id: "pending",
    stroke: "#FFAE34",
    width: 1.5,
    d: "M1.47,67.61L26.45,56.25L52.11,50.54L77.39,59.07L102.63,53.38L127.85,59.05L153.15,53.38L178.13,47.70L203.68,42.02",
    dots: [
      [26.68, 56.77, 1.42],
      [52.23, 51.09, 1.42],
      [77.21, 59.61, 1.42],
      [102.75, 53.93, 1.42],
      [127.73, 59.61, 1.42],
      [153.28, 53.93, 1.42],
      [178.25, 48.25, 1.42],
      [203.8, 42.58, 1.42],
    ],
  },
  {
    id: "fail",
    stroke: "#FF5B5B",
    width: 1.5,
    d: "M1.58,76.08L26.55,70.41L52.23,70.39L77.21,70.39L102.69,67.56L127.79,70.40L153.15,64.73L178.25,64.72L203.86,67.56",
    dots: [
      [26.68, 70.96, 1.42],
      [52.23, 70.96, 1.42],
      [77.21, 70.96, 1.42],
      [102.75, 68.12, 1.42],
      [127.73, 70.96, 1.42],
      [153.28, 65.28, 1.42],
      [178.25, 65.28, 1.42],
      [203.8, 68.12, 1.42],
    ],
  },
];

const GRID = [
  { y: 0.28, w: CHART_END },
  { y: 28.38, w: CHART_END },
  { y: 56.2, w: CHART_END },
  { y: 84.87, w: CHART_END },
];

const CYCLE_MS = 3200;
const DRAW_RATIO = 0.55;

const reduceMotion = ref(false);
const chartOffset = ref(1);
const chartOpacity = ref(1);
/** 0 → 1 ring fill progress (also drives legend count-up) */
const donutFill = ref(0);
const donutOpacity = ref(1);
let rafId = 0;
let cycleStart = 0;

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

const segmentVisible = computed(() => {
  const filled = donutFill.value * 100;
  return SEGMENT_LAYOUT.map((s) => {
    if (filled <= s.start) return 0;
    if (filled >= s.start + s.value) return s.value;
    return filled - s.start;
  });
});

const pctDisplays = computed(() =>
  SEGMENTS.map((s) => Math.round(s.value * donutFill.value)),
);

/** Center revenue: ₹0.0M → ₹24.8M with donut fill */
const REVENUE_TARGET = 24.8;
const revenueDisplay = computed(() => {
  const n = REVENUE_TARGET * donutFill.value;
  return `₹${n.toFixed(1)}M`;
});

function tick(now) {
  if (!cycleStart) cycleStart = now;
  const t = ((now - cycleStart) % CYCLE_MS) / CYCLE_MS;

  if (t < DRAW_RATIO) {
    const p = easeInOut(t / DRAW_RATIO);
    chartOffset.value = 1 - p;
    chartOpacity.value = 1;
    donutFill.value = p;
    donutOpacity.value = 1;
  } else if (t < 0.72) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
    donutFill.value = 1;
    donutOpacity.value = 1;
  } else if (t < 0.88) {
    const fade = 1 - (t - 0.72) / (0.88 - 0.72);
    chartOffset.value = 0;
    chartOpacity.value = fade;
    donutFill.value = 1;
    donutOpacity.value = fade;
  } else if (t < 0.9) {
    chartOffset.value = 1;
    chartOpacity.value = 0;
    donutFill.value = 0;
    donutOpacity.value = 0;
  } else {
    const fadeIn = (t - 0.9) / (1 - 0.9);
    chartOffset.value = 1;
    chartOpacity.value = fadeIn;
    donutFill.value = 0;
    donutOpacity.value = fadeIn;
  }

  rafId = window.requestAnimationFrame(tick);
}

function start() {
  stop();
  if (reduceMotion.value) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
    donutFill.value = 1;
    donutOpacity.value = 1;
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
  start();
});

onBeforeUnmount(stop);
</script>

<template>
  <div
    class="ud-ins"
    :class="{ 'ud-ins--static': reduceMotion }"
  >
    <img
      class="ud-ins__img"
      src="/images/figma-unified-dashboard/features/insights-graphic.png"
      :alt="alt"
      :width="ART_W"
      :height="ART_H"
      decoding="async"
      loading="lazy"
      draggable="false"
    />

    <svg
      class="ud-ins__fx"
      :viewBox="`0 0 ${ART_W} ${ART_H}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="none"
    >
      <defs>
        <clipPath id="ud-ins-plot-clip">
          <!-- Start after the axis gutter so lines don't rebuild the start markers -->
          <rect
            x="8"
            y="0"
            :width="CHART_END - 8"
            :height="PLOT.h"
          />
        </clipPath>
      </defs>

      <!-- Cover entire baked donut (ring + fringe); center label redrawn below -->
      <circle
        :cx="DONUT.cx"
        :cy="DONUT.cy"
        :r="DONUT.coverR"
        fill="#ffffff"
      />
      <!-- Revenue donut: fill clockwise -->
      <g :style="{ opacity: donutOpacity }">
        <circle
          v-for="(seg, i) in SEGMENT_LAYOUT"
          :key="seg.id"
          :cx="DONUT.cx"
          :cy="DONUT.cy"
          :r="DONUT.r"
          fill="none"
          :stroke="seg.color"
          :stroke-width="DONUT.stroke"
          stroke-linecap="butt"
          pathLength="100"
          :transform="`rotate(${seg.rotate} ${DONUT.cx} ${DONUT.cy})`"
          :style="{
            strokeDasharray: `${segmentVisible[i]} 100`,
          }"
        />
      </g>
      <!-- Center label (PNG text was covered with the disc) -->
      <g :style="{ opacity: donutOpacity }">
        <text
          class="ud-ins__donut-value"
          :x="DONUT.cx"
          :y="DONUT.cy - 4"
          text-anchor="middle"
          dominant-baseline="central"
        >
          {{ revenueDisplay }}
        </text>
        <text
          class="ud-ins__donut-label"
          :x="DONUT.cx"
          :y="DONUT.cy + 10"
          text-anchor="middle"
          dominant-baseline="central"
        >
          Revenue
        </text>
      </g>

      <!-- Legend % cover + growing numbers -->
      <rect
        :x="PCT_COVER.x"
        :y="PCT_COVER.y"
        :width="PCT_COVER.w"
        :height="PCT_COVER.h"
        fill="#ffffff"
      />
      <g :style="{ opacity: donutOpacity }">
        <text
          v-for="(seg, i) in SEGMENTS"
          :key="`pct-${seg.id}`"
          class="ud-ins__pct"
          :x="PCT_X"
          :y="LEGEND.y + i * LEGEND.row + 6"
          text-anchor="end"
          dominant-baseline="central"
        >
          {{ pctDisplays[i] }}%
        </text>
      </g>

      <g :transform="`translate(${PLOT.x} ${PLOT.y})`">
        <!-- Cover baked chart; extend left to hide PNG start dots (sit ~1–2px left of plot) -->
        <rect
          x="-6"
          y="-2"
          :width="PLOT_COVER_W + 6"
          :height="PLOT.h + 4"
          fill="#ffffff"
        />

        <g clip-path="url(#ud-ins-plot-clip)">
          <g class="ud-ins__grid">
            <line
              v-for="(g, i) in GRID"
              :key="`grid-${i}`"
              x1="0"
              :y1="g.y"
              :x2="g.w"
              :y2="g.y"
              stroke="#C5CDD8"
              stroke-width="0.75"
              stroke-dasharray="2.4 3.6"
            />
          </g>

          <g :style="{ opacity: chartOpacity }">
            <path
              v-for="s in SERIES"
              :key="s.id"
              class="ud-ins__line"
              pathLength="1"
              :d="s.d"
              fill="none"
              :stroke="s.stroke"
              :stroke-width="s.width"
              stroke-linecap="butt"
              stroke-linejoin="round"
              :style="{
                strokeDasharray: 1,
                strokeDashoffset: chartOffset,
              }"
            />
            <g
              v-for="s in SERIES"
              :key="`${s.id}-dots`"
            >
              <circle
                v-for="(dot, i) in s.dots"
                :key="`${s.id}-d-${i}`"
                :cx="dot[0]"
                :cy="dot[1]"
                :r="dot[2]"
                :fill="s.stroke"
                :style="{
                  opacity: chartOffset < 0.02 ? 1 : 0,
                }"
              />
            </g>
          </g>
        </g>
      </g>

      <!-- Restore Transaction Volume card edge -->
      <rect
        :x="VOLUME_CARD.x + 0.5"
        :y="VOLUME_CARD.y + 0.5"
        :width="VOLUME_CARD.w - 1"
        :height="VOLUME_CARD.h - 1"
        fill="none"
        stroke="#e2e8f0"
        stroke-width="1"
        rx="12"
        ry="12"
      />
    </svg>
  </div>
</template>

<style scoped>
.ud-ins {
  position: relative;
  width: 100%;
  max-width: 600px;
  line-height: 0;
}

.ud-ins__img {
  display: block;
  width: 100%;
  height: auto;
}

.ud-ins__fx {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.ud-ins__pct {
  fill: #252b37;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0;
}

.ud-ins__donut-value {
  fill: #252b37;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 12px;
  font-weight: 700;
}

.ud-ins__donut-label {
  fill: #535862;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 8px;
  font-weight: 500;
}
</style>
