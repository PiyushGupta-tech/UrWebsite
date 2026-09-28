<script setup>
import { useId } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Settlement transactions table highlighting an exception with a detected mismatch alert",
  },
});

/** Full 637×372 canvases cut from "Frame 2147226952.svg". */
const ASSET = "/images/figma-reconciliation/showcase-exception";
const uid = useId();

/**
 * Blue-panel beacons: centre, solid core radius and outer halo radius. Each
 * ripple grows from the core to 1.25× the halo.
 */
const BEACONS = [
  { cx: 198.523, cy: 27.3745, r: 10.7242, halo: 39.8326 },
  { cx: 322.719, cy: 70.5702, r: 8.18345, halo: 57.2842 },
  { cx: 451.054, cy: 28.9056, r: 5.40365, halo: 16.9829 },
];
const RIPPLE_S = 3.2;
const RIPPLES = BEACONS.flatMap((b, i) =>
  [0, 1].map((k) => ({
    key: `${i}-${k}`,
    ...b,
    style: {
      transformOrigin: `${b.cx}px ${b.cy}px`,
      "--rc-exception-reach": ((b.halo * 1.25) / b.r).toFixed(3),
      animationDelay: `${-(i * 0.9 + k * (RIPPLE_S / 2)).toFixed(2)}s`,
    },
  })),
);
</script>

<template>
  <svg
    class="rc-exception"
    viewBox="0 0 637 372"
    width="637"
    height="372"
    fill="none"
    role="img"
    :aria-label="alt"
    :style="{ '--rc-exception-ripple': `${RIPPLE_S}s` }"
  >
    <defs>
      <clipPath :id="`${uid}-panel`">
        <path
          d="M110.207 14.2857C110.207 6.39594 116.603 0 124.493 0H475.207C483.097 0 489.493 6.39593 489.493 14.2857V251.737C489.493 259.627 483.097 266.023 475.207 266.023H124.493C116.603 266.023 110.207 259.627 110.207 251.737V14.2857Z"
        />
      </clipPath>
      <clipPath :id="`${uid}-connector`">
        <rect class="rc-exception__connector-reveal" x="398" y="158" width="66" height="60" />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/panel.svg`" width="637" height="372" />
    <g :clip-path="`url(#${uid}-panel)`">
      <circle
        v-for="ripple in RIPPLES"
        :key="ripple.key"
        class="rc-exception__ripple"
        :cx="ripple.cx"
        :cy="ripple.cy"
        :r="ripple.r"
        :style="ripple.style"
        fill="white"
        fill-opacity="0.15"
        stroke="white"
        stroke-opacity="0.7"
        stroke-width="1"
        vector-effect="non-scaling-stroke"
      />
    </g>

    <g class="rc-exception__connector" :clip-path="`url(#${uid}-connector)`">
      <image :href="`${ASSET}/connector.svg`" width="637" height="372" />
    </g>
    <g class="rc-exception__popup">
      <image :href="`${ASSET}/popup.svg`" width="637" height="372" />
      <g class="rc-exception__icon">
        <image :href="`${ASSET}/popup-icon.svg`" width="637" height="372" />
      </g>
    </g>

    <image :href="`${ASSET}/table.svg`" width="637" height="372" />
    <g class="rc-exception__flag">
      <image :href="`${ASSET}/row-flag.svg`" width="637" height="372" />
    </g>
    <rect
      class="rc-exception__flash"
      x="14.0723"
      y="294.238"
      width="368.284"
      height="20.866"
      fill="#EF4444"
    />
    <circle
      v-for="n in 2"
      :key="n"
      :class="`rc-exception__ping rc-exception__ping--${n}`"
      cx="282.997"
      cy="304.671"
      r="1.20617"
      fill="#991B1B"
    />
  </svg>
</template>

<style scoped>
/*
 * Beacon ripples on the blue panel run continuously. On an 8s loop (1s =
 * 12.5%) row 3 flashes and glows red at 0.6s while its status dot pings, the
 * dotted line draws to the Exception Detected pop-up at 1.4s, the pop-up rises
 * in at 1.9s and its warning icon shakes at 2.6s. At 7s → 7.5s the row glow,
 * line and pop-up fade out; the line's reveal resets at 95%.
 */
.rc-exception {
  display: block;
  pointer-events: none;
  user-select: none;
}

.rc-exception__ripple,
.rc-exception__connector,
.rc-exception__connector-reveal,
.rc-exception__popup,
.rc-exception__icon,
.rc-exception__flag,
.rc-exception__flash,
.rc-exception__ping {
  transform-box: view-box;
}

.rc-exception__connector,
.rc-exception__connector-reveal,
.rc-exception__popup,
.rc-exception__icon,
.rc-exception__flag,
.rc-exception__flash,
.rc-exception__ping {
  animation-duration: 8s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

/* Decorations are hidden at rest so the static art matches the original. */
.rc-exception__ripple,
.rc-exception__flash,
.rc-exception__ping {
  opacity: 0;
}

.rc-exception__ripple {
  animation: rc-exception-ripple var(--rc-exception-ripple) cubic-bezier(0, 0, 0.58, 1) infinite;
}

.rc-exception__connector {
  animation-name: rc-exception-fade;
}

.rc-exception__connector-reveal {
  transform-box: fill-box;
  transform-origin: 0 50%;
  animation-name: rc-exception-draw;
}

.rc-exception__popup {
  animation-name: rc-exception-popup;
}

.rc-exception__icon {
  transform-origin: 480.134px 209.98px;
  animation-name: rc-exception-shake;
}

.rc-exception__flag {
  animation-name: rc-exception-flag;
}

.rc-exception__flash {
  animation-name: rc-exception-flash;
}

.rc-exception__ping {
  transform-origin: 282.997px 304.671px;
}

.rc-exception__ping--1 {
  animation-name: rc-exception-ping-1;
}

.rc-exception__ping--2 {
  animation-name: rc-exception-ping-2;
}

@keyframes rc-exception-ripple {
  0% {
    opacity: 0.9;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(var(--rc-exception-reach));
  }
}

@keyframes rc-exception-flag {
  0%,
  7.5% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  12.5%,
  87.5% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  93.75%,
  100% {
    opacity: 0;
  }
}

@keyframes rc-exception-flash {
  0%,
  7.5% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  11.25% {
    opacity: 0.14;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  17.5%,
  100% {
    opacity: 0;
  }
}

/* Two staggered pings per ring: 0.7s and 3.5s, then 1.4s and 4.2s. */
@keyframes rc-exception-ping-1 {
  0%,
  8.75% {
    opacity: 0;
    transform: scale(1);
  }
  8.76% {
    opacity: 0.45;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  26.25% {
    opacity: 0;
    transform: scale(5);
  }
  26.26%,
  43.75% {
    opacity: 0;
    transform: scale(1);
  }
  43.76% {
    opacity: 0.45;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  61.25%,
  100% {
    opacity: 0;
    transform: scale(5);
  }
}

@keyframes rc-exception-ping-2 {
  0%,
  17.5% {
    opacity: 0;
    transform: scale(1);
  }
  17.51% {
    opacity: 0.45;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  35% {
    opacity: 0;
    transform: scale(5);
  }
  35.01%,
  52.5% {
    opacity: 0;
    transform: scale(1);
  }
  52.51% {
    opacity: 0.45;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  70%,
  100% {
    opacity: 0;
    transform: scale(5);
  }
}

/* The dotted line runs top-left → bottom-right, so it reveals from the left. */
@keyframes rc-exception-draw {
  0%,
  17.5% {
    transform: scaleX(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  25%,
  95% {
    transform: scaleX(1);
  }
  95.1%,
  100% {
    transform: scaleX(0);
  }
}

@keyframes rc-exception-fade {
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

@keyframes rc-exception-popup {
  0%,
  23.75% {
    opacity: 0;
    transform: translateY(10px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  30%,
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

@keyframes rc-exception-shake {
  0%,
  32.5% {
    transform: rotate(0deg);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  34.25% {
    transform: rotate(-14deg);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  36% {
    transform: rotate(12deg);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  37.75% {
    transform: rotate(-8deg);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  39.5% {
    transform: rotate(5deg);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  41.25%,
  100% {
    transform: rotate(0deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rc-exception__ripple,
  .rc-exception__connector,
  .rc-exception__connector-reveal,
  .rc-exception__popup,
  .rc-exception__icon,
  .rc-exception__flag,
  .rc-exception__flash,
  .rc-exception__ping {
    animation: none;
  }
}
</style>
