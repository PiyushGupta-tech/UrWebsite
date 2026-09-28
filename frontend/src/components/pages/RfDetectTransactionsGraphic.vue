<script setup>
import { useId } from "vue";

const ASSET = "/images/figma-risk-fraud/detect/transactions";
const uid = useId();
</script>

<template>
  <svg
    class="rf-tx"
    viewBox="0 0 454 308"
    preserveAspectRatio="xMidYMid meet"
    aria-hidden="true"
  >
    <defs>
      <filter
        :id="`${uid}-glow`"
        x="0"
        y="105"
        width="454"
        height="114"
        filterUnits="userSpaceOnUse"
      >
        <feGaussianBlur stdDeviation="7" />
      </filter>
    </defs>

    <rect
      class="rf-tx__glow"
      x="16.5908"
      y="129.08"
      width="409"
      height="66"
      rx="14"
      fill="#FFA72E"
      :filter="`url(#${uid}-glow)`"
    />
    <g class="rf-tx__row rf-tx__row--success">
      <image :href="`${ASSET}/row-success.svg`" width="454" height="308" />
    </g>
    <g class="rf-tx__row rf-tx__row--pending">
      <image :href="`${ASSET}/row-pending.svg`" width="454" height="308" />
    </g>
    <g class="rf-tx__row rf-tx__row--failed">
      <image :href="`${ASSET}/row-failed.svg`" width="454" height="308" />
    </g>
    <g class="rf-tx__badge">
      <image :href="`${ASSET}/badge.svg`" width="454" height="308" />
    </g>
  </svg>
</template>

<style scoped>
/*
 * 6s loop (1s ≈ 16.67%): rows slide up one after another, the Pending row
 * starts glowing amber at 1.4s, the badge pops in at 1.7s and pulses, then
 * everything fades out 5.3s → 5.65s and resets while hidden.
 */
.rf-tx {
  display: block;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  user-select: none;
}

.rf-tx__glow,
.rf-tx__row,
.rf-tx__badge {
  transform-box: view-box;
  animation-duration: 6s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rf-tx__glow {
  opacity: 0;
  animation-name: rf-tx-glow;
}

.rf-tx__row--success {
  animation-name: rf-tx-row-1;
}

.rf-tx__row--pending {
  animation-name: rf-tx-row-2;
}

.rf-tx__row--failed {
  animation-name: rf-tx-row-3;
}

.rf-tx__badge {
  transform-origin: 425.591px 138px;
  animation-name: rf-tx-badge;
}

@keyframes rf-tx-row-1 {
  0% {
    opacity: 0;
    transform: translateY(16px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  8%,
  88% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94% {
    opacity: 0;
    transform: translateY(0);
  }
  94.1%,
  100% {
    opacity: 0;
    transform: translateY(16px);
  }
}

@keyframes rf-tx-row-2 {
  0%,
  6% {
    opacity: 0;
    transform: translateY(16px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  14%,
  88% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94% {
    opacity: 0;
    transform: translateY(0);
  }
  94.1%,
  100% {
    opacity: 0;
    transform: translateY(16px);
  }
}

@keyframes rf-tx-row-3 {
  0%,
  12% {
    opacity: 0;
    transform: translateY(16px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  20%,
  88% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94% {
    opacity: 0;
    transform: translateY(0);
  }
  94.1%,
  100% {
    opacity: 0;
    transform: translateY(16px);
  }
}

/* Breathes twice between 0.35 and 0.15 once the Pending row is flagged. */
@keyframes rf-tx-glow {
  0%,
  24% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  30% {
    opacity: 0.35;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  45% {
    opacity: 0.15;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  60% {
    opacity: 0.35;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  75% {
    opacity: 0.15;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  88% {
    opacity: 0.35;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94%,
  100% {
    opacity: 0;
  }
}

@keyframes rf-tx-badge {
  0%,
  28% {
    opacity: 0;
    transform: scale(0.4);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  33% {
    opacity: 1;
    transform: scale(1.14);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  38% {
    transform: scale(1);
  }
  52% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  57% {
    transform: scale(1.12);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  63% {
    transform: scale(1);
  }
  72% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  77% {
    transform: scale(1.12);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  83%,
  88% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94%,
  100% {
    opacity: 0;
    transform: scale(0.6);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rf-tx__glow,
  .rf-tx__row,
  .rf-tx__badge {
    animation: none;
  }
}
</style>
