<script setup>
defineProps({
  alt: {
    type: String,
    default: "Side-by-side transaction and settlement records with a reconciled success state",
  },
});

/** Full 570×373 canvases cut from "Group 1171275349.svg" (Figma 652:8969). */
const ASSET = "/images/figma-reconciliation/showcase-reconciled";
</script>

<template>
  <svg
    class="rc-reconciled"
    viewBox="0 0 570 373"
    width="570"
    height="373"
    fill="none"
    role="img"
    :aria-label="alt"
  >
    <image :href="`${ASSET}/background.svg`" width="570" height="373" />

    <g class="rc-reconciled__notification">
      <image :href="`${ASSET}/notification.svg`" width="570" height="373" />
    </g>

    <image :href="`${ASSET}/details.svg`" width="570" height="373" />
    <g class="rc-reconciled__settlement">
      <image :href="`${ASSET}/settlement.svg`" width="570" height="373" />
    </g>

    <g class="rc-reconciled__indicator">
      <rect
        x="292.088"
        y="297.045"
        width="39.666"
        height="39.666"
        rx="19.833"
        fill="#991B1B"
        fill-opacity="0.39"
      />
      <rect
        x="292.639"
        y="297.596"
        width="38.5642"
        height="38.5642"
        rx="19.2821"
        stroke="#991B1B"
        stroke-opacity="0.11"
        stroke-width="1.10183"
      />
      <path
        d="M312.675 312.528H315.281L311.217 323.163H308.604L312.675 312.528ZM307.055 316.753V314.253H316.781V316.753H307.055ZM307.055 321.43V318.93H316.781V321.43H307.055Z"
        fill="#991B1B"
      />
      <g class="rc-reconciled__resolved">
        <rect x="292.088" y="297.045" width="39.666" height="39.666" rx="19.833" fill="#059669" />
        <path
          class="rc-reconciled__check"
          d="M305.6 317.1L309.9 321.3L318.3 312.7"
          stroke="white"
          stroke-width="2.6"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </g>
    </g>
  </svg>
</template>

<style scoped>
/*
 * 6s loop after Figma 848:2574 (1s ≈ 16.67%). Both record cards stay put: the
 * mismatch indicator wobbles 0.8s → 2.1s, Settlement Record pulses at 2.2s,
 * the indicator turns green with a check at 2.8s, "Transaction Reconciled"
 * drops in at 3.5s, then the notification fades out while the indicator
 * eases back to the red mismatch state (5.3s → 5.8s) for the next loop.
 */
/* Settlement's 1.03 pulse reaches ~3px past the canvas edge. */
.rc-reconciled {
  display: block;
  overflow: visible;
  pointer-events: none;
  user-select: none;
}

.rc-reconciled__notification,
.rc-reconciled__settlement,
.rc-reconciled__indicator,
.rc-reconciled__resolved,
.rc-reconciled__check {
  transform-box: view-box;
  animation-duration: 6s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rc-reconciled__notification {
  animation-name: rc-reconciled-notification;
}

.rc-reconciled__settlement {
  transform-origin: 444.058px 282.156px;
  animation-name: rc-reconciled-settlement;
}

.rc-reconciled__indicator,
.rc-reconciled__check {
  transform-origin: 311.921px 316.878px;
}

.rc-reconciled__indicator {
  animation-name: rc-reconciled-indicator;
}

.rc-reconciled__resolved {
  opacity: 0;
  animation-name: rc-reconciled-resolved;
}

.rc-reconciled__check {
  animation-name: rc-reconciled-check;
}

@keyframes rc-reconciled-settlement {
  0%,
  36.67% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  40% {
    transform: scale(1.03);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  43.33%,
  100% {
    transform: scale(1);
  }
}

@keyframes rc-reconciled-indicator {
  0%,
  13.33% {
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  20% {
    transform: scale(1.12);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  25% {
    transform: scale(0.95);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  30% {
    transform: scale(1.08);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  35%,
  100% {
    transform: scale(1);
  }
}

/* Red → green (#991B1B → #059669) as a crossfade over the mismatch badge. */
@keyframes rc-reconciled-resolved {
  0%,
  46.67% {
    opacity: 0;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  55%,
  88.33% {
    opacity: 1;
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  96.67%,
  100% {
    opacity: 0;
  }
}

@keyframes rc-reconciled-check {
  0%,
  50% {
    opacity: 0;
    transform: scale(0.5);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  55%,
  88.33% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes rc-reconciled-notification {
  0%,
  58.33% {
    opacity: 0;
    transform: translateY(-20px);
    animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
  }
  66.67% {
    opacity: 1;
    transform: translateY(0);
  }
  88.33% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
  }
  96.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .rc-reconciled__notification,
  .rc-reconciled__settlement,
  .rc-reconciled__indicator,
  .rc-reconciled__resolved,
  .rc-reconciled__check {
    animation: none;
  }
}
</style>
