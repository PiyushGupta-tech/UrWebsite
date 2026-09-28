<script setup>
import { onMounted, ref } from "vue";

defineProps({
  ready: { type: Boolean, default: false },
  alt: { type: String, default: "Distribute funds across recipients" },
});

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});

/**
 * Hero fan 643:6031 — exact Figma stroke outlines in fan-wires.svg.
 * Centerlines below drive animateMotion only (invisible).
 * Fan origin in cropped viewBox (72 0 804 510): (266.12, 228.31).
 */
const FAN = {
  leftPct: 24.144,
  topPct: 44.767,
  widthPct: 54.134,
  heightPct: 31.799,
  w: 435.23583984375,
  h: 162.17295837402344,
  wires: [
    {
      id: "413:8110",
      matrix: [
        -0.01992146112024784, -0.999801516532898, -0.9998041987419128,
        0.01978776417672634, 432.4775390625, 82.98352813720703,
      ],
      d: "M 0 4.18738331411809 L 35.345335749290605 0 L 45.83701968096372 84.9167038691779 L 57.18436616116679 202.4133608599758 L 83 213",
    },
    {
      id: "413:8112",
      matrix: [
        -0.013578505255281925, -0.9999077916145325, -0.9995786547660828,
        0.029027795419096947, 309.1982421875, 151.1846923828125,
      ],
      d: "M 0 4.708025554436927 L 61.66929590213385 0 L 79.81656503207651 52.25142447264891 L 102.14905100569287 76.18443975643201 C 102.14905100569287 76.18443975643201 108.58280485350494 80.9633254016211 112.83244963239352 82.877539687543 C 116.82709081772896 84.676889808139 122.6610862538311 85.80006407434588 122.6610862538311 85.80006407434588 L 148.66017150878906 91.49235534667969",
    },
    {
      id: "413:8113",
      matrix: [
        0.013578508980572224, -0.9999077916145325, 0.9995786547660828,
        0.029027795419096947, 111.44287109375, 154.9210205078125,
      ],
      d: "M 0 5.193668627948866 L 62.29728364096778 0 L 85.90464240705954 63.69322693066846 L 106.03110719197781 103.8015365600586 L 153.00628662109375 100.79610198721842",
    },
    {
      id: "413:8199",
      matrix: [
        -0.01992146112024784, -0.999801516532898, 0.9998041987419128,
        -0.01978776417672634, 2.028369188308716, 91.50346148014069,
      ],
      d: "M 0 4.18738331411809 L 35.345335749290605 0 L 45.83701968096372 84.9167038691779 L 57.18436616116679 202.4133608599758 L 83 213",
    },
  ],
};

function matrixAttr(m) {
  return `matrix(${m.join(" ")})`;
}
</script>

<template>
  <div
    class="po-hero-graphic"
    :class="{
      'po-hero-graphic--ready': ready,
      'po-hero-graphic--motion': ready && !reduceMotion,
    }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="po-hero-graphic__art"
      data-po-part="distribute"
      src="/images/figma-payouts/hero/distribute-hero.svg?v=8"
      alt=""
      width="804"
      height="510"
      decoding="async"
    />

    <!-- Exact Figma 643:6031 stroke outlines (blue) -->
    <img
      class="po-hero-graphic__wires"
      src="/images/figma-payouts/hero/fan-wires.svg?v=1"
      alt=""
      decoding="async"
      aria-hidden="true"
      :style="{
        left: `${FAN.leftPct}%`,
        top: `${FAN.topPct}%`,
        width: `${FAN.widthPct}%`,
        height: `${FAN.heightPct}%`,
      }"
    />

    <!-- Invisible centerlines — flow dots only -->
    <svg
      class="po-hero-graphic__fx"
      :viewBox="`0 0 ${FAN.w} ${FAN.h}`"
      fill="none"
      aria-hidden="true"
      :style="{
        left: `${FAN.leftPct}%`,
        top: `${FAN.topPct}%`,
        width: `${FAN.widthPct}%`,
        height: `${FAN.heightPct}%`,
      }"
    >
      <g
        v-for="(wire, i) in FAN.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path :d="wire.d" fill="none" stroke="none" />
        <circle
          v-show="ready && !reduceMotion"
          class="po-hero-graphic__flow-dot"
          r="2.2"
        >
          <!-- Path runs outer→hub; reverse so flow is hub→recipients -->
          <animateMotion
            :dur="`${2.6 + i * 0.22}s`"
            :begin="`${i * 0.32}s`"
            repeatCount="indefinite"
            calcMode="linear"
            keyPoints="1;0"
            keyTimes="0;1"
            :path="wire.d"
          />
        </circle>
      </g>
    </svg>
  </div>
</template>

<style scoped>
/* Cropped content frame 804×510 — no empty SVG padding */
.po-hero-graphic {
  position: relative;
  width: 100%;
  max-width: 100%;
  max-height: calc(100svh - var(--page-nav-offset, 129px) - 32px);
  aspect-ratio: 804 / 510;
  margin: 0;
  padding: 0;
  overflow: hidden;
  line-height: 0;
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.7s ease,
    transform 0.7s ease;
}

.po-hero-graphic--ready {
  opacity: 1;
  transform: translateY(0);
}

.po-hero-graphic__art {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  object-fit: fill;
  pointer-events: none;
  user-select: none;
}

.po-hero-graphic__wires,
.po-hero-graphic__fx {
  position: absolute;
  display: block;
  overflow: visible;
  pointer-events: none;
  user-select: none;
}

.po-hero-graphic__wires {
  object-fit: fill;
}

.po-hero-graphic--motion .po-hero-graphic__wires {
  animation: po-hero-wires-pulse 1.8s ease-in-out infinite;
}

.po-hero-graphic__flow-dot {
  fill: #38b7d3;
  filter: drop-shadow(0 0 3px rgba(56, 183, 211, 0.95));
}

@keyframes po-hero-wires-pulse {
  0%,
  100% {
    opacity: 0.88;
  }
  50% {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .po-hero-graphic--motion .po-hero-graphic__wires {
    animation: none;
  }
}
</style>
