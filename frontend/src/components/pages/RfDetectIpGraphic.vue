<script setup>
import { useId } from "vue";

const ASSET = "/images/figma-risk-fraud/detect/ip";
const uid = useId();
</script>

<template>
  <svg
    class="rf-ip"
    viewBox="0 0 436 331"
    preserveAspectRatio="xMidYMid meet"
    aria-hidden="true"
  >
    <defs>
      <clipPath :id="`${uid}-card`">
        <rect x="95.8203" y="107.141" width="243.895" height="104.526" rx="10.4526" />
      </clipPath>
      <linearGradient :id="`${uid}-scan`" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#3B82F6" stop-opacity="0" />
        <stop offset="0.85" stop-color="#3B82F6" stop-opacity="0.18" />
        <stop offset="1" stop-color="#3B82F6" stop-opacity="0.45" />
      </linearGradient>
    </defs>

    <image :href="`${ASSET}/laptop.svg`" width="436" height="331" />

    <g :clip-path="`url(#${uid}-card)`">
      <rect
        class="rf-ip__scan"
        x="47.8203"
        y="107.141"
        width="48"
        height="104.526"
        :fill="`url(#${uid}-scan)`"
      />
    </g>

    <circle
      class="rf-ip__ripple"
      cx="313.576"
      cy="191.631"
      r="43.5526"
      fill="#FF4B55"
      fill-opacity="0.12"
      stroke="#FF4B55"
      stroke-opacity="0.5"
      stroke-width="1.2"
    />
    <g class="rf-ip__pin">
      <image :href="`${ASSET}/pin.svg`" width="436" height="331" />
    </g>
    <g class="rf-ip__badge">
      <image :href="`${ASSET}/badge.svg`" width="436" height="331" />
    </g>
  </svg>
</template>

<style scoped>
/*
 * 5s loop (1s = 20%): a scan sweeps the IP card 0.1s → 1.8s, the pin circle
 * pops and ripples, the badge pops in at 2s, pulses once more, then fades out
 * at 4.4s → 4.7s so the next scan starts clean.
 */
.rf-ip {
  display: block;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  user-select: none;
}

.rf-ip__scan,
.rf-ip__ripple,
.rf-ip__pin,
.rf-ip__badge {
  transform-box: view-box;
  animation-duration: 5s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rf-ip__scan {
  opacity: 0;
  animation-name: rf-ip-scan;
}

.rf-ip__ripple {
  opacity: 0;
  transform-origin: 313.576px 191.631px;
  animation-name: rf-ip-ripple;
}

.rf-ip__pin {
  transform-origin: 313.576px 191.631px;
  animation-name: rf-ip-pin;
}

.rf-ip__badge {
  transform-origin: 366.709px 227.346px;
  animation-name: rf-ip-badge;
}

/* Card is 243.9 wide; the 48-wide beam travels fully across it. */
@keyframes rf-ip-scan {
  0% {
    opacity: 0;
    transform: translateX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  4% {
    opacity: 1;
  }
  32% {
    opacity: 1;
  }
  36% {
    opacity: 0;
    transform: translateX(292px);
  }
  36.1%,
  100% {
    opacity: 0;
    transform: translateX(0);
  }
}

@keyframes rf-ip-pin {
  0%,
  36% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  42% {
    transform: scale(1.1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  50%,
  100% {
    transform: scale(1);
  }
}

@keyframes rf-ip-ripple {
  0%,
  36% {
    opacity: 0;
    transform: scale(1);
  }
  37% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  64% {
    opacity: 0;
    transform: scale(1.55);
  }
  64.1%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rf-ip-badge {
  0%,
  40% {
    opacity: 0;
    transform: scale(0.4);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  45% {
    opacity: 1;
    transform: scale(1.14);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  50% {
    transform: scale(1);
  }
  62% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  67% {
    transform: scale(1.12);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  74%,
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
  .rf-ip__scan,
  .rf-ip__ripple,
  .rf-ip__pin,
  .rf-ip__badge {
    animation: none;
  }
}
</style>
