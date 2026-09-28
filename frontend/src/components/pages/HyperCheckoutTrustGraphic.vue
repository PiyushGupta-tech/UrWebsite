<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  /** 0 Adaptive · 1 Multi-Mode · 2 Intelligent Routing */
  activeIndex: { type: Number, default: 0 },
  alt: { type: String, default: "" },
});

/**
 * Adaptive: layered card → arrow → device (desktop → tablet → mobile)
 * Modes: static rings/badges + 3 orbiting nodes (Figma 296:1984, 10s loop)
 * Routing: layered flow with dotted arrows drawing (Figma 841:28554)
 */
const ASSET = "/images/figma-hyper-checkout/trust";
const ADAPTIVE = `${ASSET}/adaptive`;
const MODES_ASSET = `${ASSET}/modes`;
const ROUTING = `${ASSET}/routing`;

/** Artboard matches adaptive-1..3 exports */
const ART_W = 706;
const ART_H = 644;

/** Modes artboard (modes.svg / Figma Frame 2147226296 padded) */
const MODES_W = 694;
const MODES_H = 684;

/** Routing artboard (routing-4.svg) */
const ROUTING_W = 521;
const ROUTING_H = 614;

/** Orbit node start positions in modes artboard px (from modes.svg) */
const MODE_NODES = [
  { id: "a", left: 348.687, top: 134.101 },
  { id: "b", left: 548.688, top: 276.103 },
  { id: "c", left: 191.685, top: 460.102 },
];
const MODE_NODE_SRC = `${MODES_ASSET}/node.svg`;
const MODE_STATIC_SRC = `${MODES_ASSET}/static.svg`;

/**
 * Layer boxes in artboard px (derived from adaptive-3 + per-export content offsets).
 * glow.svg circle matches adaptive-3 at (0,0) 644×644.
 */
const LAYERS = {
  glow: { left: 0, top: 0, w: 644, h: 644, src: `${ADAPTIVE}/glow.svg` },
  card: { left: 167.304, top: 106.745, w: 321, h: 326, src: `${ADAPTIVE}/card.svg` },
  desktopArrow: {
    left: 471.135,
    top: 242.013,
    w: 72,
    h: 41,
    src: `${ADAPTIVE}/desktop-arrow.svg`,
    grow: "ltr",
  },
  desktop: { left: 532.14, top: 197.645, w: 174, h: 117, src: `${ADAPTIVE}/desktop.svg` },
  tabletArrow: {
    left: 321.023,
    top: 401.739,
    w: 5,
    h: 53,
    src: `${ADAPTIVE}/tablet-arrow.svg`,
    grow: "ttb",
  },
  tablet: { left: 253.734, top: 454.981, w: 143, h: 118, src: `${ADAPTIVE}/tablet.svg` },
  mobileArrow: {
    left: 113.973,
    top: 243.124,
    w: 72,
    h: 41,
    src: `${ADAPTIVE}/mobile-arrow.svg`,
    grow: "rtl",
  },
  mobile: { left: 33.002, top: 187.663, w: 88, h: 150, src: `${ADAPTIVE}/mobile.svg` },
};

/** Routing layers in routing-4 artboard px */
const ROUTING_LAYERS = {
  glow: { left: 170.315, top: 0, w: 174, h: 174, src: `${ROUTING}/glow.svg` },
  user: { left: 176.946, top: 20.641, w: 160, h: 160, src: `${ROUTING}/user.svg` },
  arrow11: { left: 250.297, top: 150.322, w: 14, h: 51, src: `${ROUTING}/arrow-11.svg` },
  hub: { left: 176.947, top: 192.74, w: 160, h: 160, src: `${ROUTING}/hub.svg` },
  arrow12: { left: 249.692, top: 317.573, w: 14, h: 102, src: `${ROUTING}/arrow-12.svg` },
  arrow13: { left: 119.984, top: 317.573, w: 113, h: 96, src: `${ROUTING}/arrow-13.svg` },
  arrow18: { left: 286.024, top: 317.573, w: 113, h: 96, src: `${ROUTING}/arrow-18.svg` },
  payments: { left: 11.744, top: 388.285, w: 497, h: 158, src: `${ROUTING}/payments.svg` },
  arrow15: { left: 71.567, top: 490.885, w: 3, h: 70, src: `${ROUTING}/arrow-15.svg` },
  arrow16: { left: 255.786, top: 506.641, w: 3, h: 55, src: `${ROUTING}/arrow-16.svg` },
  arrow17: { left: 442.429, top: 490.885, w: 3, h: 70, src: `${ROUTING}/arrow-17.svg` },
  status: { left: 0, top: 564.815, w: 521, h: 49, src: `${ROUTING}/status.svg` },
};

/** Shared timing — full beat finishes well under the 10s tab interval */
const BEAT_MS = {
  card: 280,
  arrow: 300,
  device: 200,
  hold: 1600,
};

const reduceMotion = ref(false);
/** Adaptive visibility flags */
const show = ref({
  glow: false,
  card: false,
  desktopArrow: false,
  desktop: false,
  tabletArrow: false,
  tablet: false,
  mobileArrow: false,
  mobile: false,
});
/** Routing visibility flags */
const routingShow = ref({
  glow: false,
  user: false,
  arrow11: false,
  hub: false,
  arrow12: false,
  arrow13: false,
  arrow18: false,
  payments: false,
  arrow15: false,
  arrow16: false,
  arrow17: false,
  status: false,
});

const variant = computed(() => {
  if (props.activeIndex === 1) return "modes";
  if (props.activeIndex === 2) return "routing";
  return "adaptive";
});

let timers = [];
let loopTimer = null;

function clearTimers() {
  timers.forEach((id) => clearTimeout(id));
  timers = [];
  if (loopTimer) {
    clearTimeout(loopTimer);
    loopTimer = null;
  }
}

function wait(ms) {
  return new Promise((resolve) => {
    timers.push(setTimeout(resolve, ms));
  });
}

function pct(n, total) {
  return `${(n / total) * 100}%`;
}

function layerStyle(layer, artW = ART_W, artH = ART_H) {
  return {
    left: pct(layer.left, artW),
    top: pct(layer.top, artH),
    width: pct(layer.w, artW),
    height: pct(layer.h, artH),
  };
}

function routingLayerStyle(layer) {
  return layerStyle(layer, ROUTING_W, ROUTING_H);
}

function modeNodeStyle(node) {
  return {
    left: pct(node.left, MODES_W),
    top: pct(node.top, MODES_H),
    width: pct(10, MODES_W),
    height: pct(10, MODES_H),
  };
}

function resetAdaptive(allVisible = false) {
  const on = allVisible;
  show.value = {
    glow: on,
    card: on,
    desktopArrow: on,
    desktop: on,
    tabletArrow: on,
    tablet: on,
    mobileArrow: on,
    mobile: on,
  };
}

function resetRouting(allVisible = false) {
  const on = allVisible;
  routingShow.value = {
    glow: on,
    user: on,
    arrow11: on,
    hub: on,
    arrow12: on,
    arrow13: on,
    arrow18: on,
    payments: on,
    arrow15: on,
    arrow16: on,
    arrow17: on,
    status: on,
  };
}

async function runAdaptive() {
  if (reduceMotion.value) {
    resetAdaptive(true);
    return;
  }
  clearTimers();
  resetAdaptive(false);

  // 1. Center checkout only
  show.value.glow = true;
  show.value.card = true;
  await wait(BEAT_MS.card);
  if (variant.value !== "adaptive") return;

  // 2–3. Arrow draws, then desktop / tablet / mobile
  const beats = [
    ["desktopArrow", "desktop"],
    ["tabletArrow", "tablet"],
    ["mobileArrow", "mobile"],
  ];

  for (const [arrowKey, deviceKey] of beats) {
    show.value[arrowKey] = true;
    await wait(BEAT_MS.arrow);
    if (variant.value !== "adaptive") return;
    show.value[deviceKey] = true;
    await wait(BEAT_MS.device);
    if (variant.value !== "adaptive") return;
  }

  await wait(BEAT_MS.hold);
  if (reduceMotion.value || variant.value !== "adaptive") return;

  loopTimer = setTimeout(() => {
    if (!reduceMotion.value && variant.value === "adaptive") {
      runAdaptive();
    }
  }, 60);
}

async function runRouting() {
  if (reduceMotion.value) {
    resetRouting(true);
    return;
  }
  clearTimers();
  resetRouting(false);

  // 1. User
  routingShow.value.glow = true;
  routingShow.value.user = true;
  await wait(BEAT_MS.card);
  if (variant.value !== "routing") return;

  // 2. Dotted arrow → routing hub
  routingShow.value.arrow11 = true;
  await wait(BEAT_MS.arrow);
  if (variant.value !== "routing") return;
  routingShow.value.hub = true;
  await wait(BEAT_MS.device);
  if (variant.value !== "routing") return;

  // 3. Fan-out dotted arrows toward payment methods
  routingShow.value.arrow12 = true;
  routingShow.value.arrow13 = true;
  routingShow.value.arrow18 = true;
  await wait(BEAT_MS.arrow + 40);
  if (variant.value !== "routing") return;
  routingShow.value.payments = true;
  await wait(BEAT_MS.device);
  if (variant.value !== "routing") return;

  // 4. Status connectors + result pills
  routingShow.value.arrow15 = true;
  routingShow.value.arrow16 = true;
  routingShow.value.arrow17 = true;
  await wait(BEAT_MS.arrow);
  if (variant.value !== "routing") return;
  routingShow.value.status = true;

  await wait(BEAT_MS.hold);
  if (reduceMotion.value || variant.value !== "routing") return;

  loopTimer = setTimeout(() => {
    if (!reduceMotion.value && variant.value === "routing") {
      runRouting();
    }
  }, 60);
}

async function runSequence() {
  if (variant.value === "adaptive") {
    await runAdaptive();
    return;
  }
  if (variant.value === "routing") {
    await runRouting();
    return;
  }
  /* Modes: continuous CSS orbit — no frame stepping */
  clearTimers();
}

function preloadTrustImages() {
  if (typeof Image === "undefined") return;
  const urls = [
    ...Object.values(LAYERS).map((l) => l.src),
    ...Object.values(ROUTING_LAYERS).map((l) => l.src),
    MODE_STATIC_SRC,
    MODE_NODE_SRC,
  ];
  urls.forEach((src) => {
    const img = new Image();
    img.src = src;
  });
}

watch(
  () => props.activeIndex,
  () => {
    clearTimers();
    resetAdaptive(false);
    resetRouting(false);
    runSequence();
  },
);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  preloadTrustImages();
  if (reduceMotion.value) {
    if (variant.value === "adaptive") resetAdaptive(true);
    else if (variant.value === "routing") resetRouting(true);
    return;
  }
  runSequence();
});

onBeforeUnmount(() => clearTimers());
</script>

<template>
  <div
    class="hc-trust-g"
    :class="[
      `hc-trust-g--${variant}`,
      { 'hc-trust-g--motion': !reduceMotion },
    ]"
    role="img"
    :aria-label="alt"
  >
    <!-- Adaptive: layered card → arrows → devices -->
    <div
      v-if="variant === 'adaptive'"
      class="hc-trust-g__stage"
      aria-hidden="true"
    >
      <img
        class="hc-trust-g__layer hc-trust-g__layer--glow"
        :class="{ 'hc-trust-g__layer--on': show.glow }"
        :style="layerStyle(LAYERS.glow)"
        :src="LAYERS.glow.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--card"
        :class="{ 'hc-trust-g__layer--on': show.card }"
        :style="layerStyle(LAYERS.card)"
        :src="LAYERS.card.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ltr"
        :class="{ 'hc-trust-g__layer--on': show.desktopArrow }"
        :style="layerStyle(LAYERS.desktopArrow)"
        :src="LAYERS.desktopArrow.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': show.desktop }"
        :style="layerStyle(LAYERS.desktop)"
        :src="LAYERS.desktop.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': show.tabletArrow }"
        :style="layerStyle(LAYERS.tabletArrow)"
        :src="LAYERS.tabletArrow.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': show.tablet }"
        :style="layerStyle(LAYERS.tablet)"
        :src="LAYERS.tablet.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-rtl"
        :class="{ 'hc-trust-g__layer--on': show.mobileArrow }"
        :style="layerStyle(LAYERS.mobileArrow)"
        :src="LAYERS.mobileArrow.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': show.mobile }"
        :style="layerStyle(LAYERS.mobile)"
        :src="LAYERS.mobile.src"
        alt=""
        decoding="async"
        draggable="false"
      />
    </div>

    <!-- Multi-Mode: rings + badges with orbiting nodes (Figma 296:1984) -->
    <div
      v-else-if="variant === 'modes'"
      class="hc-trust-g__stage hc-trust-g__stage--modes"
      aria-hidden="true"
    >
      <img
        class="hc-trust-g__modes-base"
        :src="MODE_STATIC_SRC"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        v-for="node in MODE_NODES"
        :key="node.id"
        class="hc-trust-g__modes-node"
        :class="[
          `hc-trust-g__modes-node--${node.id}`,
          { 'hc-trust-g__modes-node--motion': !reduceMotion },
        ]"
        :style="modeNodeStyle(node)"
        :src="MODE_NODE_SRC"
        alt=""
        decoding="async"
        draggable="false"
      />
    </div>

    <!-- Intelligent Routing: dotted arrows draw top → bottom (Figma 841:28554) -->
    <div
      v-else
      class="hc-trust-g__stage hc-trust-g__stage--routing"
      aria-hidden="true"
    >
      <img
        class="hc-trust-g__layer hc-trust-g__layer--glow"
        :class="{ 'hc-trust-g__layer--on': routingShow.glow }"
        :style="routingLayerStyle(ROUTING_LAYERS.glow)"
        :src="ROUTING_LAYERS.glow.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': routingShow.user }"
        :style="routingLayerStyle(ROUTING_LAYERS.user)"
        :src="ROUTING_LAYERS.user.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow11 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow11)"
        :src="ROUTING_LAYERS.arrow11.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': routingShow.hub }"
        :style="routingLayerStyle(ROUTING_LAYERS.hub)"
        :src="ROUTING_LAYERS.hub.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow12 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow12)"
        :src="ROUTING_LAYERS.arrow12.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow13 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow13)"
        :src="ROUTING_LAYERS.arrow13.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow18 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow18)"
        :src="ROUTING_LAYERS.arrow18.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': routingShow.payments }"
        :style="routingLayerStyle(ROUTING_LAYERS.payments)"
        :src="ROUTING_LAYERS.payments.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow15 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow15)"
        :src="ROUTING_LAYERS.arrow15.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow16 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow16)"
        :src="ROUTING_LAYERS.arrow16.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--arrow hc-trust-g__layer--grow-ttb"
        :class="{ 'hc-trust-g__layer--on': routingShow.arrow17 }"
        :style="routingLayerStyle(ROUTING_LAYERS.arrow17)"
        :src="ROUTING_LAYERS.arrow17.src"
        alt=""
        decoding="async"
        draggable="false"
      />
      <img
        class="hc-trust-g__layer hc-trust-g__layer--device"
        :class="{ 'hc-trust-g__layer--on': routingShow.status }"
        :style="routingLayerStyle(ROUTING_LAYERS.status)"
        :src="ROUTING_LAYERS.status.src"
        alt=""
        decoding="async"
        draggable="false"
      />
    </div>
  </div>
</template>

<style scoped>
.hc-trust-g {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.hc-trust-g__stage {
  position: absolute;
  inset: 0;
}

.hc-trust-g__stage--modes {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
  aspect-ratio: 694 / 684;
  margin: auto;
  container-type: size;
}

.hc-trust-g__stage--routing {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
  aspect-ratio: 521 / 614;
  margin: auto;
}

.hc-trust-g__modes-base {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
  pointer-events: none;
}

.hc-trust-g__modes-node {
  position: absolute;
  display: block;
  object-fit: fill;
  pointer-events: none;
  z-index: 2;
  will-change: transform;
}

.hc-trust-g__modes-node--motion.hc-trust-g__modes-node--a {
  animation: hc-modes-orbit-a 10s linear infinite;
}

.hc-trust-g__modes-node--motion.hc-trust-g__modes-node--b {
  animation: hc-modes-orbit-b 10s linear infinite;
}

.hc-trust-g__modes-node--motion.hc-trust-g__modes-node--c {
  animation: hc-modes-orbit-c 10s linear infinite;
}

/* Figma 296:1991 / 1993 / 1997 — 10s circular orbits */
@keyframes hc-modes-orbit-a {
  0% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
  4.17% { transform: translate(calc(58.234 / 694 * 100cqw), calc(7.667 / 684 * 100cqh)); }
  8.33% { transform: translate(calc(112.5 / 694 * 100cqw), calc(30.145 / 684 * 100cqh)); }
  12.5% { transform: translate(calc(159.099 / 694 * 100cqw), calc(65.902 / 684 * 100cqh)); }
  16.67% { transform: translate(calc(194.855 / 694 * 100cqw), calc(112.501 / 684 * 100cqh)); }
  20.83% { transform: translate(calc(217.332 / 694 * 100cqw), calc(166.767 / 684 * 100cqh)); }
  25% { transform: translate(calc(224.999 / 694 * 100cqw), calc(225.001 / 684 * 100cqh)); }
  29.17% { transform: translate(calc(217.332 / 694 * 100cqw), calc(283.235 / 684 * 100cqh)); }
  33.33% { transform: translate(calc(194.854 / 694 * 100cqw), calc(337.501 / 684 * 100cqh)); }
  37.5% { transform: translate(calc(159.097 / 694 * 100cqw), calc(384.1 / 684 * 100cqh)); }
  41.67% { transform: translate(calc(112.498 / 694 * 100cqw), calc(419.856 / 684 * 100cqh)); }
  45.83% { transform: translate(calc(58.232 / 694 * 100cqw), calc(442.333 / 684 * 100cqh)); }
  50% { transform: translate(calc(-0.002 / 694 * 100cqw), calc(450 / 684 * 100cqh)); }
  54.17% { transform: translate(calc(-58.236 / 694 * 100cqw), calc(442.333 / 684 * 100cqh)); }
  58.33% { transform: translate(calc(-112.502 / 694 * 100cqw), calc(419.855 / 684 * 100cqh)); }
  62.5% { transform: translate(calc(-159.101 / 694 * 100cqw), calc(384.098 / 684 * 100cqh)); }
  66.67% { transform: translate(calc(-194.857 / 694 * 100cqw), calc(337.499 / 684 * 100cqh)); }
  70.83% { transform: translate(calc(-217.335 / 694 * 100cqw), calc(283.233 / 684 * 100cqh)); }
  75% { transform: translate(calc(-225.001 / 694 * 100cqw), calc(224.999 / 684 * 100cqh)); }
  79.17% { transform: translate(calc(-217.334 / 694 * 100cqw), calc(166.765 / 684 * 100cqh)); }
  83.33% { transform: translate(calc(-194.856 / 694 * 100cqw), calc(112.499 / 684 * 100cqh)); }
  87.5% { transform: translate(calc(-159.099 / 694 * 100cqw), calc(65.9 / 684 * 100cqh)); }
  91.67% { transform: translate(calc(-112.5 / 694 * 100cqw), calc(30.144 / 684 * 100cqh)); }
  95.83% { transform: translate(calc(-58.234 / 694 * 100cqw), calc(7.666 / 684 * 100cqh)); }
  100% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
}

@keyframes hc-modes-orbit-b {
  0% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
  4.17% { transform: translate(calc(14.667 / 694 * 100cqw), calc(54.593 / 684 * 100cqh)); }
  8.33% { transform: translate(calc(14.704 / 694 * 100cqw), calc(111.121 / 684 * 100cqh)); }
  12.5% { transform: translate(calc(0.109 / 694 * 100cqw), calc(165.733 / 684 * 100cqh)); }
  16.67% { transform: translate(calc(-28.122 / 694 * 100cqw), calc(214.707 / 684 * 100cqh)); }
  20.83% { transform: translate(calc(-68.068 / 694 * 100cqw), calc(254.705 / 684 * 100cqh)); }
  25% { transform: translate(calc(-117.004 / 694 * 100cqw), calc(283.001 / 684 * 100cqh)); }
  29.17% { transform: translate(calc(-171.597 / 694 * 100cqw), calc(297.668 / 684 * 100cqh)); }
  33.33% { transform: translate(calc(-228.125 / 694 * 100cqw), calc(297.705 / 684 * 100cqh)); }
  37.5% { transform: translate(calc(-282.737 / 694 * 100cqw), calc(283.111 / 684 * 100cqh)); }
  41.67% { transform: translate(calc(-331.711 / 694 * 100cqw), calc(254.879 / 684 * 100cqh)); }
  45.83% { transform: translate(calc(-371.709 / 694 * 100cqw), calc(214.933 / 684 * 100cqh)); }
  50% { transform: translate(calc(-400.005 / 694 * 100cqw), calc(165.997 / 684 * 100cqh)); }
  54.17% { transform: translate(calc(-414.672 / 694 * 100cqw), calc(111.404 / 684 * 100cqh)); }
  58.33% { transform: translate(calc(-414.709 / 694 * 100cqw), calc(54.876 / 684 * 100cqh)); }
  62.5% { transform: translate(calc(-400.115 / 694 * 100cqw), calc(0.264 / 684 * 100cqh)); }
  66.67% { transform: translate(calc(-371.883 / 694 * 100cqw), calc(-48.71 / 684 * 100cqh)); }
  70.83% { transform: translate(calc(-331.937 / 694 * 100cqw), calc(-88.708 / 684 * 100cqh)); }
  75% { transform: translate(calc(-283.001 / 694 * 100cqw), calc(-117.004 / 684 * 100cqh)); }
  79.17% { transform: translate(calc(-228.409 / 694 * 100cqw), calc(-131.671 / 684 * 100cqh)); }
  83.33% { transform: translate(calc(-171.88 / 694 * 100cqw), calc(-131.708 / 684 * 100cqh)); }
  87.5% { transform: translate(calc(-117.268 / 694 * 100cqw), calc(-117.113 / 684 * 100cqh)); }
  91.67% { transform: translate(calc(-68.295 / 694 * 100cqw), calc(-88.882 / 684 * 100cqh)); }
  95.83% { transform: translate(calc(-28.297 / 694 * 100cqw), calc(-48.936 / 684 * 100cqh)); }
  100% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
}

@keyframes hc-modes-orbit-c {
  0% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
  4.17% { transform: translate(calc(-20.791 / 694 * 100cqw), calc(-44.076 / 684 * 100cqh)); }
  8.33% { transform: translate(calc(-29.466 / 694 * 100cqw), calc(-92.032 / 684 * 100cqh)); }
  12.5% { transform: translate(calc(-25.434 / 694 * 100cqw), calc(-140.599 / 684 * 100cqh)); }
  16.67% { transform: translate(calc(-8.969 / 694 * 100cqw), calc(-186.467 / 684 * 100cqh)); }
  20.83% { transform: translate(calc(18.807 / 694 * 100cqw), calc(-226.511 / 684 * 100cqh)); }
  25% { transform: translate(calc(56 / 694 * 100cqw), calc(-258.002 / 684 * 100cqh)); }
  29.17% { transform: translate(calc(100.077 / 694 * 100cqw), calc(-278.793 / 684 * 100cqh)); }
  33.33% { transform: translate(calc(148.032 / 694 * 100cqw), calc(-287.468 / 684 * 100cqh)); }
  37.5% { transform: translate(calc(196.599 / 694 * 100cqw), calc(-283.435 / 684 * 100cqh)); }
  41.67% { transform: translate(calc(242.468 / 694 * 100cqw), calc(-266.97 / 684 * 100cqh)); }
  45.83% { transform: translate(calc(282.511 / 694 * 100cqw), calc(-239.195 / 684 * 100cqh)); }
  50% { transform: translate(calc(314.002 / 694 * 100cqw), calc(-202.001 / 684 * 100cqh)); }
  54.17% { transform: translate(calc(334.793 / 694 * 100cqw), calc(-157.925 / 684 * 100cqh)); }
  58.33% { transform: translate(calc(343.468 / 694 * 100cqw), calc(-109.969 / 684 * 100cqh)); }
  62.5% { transform: translate(calc(339.436 / 694 * 100cqw), calc(-61.402 / 684 * 100cqh)); }
  66.67% { transform: translate(calc(322.971 / 694 * 100cqw), calc(-15.534 / 684 * 100cqh)); }
  70.83% { transform: translate(calc(295.195 / 694 * 100cqw), calc(24.51 / 684 * 100cqh)); }
  75% { transform: translate(calc(258.002 / 694 * 100cqw), calc(56 / 684 * 100cqh)); }
  79.17% { transform: translate(calc(213.925 / 694 * 100cqw), calc(76.792 / 684 * 100cqh)); }
  83.33% { transform: translate(calc(165.97 / 694 * 100cqw), calc(85.467 / 684 * 100cqh)); }
  87.5% { transform: translate(calc(117.403 / 694 * 100cqw), calc(81.434 / 684 * 100cqh)); }
  91.67% { transform: translate(calc(71.534 / 694 * 100cqw), calc(64.969 / 684 * 100cqh)); }
  95.83% { transform: translate(calc(31.491 / 694 * 100cqw), calc(37.193 / 684 * 100cqh)); }
  100% { transform: translate(calc(0 / 694 * 100cqw), calc(0 / 684 * 100cqh)); }
}

.hc-trust-g__layer {
  position: absolute;
  display: block;
  object-fit: fill;
  pointer-events: none;
  opacity: 0;
  transform: scale(0.96);
  transition:
    opacity 0.22s ease,
    transform 0.22s ease;
}

.hc-trust-g__layer--glow {
  transform: none;
  transition: opacity 0.35s ease;
}

.hc-trust-g__layer--card {
  transform: scale(0.97);
  transition:
    opacity 0.28s ease,
    transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
  z-index: 2;
}

.hc-trust-g__layer--arrow {
  z-index: 3;
  transform: none;
  opacity: 0;
  transition: none;
}

.hc-trust-g__layer--device {
  z-index: 4;
  transform: scale(0.94);
  transition:
    opacity 0.2s ease,
    transform 0.2s cubic-bezier(0.22, 1, 0.36, 1);
}

.hc-trust-g__layer--on {
  opacity: 1;
  transform: scale(1);
}

.hc-trust-g__layer--glow.hc-trust-g__layer--on {
  transform: none;
}

/* Arrow draw: clip reveal (same dotted-line feel as Adaptive) */
.hc-trust-g__layer--grow-ltr {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hc-trust-g__layer--grow-ltr.hc-trust-g__layer--on {
  clip-path: inset(0 0 0 0);
  opacity: 1;
}

.hc-trust-g__layer--grow-ttb {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 0.32s cubic-bezier(0.4, 0, 0.2, 1);
}

.hc-trust-g__layer--grow-ttb.hc-trust-g__layer--on {
  clip-path: inset(0 0 0 0);
  opacity: 1;
}

.hc-trust-g__layer--grow-rtl {
  clip-path: inset(0 0 0 100%);
  transition: clip-path 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hc-trust-g__layer--grow-rtl.hc-trust-g__layer--on {
  clip-path: inset(0 0 0 0);
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .hc-trust-g__layer,
  .hc-trust-g__layer--arrow {
    transition: none;
    transform: none;
    clip-path: none;
  }

  .hc-trust-g__modes-node {
    animation: none !important;
  }
}
</style>
