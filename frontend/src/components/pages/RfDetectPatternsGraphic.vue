<script setup>
import { useId } from "vue";

const uid = useId();

/*
 * Bars from Figma "Frame 2147226663" (403×300). Each path runs down to y=400 so
 * rising bars never lift off the baseline; the canvas clip hides the overflow,
 * which would otherwise show in the letterbox below the 403×300 viewBox.
 * `up` / `down` are translateY limits: `up` keeps the bar's rounded top at
 * least ~8px below the green line, its node dots, the dashed ring and the
 * alert badge above it.
 */
const BARS = [
  {
    d: "M26.2285 218.528C26.2285 211.607 31.8394 205.996 38.7608 205.996H49.6962C56.6176 205.996 62.2285 211.607 62.2285 218.528V400H26.2285V218.528Z",
    y1: 205.996,
    up: -62,
    down: 20,
    dur: 3.2,
    delay: -0.4,
  },
  {
    d: "M74.2285 130.528C74.2285 123.607 79.8394 117.996 86.7608 117.996H100.696C107.618 117.996 113.229 123.607 113.229 130.528V400H74.2285V130.528Z",
    y1: 117.996,
    up: 0,
    down: 60,
    dur: 2.6,
    delay: -1.9,
  },
  {
    d: "M125.229 218.528C125.229 211.607 130.839 205.996 137.761 205.996H151.696C158.618 205.996 164.229 211.607 164.229 218.528V400H125.229V218.528Z",
    y1: 205.996,
    up: -86,
    down: 20,
    dur: 3.4,
    delay: -2.6,
  },
  {
    d: "M178.229 145.528C178.229 138.607 183.839 132.996 190.761 132.996H204.696C211.618 132.996 217.229 138.607 217.229 145.528V400H178.229V145.528Z",
    y1: 132.996,
    up: -8,
    down: 50,
    dur: 2.8,
    delay: -0.9,
  },
  {
    d: "M231.229 180.528C231.229 173.607 236.839 167.996 243.761 167.996H257.696C264.618 167.996 270.229 173.607 270.229 180.528V400H231.229V180.528Z",
    y1: 167.996,
    up: -72,
    down: 24,
    dur: 3,
    delay: -2.2,
  },
  {
    d: "M283.229 115.528C283.229 108.607 288.839 102.996 295.761 102.996H310.696C317.618 102.996 323.229 108.607 323.229 115.528V400H283.229V115.528Z",
    y1: 102.996,
    up: -12,
    down: 50,
    dur: 2.5,
    delay: -1.3,
  },
  {
    d: "M336.229 137.528C336.229 130.607 341.839 124.996 348.761 124.996H364.696C371.618 124.996 377.229 130.607 377.229 137.528V400H336.229V137.528Z",
    y1: 124.996,
    up: -22,
    down: 40,
    dur: 3.1,
    delay: -0.2,
  },
];
</script>

<template>
  <svg
    class="rf-patterns"
    viewBox="0 0 403 300"
    preserveAspectRatio="xMidYMid meet"
    fill="none"
    aria-hidden="true"
  >
    <defs>
      <clipPath :id="`${uid}-canvas`">
        <rect width="403" height="300" />
      </clipPath>
      <linearGradient
        v-for="(bar, i) in BARS"
        :id="`${uid}-bar-${i}`"
        :key="i"
        x1="0"
        :y1="bar.y1"
        x2="0"
        y2="299.996"
        gradientUnits="userSpaceOnUse"
      >
        <stop stop-color="#BDE7FF" />
        <stop offset="1" stop-color="#79C8FF" />
      </linearGradient>
      <filter
        :id="`${uid}-badge`"
        x="344.366"
        y="48.9528"
        width="57.885"
        height="57.886"
        filterUnits="userSpaceOnUse"
        color-interpolation-filters="sRGB"
      >
        <feFlood flood-opacity="0" result="BackgroundImageFix" />
        <feColorMatrix
          in="SourceAlpha"
          type="matrix"
          values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
          result="hardAlpha"
        />
        <feOffset dy="5.0335" />
        <feGaussianBlur stdDeviation="5.0335" />
        <feComposite in2="hardAlpha" operator="out" />
        <feColorMatrix
          type="matrix"
          values="0 0 0 0 0.937255 0 0 0 0 0.266667 0 0 0 0 0.266667 0 0 0 0.25098 0"
        />
        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow" />
        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow" result="shape" />
      </filter>
    </defs>

    <g :clip-path="`url(#${uid}-canvas)`">
      <path
        v-for="(bar, i) in BARS"
        :key="i"
        class="rf-patterns__bar"
        :d="bar.d"
        :fill="`url(#${uid}-bar-${i})`"
        :style="{
          '--rf-bar-up': `${bar.up}px`,
          '--rf-bar-down': `${bar.down}px`,
          '--rf-bar-dur': `${bar.dur}s`,
          '--rf-bar-delay': `${bar.delay}s`,
        }"
      />
    </g>

    <line x1="11.6515" y1="140.535" x2="99.7393" y2="90.209" stroke="#10B981" stroke-width="3.77513" />
    <line x1="100.942" y1="89.9693" x2="189.027" y2="102.553" stroke="#10B981" stroke-width="3.77513" />
    <line x1="187.837" y1="102.772" x2="301.144" y2="39.8354" stroke="#10B981" stroke-width="3.77513" />
    <line x1="302.959" y1="39.8735" x2="378.456" y2="83.92" stroke="#10B981" stroke-width="3.77513" />

    <circle
      class="rf-patterns__ring"
      cx="302.014"
      cy="41.5052"
      r="36.8075"
      fill="#991B1B"
      fill-opacity="0.0823529"
      stroke="#991B1B"
      stroke-width="1.88756"
      stroke-dasharray="5.03 3.78"
    />

    <path
      d="M12.4004 132.594C14.61 132.913 16.8658 134.126 18.7041 135.977C20.5343 137.819 21.7784 140.122 22.1621 142.392C22.0462 147.584 17.804 151.758 12.584 151.758C7.2911 151.758 3.00012 147.467 3 142.174C3 136.942 7.19207 132.692 12.4004 132.594Z"
      fill="white"
      stroke="#20BE92"
      stroke-width="6"
    />
    <circle cx="100.671" cy="91.8396" r="9.58376" fill="#059669" stroke="#20BE92" stroke-width="6" />
    <circle cx="188.759" cy="104.422" r="9.58376" fill="white" stroke="#20BE92" stroke-width="6" />
    <circle cx="302.012" cy="41.5037" r="9.43782" fill="white" stroke="#991B1B" stroke-width="6.29188" />

    <circle class="rf-patterns__ripple" cx="373.309" cy="72.862" r="18.876" fill="#991B1B" />
    <g class="rf-patterns__badge" :filter="`url(#${uid}-badge)`">
      <rect
        x="354.433"
        y="53.9863"
        width="37.7513"
        height="37.7513"
        rx="18"
        fill="#991B1B"
        shape-rendering="crispEdges"
      />
      <path
        d="M375.107 65.2184L374.778 75.3784H371.839L371.51 65.2184H375.107ZM373.305 80.0687C372.795 80.0687 372.356 79.8875 371.989 79.5253C371.627 79.163 371.446 78.7245 371.446 78.2097C371.446 77.7045 371.627 77.2731 371.989 76.9156C372.356 76.5533 372.795 76.3722 373.305 76.3722C373.796 76.3722 374.227 76.5533 374.599 76.9156C374.976 77.2731 375.164 77.7045 375.164 78.2097C375.164 78.5529 375.076 78.8651 374.899 79.1463C374.728 79.4276 374.501 79.6516 374.22 79.8184C373.944 79.9853 373.639 80.0687 373.305 80.0687Z"
        fill="white"
      />
    </g>
  </svg>
</template>

<style scoped>
.rf-patterns {
  display: block;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  user-select: none;
}

.rf-patterns__bar {
  animation: rf-patterns-bar var(--rf-bar-dur) cubic-bezier(0.42, 0, 0.58, 1)
    var(--rf-bar-delay) infinite alternate;
}

/* Only the dashes travel; the ring's tinted fill is rotation-invariant. */
.rf-patterns__ring {
  transform-box: fill-box;
  transform-origin: center;
  animation: rf-patterns-ring 10s linear infinite;
}

.rf-patterns__badge,
.rf-patterns__ripple {
  transform-box: fill-box;
  transform-origin: center;
}

.rf-patterns__badge {
  animation: rf-patterns-badge 1.8s infinite;
}

.rf-patterns__ripple {
  opacity: 0;
  animation: rf-patterns-ripple 1.8s cubic-bezier(0, 0, 0.58, 1) infinite;
}

@keyframes rf-patterns-bar {
  from {
    transform: translateY(var(--rf-bar-down));
  }
  to {
    transform: translateY(var(--rf-bar-up));
  }
}

@keyframes rf-patterns-ring {
  to {
    transform: rotate(360deg);
  }
}

@keyframes rf-patterns-badge {
  0% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  25% {
    transform: scale(1.14);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  60%,
  100% {
    transform: scale(1);
  }
}

@keyframes rf-patterns-ripple {
  0% {
    opacity: 0.35;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(1.6);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rf-patterns__bar,
  .rf-patterns__ring,
  .rf-patterns__badge,
  .rf-patterns__ripple {
    animation: none;
  }
}
</style>
