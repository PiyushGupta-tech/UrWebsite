<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const INCOMING = [
  { cx: 12 },
  { cx: 39 },
  { cx: 66 },
  { cx: 93 },
  { cx: 120 },
];

/** Five success bubbles, evenly spaced on the green baseline (528→746) */
const SUCCESS = [
  { x: 528 },
  { x: 577 },
  { x: 626 },
  { x: 675 },
  { x: 724 },
];

/** Figma 182:11066 mobile success bubble x positions */
const MOBILE_SUCCESS_X = [2, 47.25, 96.49, 139.74, 189.99];

/** Indices that flash red first (failed attempt), then still recover via retry */
const FAIL_FIRST = new Set([1, 3]);

const PHASES = [
  { id: "attempt", ms: 750 },
  { id: "travel1", ms: 650 },
  { id: "retry", ms: 950 },
  { id: "travel2", ms: 650 },
  { id: "success", ms: 850 },
  { id: "pause", ms: 280 },
];

const reduceMotion = ref(false);
const isMobile = ref(false);
const phase = ref("idle");
const activeIndex = ref(0);
const completed = ref([]);
const packetOn = ref(false);
const packetLeg = ref(1);

let timers = [];
let running = false;
let mobileMediaQuery = null;
let handleMobileQueryChange = null;

function clearTimers() {
  timers.forEach((id) => window.clearTimeout(id));
  timers = [];
}

function schedule(fn, ms) {
  const id = window.setTimeout(fn, ms);
  timers.push(id);
}

function wait(ms) {
  return new Promise((resolve) => schedule(resolve, ms));
}

async function runJourney() {
  if (!running || reduceMotion.value) return;

  const index = activeIndex.value;
  const failsFirst = FAIL_FIRST.has(index);

  // 1) Attempt pulse
  phase.value = "attempt";
  packetOn.value = false;
  await wait(PHASES[0].ms);
  if (!running) return;

  // 2) Travel to retry
  phase.value = "travel1";
  packetLeg.value = 1;
  packetOn.value = true;
  await wait(PHASES[1].ms);
  if (!running) return;
  packetOn.value = false;

  // 3) Retry spinning
  phase.value = "retry";
  await wait(PHASES[2].ms);
  if (!running) return;

  // 4) Travel to success
  phase.value = "travel2";
  packetLeg.value = 2;
  packetOn.value = true;
  await wait(PHASES[3].ms);
  if (!running) return;
  packetOn.value = false;

  // 5) Success tick
  phase.value = "success";
  if (!completed.value.includes(index)) {
    completed.value = [...completed.value, index];
  }
  await wait(PHASES[4].ms);
  if (!running) return;

  // Keep failsFirst referenced for attempt styling only
  void failsFirst;

  // 6) Pause, then next payment (reset completed when cycle wraps)
  phase.value = "pause";
  await wait(PHASES[5].ms);
  if (!running) return;

  const next = (index + 1) % INCOMING.length;
  if (next === 0) completed.value = [];
  activeIndex.value = next;
  phase.value = "idle";

  schedule(() => {
    runJourney();
  }, 40);
}

function attemptClass(i) {
  if (reduceMotion.value) {
    return FAIL_FIRST.has(i)
      ? "success-graphic__attempt--dim-red"
      : "success-graphic__attempt--dim-green";
  }
  if (phase.value !== "attempt" || activeIndex.value !== i) {
    return completed.value.includes(i) ? "success-graphic__attempt--done" : "";
  }
  return FAIL_FIRST.has(i)
    ? "success-graphic__attempt--fail"
    : "success-graphic__attempt--pass";
}

function tickDrawn(i) {
  if (reduceMotion.value) return true;
  if (completed.value.includes(i) && !(phase.value === "success" && activeIndex.value === i)) {
    return true;
  }
  return phase.value === "success" && activeIndex.value === i;
}

function tickDrawing(i) {
  return !reduceMotion.value && phase.value === "success" && activeIndex.value === i;
}

const retryActive = computed(() => !reduceMotion.value && phase.value === "retry");
const dash1Active = computed(() => !reduceMotion.value && phase.value === "travel1");
const dash2Active = computed(() => !reduceMotion.value && phase.value === "travel2");

onMounted(() => {
  reduceMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  mobileMediaQuery = window.matchMedia("(max-width: 1200px)");
  isMobile.value = mobileMediaQuery.matches;
  handleMobileQueryChange = (event) => {
    isMobile.value = event.matches;
  };
  mobileMediaQuery.addEventListener("change", handleMobileQueryChange);
  if (reduceMotion.value) {
    phase.value = "idle";
    completed.value = SUCCESS.map((_, i) => i);
    return;
  }
  running = true;
  runJourney();
});

onUnmounted(() => {
  running = false;
  clearTimers();
  if (mobileMediaQuery && handleMobileQueryChange) {
    mobileMediaQuery.removeEventListener("change", handleMobileQueryChange);
  }
});
</script>

<template>
  <!-- Figma 73:1302 — payment journey: attempt → retry → success -->
  <svg
    v-if="!isMobile"
    class="success-graphic"
    :class="{ 'success-graphic--static': reduceMotion }"
    width="748"
    height="87"
    viewBox="0 0 748 87"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="A payment attempt passes through smart retry and becomes successful"
  >
    <text class="success-graphic__label" x="0" y="18">Incoming</text>
    <text class="success-graphic__label" x="0" y="36">Attempts</text>

    <g class="success-graphic__incoming" aria-hidden="true">
      <circle
        v-for="(dot, i) in INCOMING"
        :key="`in-${i}`"
        class="success-graphic__attempt"
        :class="attemptClass(i)"
        :cx="dot.cx"
        cy="68"
        r="11"
        stroke="#ffffff"
        stroke-width="2"
      />
    </g>

    <line
      class="success-graphic__dash"
      :class="{ 'is-active': dash1Active }"
      x1="153"
      y1="46.5"
      x2="246"
      y2="46.5"
      stroke="#097495"
      stroke-opacity="0.35"
      stroke-width="1.5"
      stroke-dasharray="5 5"
      stroke-linecap="round"
    />

    <text class="success-graphic__label success-graphic__label--center" x="320" y="15">
      Smart Retry
    </text>

    <g aria-hidden="true">
      <rect
        x="292"
        y="30.5"
        width="56"
        height="56"
        rx="28"
        fill="#ffffff"
        stroke="#EEEEEE"
        :class="{ 'success-graphic__hub--active': retryActive }"
      />
      <rect
        x="303.375"
        y="41.875"
        width="33.25"
        height="33.25"
        rx="16.625"
        fill="#097495"
        :fill-opacity="retryActive ? 0.22 : 0.1"
      />
      <g>
        <animateTransform
          v-if="retryActive"
          attributeName="transform"
          type="rotate"
          from="0 320 58.5"
          to="360 320 58.5"
          dur="0.9s"
          repeatCount="indefinite"
        />
        <path
          d="M324.196 57.3131H328.865C328.922 57.3131 328.977 57.3292 329.025 57.3595C329.072 57.3898 329.11 57.433 329.134 57.4841C329.158 57.5352 329.167 57.592 329.16 57.648C329.153 57.7039 329.13 57.7566 329.093 57.8L326.759 60.6025C326.731 60.6359 326.696 60.6628 326.657 60.6812C326.617 60.6997 326.574 60.7092 326.531 60.7092C326.487 60.7092 326.444 60.6997 326.405 60.6812C326.366 60.6628 326.331 60.6359 326.303 60.6025L323.968 57.8C323.932 57.7566 323.909 57.7039 323.902 57.648C323.895 57.592 323.904 57.5352 323.927 57.4841C323.951 57.433 323.989 57.3898 324.037 57.3595C324.085 57.3292 324.14 57.3131 324.196 57.3131ZM311.134 59.6881H315.803C315.859 59.6881 315.915 59.672 315.962 59.6417C316.01 59.6114 316.048 59.5682 316.072 59.5171C316.096 59.4661 316.104 59.4092 316.097 59.3533C316.09 59.2973 316.067 59.2446 316.031 59.2012L313.696 56.3987C313.668 56.3653 313.634 56.3384 313.594 56.32C313.555 56.3016 313.512 56.292 313.468 56.292C313.425 56.292 313.382 56.3016 313.342 56.32C313.303 56.3384 313.268 56.3653 313.24 56.3987L310.906 59.2012C310.87 59.2446 310.847 59.2973 310.839 59.3533C310.832 59.4092 310.841 59.4661 310.865 59.5171C310.889 59.5682 310.927 59.6114 310.974 59.6417C311.022 59.672 311.077 59.6881 311.134 59.6881Z"
          fill="#097495"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M319.999 52.5628C318.156 52.5628 316.508 53.4024 315.419 54.7217C315.37 54.7847 315.309 54.8373 315.24 54.8764C315.171 54.9154 315.094 54.9401 315.015 54.949C314.936 54.9579 314.856 54.9508 314.78 54.9281C314.703 54.9055 314.632 54.8677 314.571 54.817C314.51 54.7664 314.459 54.7039 314.422 54.6333C314.385 54.5627 314.363 54.4854 314.357 54.4061C314.351 54.3267 314.36 54.2469 314.385 54.1714C314.411 54.0958 314.451 54.0262 314.503 53.9664C315.373 52.9137 316.526 52.1329 317.827 51.7169C319.127 51.3009 320.52 51.2671 321.839 51.6196C323.158 51.9721 324.348 52.696 325.267 53.7053C326.187 54.7146 326.797 55.9667 327.026 57.3128H325.818C325.544 55.9717 324.815 54.7663 323.755 53.9008C322.695 53.0352 321.368 52.5625 319.999 52.5628ZM314.18 59.6878C314.405 60.7858 314.936 61.7978 315.712 62.6068C316.487 63.4159 317.476 63.989 318.563 64.26C319.651 64.531 320.793 64.4888 321.857 64.1382C322.922 63.7877 323.866 63.1431 324.579 62.2789C324.628 62.2159 324.689 62.1633 324.758 62.1242C324.827 62.0852 324.904 62.0605 324.983 62.0516C325.062 62.0427 325.142 62.0498 325.219 62.0725C325.295 62.0952 325.366 62.1329 325.427 62.1836C325.489 62.2343 325.539 62.2967 325.576 62.3673C325.613 62.4379 325.635 62.5152 325.641 62.5946C325.648 62.6739 325.638 62.7537 325.613 62.8292C325.588 62.9048 325.547 62.9745 325.495 63.0342C324.625 64.0869 323.472 64.8677 322.171 65.2837C320.871 65.6998 319.478 65.7335 318.159 65.3811C316.84 65.0286 315.65 64.3046 314.731 63.2953C313.811 62.286 313.201 61.0339 312.973 59.6878H314.18Z"
          fill="#097495"
        />
      </g>
    </g>

    <line
      class="success-graphic__dash"
      :class="{ 'is-active': dash2Active }"
      x1="398"
      y1="46.5"
      x2="504"
      y2="46.5"
      stroke="#097495"
      stroke-opacity="0.35"
      stroke-width="1.5"
      stroke-dasharray="5 5"
      stroke-linecap="round"
    />

    <!-- Traveling payment packet -->
    <circle
      v-if="packetOn"
      class="success-graphic__packet"
      :class="packetLeg === 1 ? 'success-graphic__packet--leg1' : 'success-graphic__packet--leg2'"
      r="4.5"
      fill="#097495"
      cx="0"
      cy="0"
    />

    <text class="success-graphic__label" x="528" y="18">Successful</text>
    <text class="success-graphic__label" x="528" y="36">Attempts</text>

    <line
      x1="528"
      y1="68.5"
      x2="746"
      y2="68.5"
      stroke="#2DCE89"
      stroke-opacity="0.31"
      stroke-width="3"
    />

    <g
      v-for="(item, i) in SUCCESS"
      :key="`ok-${i}`"
      class="success-graphic__ok"
      :class="{
        'is-lit': tickDrawn(i) || tickDrawing(i),
        'is-drawing': tickDrawing(i),
      }"
      aria-hidden="true"
    >
      <rect
        :x="item.x"
        y="57"
        width="22"
        height="22"
        rx="11"
        class="success-graphic__ok-bubble"
        stroke="#ffffff"
        stroke-width="2"
      />
      <path
        class="success-graphic__tick"
        :d="`M${item.x + 8.083} 68.833 L${item.x + 9.541} 70.291 L${item.x + 13.916} 65.708`"
        fill="none"
        stroke="#ffffff"
        stroke-width="1.6"
        stroke-linecap="round"
        stroke-linejoin="round"
        pathLength="1"
      />
    </g>
  </svg>

  <svg
    v-else
    class="success-graphic success-graphic--mobile"
    :class="{ 'success-graphic--static': reduceMotion }"
    width="220"
    height="305"
    viewBox="0 0 220 305"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="A payment attempt passes through smart retry and becomes successful"
  >
    <!-- Incoming Attempts: Figma 182:11050 -->
    <text class="success-graphic__label success-graphic__label--mobile-center" x="110" y="16">
      INCOMING ATTEMPTS
    </text>

    <g class="success-graphic__incoming" aria-hidden="true">
      <circle
        v-for="(dot, i) in INCOMING"
        :key="`mobile-in-${i}`"
        class="success-graphic__attempt"
        :class="attemptClass(i)"
        :cx="56 + i * 27"
        cy="40"
        r="12"
        stroke="#ffffff"
        stroke-width="2"
      />
    </g>

    <line
      class="success-graphic__dash"
      :class="{ 'is-active': dash1Active }"
      x1="110"
      y1="64"
      x2="110"
      y2="116"
      stroke="#097495"
      stroke-opacity="0.35"
      stroke-width="1.5"
      stroke-dasharray="5 5"
      stroke-linecap="round"
    />

    <!-- Smart Retry: Figma 199:306 — SMART | hub | RETRY -->
    <text class="success-graphic__label success-graphic__label--mobile-side-left" x="73.5" y="157">
      SMART
    </text>

    <g aria-hidden="true" transform="translate(81.5 124)">
      <rect
        x="0"
        y="0"
        width="57"
        height="57"
        rx="28.5"
        fill="#ffffff"
        stroke="#EEEEEE"
        :class="{ 'success-graphic__hub--active': retryActive }"
      />
      <rect
        x="11.875"
        y="11.875"
        width="33.25"
        height="33.25"
        rx="16.625"
        fill="#097495"
        :fill-opacity="retryActive ? 0.22 : 0.1"
      />
      <g>
        <animateTransform
          v-if="retryActive"
          attributeName="transform"
          type="rotate"
          from="0 28.5 28.5"
          to="360 28.5 28.5"
          dur="0.9s"
          repeatCount="indefinite"
        />
        <path
          d="M32.696 27.313H37.365C37.422 27.313 37.477 27.329 37.525 27.36C37.572 27.39 37.61 27.433 37.634 27.484C37.658 27.535 37.667 27.592 37.66 27.648C37.653 27.704 37.63 27.757 37.593 27.8L35.259 30.603C35.231 30.636 35.196 30.663 35.157 30.681C35.117 30.7 35.074 30.709 35.031 30.709C34.987 30.709 34.944 30.7 34.905 30.681C34.866 30.663 34.831 30.636 34.803 30.603L32.468 27.8C32.432 27.757 32.409 27.704 32.402 27.648C32.395 27.592 32.404 27.535 32.427 27.484C32.451 27.433 32.489 27.39 32.537 27.36C32.585 27.329 32.64 27.313 32.696 27.313ZM19.634 29.688H24.303C24.359 29.688 24.415 29.672 24.462 29.642C24.51 29.611 24.548 29.568 24.572 29.517C24.596 29.466 24.604 29.409 24.597 29.353C24.59 29.297 24.567 29.245 24.531 29.201L22.196 26.399C22.168 26.365 22.134 26.338 22.094 26.32C22.055 26.302 22.012 26.292 21.968 26.292C21.925 26.292 21.882 26.302 21.842 26.32C21.803 26.338 21.768 26.365 21.74 26.399L19.406 29.201C19.37 29.245 19.347 29.297 19.339 29.353C19.332 29.409 19.341 29.466 19.365 29.517C19.389 29.568 19.427 29.611 19.474 29.642C19.522 29.672 19.577 29.688 19.634 29.688Z"
          fill="#097495"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M28.499 22.563C26.656 22.563 25.008 23.402 23.919 24.722C23.87 24.785 23.809 24.837 23.74 24.876C23.671 24.915 23.594 24.94 23.515 24.949C23.436 24.958 23.356 24.951 23.28 24.928C23.203 24.905 23.132 24.868 23.071 24.817C23.01 24.766 22.959 24.704 22.922 24.633C22.885 24.563 22.863 24.485 22.857 24.406C22.851 24.327 22.86 24.247 22.885 24.171C22.911 24.096 22.951 24.026 23.003 23.966C23.873 22.914 25.026 22.133 26.327 21.717C27.627 21.301 29.02 21.267 30.339 21.62C31.658 21.972 32.848 22.696 33.767 23.705C34.687 24.715 35.297 25.967 35.526 27.313H34.318C34.044 25.972 33.315 24.766 32.255 23.901C31.195 23.035 29.868 22.563 28.499 22.563ZM22.68 29.688C22.905 30.786 23.436 31.798 24.212 32.607C24.987 33.416 25.976 33.989 27.063 34.26C28.151 34.531 29.293 34.489 30.357 34.138C31.422 33.788 32.366 33.143 33.079 32.279C33.128 32.216 33.189 32.163 33.258 32.124C33.327 32.085 33.404 32.061 33.483 32.052C33.562 32.043 33.642 32.05 33.719 32.072C33.795 32.095 33.866 32.133 33.927 32.184C33.989 32.234 34.039 32.297 34.076 32.367C34.113 32.438 34.135 32.515 34.141 32.595C34.148 32.674 34.138 32.754 34.113 32.829C34.088 32.905 34.047 32.974 33.995 33.034C33.125 34.087 31.972 34.868 30.671 35.284C29.371 35.7 27.978 35.734 26.659 35.381C25.34 35.029 24.15 34.305 23.231 33.295C22.311 32.286 21.701 31.034 21.473 29.688H22.68Z"
          fill="#097495"
        />
      </g>
    </g>

    <text class="success-graphic__label success-graphic__label--mobile-side-right" x="146.5" y="157">
      RETRY
    </text>

    <!-- Successful Attempts: Figma 199:307 — connector, dots, then label below -->
    <line
      class="success-graphic__dash"
      :class="{ 'is-active': dash2Active }"
      x1="110"
      y1="189"
      x2="110"
      y2="241"
      stroke="#097495"
      stroke-opacity="0.35"
      stroke-width="1.5"
      stroke-dasharray="5 5"
      stroke-linecap="round"
    />

    <circle
      v-if="packetOn"
      class="success-graphic__packet"
      :class="packetLeg === 1 ? 'success-graphic__packet--mobile-leg1' : 'success-graphic__packet--mobile-leg2'"
      r="3.5"
      fill="#097495"
      cx="0"
      cy="0"
    />

    <line
      x1="2"
      y1="267"
      x2="214"
      y2="267"
      stroke="#2DCE89"
      stroke-opacity="0.31"
      stroke-width="3"
    />

    <g
      v-for="(item, i) in SUCCESS"
      :key="`mobile-ok-${i}`"
      class="success-graphic__ok"
      :class="{
        'is-lit': tickDrawn(i) || tickDrawing(i),
        'is-drawing': tickDrawing(i),
      }"
      aria-hidden="true"
    >
      <rect
        :x="MOBILE_SUCCESS_X[i]"
        y="253"
        width="24"
        height="24"
        rx="12"
        class="success-graphic__ok-bubble"
        stroke="#ffffff"
        stroke-width="2"
      />
      <path
        class="success-graphic__tick"
        :d="`M${MOBILE_SUCCESS_X[i] + 8.083} 264.833 L${MOBILE_SUCCESS_X[i] + 9.541} 266.291 L${MOBILE_SUCCESS_X[i] + 13.916} 261.708`"
        fill="none"
        stroke="#ffffff"
        stroke-width="1.6"
        stroke-linecap="round"
        stroke-linejoin="round"
        pathLength="1"
      />
    </g>

    <text class="success-graphic__label success-graphic__label--mobile-center" x="110" y="301">
      SUCCESSFUL ATTEMPTS
    </text>
  </svg>
</template>

<style scoped>
.success-graphic {
  display: block;
  width: 100%;
  max-width: 748px;
  height: auto;
  overflow: visible;
}

.success-graphic__label {
  fill: #535862;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.success-graphic__label--center {
  text-anchor: middle;
}

.success-graphic__label--mobile-center {
  text-anchor: middle;
  font-size: 14px;
}

.success-graphic__label--mobile-side-left {
  text-anchor: end;
  font-size: 14px;
}

.success-graphic__label--mobile-side-right {
  text-anchor: start;
  font-size: 14px;
}

.success-graphic__attempt {
  fill: #9ca3af;
  transition: fill 0.2s ease;
}

.success-graphic__attempt--pass {
  animation: success-pulse-green 0.75s ease-in-out;
}

.success-graphic__attempt--fail {
  animation: success-pulse-red 0.75s ease-in-out;
}

.success-graphic__attempt--done {
  fill: #9ca3af;
  opacity: 0.7;
}

.success-graphic__attempt--dim-green {
  fill: #10b981;
}

.success-graphic__attempt--dim-red {
  fill: #ef4444;
}

.success-graphic__dash {
  transition: stroke-opacity 0.2s ease;
}

.success-graphic__dash.is-active {
  stroke-opacity: 1;
  animation: success-dash-move 0.45s linear infinite;
}

.success-graphic__hub--active {
  stroke: #097495;
}

.success-graphic__packet {
  transform-box: view-box;
  transform-origin: 0 0;
}

.success-graphic__packet--leg1 {
  animation: success-packet-leg1 0.65s linear forwards;
}

.success-graphic__packet--leg2 {
  animation: success-packet-leg2 0.65s linear forwards;
}

.success-graphic__ok-bubble {
  fill: #d1d5db;
  transition: fill 0.25s ease;
}

.success-graphic__ok.is-lit .success-graphic__ok-bubble {
  fill: #10b981;
}

.success-graphic__tick {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  opacity: 0;
}

.success-graphic__ok.is-lit .success-graphic__tick {
  opacity: 1;
  stroke-dashoffset: 0;
}

.success-graphic__ok.is-drawing .success-graphic__tick {
  opacity: 1;
  animation: success-tick-draw 0.75s ease-out forwards;
}

@keyframes success-pulse-green {
  0%,
  100% {
    fill: #9ca3af;
  }
  35%,
  70% {
    fill: #10b981;
  }
}

@keyframes success-pulse-red {
  0%,
  100% {
    fill: #9ca3af;
  }
  30%,
  55% {
    fill: #ef4444;
  }
  75% {
    fill: #f59e0b;
  }
}

@keyframes success-dash-move {
  to {
    stroke-dashoffset: -20;
  }
}

@keyframes success-packet-leg1 {
  from {
    transform: translate(153px, 46.5px);
  }
  to {
    transform: translate(246px, 46.5px);
  }
}

@keyframes success-packet-leg2 {
  from {
    transform: translate(398px, 46.5px);
  }
  to {
    transform: translate(504px, 46.5px);
  }
}

@keyframes success-packet-mobile-leg1 {
  from {
    transform: translate(110px, 64px);
  }
  to {
    transform: translate(110px, 116px);
  }
}

@keyframes success-packet-mobile-leg2 {
  from {
    transform: translate(110px, 189px);
  }
  to {
    transform: translate(110px, 241px);
  }
}

@keyframes success-tick-draw {
  from {
    stroke-dashoffset: 1;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .success-graphic--static .success-graphic__attempt,
  .success-graphic--static .success-graphic__dash,
  .success-graphic--static .success-graphic__tick {
    animation: none;
  }

  .success-graphic--static .success-graphic__ok-bubble {
    fill: #10b981;
  }

  .success-graphic--static .success-graphic__tick {
    opacity: 1;
    stroke-dashoffset: 0;
  }
}

.success-graphic__packet--mobile-leg1 {
  animation: success-packet-mobile-leg1 0.65s linear forwards;
}

.success-graphic__packet--mobile-leg2 {
  animation: success-packet-mobile-leg2 0.65s linear forwards;
}

@media (max-width: 1200px) {
  .success-graphic--mobile {
    width: 220px;
    max-width: 100%;
    height: auto;
    overflow: visible;
  }
}
</style>
