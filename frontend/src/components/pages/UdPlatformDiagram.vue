<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { CONNECTORS, VOLUME } from "./udPlatformConnectors.js";

const props = defineProps({
  image: { type: String, required: true },
  alt: { type: String, default: "" },
  width: { type: Number, default: 1291 },
  height: { type: Number, default: 523 },
});

const CYCLE_MS = 3200;
const DRAW_RATIO = 0.55;

const reduceMotion = ref(false);
const chartOffset = ref(1);
const chartOpacity = ref(1);
let rafId = 0;
let cycleStart = 0;

/** Left→right reveal progress shared by stroke + area fill. */
const chartProgress = computed(() => 1 - chartOffset.value);
const areaClipWidth = computed(() => VOLUME.width * chartProgress.value);

function matrixAttr(m) {
  return `matrix(${m.join(" ")})`;
}

function dashAttr(dash) {
  return dash.join(" ");
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

function tick(now) {
  if (!cycleStart) cycleStart = now;
  const t = ((now - cycleStart) % CYCLE_MS) / CYCLE_MS;

  if (t < DRAW_RATIO) {
    const p = easeInOut(t / DRAW_RATIO);
    chartOffset.value = 1 - p;
    chartOpacity.value = 1;
  } else if (t < 0.72) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
  } else if (t < 0.88) {
    chartOffset.value = 0;
    chartOpacity.value = 1 - (t - 0.72) / (0.88 - 0.72);
  } else if (t < 0.9) {
    chartOffset.value = 1;
    chartOpacity.value = 0;
  } else {
    chartOffset.value = 1;
    chartOpacity.value = (t - 0.9) / (1 - 0.9);
  }

  rafId = window.requestAnimationFrame(tick);
}

function startChart() {
  stopChart();
  if (reduceMotion.value) {
    chartOffset.value = 0;
    chartOpacity.value = 1;
    return;
  }
  cycleStart = 0;
  rafId = window.requestAnimationFrame(tick);
}

function stopChart() {
  if (rafId) {
    window.cancelAnimationFrame(rafId);
    rafId = 0;
  }
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startChart();
});

onBeforeUnmount(stopChart);
</script>

<template>
  <div
    class="ud-platform-diagram"
    :class="{ 'ud-platform-diagram--static': reduceMotion }"
  >
    <img
      class="ud-platform-diagram__img"
      :src="image"
      :alt="alt"
      :width="width"
      :height="height"
      decoding="async"
      loading="lazy"
      draggable="false"
    />

    <svg
      class="ud-platform-diagram__fx"
      :viewBox="`0 0 ${width} ${height}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Exact Figma stroke paths + transforms (dots stay in base PNG) -->
      <g class="ud-platform-diagram__connectors">
        <g
          v-for="line in CONNECTORS"
          :key="line.id"
          :transform="matrixAttr(line.matrix)"
        >
          <path
            class="ud-platform-diagram__dash"
            :class="{ 'ud-platform-diagram__dash--rtl': line.matrix[0] < 0 }"
            :d="line.d"
            fill="none"
            stroke="#ffffff"
            :stroke-width="line.strokeWidth"
            stroke-linecap="round"
            stroke-linejoin="round"
            :stroke-dasharray="dashAttr(line.dash)"
          />
        </g>
      </g>

      <!-- Growing volume area + line — 689:3089 / 689:3090 -->
      <g
        :transform="matrixAttr(VOLUME.matrix)"
        :style="{ opacity: chartOpacity }"
      >
        <defs>
          <linearGradient
            id="ud-volume-area-fill"
            x1="0"
            y1="0"
            x2="0"
            y2="1"
          >
            <!-- Figma fill opacity 0.6 × stop a 0.18 → ~0.108 at top -->
            <stop offset="0" stop-color="#2563EB" stop-opacity="0.108" />
            <stop offset="1" stop-color="#2563EB" stop-opacity="0" />
          </linearGradient>
          <clipPath id="ud-volume-area-clip">
            <rect
              x="0"
              y="0"
              :width="areaClipWidth"
              :height="VOLUME.height"
            />
          </clipPath>
        </defs>

        <path
          class="ud-platform-diagram__volume-area"
          :d="VOLUME.areaD"
          fill="url(#ud-volume-area-fill)"
          clip-path="url(#ud-volume-area-clip)"
        />
        <path
          class="ud-platform-diagram__volume"
          pathLength="1"
          :d="VOLUME.d"
          fill="none"
          stroke="#2563EB"
          :stroke-width="VOLUME.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :style="{
            strokeDasharray: 1,
            strokeDashoffset: chartOffset,
          }"
        />
      </g>
    </svg>
  </div>
</template>

<style scoped>
.ud-platform-diagram {
  position: relative;
  width: 100%;
  max-width: 1291px;
  margin-inline: auto;
  line-height: 0;
  border-radius: 16px;
  overflow: hidden;
}

.ud-platform-diagram__img {
  display: block;
  width: 100%;
  height: auto;
}

.ud-platform-diagram__fx {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.ud-platform-diagram__dash {
  animation: ud-platform-dash 1.1s linear infinite;
}

.ud-platform-diagram__dash--rtl {
  animation-name: ud-platform-dash-rtl;
}

.ud-platform-diagram--static .ud-platform-diagram__dash {
  animation: none;
}

@keyframes ud-platform-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes ud-platform-dash-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ud-platform-diagram__dash {
    animation: none;
  }
}
</style>
