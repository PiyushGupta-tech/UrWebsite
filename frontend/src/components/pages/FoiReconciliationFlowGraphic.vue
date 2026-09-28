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
    default: "Reconciliation workflow matching payouts, payments and settlements",
  },
});

const ASSET = "/images/figma-financial-ops/showcase/reconciliation-flow";
const uid = useId();
</script>

<template>
  <!-- Every layer is a full 576×505 canvas exported from Figma 845:3263. -->
  <svg
    class="foi-recon"
    viewBox="0 0 576 505"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    :aria-label="alt"
    :style="{ '--foi-recon-dur': `${LOOP_MS}ms` }"
  >
    <defs>
      <clipPath :id="`${uid}-lines-top`">
        <rect
          class="foi-recon__reveal foi-recon__reveal--top"
          x="160"
          y="203"
          width="256"
          height="64"
        />
      </clipPath>
      <clipPath :id="`${uid}-line-bottom`">
        <rect
          class="foi-recon__reveal foi-recon__reveal--bottom"
          x="278"
          y="378"
          width="20"
          height="41"
        />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/text.svg`" width="576" height="505" />

    <g class="foi-recon__flow">
      <g class="foi-recon__card foi-recon__card--sources">
        <image :href="`${ASSET}/cards-top.svg`" width="576" height="505" />
      </g>
      <image
        :href="`${ASSET}/lines-top.svg`"
        width="576"
        height="505"
        :clip-path="`url(#${uid}-lines-top)`"
      />
      <g class="foi-recon__card foi-recon__card--center">
        <image :href="`${ASSET}/center.svg`" width="576" height="505" />
        <image :href="`${ASSET}/sync.svg`" width="576" height="505" />
      </g>
      <image
        :href="`${ASSET}/line-bottom.svg`"
        width="576"
        height="505"
        :clip-path="`url(#${uid}-line-bottom)`"
      />
      <g class="foi-recon__card foi-recon__card--books">
        <image :href="`${ASSET}/books.svg`" width="576" height="505" />
      </g>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 7s loop (1s ≈ 14.29%): Payouts / Payments / Settlements rise in → dashed
 * lines draw top → bottom together → Auto Reconciliation rises in → single
 * dashed line draws → Books Balanced rises in → everything but the heading
 * fades out.
 */
.foi-recon {
  display: block;
  width: 100%;
  height: 100%;
  pointer-events: none;
  user-select: none;
}

.foi-recon__flow,
.foi-recon__reveal,
.foi-recon__card {
  animation-duration: var(--foi-recon-dur);
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.foi-recon__flow {
  animation-name: foi-recon-flow;
}

.foi-recon__reveal {
  transform-box: fill-box;
  transform-origin: 50% 0;
}

.foi-recon__reveal--top {
  animation-name: foi-recon-draw-top;
}

.foi-recon__reveal--bottom {
  animation-name: foi-recon-draw-bottom;
}

.foi-recon__card--sources {
  animation-name: foi-recon-sources;
}

.foi-recon__card--center {
  animation-name: foi-recon-center;
}

.foi-recon__card--books {
  animation-name: foi-recon-books;
}

/*
 * The flow fades in over 0.3s and out at 6.0s → 6.5s. It is fully transparent
 * across the loop boundary, and every child resets at 95% while hidden, so the
 * restart never shows a jump.
 */
@keyframes foi-recon-flow {
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

/* Source cards, 0.2s → 0.6s. */
@keyframes foi-recon-sources {
  0%,
  2.86% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  8.57%,
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

/* All three dashed lines draw top → bottom together, 0.8s → 1.4s. */
@keyframes foi-recon-draw-top {
  0%,
  11.43% {
    transform: scaleY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  20%,
  95% {
    transform: scaleY(1);
  }
  95.1%,
  100% {
    transform: scaleY(0);
  }
}

/* Auto Reconciliation card, 1.5s → 1.9s. */
@keyframes foi-recon-center {
  0%,
  21.43% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  27.14%,
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

/* Single dashed line into Books Balanced, 2.1s → 2.5s. */
@keyframes foi-recon-draw-bottom {
  0%,
  30% {
    transform: scaleY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  35.71%,
  95% {
    transform: scaleY(1);
  }
  95.1%,
  100% {
    transform: scaleY(0);
  }
}

/* Books Balanced card, 2.6s → 3.0s. */
@keyframes foi-recon-books {
  0%,
  37.14% {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  42.86%,
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

@media (prefers-reduced-motion: reduce) {
  .foi-recon__flow,
  .foi-recon__reveal,
  .foi-recon__card {
    animation: none;
  }
}
</style>
