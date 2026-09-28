<script>
/** Loop length, and when one play-through has fully faded out (93.75%). */
export const LOOP_MS = 8000;
export const PLAYBACK_MS = 7500;
</script>

<script setup>
import { useId } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Collections QR scan and pay flow with payment received",
  },
});

const ASSET = "/images/figma-financial-ops/showcase/payin";
const uid = useId();

/** Connector layers are full 576×542 canvases; each draws across the same x span. */
const CONNECTORS = [1, 2, 3, 4];
const CONNECTOR_X = 144;
const CONNECTOR_W = 68;

/** "Pay Now" button geometry from Figma 837:4821 in the 576×542 export space. */
const BUTTON = { x: 236.917, y: 419.334, w: 119.809, h: 25.213, r: 7.55 };
const BUTTON_CX = BUTTON.x + BUTTON.w / 2;
const BUTTON_CY = BUTTON.y + BUTTON.h / 2;
</script>

<template>
  <svg
    class="foi-payin"
    viewBox="0 0 576 542"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    :aria-label="alt"
    :style="{ '--foi-payin-dur': `${LOOP_MS}ms` }"
  >
    <defs>
      <clipPath
        v-for="n in CONNECTORS"
        :id="`${uid}-connector-${n}`"
        :key="n"
      >
        <rect
          class="foi-payin__reveal foi-payin__reveal--connector"
          :x="CONNECTOR_X"
          y="0"
          :width="CONNECTOR_W"
          height="542"
        />
      </clipPath>
      <clipPath :id="`${uid}-arrow`">
        <rect
          class="foi-payin__reveal foi-payin__reveal--arrow"
          x="390"
          y="300"
          width="39"
          height="34"
        />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/text.svg`" width="576" height="542" />

    <g class="foi-payin__flow">
      <image :href="`${ASSET}/cards.svg`" width="576" height="542" />
      <image
        v-for="n in CONNECTORS"
        :key="n"
        :href="`${ASSET}/connector-${n}.svg`"
        width="576"
        height="542"
        :clip-path="`url(#${uid}-connector-${n})`"
      />

      <g class="foi-payin__phone">
        <image :href="`${ASSET}/phone.svg`" width="576" height="542" />
        <g class="foi-payin__processing">
          <rect
            :x="BUTTON.x"
            :y="BUTTON.y"
            :width="BUTTON.w"
            :height="BUTTON.h"
            :rx="BUTTON.r"
            fill="#097495"
          />
          <circle
            :cx="BUTTON_CX - 25"
            :cy="BUTTON_CY"
            r="3.2"
            fill="none"
            stroke="#fff"
            stroke-opacity="0.35"
            stroke-width="1.2"
          />
          <circle
            class="foi-payin__spinner"
            :cx="BUTTON_CX - 25"
            :cy="BUTTON_CY"
            r="3.2"
            fill="none"
            stroke="#fff"
            stroke-width="1.2"
            stroke-linecap="round"
            stroke-dasharray="7 13.1"
          />
          <text
            class="foi-payin__processing-label"
            :x="BUTTON_CX + 5"
            :y="BUTTON_CY"
            text-anchor="middle"
            dominant-baseline="central"
          >
            Processing...
          </text>
        </g>
      </g>

      <image
        :href="`${ASSET}/arrow.svg`"
        x="390.283"
        y="312.148"
        width="38"
        height="10"
        :clip-path="`url(#${uid}-arrow)`"
      />

      <g class="foi-payin__success">
        <image
          :href="`${ASSET}/success.svg`"
          x="436.761"
          y="261"
          width="107"
          height="112"
        />
      </g>
    </g>

    <g class="foi-payin__cursor">
      <g class="foi-payin__cursor-move">
        <g class="foi-payin__cursor-click">
          <image
            :href="`${ASSET}/cursor.svg`"
            x="550"
            y="400"
            width="24"
            height="24"
          />
        </g>
      </g>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 8s loop (1s = 12.5%): cards fade in → connectors draw → phone → cursor
 * clicks Pay Now → Processing → arrow draws → Payment Received → everything
 * but the heading fades out.
 */
.foi-payin {
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
  user-select: none;
}

.foi-payin__flow,
.foi-payin__reveal,
.foi-payin__phone,
.foi-payin__processing,
.foi-payin__success,
.foi-payin__cursor,
.foi-payin__cursor-move,
.foi-payin__cursor-click {
  animation-duration: var(--foi-payin-dur);
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.foi-payin__flow {
  animation-name: foi-payin-flow;
}

.foi-payin__reveal {
  transform-box: fill-box;
  transform-origin: 0 50%;
}

.foi-payin__reveal--connector {
  animation-name: foi-payin-draw-connector;
}

.foi-payin__reveal--arrow {
  animation-name: foi-payin-draw-arrow;
}

.foi-payin__phone {
  transform-box: fill-box;
  transform-origin: center;
  animation-name: foi-payin-phone;
}

.foi-payin__processing {
  opacity: 0;
  animation-name: foi-payin-processing;
}

.foi-payin__processing-label {
  fill: #fff;
  font-family: var(--font, "DM Sans", system-ui, sans-serif);
  font-size: 8px;
  font-weight: 600;
}

.foi-payin__spinner {
  transform-box: fill-box;
  transform-origin: center;
  animation: foi-payin-spin 0.8s linear infinite;
}

.foi-payin__success {
  transform-box: fill-box;
  transform-origin: center;
  animation-name: foi-payin-success;
}

.foi-payin__cursor {
  opacity: 0;
  animation-name: foi-payin-cursor-fade;
}

.foi-payin__cursor-move {
  animation-name: foi-payin-cursor-move;
}

.foi-payin__cursor-click {
  transform-box: fill-box;
  transform-origin: center;
  animation-name: foi-payin-cursor-click;
}

/*
 * The flow (cards and everything after them) fades in over 0.3s and out at
 * 7.0s → 7.5s. It is fully transparent across the loop boundary, and every
 * child resets at 95% while hidden, so the restart never shows a jump.
 */
@keyframes foi-payin-flow {
  0% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  3.75%,
  87.5% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
  }
}

/* All four connectors draw left → right together, 0.3s → 0.9s. */
@keyframes foi-payin-draw-connector {
  0%,
  3.75% {
    transform: scaleX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  11.25%,
  95% {
    transform: scaleX(1);
  }
  95.1%,
  100% {
    transform: scaleX(0);
  }
}

/* 1.45s → 1.85s */
@keyframes foi-payin-phone {
  0%,
  18.125% {
    opacity: 0;
    transform: scale(0.96);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  23.125%,
  95% {
    opacity: 1;
    transform: scale(1);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: scale(0.96);
  }
}

/* Cursor: in at 2.3s, travels to Pay Now by 2.9s, clicks at 3.2s, out by 3.6s. */
@keyframes foi-payin-cursor-fade {
  0%,
  28.75% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  31.25% {
    opacity: 1;
  }
  42.5% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  45%,
  100% {
    opacity: 0;
  }
}

@keyframes foi-payin-cursor-move {
  0%,
  28.75% {
    transform: translate(0, 0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  36.25%,
  95% {
    transform: translate(-220px, 30px);
  }
  95.1%,
  100% {
    transform: translate(0, 0);
  }
}

@keyframes foi-payin-cursor-click {
  0%,
  38.125% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  40% {
    transform: scale(0.8);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  41.875%,
  100% {
    transform: scale(1);
  }
}

/* Pay Now → Processing on the click (3.2s). */
@keyframes foi-payin-processing {
  0%,
  40% {
    opacity: 0;
  }
  41.5%,
  95% {
    opacity: 1;
  }
  95.1%,
  100% {
    opacity: 0;
  }
}

@keyframes foi-payin-spin {
  to {
    transform: rotate(360deg);
  }
}

/* 4.3s → 4.9s */
@keyframes foi-payin-draw-arrow {
  0%,
  53.75% {
    transform: scaleX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  61.25%,
  95% {
    transform: scaleX(1);
  }
  95.1%,
  100% {
    transform: scaleX(0);
  }
}

/* 4.9s → 5.3s, once the arrow has finished drawing. */
@keyframes foi-payin-success {
  0%,
  61.25% {
    opacity: 0;
    transform: scale(0.5);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  66.25%,
  95% {
    opacity: 1;
    transform: scale(1);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: scale(0.5);
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-payin__flow,
  .foi-payin__reveal,
  .foi-payin__phone,
  .foi-payin__processing,
  .foi-payin__spinner,
  .foi-payin__success,
  .foi-payin__cursor,
  .foi-payin__cursor-move,
  .foi-payin__cursor-click {
    animation: none;
  }
}
</style>
