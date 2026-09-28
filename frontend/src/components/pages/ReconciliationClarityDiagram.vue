<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  image: { type: String, required: true },
  alt: { type: String, default: "" },
  width: { type: Number, default: 1291 },
  height: { type: Number, default: 627 },
});

/** Engine core center — Figma white disc at (563.715, 218.6) size 162.555×165.118 */
const RIPPLE_CX = 644.99;
const RIPPLE_CY = 301.16;
const RIPPLE_BASE_R = 92;

/**
 * Figma 652:9419 / 652:9401 — exact vector beziers (Line 613/614/615/617)
 * with each vector's relativeTransform baked into fan-local coords.
 * Absolute anchors inside Frame 214722621 (1291×627):
 *   left  = 46+244-0.4, 68+134 → (289.6, 202)
 *   right = 46+739+222, 68+33+98 → (1007, 199) with scale(-1,1)
 *     matching Figma relativeTransform [[-1,0,222],[0,1,0]]
 */
const FAN_PATHS = [
  "M11.409 4.602C11.368 6.882 39.026 8.676 47.245 16.669C55.464 24.662 67.510 72.303 78.427 98.924C89.343 125.545 103.034 122.584 103.034 122.584L108.849 122.625",
  "M11.000 75.227C10.932 76.162 38.381 75.325 47.859 79.693C57.338 84.061 68.157 102.220 79.128 112.983C90.099 123.746 104.266 122.349 104.266 122.349L110.268 122.288",
  "M14.758 152.652C14.669 152.116 40.222 151.700 48.919 148.875C57.615 146.050 67.180 135.239 77.090 128.682C86.999 122.125 100.214 122.466 100.214 122.466L105.798 122.305",
  "M14.239 228.973C14.195 226.925 41.374 225.366 49.439 218.205C57.505 211.044 69.271 168.293 79.958 144.412C90.646 120.531 104.106 123.215 104.106 123.215L109.820 123.189",
];

const FAN_DOTS = [
  { cx: 7.327, cy: 6.088 },
  { cx: 6.327, cy: 76.088 },
  { cx: 8.727, cy: 152.088 },
  { cx: 7.327, cy: 229.09 },
];

/** Match Risk & Fraud fan density (3.4 on / 10 gap) */
const FAN_STROKE = {
  width: 1.5,
  dash: "3.4 10",
  color: "#E8F8FB",
};

const DOT_R_FILL = 4.588;
const DOT_R_RING = 6.118;

const LEFT_FAN = { x: 289.6, y: 202 };
/** Flip origin at card-rail so Outputs←→results matches Figma 652:9401 */
const RIGHT_FAN = { x: 1007, y: 199 };

/** Short dashed bridges — Figma 461:7453 / 461:7457 (Line 607) */
const BRIDGE_LINES = [
  {
    id: "ingest-bridge",
    d: "M464.87 319.97H490.27",
  },
  {
    id: "outputs-bridge",
    d: "M785 316.97H810.4",
  },
];

const BRIDGE_STROKE = {
  width: 1.73,
  dash: "3.4 10",
  color: "#62E9FE",
  opacity: 0.94,
};

/** Filled connector paths in the base export — replaced by Figma curve strokes */
const STATIC_FLOW_FILLS = new Set([
  "paint1_linear_461_7373",
  "paint2_linear_461_7373",
  "paint4_linear_461_7373",
  "paint6_linear_461_7373",
  "paint8_linear_461_7373",
  "paint10_linear_461_7373",
  "paint12_linear_461_7373",
  "paint14_linear_461_7373",
  "paint16_linear_461_7373",
  "paint18_linear_461_7373",
]);

const hostRef = ref(null);
const reduceMotion = ref(false);
const loadFailed = ref(false);
let abort = null;

const viewBox = computed(() => `0 0 ${props.width} ${props.height}`);

async function injectSvg() {
  if (abort) abort.abort();
  abort = new AbortController();
  loadFailed.value = false;

  const host = hostRef.value;
  if (!host || typeof fetch === "undefined") return;

  host.querySelectorAll(":scope > .rc-clarity-svg").forEach((el) => el.remove());

  try {
    const res = await fetch(props.image, { signal: abort.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const raw = await res.text();
    const doc = new DOMParser().parseFromString(raw, "image/svg+xml");
    if (doc.querySelector("parsererror")) throw new Error("SVG parse error");

    const svg = doc.documentElement;
    svg.classList.add("rc-clarity-svg");
    svg.setAttribute("role", "img");
    if (props.alt) svg.setAttribute("aria-label", props.alt);
    svg.removeAttribute("width");
    svg.removeAttribute("height");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

    svg.querySelectorAll("path[stroke-dasharray]").forEach((el) => {
      el.classList.add("rc-clarity-dash");
      // Loosen baked dashes to match Risk & Fraud fan density
      el.setAttribute("stroke-dasharray", FAN_STROKE.dash);
    });
    // Hide baked nearly-straight connector fills + junction dots
    // (exact Figma 652:9419 / 652:9401 curves are drawn in the overlay)
    svg.querySelectorAll("path[fill^='url(#paint']").forEach((el) => {
      const fill = el.getAttribute("fill") || "";
      const id = fill.match(/url\(#([^)]+)\)/)?.[1];
      if (id && STATIC_FLOW_FILLS.has(id)) {
        el.setAttribute("opacity", "0");
        el.setAttribute("visibility", "hidden");
        el.style.pointerEvents = "none";
      }
    });
    svg.querySelectorAll('circle[fill="#38B7D3"]').forEach((el) => {
      el.setAttribute("opacity", "0");
      el.setAttribute("visibility", "hidden");
      el.style.pointerEvents = "none";
    });
    // Hide white/gradient junction rings around those dots
    svg.querySelectorAll('rect[width="11"][height="11"]').forEach((el) => {
      el.setAttribute("opacity", "0");
      el.setAttribute("visibility", "hidden");
      el.style.pointerEvents = "none";
    });
    if (reduceMotion.value) {
      svg.classList.add("rc-clarity-svg--static");
    }

    host.insertBefore(svg, host.firstChild);
  } catch (err) {
    if (err?.name === "AbortError") return;
    loadFailed.value = true;
  }
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  injectSvg();
});

watch(
  () => props.image,
  () => {
    injectSvg();
  },
);

onBeforeUnmount(() => {
  if (abort) abort.abort();
});
</script>

<template>
  <div
    ref="hostRef"
    class="rc-clarity-diagram"
    :class="{ 'rc-clarity-diagram--static': reduceMotion }"
  >
    <img
      v-if="loadFailed"
      class="rc-clarity-diagram__fallback"
      :src="image"
      :alt="alt"
      :width="width"
      :height="height"
      decoding="async"
      loading="lazy"
    />

    <svg
      v-if="!loadFailed"
      class="rc-clarity-fx"
      :viewBox="viewBox"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <g v-if="!reduceMotion" class="rc-clarity-fx__ripples">
        <circle
          v-for="n in 3"
          :key="`ripple-${n}`"
          class="rc-clarity-fx__ripple"
          :class="`rc-clarity-fx__ripple--${n}`"
          :cx="RIPPLE_CX"
          :cy="RIPPLE_CY"
          :r="RIPPLE_BASE_R"
        />
      </g>

      <!-- Sources → Ingest (Figma 652:9419) -->
      <g
        class="rc-clarity-fx__fan"
        :class="{ 'rc-clarity-fx__fan--motion': !reduceMotion }"
        :transform="`translate(${LEFT_FAN.x} ${LEFT_FAN.y})`"
      >
        <path
          v-for="(d, i) in FAN_PATHS"
          :key="`l-path-${i}`"
          class="rc-clarity-fx__curve"
          :d="d"
          fill="none"
          :stroke="FAN_STROKE.color"
          :stroke-width="FAN_STROKE.width"
          :stroke-dasharray="FAN_STROKE.dash"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <g v-for="(dot, i) in FAN_DOTS" :key="`l-dot-${i}`">
          <circle
            :cx="dot.cx"
            :cy="dot.cy"
            :r="DOT_R_RING"
            fill="white"
            fill-opacity="0.35"
          />
          <circle
            :cx="dot.cx"
            :cy="dot.cy"
            :r="DOT_R_FILL"
            fill="#38B7D3"
            stroke="white"
            stroke-width="1"
          />
        </g>
      </g>

      <!-- Outputs → results (Figma 652:9401, mirrored) -->
      <g
        class="rc-clarity-fx__fan rc-clarity-fx__fan--rtl"
        :class="{ 'rc-clarity-fx__fan--motion': !reduceMotion }"
        :transform="`translate(${RIGHT_FAN.x} ${RIGHT_FAN.y}) scale(-1 1)`"
      >
        <path
          v-for="(d, i) in FAN_PATHS"
          :key="`r-path-${i}`"
          class="rc-clarity-fx__curve"
          :d="d"
          fill="none"
          :stroke="FAN_STROKE.color"
          :stroke-width="FAN_STROKE.width"
          :stroke-dasharray="FAN_STROKE.dash"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <g v-for="(dot, i) in FAN_DOTS" :key="`r-dot-${i}`">
          <circle
            :cx="dot.cx"
            :cy="dot.cy"
            :r="DOT_R_RING"
            fill="white"
            fill-opacity="0.35"
          />
          <circle
            :cx="dot.cx"
            :cy="dot.cy"
            :r="DOT_R_FILL"
            fill="#38B7D3"
            stroke="white"
            stroke-width="1"
          />
        </g>
      </g>

      <path
        v-for="line in BRIDGE_LINES"
        :key="line.id"
        class="rc-clarity-fx__bridge"
        :class="{ 'rc-clarity-fx__bridge--motion': !reduceMotion }"
        :d="line.d"
        fill="none"
        :stroke="BRIDGE_STROKE.color"
        :stroke-opacity="BRIDGE_STROKE.opacity"
        :stroke-width="BRIDGE_STROKE.width"
        :stroke-dasharray="BRIDGE_STROKE.dash"
        stroke-linecap="round"
      />    </svg>
  </div>
</template>

<style scoped>
.rc-clarity-diagram {
  position: relative;
  width: min(1291px, 100%);
  margin-inline: auto;
  line-height: 0;
}

.rc-clarity-diagram :deep(.rc-clarity-svg),
.rc-clarity-diagram__fallback,
.rc-clarity-fx {
  display: block;
  width: 100%;
  height: auto;
}

.rc-clarity-diagram :deep(.rc-clarity-svg) {
  position: relative;
  z-index: 0;
}

.rc-clarity-fx {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  overflow: visible;
}

.rc-clarity-diagram :deep(.rc-clarity-dash) {
  animation: rc-clarity-dash-move 1.1s linear infinite;
}

.rc-clarity-fx__curve {
  fill: none;
}

.rc-clarity-fx__fan--motion .rc-clarity-fx__curve {
  animation: rc-clarity-fan-dash 1.1s linear infinite;
}

/* Mirrored right fan: flip dash march so flow still reads left → right */
.rc-clarity-fx__fan--rtl.rc-clarity-fx__fan--motion .rc-clarity-fx__curve {
  animation-name: rc-clarity-fan-dash-rtl;
}

@keyframes rc-clarity-fan-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes rc-clarity-fan-dash-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

.rc-clarity-fx__bridge--motion {
  animation: rc-clarity-bridge-dash 1.1s linear infinite;
}

@keyframes rc-clarity-bridge-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

.rc-clarity-fx__ripple {
  fill: none;
  stroke: #62e9fe;
  stroke-width: 1.4;
  stroke-dasharray: 3.4 10;
  transform-box: fill-box;
  transform-origin: center;
  animation: rc-clarity-ripple 2.8s ease-out infinite;
}

.rc-clarity-fx__ripple--1 {
  animation-delay: 0s;
}

.rc-clarity-fx__ripple--2 {
  animation-delay: 0.9s;
}

.rc-clarity-fx__ripple--3 {
  animation-delay: 1.8s;
}

.rc-clarity-diagram--static :deep(.rc-clarity-dash),
.rc-clarity-diagram--static .rc-clarity-fx__ripple,
.rc-clarity-diagram--static .rc-clarity-fx__bridge--motion,
.rc-clarity-diagram--static .rc-clarity-fx__curve {
  animation: none;
}

@keyframes rc-clarity-dash-move {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes rc-clarity-ripple {
  0% {
    transform: scale(0.72);
    stroke-opacity: 0.55;
  }

  70% {
    stroke-opacity: 0.12;
  }

  100% {
    transform: scale(1.28);
    stroke-opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .rc-clarity-diagram :deep(.rc-clarity-dash),
  .rc-clarity-fx__ripple,
  .rc-clarity-fx__bridge--motion,
  .rc-clarity-fx__curve {
    animation: none;
  }
}
</style>
