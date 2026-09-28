<script>
export const LOOP_MS = 8000;
</script>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, useId } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Settlement reconciliation dashboard showing matched transactions and an amount mismatch detail",
  },
});

/** Full 642×365 canvases cut from "Frame 2147226717.svg" (Figma 461:7690). */
const ASSET = "/images/figma-reconciliation/showcase-matching";
const uid = useId();

/** Table row tops; each row is 20.866 tall and starts at x 14.072. */
const ROW_TOPS = [245.66, 266.525, 287.393, 308.258, 329.123];
const ROWS = ROW_TOPS.map((top, i) => ({ n: i + 1, cy: top + 10.433 }));

/** Difference counts ₹0 → ₹150 while the pop-up settles, 3.2s → 4.2s. */
const DIFFERENCE = 150;
const COUNT_START_MS = 3200;
const COUNT_END_MS = 4200;
/** Matches the 95% reset, after the pop-up has faded out. */
const RESET_MS = LOOP_MS * 0.95;

const easeOutCubic = (p) => 1 - (1 - p) ** 3;

/** 1 = final value; also the resting state without animation. */
const progress = ref(1);
const amount = computed(() => `₹${(DIFFERENCE * easeOutCubic(progress.value)).toFixed(2)}`);

const svgEl = ref(null);
const popupEl = ref(null);
let frame = 0;
let observer = null;

function sync() {
  const time = popupEl.value?.getAnimations?.()[0]?.currentTime;
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
  <svg
    ref="svgEl"
    class="rc-matching"
    viewBox="0 0 642 365"
    width="642"
    height="365"
    fill="none"
    role="img"
    :aria-label="alt"
    :style="{ '--rc-matching-dur': `${LOOP_MS}ms` }"
  >
    <defs>
      <clipPath :id="`${uid}-connector`">
        <rect class="rc-matching__connector-reveal" x="394" y="183" width="74" height="80" />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/background.svg`" width="642" height="365" />
    <g class="rc-matching__connector" :clip-path="`url(#${uid}-connector)`">
      <image :href="`${ASSET}/connector.svg`" width="642" height="365" />
    </g>

    <image :href="`${ASSET}/table.svg`" width="642" height="365" />
    <g class="rc-matching__flag">
      <image :href="`${ASSET}/row-flag.svg`" width="642" height="365" />
    </g>
    <g class="rc-matching__scan" :transform="`translate(0 ${ROW_TOPS[0]})`">
      <g class="rc-matching__scan-move">
        <rect x="14.0723" width="368.284" height="20.866" fill="#097495" fill-opacity="0.08" />
        <rect x="14.0723" width="2" height="20.866" fill="#097495" />
      </g>
    </g>
    <g
      v-for="row in ROWS"
      :key="row.n"
      :class="`rc-matching__status rc-matching__status--${row.n}`"
      :style="{ transformOrigin: `314px ${row.cy}px` }"
    >
      <image :href="`${ASSET}/status-${row.n}.svg`" width="642" height="365" />
    </g>

    <g ref="popupEl" class="rc-matching__popup">
      <image :href="`${ASSET}/popup.svg`" width="642" height="365" />
      <text class="rc-matching__amount" x="486.207" y="154.23">{{ amount }}</text>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 8s loop (1s = 12.5%). A highlight scans down the rows and each status ticks
 * in as it passes; row 3 turns red with "Difference", the dotted line draws
 * to the Amount Mismatch pop-up, which fades in while ₹150 counts up; the scan
 * then finishes rows 4–5. At 7s → 7.5s the statuses, red row, line and pop-up
 * fade out, leaving the table as it started; transforms reset at 95%.
 */
.rc-matching {
  display: block;
  pointer-events: none;
  user-select: none;
}

.rc-matching__connector,
.rc-matching__connector-reveal,
.rc-matching__flag,
.rc-matching__scan-move,
.rc-matching__status,
.rc-matching__popup {
  transform-box: view-box;
  animation-duration: var(--rc-matching-dur);
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rc-matching__connector {
  animation-name: rc-matching-connector;
}

.rc-matching__connector-reveal {
  transform-box: fill-box;
  transform-origin: 0 50%;
  animation-name: rc-matching-draw;
}

.rc-matching__flag {
  animation-name: rc-matching-flag;
}

/* Hidden at rest; the scan only exists while animating. */
.rc-matching__scan {
  opacity: 0;
  animation: rc-matching-scan var(--rc-matching-dur) linear infinite;
}

.rc-matching__scan-move {
  animation-name: rc-matching-scan-move;
}

.rc-matching__status--1 {
  animation-name: rc-matching-status-1;
}

.rc-matching__status--2 {
  animation-name: rc-matching-status-2;
}

.rc-matching__status--3 {
  animation-name: rc-matching-status-3;
}

.rc-matching__status--4 {
  animation-name: rc-matching-status-4;
}

.rc-matching__status--5 {
  animation-name: rc-matching-status-5;
}

.rc-matching__popup {
  animation-name: rc-matching-popup;
}

.rc-matching__amount {
  font-family: Manrope, sans-serif;
  font-size: 12px;
  font-weight: 600;
  fill: #991b1b;
}

@keyframes rc-matching-scan {
  0%,
  3.75% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  6.25%,
  63.75% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  66.25%,
  100% {
    opacity: 0;
  }
}

/* Row steps: 20.865 / 41.733 / 62.598 / 83.463 below row 1. */
@keyframes rc-matching-scan-move {
  0%,
  11.875% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  15%,
  21.25% {
    transform: translateY(20.865px);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  24.375%,
  45% {
    transform: translateY(41.733px);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  48.125%,
  54.375% {
    transform: translateY(62.598px);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  57.5%,
  100% {
    transform: translateY(83.463px);
  }
}

@keyframes rc-matching-status-1 {
  0%,
  6.875% {
    opacity: 0;
    transform: scale(0.6);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  10.625%,
  87.5% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rc-matching-status-2 {
  0%,
  16.25% {
    opacity: 0;
    transform: scale(0.6);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  20%,
  87.5% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

/* "Difference" overshoots so the flagged row reads as an alert. */
@keyframes rc-matching-status-3 {
  0%,
  26.25% {
    opacity: 0;
    transform: scale(0.6);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  28.75% {
    opacity: 1;
    transform: scale(1.15);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  30.625%,
  87.5% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rc-matching-status-4 {
  0%,
  49.375% {
    opacity: 0;
    transform: scale(0.6);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  53.125%,
  87.5% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rc-matching-status-5 {
  0%,
  58.75% {
    opacity: 0;
    transform: scale(0.6);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  62.5%,
  87.5% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rc-matching-flag {
  0%,
  25% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  28.75%,
  87.5% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
  }
}

/* Dotted line runs bottom-left → top-right, so it reveals from the left. */
@keyframes rc-matching-draw {
  0%,
  31.25% {
    transform: scaleX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  37.5%,
  95% {
    transform: scaleX(1);
  }
  95.1%,
  100% {
    transform: scaleX(0);
  }
}

@keyframes rc-matching-connector {
  0%,
  87.5% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
  }
}

@keyframes rc-matching-popup {
  0%,
  37.5% {
    opacity: 0;
    transform: translateY(8px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  42.5%,
  87.5% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rc-matching__connector,
  .rc-matching__connector-reveal,
  .rc-matching__flag,
  .rc-matching__scan,
  .rc-matching__scan-move,
  .rc-matching__status,
  .rc-matching__popup {
    animation: none;
  }
}
</style>
