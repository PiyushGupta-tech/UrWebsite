<script setup>
import { onMounted, ref } from "vue";

defineProps({
  alt: { type: String, default: "Intelligent Routing" },
});

/**
 * Figma 800:2746 Payment Gateway Animation — 6s infinite loop.
 * Frame1 800:2747 → Frame2 800:2789 → Frame3 800:2840
 *
 * Scene is a fixed 447×380 artboard, centered + scaled to fit the
 * visual slot so Figma’s left:-20 gateways aren’t clipped.
 */
const ASSET = "/images/figma-upi/caps/routing";

const reduceMotion = ref(false);

function pos(left, top, width, height) {
  const s = {
    left: `${left}px`,
    top: `${top}px`,
  };
  if (width != null) s.width = `${width}px`;
  if (height != null) s.height = `${height}px`;
  return s;
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});
</script>

<template>
  <div
    class="upi-route"
    :class="{ 'upi-route--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div class="upi-route__art" aria-hidden="true">
      <div class="upi-route__scene">
        <!-- Glow -->
        <div class="upi-route__glow-wrap" :style="pos(-2, 6, 381.832, 342.463)">
          <img class="upi-route__glow" :src="`${ASSET}/glow.svg`" alt="" />
        </div>

        <!-- Payment request — always visible (no blank-loop gap) -->
        <div class="upi-route__request" :style="pos(147, -3, 151, 85)">
          <div class="upi-route__request-title">
            <span class="upi-route__user">
              <img :src="`${ASSET}/user.svg`" alt="" width="13" height="13" />
            </span>
            <span>Payment Request</span>
          </div>
          <p class="upi-route__amount">₹1,299</p>
          <span class="upi-route__line upi-route__line--lg" />
          <span class="upi-route__line upi-route__line--sm" />
        </div>

        <!-- Frame1 top wires -->
        <div
          class="upi-route__wire upi-route__wire--top-c"
          :style="pos(208.97, 84.66, 0, 80.56)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--top-c">
            <img :src="`${ASSET}/arrow-top-center.png`" alt="" />
          </div>
        </div>
        <div
          class="upi-route__wire upi-route__wire--top-l"
          :style="pos(70, 86, 120, 79)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--top-l">
            <img :src="`${ASSET}/arrow-top-left.png`" alt="" />
          </div>
        </div>
        <div
          class="upi-route__wire upi-route__wire--top-r"
          :style="pos(225, 85, 119, 79)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--top-r">
            <img :src="`${ASSET}/arrow-top-right.png`" alt="" />
          </div>
        </div>

        <!-- Idle gateways — Frame1 -->
        <div class="upi-route__gates upi-route__gates--idle" :style="pos(-20, 168)">
          <div class="upi-route__gate upi-route__gate--idle upi-route__gate--wide">
            <span class="upi-route__gate-icon upi-route__gate-icon--muted">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <p class="upi-route__gate-name">Gateway A</p>
          </div>
          <div class="upi-route__gate upi-route__gate--idle upi-route__gate--wide">
            <span class="upi-route__gate-icon upi-route__gate-icon--muted">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <p class="upi-route__gate-name">Gateway B</p>
          </div>
          <div class="upi-route__gate upi-route__gate--idle upi-route__gate--narrow">
            <span class="upi-route__gate-icon upi-route__gate-icon--muted">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <p class="upi-route__gate-name upi-route__gate-name--sm">Gateway C</p>
          </div>
        </div>

        <!-- Result gateways — Frame2 + Frame3 -->
        <div class="upi-route__gates upi-route__gates--result" :style="pos(-20, 168)">
          <div class="upi-route__gate upi-route__gate--fail upi-route__gate--wide">
            <span class="upi-route__gate-icon">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <div class="upi-route__gate-copy">
              <p class="upi-route__gate-name">Gateway A</p>
              <p class="upi-route__gate-status">Unavailable</p>
            </div>
            <img
              class="upi-route__mark"
              :src="`${ASSET}/danger.svg`"
              alt=""
              width="16"
              height="16"
            />
          </div>
          <div class="upi-route__gate upi-route__gate--ok upi-route__gate--wide">
            <span class="upi-route__gate-icon">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <div class="upi-route__gate-copy">
              <p class="upi-route__gate-name">Gateway B</p>
              <p class="upi-route__gate-status upi-route__gate-status--ok">
                Optimal Route
              </p>
            </div>
            <span class="upi-route__check">✓</span>
          </div>
          <div class="upi-route__gate upi-route__gate--fail upi-route__gate--narrow">
            <span class="upi-route__gate-icon">
              <img :src="`${ASSET}/finance.svg`" alt="" width="12" height="12" />
            </span>
            <div class="upi-route__gate-copy">
              <p class="upi-route__gate-name upi-route__gate-name--sm">Gateway C</p>
              <p class="upi-route__gate-status">Unavailable</p>
            </div>
            <img
              class="upi-route__mark"
              :src="`${ASSET}/danger.svg`"
              alt=""
              width="16"
              height="16"
            />
          </div>
        </div>

        <!-- Frame3 bottom wires (optimal path + side trails) -->
        <div
          class="upi-route__wire upi-route__wire--bot-l"
          :style="pos(63, 200, 146, 65)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--bot-l">
            <img :src="`${ASSET}/arrow-bot-left.png`" alt="" />
          </div>
        </div>
        <div
          class="upi-route__wire upi-route__wire--bot-r"
          :style="pos(208, 200, 146, 66)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--bot-r">
            <img :src="`${ASSET}/arrow-bot-right.png`" alt="" />
          </div>
        </div>
        <div
          class="upi-route__wire upi-route__wire--bot-c"
          :style="pos(209, 203, 0, 71)"
        >
          <div class="upi-route__wire-inner upi-route__wire-inner--bot-c">
            <img :src="`${ASSET}/arrow-bot-center.png`" alt="" />
          </div>
        </div>

        <!-- Transaction successful -->
        <div class="upi-route__success" :style="pos(169, 280, 89, 77)">
          <span class="upi-route__success-badge">
            <img
              :src="`${ASSET}/success-badge.svg`"
              alt=""
              width="28"
              height="28"
            />
            <span class="upi-route__success-check">✓</span>
          </span>
          <p>Transaction<br />Successful</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upi-route {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
}

.upi-route__art {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}

/* Fixed Figma artboard, scaled to fit with side margin so gates don’t clip */
.upi-route__scene {
  position: relative;
  width: 447px;
  height: 380px;
  flex-shrink: 0;
  transform: scale(0.9);
  transform-origin: center center;
}

.upi-route__glow-wrap {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  opacity: 0.95;
  z-index: 0;
}

.upi-route__glow {
  width: 350.57px;
  height: auto;
  transform: rotate(6.62deg) skewX(0.27deg);
  display: block;
}

.upi-route__request {
  position: absolute;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  box-sizing: border-box;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 7.706px 21.192px rgba(59, 125, 181, 0.1);
}

.upi-route__request-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
  white-space: nowrap;
}

.upi-route__user {
  display: grid;
  place-items: center;
  width: 19px;
  height: 19px;
  border-radius: 5px;
  background: #e8f3ff;
  flex-shrink: 0;
}

.upi-route__user img {
  display: block;
  width: 13px;
  height: 13px;
}

.upi-route__amount {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #252b37;
}

.upi-route__line {
  display: block;
  height: 4px;
  border-radius: 2px;
}
.upi-route__line--lg {
  width: 65px;
  background: #dfeaf5;
}
.upi-route__line--sm {
  width: 41px;
  background: #e7eff7;
}

.upi-route__wire {
  position: absolute;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  opacity: 0;
}

.upi-route__wire-inner {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 0;
}

.upi-route__wire-inner img {
  display: block;
  max-width: none;
}

.upi-route__wire-inner--top-c {
  transform: rotate(90deg);
}
.upi-route__wire-inner--top-c img {
  width: 80.56px;
  height: 10.507px;
}

.upi-route__wire-inner--top-l {
  transform: rotate(90deg);
}
.upi-route__wire-inner--top-l img {
  width: 79px;
  height: 121px;
}

.upi-route__wire-inner--top-r {
  transform: rotate(90deg) scaleY(-1);
}
.upi-route__wire-inner--top-r img {
  width: 79px;
  height: 120px;
}

.upi-route__wire-inner--bot-l {
  transform: rotate(90deg) scaleY(-1);
}
.upi-route__wire-inner--bot-l img {
  width: 65px;
  height: 147px;
}

.upi-route__wire-inner--bot-r {
  transform: rotate(90deg);
}
.upi-route__wire-inner--bot-r img {
  width: 66px;
  height: 147px;
}

.upi-route__wire-inner--bot-c {
  transform: rotate(90deg);
}
.upi-route__wire-inner--bot-c img {
  width: 71px;
  height: 10.507px;
}

.upi-route__gates {
  position: absolute;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: 44px;
}

.upi-route__gates--idle {
  opacity: 1;
}
.upi-route__gates--result {
  opacity: 0;
}

.upi-route__gate {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 44px;
  padding: 8px 12px;
  box-sizing: border-box;
  border-radius: 21px;
  box-shadow: 0 7.636px 21px rgba(59, 125, 181, 0.1);
}

.upi-route__gate--wide {
  width: 146px;
  flex-shrink: 0;
}
.upi-route__gate--narrow {
  width: 135px;
  flex-shrink: 0;
}

.upi-route__gate--idle {
  border: 1px solid #e9eaeb;
  background: #ffffff;
}
.upi-route__gate--fail {
  background: #ffeeee;
  border: 0;
}
.upi-route__gate--ok {
  background: #eefff7;
  border: 0;
}

.upi-route__gate-icon {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 14px;
  background: #ffffff;
  flex-shrink: 0;
}
.upi-route__gate-icon--muted {
  background: #e9eaeb;
}
.upi-route__gate-icon img {
  display: block;
  width: 12px;
  height: 12px;
}

.upi-route__gate-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1px;
  min-width: 0;
  flex: 1;
}

.upi-route__gate-name {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.15;
  color: #10234b;
  white-space: nowrap;
}
.upi-route__gate-name--sm {
  font-size: 10px;
}

.upi-route__gate-status {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 8px;
  font-weight: 500;
  line-height: 1.15;
  color: #8290ac;
  white-space: nowrap;
}
.upi-route__gate-status--ok {
  color: #2d6a4f;
}

.upi-route__mark {
  display: block;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.upi-route__check {
  display: grid;
  place-items: center;
  width: 19px;
  height: 19px;
  border-radius: 50%;
  background: #2d6a4f;
  color: #ffffff;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
  line-height: 1;
}

.upi-route__success {
  position: absolute;
  z-index: 4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 12px;
  box-sizing: border-box;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 7.706px 21.192px rgba(59, 125, 181, 0.1);
  opacity: 0;
  transform: scale(0.5);
  transform-origin: center center;
}

.upi-route__success-badge {
  position: relative;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}
.upi-route__success-badge img {
  display: block;
  width: 100%;
  height: 100%;
}
.upi-route__success-check {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.upi-route__success p {
  margin: 0;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 500;
  line-height: 1.25;
  text-align: center;
  color: #10234b;
}

/* ——— 6s motion ——— */
.upi-route--motion .upi-route__glow-wrap {
  animation: upi-route-glow 6s linear infinite;
}
.upi-route--motion .upi-route__wire--top-c {
  animation: upi-route-top-c 6s linear infinite;
}
.upi-route--motion .upi-route__wire--top-l {
  animation: upi-route-top-l 6s linear infinite;
}
.upi-route--motion .upi-route__wire--top-r {
  animation: upi-route-top-r 6s linear infinite;
}
.upi-route--motion .upi-route__gates--idle {
  animation: upi-route-frame1 6s linear infinite;
}
.upi-route--motion .upi-route__gates--result {
  animation: upi-route-result-gates 6s linear infinite;
}
.upi-route--motion .upi-route__wire--bot-l {
  animation: upi-route-bot-l 6s linear infinite;
}
.upi-route--motion .upi-route__wire--bot-r {
  animation: upi-route-bot-r 6s linear infinite;
}
.upi-route--motion .upi-route__wire--bot-c {
  animation: upi-route-bot-c 6s linear infinite;
}
.upi-route--motion .upi-route__success {
  animation: upi-route-success 6s linear infinite;
}

/*
 * Idle Frame1: 0–29.17%, out by 30%.
 * Return at 91.67% so the loop doesn’t flash blank white.
 */
@keyframes upi-route-frame1 {
  0%,
  29.17% {
    opacity: 1;
  }
  30%,
  91.67% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes upi-route-result-gates {
  0%,
  29.17% {
    opacity: 0;
  }
  30%,
  83.33% {
    opacity: 1;
  }
  91.67%,
  100% {
    opacity: 0;
  }
}

@keyframes upi-route-glow {
  0%,
  29.17% {
    opacity: 0.95;
  }
  30%,
  91.67% {
    opacity: 0;
  }
  100% {
    opacity: 0.95;
  }
}

/* Top wires stay visible through the success phase (with bottom wires). */
@keyframes upi-route-top-c {
  0%,
  5% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  13.33%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-top-l {
  0%,
  8.33% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  16.67%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-top-r {
  0%,
  11.67% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  20%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-bot-l {
  0%,
  43.33% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  51.67%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-bot-r {
  0%,
  45% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  53.33%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-bot-c {
  0%,
  46.67% {
    opacity: 0;
    transform: translateY(-15px);
    animation-timing-function: ease-out;
  }
  55%,
  83.33% {
    opacity: 1;
    transform: translateY(0);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes upi-route-success {
  0%,
  55% {
    opacity: 0;
    transform: scale(0.5);
    animation-timing-function: ease-out;
  }
  61.67%,
  83.33% {
    opacity: 1;
    transform: scale(1);
  }
  91.67%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .upi-route__gates--idle,
  .upi-route__glow-wrap,
  .upi-route__wire--top-c,
  .upi-route__wire--top-l,
  .upi-route__wire--top-r {
    opacity: 0 !important;
  }
  .upi-route__gates--result,
  .upi-route__wire--bot-c,
  .upi-route__wire--bot-l,
  .upi-route__wire--bot-r {
    opacity: 1 !important;
    transform: none !important;
  }
  .upi-route__success {
    opacity: 1 !important;
    transform: scale(1) !important;
  }
}
</style>
