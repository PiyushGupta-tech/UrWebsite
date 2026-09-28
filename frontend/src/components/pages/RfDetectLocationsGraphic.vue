<script setup>
import { useId } from "vue";

const ASSET = "/images/figma-risk-fraud/detect/locations";
const uid = useId();

/** Blue "locating" dots, left → right so the pulse travels toward the pin. */
const DOTS = [123.815, 134.335, 144.855];
</script>

<template>
  <svg
    class="rf-loc"
    viewBox="0 0 382 256"
    preserveAspectRatio="xMidYMid meet"
    fill="none"
    aria-hidden="true"
  >
    <defs>
      <clipPath :id="`${uid}-map`">
        <rect x="2.42773" y="41.5156" width="339.884" height="210.405" rx="22.659" />
      </clipPath>
    </defs>

    <image :href="`${ASSET}/map.svg`" width="382" height="256" />

    <g :clip-path="`url(#${uid}-map)`">
      <circle
        v-for="(cx, i) in DOTS"
        :key="cx"
        class="rf-loc__dot"
        :style="{ animationDelay: `${i * 0.18}s` }"
        :cx="cx"
        :cy="i === 2 ? 164.521 : 166.139"
        r="2.42775"
        fill="#2563EB"
      />

      <circle
        class="rf-loc__ripple"
        cx="204.93"
        cy="95.1191"
        r="37.5"
        fill="#991B1B"
        fill-opacity="0.16"
      />

      <g class="rf-loc__warning">
        <path
          d="M262.71 86.2237C263.984 84.2382 266.886 84.2382 268.16 86.2237L276.254 98.8415C277.636 100.996 276.089 103.826 273.529 103.826H257.341C254.781 103.826 253.234 100.996 254.616 98.8415L262.71 86.2237Z"
          fill="#991B1B"
        />
        <rect x="263.816" y="89.2617" width="3.23699" height="8.09249" rx="1.6185" fill="white" />
        <circle cx="265.435" cy="99.7806" r="1.6185" fill="white" />
      </g>

      <g class="rf-loc__halo">
        <circle opacity="0.7" cx="204.93" cy="95.1191" r="37.5" fill="#991B1B" fill-opacity="0.16" />
      </g>

      <g class="rf-loc__pin">
        <path
          d="M206.36 75.6387C197.141 75.6387 189.636 83.1438 189.636 92.3631C189.573 105.826 204.521 116.614 205.148 117.074C205.503 117.324 205.942 117.471 206.36 117.471C206.779 117.471 207.218 117.345 207.573 117.074C208.2 116.614 223.148 105.847 223.085 92.3631C223.085 83.1438 215.58 75.6387 206.36 75.6387ZM206.36 100.725C201.74 100.725 197.998 96.9833 197.998 92.3631C197.998 87.743 201.74 84.0009 206.36 84.0009C210.981 84.0009 214.723 87.743 214.723 92.3631C214.723 96.9833 210.981 100.725 206.36 100.725Z"
          fill="#991B1B"
        />
      </g>
    </g>

    <rect
      x="5.66473"
      y="44.7526"
      width="333.41"
      height="203.931"
      rx="19.422"
      stroke="white"
      stroke-width="6.47399"
    />

    <g class="rf-loc__tag">
      <image :href="`${ASSET}/tag.svg`" width="382" height="256" />
    </g>
  </svg>
</template>

<style scoped>
/*
 * 6s loop (1s ≈ 16.67%): the pin drops and bounces (0 → 1s), its halo grows
 * and ripples twice, the warning and "Login from New Location" tag appear at
 * 1.8s, then everything but the map fades out 5.3s → 5.65s. The blue dots
 * pulse on their own 1.2s cycle throughout.
 */
.rf-loc {
  display: block;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  user-select: none;
}

.rf-loc__dot,
.rf-loc__warning,
.rf-loc__ripple,
.rf-loc__halo,
.rf-loc__pin,
.rf-loc__tag {
  transform-box: view-box;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rf-loc__warning,
.rf-loc__ripple,
.rf-loc__halo,
.rf-loc__pin,
.rf-loc__tag {
  animation-duration: 6s;
}

.rf-loc__dot {
  transform-box: fill-box;
  transform-origin: center;
  animation-name: rf-loc-dot;
  animation-duration: 1.2s;
}

.rf-loc__pin {
  transform-origin: 206.36px 117.471px;
  animation-name: rf-loc-pin;
}

.rf-loc__halo {
  transform-origin: 204.93px 95.1191px;
  animation-name: rf-loc-halo;
}

.rf-loc__ripple {
  opacity: 0;
  transform-origin: 204.93px 95.1191px;
  animation-name: rf-loc-ripple;
}

.rf-loc__warning {
  transform-origin: 265.435px 94.5px;
  animation-name: rf-loc-warning;
}

.rf-loc__tag {
  animation-name: rf-loc-tag;
}

@keyframes rf-loc-dot {
  0%,
  60%,
  100% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  30% {
    opacity: 0.4;
    transform: translateY(-3.5px);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
}

/* Falls 36px, squashes on landing, one small bounce, then settles. */
@keyframes rf-loc-pin {
  0% {
    opacity: 0;
    transform: translateY(-36px) scale(1, 1);
    animation-timing-function: cubic-bezier(0.42, 0, 1, 1);
  }
  8% {
    opacity: 1;
    transform: translateY(0) scale(1, 1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  10% {
    transform: translateY(0) scale(1.08, 0.9);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  13% {
    transform: translateY(-7px) scale(1, 1);
    animation-timing-function: cubic-bezier(0.42, 0, 1, 1);
  }
  16%,
  88% {
    opacity: 1;
    transform: translateY(0) scale(1, 1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94% {
    opacity: 0;
    transform: translateY(0) scale(1, 1);
  }
  94.1%,
  100% {
    opacity: 0;
    transform: translateY(-36px) scale(1, 1);
  }
}

@keyframes rf-loc-halo {
  0%,
  10% {
    opacity: 0;
    transform: scale(0.3);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  18%,
  88% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

/* Two ripples out of the halo, 1.1s → 2.4s and 2.7s → 4s. */
@keyframes rf-loc-ripple {
  0%,
  18% {
    opacity: 0;
    transform: scale(1);
  }
  18.1% {
    opacity: 0.8;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  40% {
    opacity: 0;
    transform: scale(1.6);
  }
  40.1%,
  45% {
    opacity: 0;
    transform: scale(1);
  }
  45.1% {
    opacity: 0.8;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  67% {
    opacity: 0;
    transform: scale(1.6);
  }
  67.1%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rf-loc-warning {
  0%,
  30% {
    opacity: 0;
    transform: scale(0.4);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  35% {
    opacity: 1;
    transform: scale(1.15);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  39%,
  88% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rf-loc-tag {
  0%,
  32% {
    opacity: 0;
    transform: translateY(8px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  38%,
  88% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  94%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rf-loc__dot,
  .rf-loc__warning,
  .rf-loc__ripple,
  .rf-loc__halo,
  .rf-loc__pin,
  .rf-loc__tag {
    animation: none;
  }
}
</style>
