<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Payment overview dashboard with methods, volume, and settlements",
  },
});

/**
 * Figma 689:3378 — Centralized Visibility.
 * Connector paths use design-context transforms; artboard matches PNG aspect
 * (571×336) so overlays align with the baked graphic.
 */
const ART_W = 571;
const ART_H = 336;
/** Scale Figma 331.72-tall coords into PNG half-height 336 */
const Y = 336 / 331.72;

function sy(n) {
  return n * Y;
}

function scalePathY(d) {
  return d.replace(/([ML])(-?[\d.]+),(-?[\d.]+)/g, (_, cmd, x, y) => {
    return `${cmd}${x},${(parseFloat(y) * Y).toFixed(2)}`;
  });
}

function scaleDots(dots) {
  return dots.map(([x, y, r]) => [x, y * Y, r]);
}

const PLOT = {
  x: 118.83,
  y: sy(226.68),
  w: 234.86,
  h: sy(58.72),
};

const SERIES = [
  {
    id: "green",
    stroke: "#00C286",
    width: 1.6,
    d: scalePathY(
      "M1.31,53.36L30.66,43.09L60.00,31.35L89.62,36.21L118.75,26.45L148.46,39.68L177.46,29.87L206.84,21.55L236.38,24.47",
    ),
    dots: scaleDots([
      [1.47, 53.82, 1.47],
      [30.83, 43.55, 1.47],
      [60.18, 31.8, 1.47],
      [89.54, 36.7, 1.47],
      [118.9, 26.91, 1.47],
      [148.26, 40.12, 1.47],
      [177.62, 30.34, 1.47],
      [206.97, 22.02, 1.47],
      [236.33, 24.95, 1.47],
    ]),
  },
  {
    id: "blue",
    stroke: "#0066CC",
    width: 1.6,
    d: scalePathY(
      "M1.27,47.99L30.63,34.78L59.94,18.17L89.62,23.00L118.74,12.75L148.46,26.47L177.43,14.71L206.84,6.38L236.39,9.79",
    ),
    dots: scaleDots([
      [1.47, 48.44, 1.22],
      [30.83, 35.23, 1.22],
      [60.18, 18.59, 1.22],
      [89.54, 23.49, 1.22],
      [118.9, 13.21, 1.22],
      [148.26, 26.91, 1.22],
      [177.62, 15.17, 1.22],
      [206.97, 6.85, 1.22],
      [236.33, 10.27, 1.22],
    ]),
  },
];

const GRID = [{ y: sy(14.43) }, { y: sy(29.11) }, { y: sy(43.79) }];

/** KPI values — Figma 689:3472; positions calibrated to PNG */
const KPIS = [
  {
    id: "txns",
    x: 141,
    y: 188,
    cover: { x: 139, y: 183.5, w: 34, h: 10 },
    target: 124580,
    format: (n) => Math.round(n).toLocaleString("en-US"),
  },
  {
    id: "payments",
    x: 227.5,
    y: 188,
    cover: { x: 225.5, y: 183.5, w: 32, h: 10 },
    target: 24.8,
    format: (n) => `₹${n.toFixed(1)}M`,
  },
  {
    id: "settlements",
    x: 308.5,
    y: 188,
    cover: { x: 306.5, y: 183.5, w: 31, h: 10 },
    target: 18.6,
    format: (n) => `₹${n.toFixed(1)}M`,
  },
];

/** Payment Methods donut — Figma 689:3551; calibrated to PNG */
const DONUT = {
  cx: 425.16,
  cy: 222.12,
  r: 20.75,
  stroke: 7,
  coverR: 28,
};

const SEGMENTS = [
  { id: "upi", value: 42, color: "#0066CC" },
  { id: "cards", value: 28, color: "#00C286" },
  { id: "nb", value: 14, color: "#7000FF" },
  { id: "wallets", value: 10, color: "#FFA000" },
  { id: "others", value: 6, color: "#00B8D9" },
];

let cum = 0;
const SEGMENT_LAYOUT = SEGMENTS.map((s) => {
  const start = cum;
  cum += s.value;
  return {
    ...s,
    start,
    rotate: (start / 100) * 360 - 90,
  };
});

const LEGEND = {
  y: 258.25,
  row: 9.9,
};
const PCT_X = 474;
const PCT_COVER = { x: 463, y: LEGEND.y - 2, w: 14, h: 5 * LEGEND.row - 2 };

/**
 * Centerlines with Figma transforms (rotate / flip) from design-context 689:3378.
 * eraseD skips the origin bead so PNG cyan nodes remain.
 */
const CONNECTORS = [
  {
    id: "cards",
    erase: "#ffffff",
    stroke: "url(#ud-vis-conn-stroke)",
    d: scalePathY(
      "M59.24,90.17L63.22,90.61L66.81,92.06L69.86,94.45L72.13,97.60L73.34,100.82L74.32,105.74L74.98,109.94L75.52,113.54L76.06,117.13L76.54,120.34L77.72,124.49L79.85,127.76L82.82,130.30L85.95,131.76",
    ),
    eraseD: scalePathY(
      "M66.81,92.06L69.86,94.45L72.13,97.60L73.34,100.82L74.32,105.74L74.98,109.94L75.52,113.54L76.06,117.13L76.54,120.34L77.72,124.49L79.85,127.76L82.82,130.30L85.95,131.76",
    ),
  },
  {
    id: "upi",
    erase: "#ffffff",
    stroke: "url(#ud-vis-conn-stroke)",
    d: scalePathY(
      "M148.18,87.80L151.70,89.10L154.62,91.20L156.84,94.03L158.18,97.36L158.56,100.51L158.34,105.13L157.89,110.10L157.47,114.54L157.09,118.51L157.22,122.65L158.41,126.05L160.52,128.99L163.02,131.01",
    ),
    eraseD: scalePathY(
      "M154.62,91.20L156.84,94.03L158.18,97.36L158.56,100.51L158.34,105.13L157.89,110.10L157.47,114.54L157.09,118.51L157.22,122.65L158.41,126.05L160.52,128.99L163.02,131.01",
    ),
  },
  {
    id: "netbanking",
    erase: "#05709e",
    stroke: "#ffffff",
    d: scalePathY(
      "M260.23,87.79L262.98,91.22L264.38,95.25L264.32,99.51L263.04,103.04L260.66,106.88L258.00,110.81L255.59,114.30L253.45,117.42L251.35,122.00L251.22,126.56L252.52,130.40",
    ),
    eraseD: scalePathY(
      "M264.38,95.25L264.32,99.51L263.04,103.04L260.66,106.88L258.00,110.81L255.59,114.30L253.45,117.42L251.35,122.00L251.22,126.56L252.52,130.40",
    ),
  },
  {
    id: "wallets",
    erase: "#05709e",
    stroke: "#ffffff",
    d: scalePathY(
      "M365.76,90.17L361.78,90.61L358.19,92.06L355.14,94.45L352.87,97.60L351.66,100.82L350.68,105.74L350.02,109.94L349.48,113.54L348.94,117.13L348.46,120.34L347.28,124.49L345.15,127.76L342.18,130.30L339.05,131.76",
    ),
    eraseD: scalePathY(
      "M358.19,92.06L355.14,94.45L352.87,97.60L351.66,100.82L350.68,105.74L350.02,109.94L349.48,113.54L348.94,117.13L348.46,120.34L347.28,124.49L345.15,127.76L342.18,130.30L339.05,131.76",
    ),
  },
  {
    id: "international",
    erase: "#05709e",
    stroke: "#ffffff",
    d: scalePathY(
      "M445.76,90.17L441.78,90.61L438.19,92.06L435.14,94.45L432.87,97.60L431.66,100.82L430.68,105.74L430.02,109.94L429.48,113.54L428.94,117.13L428.46,120.34L427.28,124.49L425.15,127.76L422.18,130.30L419.05,131.76",
    ),
    eraseD: scalePathY(
      "M438.19,92.06L435.14,94.45L432.87,97.60L431.66,100.82L430.68,105.74L430.02,109.94L429.48,113.54L428.94,117.13L428.46,120.34L427.28,124.49L425.15,127.76L422.18,130.30L419.05,131.76",
    ),
  },
];

const CYCLE_MS = 3200;
const DRAW_RATIO = 0.55;

const reduceMotion = ref(false);
const chartOffset = ref(1);
const chartOpacity = ref(1);
/** Shared 0→1 progress for KPI count-up + donut fill + legend % */
const countFill = ref(0);
const countOpacity = ref(1);
let rafId = 0;
let cycleStart = 0;

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

const segmentVisible = computed(() => {
  const filled = countFill.value * 100;
  return SEGMENT_LAYOUT.map((s) => {
    if (filled <= s.start) return 0;
    if (filled >= s.start + s.value) return s.value;
    return filled - s.start;
  });
});

const pctDisplays = computed(() =>
  SEGMENTS.map((s) => Math.round(s.value * countFill.value)),
);

const kpiDisplays = computed(() =>
  KPIS.map((k) => k.format(k.target * countFill.value)),
);

function tick(now) {
  if (!cycleStart) cycleStart = now;
  const t = ((now - cycleStart) % CYCLE_MS) / CYCLE_MS;

  if (t < DRAW_RATIO) {
    const p = easeInOut(t / DRAW_RATIO);
    chartOffset.value = 1 - p;
    chartOpacity.value = 1;
    countFill.value = p;
    countOpacity.value = 1;
  } else if (t < 0.72) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
    countFill.value = 1;
    countOpacity.value = 1;
  } else if (t < 0.88) {
    const fade = 1 - (t - 0.72) / (0.88 - 0.72);
    chartOffset.value = 0;
    chartOpacity.value = fade;
    countFill.value = 1;
    countOpacity.value = fade;
  } else if (t < 0.9) {
    chartOffset.value = 1;
    chartOpacity.value = 0;
    countFill.value = 0;
    countOpacity.value = 0;
  } else {
    const fadeIn = (t - 0.9) / (1 - 0.9);
    chartOffset.value = 1;
    chartOpacity.value = fadeIn;
    countFill.value = 0;
    countOpacity.value = fadeIn;
  }

  rafId = window.requestAnimationFrame(tick);
}

function start() {
  stop();
  if (reduceMotion.value) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
    countFill.value = 1;
    countOpacity.value = 1;
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
    class="ud-vis"
    :class="{ 'ud-vis--static': reduceMotion }"
  >
    <img
      class="ud-vis__img"
      src="/images/figma-unified-dashboard/features/visibility-graphic.png"
      :alt="alt"
      :width="ART_W"
      :height="ART_H"
      decoding="async"
      loading="lazy"
      draggable="false"
    />

    <svg
      class="ud-vis__fx"
      :viewBox="`0 0 ${ART_W} ${ART_H}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient
          id="ud-vis-conn-stroke"
          x1="0"
          y1="0"
          x2="0"
          y2="1"
        >
          <stop offset="0" stop-color="#0292B8" />
          <stop offset="1" stop-color="#134E66" />
        </linearGradient>
      </defs>

      <g class="ud-vis__connectors">
        <!-- Wide erase: PNG connectors sit ~2–3px off overlay paths -->
        <path
          v-for="c in CONNECTORS"
          :key="`erase-${c.id}`"
          :d="c.eraseD"
          fill="none"
          :stroke="c.erase"
          stroke-width="7"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          v-for="c in CONNECTORS"
          :key="`dash-${c.id}`"
          class="ud-vis__dash"
          :d="c.d"
          fill="none"
          :stroke="c.stroke"
          stroke-width="1.4"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-dasharray="1.5 3.2"
        />
      </g>

      <!-- KPI count-up -->
      <rect
        v-for="k in KPIS"
        :key="`kpi-cover-${k.id}`"
        :x="k.cover.x"
        :y="k.cover.y"
        :width="k.cover.w"
        :height="k.cover.h"
        fill="#ffffff"
      />
      <g :style="{ opacity: countOpacity }">
        <text
          v-for="(k, i) in KPIS"
          :key="`kpi-${k.id}`"
          class="ud-vis__kpi"
          :x="k.x"
          :y="k.y"
          dominant-baseline="central"
        >
          {{ kpiDisplays[i] }}
        </text>
      </g>

      <!-- Payment Methods donut -->
      <circle
        :cx="DONUT.cx"
        :cy="DONUT.cy"
        :r="DONUT.coverR"
        fill="#ffffff"
      />
      <g :style="{ opacity: countOpacity }">
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
      <rect
        :x="PCT_COVER.x"
        :y="PCT_COVER.y"
        :width="PCT_COVER.w"
        :height="PCT_COVER.h"
        fill="#ffffff"
      />
      <g :style="{ opacity: countOpacity }">
        <text
          v-for="(seg, i) in SEGMENTS"
          :key="`pct-${seg.id}`"
          class="ud-vis__pct"
          :x="PCT_X"
          :y="LEGEND.y + i * LEGEND.row"
          text-anchor="end"
          dominant-baseline="central"
        >
          {{ pctDisplays[i] }}%
        </text>
      </g>

      <g :transform="`translate(${PLOT.x} ${PLOT.y})`">
        <rect
          x="-2"
          y="-2"
          :width="PLOT.w + 4"
          :height="PLOT.h + 4"
          fill="#ffffff"
        />

        <line
          v-for="(g, i) in GRID"
          :key="`grid-${i}`"
          x1="1.5"
          :y1="g.y"
          :x2="PLOT.w - 1.5"
          :y2="g.y"
          stroke="#D5D7DA"
          stroke-opacity="0.24"
          stroke-width="0.5"
        />

        <g :style="{ opacity: chartOpacity }">
          <path
            v-for="s in SERIES"
            :key="s.id"
            pathLength="1"
            :d="s.d"
            fill="none"
            :stroke="s.stroke"
            :stroke-width="s.width"
            stroke-linecap="round"
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
    </svg>
  </div>
</template>

<style scoped>
.ud-vis {
  position: relative;
  width: 100%;
  max-width: 571px;
  line-height: 0;
}

.ud-vis__img {
  display: block;
  width: 100%;
  height: auto;
}

.ud-vis__fx {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.ud-vis__dash {
  animation: ud-vis-dash 1.15s linear infinite;
}

.ud-vis__kpi {
  fill: #252b37;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 11px;
  font-weight: 700;
}

.ud-vis__pct {
  fill: #252b37;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 7px;
  font-weight: 700;
}

.ud-vis--static .ud-vis__dash {
  animation: none;
}

@keyframes ud-vis-dash {
  to {
    stroke-dashoffset: -10;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ud-vis__dash {
    animation: none;
  }
}
</style>
