<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const props = defineProps({
  title: { type: String, default: "Faster & Cleaner Reconciliation" },
});

const LANES = [
  { id: "transactions", label: "Transactions", color: "#3B82F6" },
  { id: "settlements", label: "Settlements", color: "#10B981" },
  { id: "refunds", label: "Refunds", color: "#8B5CF6" },
];

const activeIndex = ref(0);
const reduceMotion = ref(false);
const isMobile = ref(false);
let timer = null;
let mobileMediaQuery = null;
let handleMobileQueryChange = null;

const DESKTOP_CONNECTORS = {
  viewBox: "0 0 805 138",
  // Y values = source-pill centers (36px pills + 8px gaps → 18 / 62 / 106)
  top: "M291 18H385.5C392.127 18 397.5 23.373 397.5 30V54C397.5 60.627 402.873 62 409.5 62H519.5",
  middle: { x1: 291, y1: 62, x2: 519.5, y2: 62 },
  bottom:
    "M291 106H385.733C392.36 106 397.733 100.627 397.733 94V78C397.733 71.373 403.106 62 409.733 62H520",
};

const MOBILE_CONNECTORS = {
  viewBox: "0 0 336 106",
  top: "M51 0V74C51 80.627 56.373 86 63 86H168V106",
  middle: { x1: 168, y1: 0, x2: 168, y2: 106 },
  bottom: "M285 0V74C285 80.627 279.627 86 273 86H168V106",
};

const mainCardBody = computed(() =>
  isMobile.value
    ? "All transactions, settlements, refunds & payouts - accurate, matched, complete."
    : "All transactions, settlements, refunds & payouts - accurate, matched, complete.",
);

function startCycle() {
  stopCycle();
  if (reduceMotion.value) return;
  timer = window.setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % LANES.length;
  }, 1400);
}

function stopCycle() {
  if (timer != null) {
    window.clearInterval(timer);
    timer = null;
  }
}

function laneClass(index) {
  return {
    "is-live": !reduceMotion.value,
  };
}

function layerClass(index) {
  const topIndex = (LANES.length - activeIndex.value) % LANES.length;
  const midIndex = (topIndex + 1) % LANES.length;
  return {
    "is-top": index === topIndex,
    "is-mid": index === midIndex,
    "is-back": index !== topIndex && index !== midIndex,
  };
}

onMounted(() => {
  reduceMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  mobileMediaQuery = window.matchMedia("(max-width: 1200px)");
  isMobile.value = mobileMediaQuery.matches;
  handleMobileQueryChange = (event) => {
    isMobile.value = event.matches;
  };
  mobileMediaQuery.addEventListener("change", handleMobileQueryChange);
  startCycle();
});

onUnmounted(() => {
  stopCycle();
  if (mobileMediaQuery && handleMobileQueryChange) {
    mobileMediaQuery.removeEventListener("change", handleMobileQueryChange);
  }
});
</script>

<template>
  <div
    class="reconcile-graphic"
    :class="{ 'reconcile-graphic--static': reduceMotion }"
    role="img"
    :aria-label="props.title"
  >
    <svg
      v-if="!isMobile"
      class="reconcile-graphic__connectors"
      :viewBox="DESKTOP_CONNECTORS.viewBox"
      preserveAspectRatio="xMinYMin meet"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #3B82F6"
        :d="isMobile ? MOBILE_CONNECTORS.top : DESKTOP_CONNECTORS.top"
      />
      <line
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #10B981"
        :x1="isMobile ? MOBILE_CONNECTORS.middle.x1 : DESKTOP_CONNECTORS.middle.x1"
        :y1="isMobile ? MOBILE_CONNECTORS.middle.y1 : DESKTOP_CONNECTORS.middle.y1"
        :x2="isMobile ? MOBILE_CONNECTORS.middle.x2 : DESKTOP_CONNECTORS.middle.x2"
        :y2="isMobile ? MOBILE_CONNECTORS.middle.y2 : DESKTOP_CONNECTORS.middle.y2"
      />
      <path
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #8B5CF6"
        :d="isMobile ? MOBILE_CONNECTORS.bottom : DESKTOP_CONNECTORS.bottom"
      />
    </svg>

    <svg
      v-else
      class="reconcile-graphic__connectors reconcile-graphic__connectors--mobile"
      :viewBox="MOBILE_CONNECTORS.viewBox"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #3B82F6"
        :d="MOBILE_CONNECTORS.top"
      />
      <line
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #10B981"
        :x1="MOBILE_CONNECTORS.middle.x1"
        :y1="MOBILE_CONNECTORS.middle.y1"
        :x2="MOBILE_CONNECTORS.middle.x2"
        :y2="MOBILE_CONNECTORS.middle.y2"
      />
      <path
        class="reconcile-graphic__connector"
        :class="{ 'is-live': !reduceMotion }"
        style="--connector-color: #8B5CF6"
        :d="MOBILE_CONNECTORS.bottom"
      />
    </svg>

    <div class="reconcile-graphic__sources" :class="{ 'reconcile-graphic__sources--mobile': isMobile }">
      <div
        v-for="(lane, index) in LANES"
        :key="lane.id"
        class="reconcile-graphic__source-pill"
        :class="laneClass(index)"
      >
        <span class="reconcile-graphic__source-label">{{ lane.label }}</span>
        <div class="reconcile-graphic__dot-track" aria-hidden="true">
          <span
            v-for="dotIndex in 5"
            :key="`${lane.id}-${dotIndex}`"
            class="reconcile-graphic__dot"
            :style="{
              '--dot-color': lane.color,
              '--dot-opacity': `${1 - (dotIndex - 1) * 0.2}`,
              '--dot-delay': `${(dotIndex - 1) * 90}ms`,
            }"
          />
        </div>
        <span
          class="reconcile-graphic__anchor"
          :style="{ '--dot-color': lane.color }"
          aria-hidden="true"
        />
      </div>
    </div>

    <div
      class="reconcile-graphic__result"
      :class="{
        'is-live': !reduceMotion,
        'reconcile-graphic__result--mobile': isMobile,
      }"
    >
      <div class="reconcile-graphic__stack" :class="{ 'reconcile-graphic__stack--mobile': isMobile }" aria-hidden="true">
        <div class="reconcile-graphic__stack-cap" />
        <div
          v-for="(lane, index) in LANES"
          :key="`${lane.id}-layer`"
          class="reconcile-graphic__stack-layer"
          :class="layerClass(index)"
          :style="{ '--stack-rotation': `${index === 0 ? -4 : index === 1 ? 0 : 4}deg` }"
        />
      </div>

      <div class="reconcile-graphic__main-card" :class="{ 'reconcile-graphic__main-card--mobile': isMobile }">
        <div class="reconcile-graphic__badge" :class="{ 'is-active': !reduceMotion }">
          <span class="reconcile-graphic__badge-core">
            <svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M9.75 3.5L5.2 8.05L3.125 5.975" stroke="white" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
        </div>

        <div class="reconcile-graphic__copy">
          <h3>Reconciled in One Place</h3>
          <p>{{ mainCardBody }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reconcile-graphic {
  position: relative;
  width: 100%;
  max-width: 805px;
  aspect-ratio: 805 / 138;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.reconcile-graphic__connectors {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.reconcile-graphic__connector {
  fill: none;
  stroke: #d5d7da;
  stroke-width: 1.5;
  stroke-dasharray: 5 5;
  stroke-linecap: round;
  transition: stroke 0.25s ease;
}

.reconcile-graphic__connector.is-live {
  stroke: var(--connector-color);
  stroke-opacity: 0.72;
  stroke-width: 2;
  animation: reconcile-dash-move 0.75s linear infinite;
}

.reconcile-graphic__sources {
  position: absolute;
  left: 0;
  top: 0;
  width: 29.81%;
  height: 100%;
  display: grid;
  /* 36 + 8 + 36 + 8 + 36 = 124 → ~14px design padding under Refunds */
  grid-template-rows: repeat(3, calc(36 / 138 * 100%));
  gap: calc(8 / 138 * 100%);
  align-content: start;
  box-sizing: border-box;
}

.reconcile-graphic__source-pill {
  position: relative;
  display: flex;
  align-items: center;
  height: 100%;
  min-height: 0;
  padding: 0 clamp(8px, 1.7%, 14px);
  border: 1px solid #d5d7da;
  border-radius: 4px;
  background: #ffffff;
  box-sizing: border-box;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.reconcile-graphic__source-label {
  color: #535862;
  font-size: clamp(10px, 1.5vw, 12px);
  font-weight: 700;
  line-height: 1;
}

.reconcile-graphic__dot-track {
  position: absolute;
  left: 59%;
  top: 50%;
  display: flex;
  gap: clamp(2px, 0.5vw, 4px);
  transform: translateY(-50%);
}

.reconcile-graphic__dot {
  width: clamp(4px, 0.75vw, 6px);
  height: clamp(4px, 0.75vw, 6px);
  border-radius: 50%;
  background: var(--dot-color);
  opacity: var(--dot-opacity);
}

.reconcile-graphic__source-pill.is-live .reconcile-graphic__dot {
  animation: reconcile-dot-strobe 0.72s ease-in-out infinite;
  animation-delay: var(--dot-delay);
}

.reconcile-graphic__anchor {
  position: absolute;
  right: clamp(8px, 1.5%, 12px);
  top: 50%;
  width: clamp(6px, 1vw, 8px);
  height: clamp(6px, 1vw, 8px);
  border-radius: 50%;
  color: var(--dot-color);
  background: currentColor;
  transform: translateY(-50%);
  box-shadow: 0 0 0 0 transparent;
}

.reconcile-graphic__source-pill.is-live .reconcile-graphic__anchor {
  animation: reconcile-anchor-pulse 0.72s ease-out infinite;
}

.reconcile-graphic__result {
  position: absolute;
  left: 64.97%;
  top: 0;
  width: 25.71%;
  height: 100%;
  pointer-events: none;
}

.reconcile-graphic__result.is-live {
  animation: reconcile-main-card-float 1.4s ease-in-out infinite;
}

.reconcile-graphic__stack {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.reconcile-graphic__stack-cap {
  position: absolute;
  left: 3.38%;
  top: 0;
  width: 92.75%;
  height: 11.6%;
  border: 1px solid #d5d7da;
  border-bottom: none;
  border-radius: 16px 16px 0 0;
  background: #ffffff;
  opacity: 0.8;
}

.reconcile-graphic__stack-layer {
  position: absolute;
  left: 0;
  top: 5.8%;
  width: 100%;
  height: 94.2%;
  border: 1px solid #d5d7da;
  border-radius: 24px;
  background: #ffffff;
  transform-origin: center center;
  opacity: 0.08;
  transition:
    transform 0.6s cubic-bezier(0.22, 0.8, 0.3, 1),
    opacity 0.6s ease,
    border-color 0.6s ease;
}

/* Desktop: tight stack so layers don’t read as ghost borders */
.reconcile-graphic__stack-layer.is-top {
  transform: translate(0, -3px) rotate(0deg);
  opacity: 0.18;
  border-color: rgba(9, 116, 149, 0.18);
}

.reconcile-graphic__stack-layer.is-mid {
  transform: translate(0, -1.5px) rotate(0deg);
  opacity: 0.1;
}

.reconcile-graphic__stack-layer.is-back {
  transform: translate(0, 0) rotate(0deg);
  opacity: 0.06;
}

.reconcile-graphic__main-card {
  position: absolute;
  left: 0;
  top: 5.8%;
  width: 100%;
  height: 93.5%;
  border: 1px solid #d5d7da;
  border-radius: 24px;
  background: #ffffff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 8px 10px 10px;
  overflow: hidden;
}

.reconcile-graphic__badge {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: #ecfdf5;
  margin-bottom: 10px;
}

.reconcile-graphic__badge.is-active {
  animation: reconcile-badge-glow 1.8s ease-in-out infinite;
}

.reconcile-graphic__badge-core {
  display: grid;
  place-items: center;
  width: 12.3px;
  height: 12.3px;
  border-radius: 999px;
  background: #10b981;
}

.reconcile-graphic__badge-core svg {
  width: 12px;
  height: 12px;
}

.reconcile-graphic__copy {
  text-align: center;
}

.reconcile-graphic__copy h3 {
  margin: 0 0 4px;
  color: #535862;
  font-size: 12px;
  font-weight: 800;
  line-height: 18px;
}

.reconcile-graphic__copy p {
  margin: 0;
  color: #535862;
  font-size: 10px;
  font-weight: 400;
  line-height: 13px;
}

@keyframes reconcile-dot-strobe {
  0%,
  100% {
    transform: scale(1);
    filter: brightness(1);
  }

  35% {
    transform: scale(1.35);
    filter: brightness(1.18);
  }
}

@keyframes reconcile-anchor-pulse {
  0%,
  100% {
    transform: translateY(-50%) scale(1);
    box-shadow: 0 0 0 0 transparent;
  }

  55% {
    transform: translateY(-50%) scale(1.15);
    box-shadow: 0 0 0 8px rgba(9, 116, 149, 0.16);
  }
}

@keyframes reconcile-anchor-pulse-mobile {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 transparent;
  }

  55% {
    transform: scale(1.15);
    box-shadow: 0 0 0 8px rgba(9, 116, 149, 0.16);
  }
}

@keyframes reconcile-dash-move {
  to {
    stroke-dashoffset: -20;
  }
}

@keyframes reconcile-badge-glow {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.08);
  }

  50% {
    box-shadow: 0 0 0 9px rgba(16, 185, 129, 0.12);
  }
}

@keyframes reconcile-main-card-float {
  0%,
  100% {
    transform: translate(0, 0);
  }

  45% {
    transform: translate(-2px, -2px);
  }

  70% {
    transform: translate(1px, 0);
  }
}

@keyframes reconcile-main-card-float-mobile {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-2px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .reconcile-graphic__connector.is-live,
  .reconcile-graphic__source-pill.is-live .reconcile-graphic__dot,
  .reconcile-graphic__source-pill.is-live .reconcile-graphic__anchor,
  .reconcile-graphic__result.is-live,
  .reconcile-graphic__badge.is-active {
    animation: none;
  }
}

@media (max-width: 1200px) {
  .reconcile-graphic {
    width: 336px;
    max-width: 100%;
    /* sources 70 + connectors 106 + main card 138 = 314 */
    aspect-ratio: 336 / 314;
    height: auto;
    display: block;
  }

  .reconcile-graphic__connectors--mobile {
    position: absolute;
    top: 70px;
    left: 0;
    width: 100%;
    height: 106px;
  }

  .reconcile-graphic__connectors--mobile .reconcile-graphic__connector {
    stroke-width: 2;
    stroke-dasharray: 4 5;
    stroke: #d5d7da;
    stroke-opacity: 1;
  }

  .reconcile-graphic__connectors--mobile .reconcile-graphic__connector.is-live {
    stroke: var(--connector-color);
    stroke-opacity: 0.72;
  }

  .reconcile-graphic__sources--mobile {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 15px;
    box-sizing: border-box;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__source-pill {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    width: 100%;
    height: 70px;
    padding: 8px 16px;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__source-label {
    width: 100%;
    font-size: 10px;
    font-weight: 700;
    line-height: normal;
    text-align: center;
    color: #535862;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__dot-track {
    position: static;
    transform: none;
    margin: 0;
    width: 46px;
    height: 6px;
    gap: 4px;
    justify-content: center;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__dot {
    width: 6px;
    height: 6px;
    flex-shrink: 0;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__anchor {
    position: static;
    transform: none;
    margin: 0;
    width: 8px;
    height: 8px;
  }

  .reconcile-graphic__sources--mobile .reconcile-graphic__source-pill.is-live .reconcile-graphic__anchor {
    animation-name: reconcile-anchor-pulse-mobile;
  }

  .reconcile-graphic__result--mobile {
    left: 50%;
    margin-left: -103.5px;
    top: 176px;
    width: 207px;
    height: 138px;
  }

  .reconcile-graphic__result--mobile.is-live {
    animation: reconcile-main-card-float-mobile 1.4s ease-in-out infinite;
  }

  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-cap {
    left: 7px;
    top: 0;
    width: 192px;
    height: 16px;
    border-radius: 16px 16px 0 0;
  }

  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-layer,
  .reconcile-graphic__main-card--mobile {
    border-radius: 18px;
  }

  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-layer {
    top: 8px;
    height: 130px;
  }

  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-layer.is-top {
    transform: translate(0, -2px) rotate(0deg);
    opacity: 0.16;
  }

  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-layer.is-mid,
  .reconcile-graphic__stack--mobile .reconcile-graphic__stack-layer.is-back {
    transform: translate(0, 0) rotate(0deg);
    opacity: 0.08;
  }

  .reconcile-graphic__main-card--mobile {
    padding: 12px 14px;
    border-radius: 24px;
  }

  .reconcile-graphic__badge {
    width: 32px;
    height: 32px;
    margin-bottom: 8px;
  }

  .reconcile-graphic__badge-core,
  .reconcile-graphic__badge-core svg {
    width: 12px;
    height: 12px;
  }

  .reconcile-graphic__copy h3 {
    font-size: 12px;
    line-height: 16px;
    margin-bottom: 6px;
  }

  .reconcile-graphic__copy p {
    font-size: 10px;
    line-height: 14px;
  }
}
</style>
