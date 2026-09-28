<script>
/** Loop length, and when one play-through has fully faded out (92.86%). */
export const LOOP_MS = 7000;
export const PLAYBACK_MS = 6500;
</script>

<script setup>
import { useId } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Payout workflow distributing funds to multiple recipients",
  },
});

const ASSET = "/images/figma-financial-ops/showcase/payout-flow";
const uid = useId();

/** Every layer is a full 576×505 canvas exported from Figma 845:2688. */
const CARDS = ["card-a", "card-pair", "card-d"];
</script>

<template>
  <svg
    class="foi-payout"
    viewBox="0 0 576 505"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    :aria-label="alt"
    :style="{ '--foi-payout-dur': `${LOOP_MS}ms` }"
  >
    <defs>
      <clipPath :id="`${uid}-connectors`">
        <rect
          class="foi-payout__reveal"
          x="70"
          y="280"
          width="440"
          height="86"
        />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/text.svg`" width="576" height="505" />

    <g class="foi-payout__flow">
      <image :href="`${ASSET}/panel.svg`" width="576" height="505" />
      <image
        :href="`${ASSET}/connectors.svg`"
        width="576"
        height="505"
        :clip-path="`url(#${uid}-connectors)`"
      />
      <g
        v-for="card in CARDS"
        :key="card"
        :class="`foi-payout__card foi-payout__card--${card}`"
      >
        <image :href="`${ASSET}/${card}.svg`" width="576" height="505" />
      </g>
    </g>

    <g class="foi-payout__cursor">
      <g class="foi-payout__cursor-move">
        <g class="foi-payout__cursor-click">
          <image :href="`${ASSET}/cursor.svg`" width="576" height="505" />
        </g>
      </g>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 7s loop (1s ≈ 14.29%): panel fades in → cursor clicks Send money → dashed
 * lines draw top → bottom together → cards rise in → everything but the
 * heading fades out. Cursor timings follow Figma 845:2764.
 */
.foi-payout {
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
  user-select: none;
}

.foi-payout__flow,
.foi-payout__reveal,
.foi-payout__card,
.foi-payout__cursor,
.foi-payout__cursor-move,
.foi-payout__cursor-click {
  animation-duration: var(--foi-payout-dur);
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.foi-payout__flow {
  animation-name: foi-payout-flow;
}

.foi-payout__reveal {
  transform-box: fill-box;
  transform-origin: 50% 0;
  animation-name: foi-payout-draw;
}

.foi-payout__card--card-a {
  animation-name: foi-payout-card-a;
}

.foi-payout__card--card-pair {
  animation-name: foi-payout-card-pair;
}

.foi-payout__card--card-d {
  animation-name: foi-payout-card-d;
}

.foi-payout__cursor {
  opacity: 0;
  animation-name: foi-payout-cursor-fade;
}

.foi-payout__cursor-move {
  animation-name: foi-payout-cursor-move;
}

/* The cursor layer is a full canvas, so scale around the arrow's resting tip. */
.foi-payout__cursor-click {
  transform-origin: 538.5px 235.5px;
  animation-name: foi-payout-cursor-click;
}

/*
 * The flow fades in over 0.3s and out at 6.0s → 6.5s. It is fully transparent
 * across the loop boundary, and every child resets at 95% while hidden, so the
 * restart never shows a jump.
 */
@keyframes foi-payout-flow {
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

/* All four dashed lines draw top → bottom together, 1.3s → 1.9s. */
@keyframes foi-payout-draw {
  0%,
  18.57% {
    transform: scaleY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  27.14%,
  95% {
    transform: scaleY(1);
  }
  95.1%,
  100% {
    transform: scaleY(0);
  }
}

/* Cards rise 20px into place (Figma order: left, middle pair, right). */
@keyframes foi-payout-card-a {
  0%,
  28.57% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  32.86%,
  95% {
    opacity: 1;
    transform: translateY(0);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: translateY(20px);
  }
}

@keyframes foi-payout-card-pair {
  0%,
  32.14% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  36.43%,
  95% {
    opacity: 1;
    transform: translateY(0);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: translateY(20px);
  }
}

@keyframes foi-payout-card-d {
  0%,
  35.71% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  40%,
  95% {
    opacity: 1;
    transform: translateY(0);
  }
  95.1%,
  100% {
    opacity: 0;
    transform: translateY(20px);
  }
}

@keyframes foi-payout-cursor-fade {
  0%,
  4.29% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  7.14% {
    opacity: 1;
  }
  21.43% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  24.29%,
  100% {
    opacity: 0;
  }
}

@keyframes foi-payout-cursor-move {
  0%,
  4.29% {
    transform: translate(0, 0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  14.29%,
  95% {
    transform: translate(-242px, 30px);
  }
  95.1%,
  100% {
    transform: translate(0, 0);
  }
}

@keyframes foi-payout-cursor-click {
  0%,
  15.71% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  17.86% {
    transform: scale(0.8);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  19.29%,
  100% {
    transform: scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-payout__flow,
  .foi-payout__reveal,
  .foi-payout__card,
  .foi-payout__cursor,
  .foi-payout__cursor-move,
  .foi-payout__cursor-click {
    animation: none;
  }
}
</style>
