<script>
/** Loop length, and when one play-through has fully faded out (92.86%). */
export const LOOP_MS = 7000;
export const PLAYBACK_MS = 6500;
</script>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, useId } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Operational visibility dashboard with transaction KPIs",
  },
});

const ASSET = "/images/figma-financial-ops/showcase/visibility-flow";
const uid = useId();

/** Numbers count up from 0 while the flow is visible, 0.3s → 1.5s. */
const COUNT_START_MS = 300;
const COUNT_END_MS = 1500;
/** Matches the 95% reset in the keyframes, after the flow has faded out. */
const RESET_MS = LOOP_MS * 0.95;

/**
 * Live text so the values can count up. Positions are Figma 695:6554 frame
 * coordinates; y is the Manrope baseline (box top + 1.066em ascender).
 */
const METRICS = [
  { x: 63.42, y: 268.742, value: 12.4, decimals: 1, prefix: "₹ ", suffix: " Cr", kind: "value" },
  { x: 182.314, y: 268.742, value: 1.2, decimals: 1, suffix: " M", kind: "value" },
  { x: 301.208, y: 268.742, value: 98.5, decimals: 1, suffix: "%", kind: "value" },
  { x: 420.102, y: 268.742, value: 320, decimals: 0, kind: "value" },
  { x: 75.853, y: 289.974, value: 12, decimals: 0, suffix: "%", kind: "trend" },
  { x: 194.747, y: 289.974, value: 8, decimals: 0, suffix: "%", kind: "trend" },
  { x: 313.641, y: 289.974, value: 1.2, decimals: 1, suffix: "%", kind: "trend" },
  { x: 432.535, y: 289.974, value: 16, decimals: 0, suffix: "%", kind: "trend" },
];

const easeOutCubic = (p) => 1 - (1 - p) ** 3;

/** 1 = final values; also the resting state without animation. */
const progress = ref(1);
const labels = computed(() => {
  const eased = easeOutCubic(progress.value);
  return METRICS.map(
    (m) => `${m.prefix || ""}${(m.value * eased).toFixed(m.decimals)}${m.suffix || ""}`
  );
});

const svgEl = ref(null);
const flowEl = ref(null);
let frame = 0;
let observer = null;

function sync() {
  const animation = flowEl.value?.getAnimations?.()[0];
  const time = animation?.currentTime;
  if (typeof time !== "number") {
    progress.value = 1;
    return;
  }
  const t = time % LOOP_MS;
  if (t >= RESET_MS) {
    progress.value = 0;
    return;
  }
  const p = (t - COUNT_START_MS) / (COUNT_END_MS - COUNT_START_MS);
  progress.value = Math.min(1, Math.max(0, p));
}

function tick() {
  sync();
  frame = requestAnimationFrame(tick);
}

function start() {
  if (!frame) frame = requestAnimationFrame(tick);
}

function stop() {
  cancelAnimationFrame(frame);
  frame = 0;
}

onMounted(() => {
  if (typeof IntersectionObserver === "undefined") {
    start();
    return;
  }
  observer = new IntersectionObserver((entries) => {
    if (entries[entries.length - 1].isIntersecting) start();
    else stop();
  });
  observer.observe(svgEl.value);
});

onBeforeUnmount(() => {
  stop();
  observer?.disconnect();
});
</script>

<template>
  <!-- Every layer is a full 604×576 render of Figma 695:6554 (frame at x 6.6). -->
  <svg
    ref="svgEl"
    class="foi-vis"
    viewBox="0 0 604 576"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    :aria-label="alt"
    :style="{ '--foi-vis-dur': `${LOOP_MS}ms` }"
  >
    <defs>
      <clipPath :id="`${uid}-chart`">
        <rect class="foi-vis__reveal" x="58" y="318" width="292" height="118" />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/text.svg`" width="604" height="576" />

    <g ref="flowEl" class="foi-vis__flow">
      <image :href="`${ASSET}/panel.svg`" width="604" height="576" />
      <g transform="translate(6.6025 0)">
        <text
          v-for="(metric, i) in METRICS"
          :key="i"
          :class="`foi-vis__metric foi-vis__metric--${metric.kind}`"
          :x="metric.x"
          :y="metric.y"
        >{{ labels[i] }}</text>
      </g>
      <image
        :href="`${ASSET}/chart.svg`"
        width="604"
        height="576"
        :clip-path="`url(#${uid}-chart)`"
      />
      <g class="foi-vis__marker">
        <image :href="`${ASSET}/marker.svg`" width="604" height="576" />
      </g>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 7s loop (1s ≈ 14.29%): dashboard fades in → metrics count up → chart grows
 * left → right → Today marker appears → everything but the heading fades out.
 */
.foi-vis {
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
  user-select: none;
}

.foi-vis__metric {
  font-family: Manrope, system-ui, sans-serif;
}

.foi-vis__metric--value {
  font-size: 14.4726px;
  font-weight: 700;
  fill: #252b37;
}

.foi-vis__metric--trend {
  font-size: 10px;
  font-weight: 600;
  fill: #20be92;
}

.foi-vis__flow,
.foi-vis__reveal,
.foi-vis__marker {
  animation-duration: var(--foi-vis-dur);
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.foi-vis__flow {
  animation-name: foi-vis-flow;
}

.foi-vis__reveal {
  transform-box: fill-box;
  transform-origin: 0 50%;
  animation-name: foi-vis-grow;
}

.foi-vis__marker {
  animation-name: foi-vis-marker;
}

/*
 * The flow fades in over 0.3s and out at 6.0s → 6.5s. It is fully transparent
 * across the loop boundary, and every child resets at 95% while hidden, so the
 * restart never shows a jump.
 */
@keyframes foi-vis-flow {
  0% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  4.29%,
  85.71% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  92.86%,
  100% {
    opacity: 0;
  }
}

/* Chart areas and both trend lines grow left → right, 0.4s → 1.8s. */
@keyframes foi-vis-grow {
  0%,
  5.71% {
    transform: scaleX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  25.71%,
  95% {
    transform: scaleX(1);
  }
  95.1%,
  100% {
    transform: scaleX(0);
  }
}

/* Today tooltip and marker line, 1.8s → 2.1s. */
@keyframes foi-vis-marker {
  0%,
  25.71% {
    opacity: 0;
    transform: translateY(6px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  30%,
  95% {
    opacity: 1;
    transform: translateY(0);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: translateY(6px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-vis__flow,
  .foi-vis__reveal,
  .foi-vis__marker {
    animation: none;
  }
}
</style>
