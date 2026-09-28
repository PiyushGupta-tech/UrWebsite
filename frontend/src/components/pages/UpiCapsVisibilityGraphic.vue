<script setup>
import { onMounted, ref } from "vue";

defineProps({
  alt: { type: String, default: "Real-Time Visibility" },
});

/**
 * Figma 786:3111 Live Transactions Animation — 6s infinite loop.
 * Absolute artboard 466×373; motion from get_motion_context.
 */
const ASSET = "/images/figma-upi/caps/visibility";

const CURVE_D =
  "M0 63.4041C8.44179 60.8088 16.8836 58.2129 25.3258 55.6176C33.7676 53.0223 42.2094 47.8311 50.6512 47.8311C59.0934 47.8311 67.5352 52.2805 75.977 52.2805C84.4188 52.2805 92.8606 33.3706 101.303 33.3706C109.745 33.3706 118.186 41.157 126.628 41.157C135.07 41.157 143.512 14.4606 151.954 14.4606C160.396 14.4606 168.838 22.247 177.28 22.247C185.722 22.247 194.163 5.56176 202.605 5.56176C211.047 5.56176 219.489 10.0112 227.931 12.2359C236.373 14.4606 244.815 18.91 253.257 18.91C261.699 18.91 270.14 0 278.582 0C287.024 0 295.466 3.89323 303.908 7.78647";

const AREA_D =
  "M0 63.4041C8.44179 60.8088 16.8836 58.2129 25.3258 55.6176C33.7676 53.0223 42.2094 47.8311 50.6512 47.8311C59.0934 47.8311 67.5352 52.2805 75.977 52.2805C84.4188 52.2805 92.8606 33.3706 101.303 33.3706C109.745 33.3706 118.186 41.157 126.628 41.157C135.07 41.157 143.512 14.4606 151.954 14.4606C160.396 14.4606 168.838 22.247 177.28 22.247C185.722 22.247 194.163 5.56176 202.605 5.56176C211.047 5.56176 219.489 10.0112 227.931 12.2359C236.373 14.4606 244.815 18.91 253.257 18.91C261.699 18.91 270.14 0 278.582 0C287.024 0 295.466 3.89323 303.908 7.78646V94.5499C295.466 94.5499 287.024 94.5499 278.582 94.5499C270.14 94.5499 261.699 94.5499 253.257 94.5499C244.815 94.5499 236.373 94.5499 227.931 94.5499C219.489 94.5499 211.047 94.5499 202.605 94.5499C194.163 94.5499 185.722 94.5499 177.28 94.5499C168.838 94.5499 160.396 94.5499 151.954 94.5499C143.512 94.5499 135.07 94.5499 126.628 94.5499C118.186 94.5499 109.745 94.5499 101.303 94.5499C92.8606 94.5499 84.4188 94.5499 75.977 94.5499C67.5352 94.5499 59.0934 94.5499 50.6512 94.5499C42.2094 94.5499 33.7676 94.5499 25.3258 94.5499C16.8836 94.5499 8.44179 94.5499 0 94.5499V63.4041Z";

const NAV = [
  { label: "Transactions", icon: "credit-card.svg", active: true },
  { label: "Success Rate", icon: "chart-line.svg", active: false },
  { label: "Latency", icon: "clock.svg", active: false },
  { label: "Payment Methods", icon: "wallet.svg", active: false },
  { label: "Geography", icon: "map-pin.svg", active: false },
];

const METRICS = [
  { label: "Success Rate", value: "98.7%", change: "↑ +2.1%" },
  { label: "Avg. Response Time", value: "1.2s", change: "↓ -18%" },
  { label: "Total Transactions", value: "12.4K", change: "↑ +12%" },
];

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});
</script>

<template>
  <div
    class="upi-vis"
    :class="{ 'upi-vis--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div class="upi-vis__art" aria-hidden="true">
      <!-- Glow — 786:3112 -->
      <div class="upi-vis__glow-wrap">
        <img class="upi-vis__glow" :src="`${ASSET}/glow.svg`" alt="" />
      </div>

      <!-- Scene group — 786:3113 -->
      <div class="upi-vis__scene">
        <!-- Dashboard window — 786:3114 -->
        <div class="upi-vis__window">
          <aside class="upi-vis__sidebar">
            <img
              class="upi-vis__controls"
              :src="`${ASSET}/window-controls.svg`"
              alt=""
            />
            <nav class="upi-vis__nav">
              <span
                v-for="item in NAV"
                :key="item.label"
                class="upi-vis__nav-item"
                :class="{ 'upi-vis__nav-item--active': item.active }"
              >
                <img :src="`${ASSET}/${item.icon}`" alt="" />
                {{ item.label }}
              </span>
            </nav>
          </aside>

          <div class="upi-vis__main">
            <div class="upi-vis__header">
              <p>Live Transactions</p>
              <span class="upi-vis__live">
                <img :src="`${ASSET}/status-dot.svg`" alt="" />
                Live
              </span>
            </div>

            <!-- Chart — area 786:3150 + curve 786:3151 -->
            <div class="upi-vis__chart">
              <svg
                class="upi-vis__area"
                viewBox="0 0 303.908 94.55"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <defs>
                  <linearGradient
                    id="upi-vis-area-fill"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="94.5499"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop stop-color="#2563EB" stop-opacity="0.18" />
                    <stop offset="1" stop-color="#2563EB" stop-opacity="0" />
                  </linearGradient>
                </defs>
                <path :d="AREA_D" fill="url(#upi-vis-area-fill)" fill-opacity="0.6" />
              </svg>
              <svg
                class="upi-vis__curve"
                viewBox="0 0 303.908 63.404"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  class="upi-vis__curve-path"
                  :d="CURVE_D"
                  pathLength="1"
                  stroke="#2563EB"
                  stroke-width="1.25437"
                  fill="none"
                />
              </svg>
            </div>

            <div class="upi-vis__metrics">
              <article v-for="m in METRICS" :key="m.label">
                <p class="upi-vis__metric-label">{{ m.label }}</p>
                <p class="upi-vis__metric-value">
                  {{ m.value }}<span>{{ m.change }}</span>
                </p>
              </article>
            </div>
          </div>
        </div>

        <!-- Payment notification — 786:3168 -->
        <div class="upi-vis__toast">
          <span class="upi-vis__toast-icon">
            <img :src="`${ASSET}/check.svg`" alt="" />
          </span>
          <div class="upi-vis__toast-copy">
            <p>Payment Successful</p>
            <p>UPI • 22 Apr, 10:24 AM</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upi-vis {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
}

.upi-vis__art {
  position: absolute;
  inset: 0;
}

.upi-vis__glow-wrap {
  position: absolute;
  left: calc(7.97 / 466 * 100%);
  top: 0;
  width: calc(415.898 / 466 * 100%);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.upi-vis__glow {
  width: calc(381.847 / 415.898 * 100%);
  height: auto;
  transform: rotate(6.62deg) skewX(0.27deg);
  opacity: 0.9;
}

/* Group 786:3113 — left -8, top 66.11, 482.49×258.887 */
.upi-vis__scene {
  position: absolute;
  left: calc(-8 / 466 * 100%);
  top: calc(66.11 / 373 * 100%);
  width: calc(482.49 / 466 * 100%);
  height: calc(258.887 / 373 * 100%);
}

/* Window 786:3114 — left 17.55, top 31.9, 447.389×223.993 */
.upi-vis__window {
  position: absolute;
  left: calc(17.55 / 482.49 * 100%);
  top: calc(31.9 / 258.887 * 100%);
  width: calc(447.389 / 482.49 * 100%);
  height: calc(223.993 / 258.887 * 100%);
  display: flex;
  overflow: hidden;
  border-radius: 10.649px;
  background: #ffffff;
  box-shadow: 0 5.325px 15.213px rgba(80, 117, 154, 0.09);
}

.upi-vis__sidebar {
  width: calc(118.915 / 447.389 * 100%);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 9.889px;
  padding: 10.649px 7.607px 0 9.128px;
  box-sizing: border-box;
  background: #f9fcfe;
  border-right: 0.761px solid #eaf1f7;
}

.upi-vis__controls {
  display: block;
  width: 30.97px;
  height: auto;
}

.upi-vis__nav {
  display: flex;
  flex-direction: column;
  gap: 4.455px;
}

.upi-vis__nav-item {
  display: flex;
  align-items: center;
  gap: 7.607px;
  height: 23.063px;
  padding: 0 6.085px;
  border-radius: 4.564px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 8px;
  font-weight: 500;
  color: #71809a;
  white-space: nowrap;
  box-sizing: border-box;
}

.upi-vis__nav-item img {
  display: block;
  width: 11.289px;
  height: 11.532px;
  flex-shrink: 0;
}

.upi-vis__nav-item--active {
  background: rgba(9, 116, 149, 0.1);
  border-radius: 4px;
  font-weight: 600;
  color: #097495;
}

.upi-vis__main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 20.047px;
  padding: 12.171px 10.649px 9.889px 13.692px;
  box-sizing: border-box;
}

.upi-vis__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.upi-vis__header p {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 700;
  color: #102449;
  white-space: nowrap;
}

.upi-vis__live {
  display: inline-flex;
  align-items: center;
  gap: 4.564px;
  padding: 4.564px 8.367px;
  border-radius: 999px;
  background: #ddf9ee;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 8px;
  font-weight: 600;
  color: #102449;
}

.upi-vis__live img {
  display: block;
  width: 6.021px;
  height: 6.15px;
}

.upi-vis__chart {
  position: relative;
  width: 303.908px;
  max-width: 100%;
  height: 94.55px;
  flex-shrink: 0;
}

.upi-vis__area,
.upi-vis__curve {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  overflow: visible;
}

.upi-vis__area {
  height: 94.55px;
  opacity: 0;
}

.upi-vis__curve {
  height: 63.404px;
}

.upi-vis__curve-path {
  fill: none;
  stroke-dasharray: 0 1;
  opacity: 0;
}

.upi-vis__metrics {
  display: flex;
  gap: 7.607px;
  height: 49.202px;
  width: 100%;
}

.upi-vis__metrics article {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3.803px;
  height: 100%;
  padding: 7.607px 9.128px;
  box-sizing: border-box;
  border: 0.761px solid #eaf1f7;
  border-radius: 7.607px;
  background: #ffffff;
  box-shadow: 0 5.325px 15.213px rgba(80, 117, 154, 0.09);
  overflow: hidden;
}

.upi-vis__metric-label {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 6px;
  font-weight: 600;
  color: #71809a;
  white-space: nowrap;
}

.upi-vis__metric-value {
  margin: 0;
  display: flex;
  align-items: baseline;
  gap: 5.325px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #102449;
  white-space: nowrap;
}

.upi-vis__metric-value span {
  font-size: 8px;
  color: #12bd78;
}

/* Toast — right 17.49, top -14.1 within scene */
.upi-vis__toast {
  position: absolute;
  right: calc(17.49 / 482.49 * 100%);
  top: calc(-14.1 / 258.887 * 100%);
  z-index: 4;
  display: flex;
  align-items: center;
  gap: 10.961px;
  width: 191px;
  height: 62px;
  padding: 0 15.528px;
  box-sizing: border-box;
  border-radius: 12.788px;
  background: #ffffff;
  box-shadow: 0 7.307px 21.922px rgba(23, 58, 98, 0.12);
  opacity: 0;
  overflow: hidden;
}

.upi-vis__toast-icon {
  display: grid;
  place-items: center;
  width: 28.921px;
  height: 29.542px;
  border-radius: 50%;
  background: #2d6a4f;
  flex-shrink: 0;
  opacity: 0;
  transform: scale(0.3);
}

.upi-vis__toast-icon img {
  display: block;
  width: 14.46px;
  height: 14.771px;
}

.upi-vis__toast-copy {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4.567px;
  overflow: hidden;
  opacity: 0;
  transform: translateX(-25px);
}

.upi-vis__toast-copy p {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  line-height: normal;
}

.upi-vis__toast-copy p:first-child {
  font-size: 12px;
  font-weight: 700;
  color: #102449;
  white-space: nowrap;
}

.upi-vis__toast-copy p:last-child {
  font-size: 8px;
  font-weight: 500;
  color: #71809a;
}

/* —— 6s loop, exact Figma times —— */
.upi-vis--motion .upi-vis__curve-path {
  animation:
    upi-vis-curve-opacity 6s linear infinite,
    upi-vis-curve-draw 6s linear infinite;
}

.upi-vis--motion .upi-vis__area {
  animation: upi-vis-area 6s linear infinite;
}

.upi-vis--motion .upi-vis__toast {
  animation: upi-vis-toast 6s linear infinite;
}

.upi-vis--motion .upi-vis__toast-icon {
  animation: upi-vis-toast-icon 6s linear infinite;
}

.upi-vis--motion .upi-vis__toast-copy {
  animation: upi-vis-toast-copy 6s linear infinite;
}

/* Curve opacity: [0,0,1,1,0,0] @ [0, 0.075, 0.0833, 0.8333, 0.9, 1] */
@keyframes upi-vis-curve-opacity {
  0%,
  7.5% {
    opacity: 0;
  }
  8.33%,
  83.33% {
    opacity: 1;
  }
  90%,
  100% {
    opacity: 0;
  }
}

/* Curve draw: [0 1, 0 1, 1 1, 1 1, 0 1, 0 1] @ [0, 0.083, 0.417, 0.833, 0.9, 1] */
@keyframes upi-vis-curve-draw {
  0%,
  8.3% {
    stroke-dasharray: 0 1;
  }
  41.7%,
  83.3% {
    stroke-dasharray: 1 1;
  }
  90%,
  100% {
    stroke-dasharray: 0 1;
  }
}

/* Area: [0,0,1,1,0,0] @ [0, 0.1667, 0.4667, 0.8333, 0.9, 1] */
@keyframes upi-vis-area {
  0%,
  16.67% {
    opacity: 0;
  }
  46.67%,
  83.33% {
    opacity: 1;
  }
  90%,
  100% {
    opacity: 0;
  }
}

/* Toast shell: [0,0,1,1,0,0] @ [0, 0.4917, 0.5, 0.8333, 0.9, 1] */
@keyframes upi-vis-toast {
  0%,
  49.17% {
    opacity: 0;
  }
  50%,
  83.33% {
    opacity: 1;
  }
  90%,
  100% {
    opacity: 0;
  }
}

/* Icon: [0,0,1,1] @ [0, 0.5, 0.55, 1] — holds through end */
@keyframes upi-vis-toast-icon {
  0%,
  50% {
    opacity: 0;
    transform: scale(0.3);
  }
  55%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Copy: [0,0,1,1] x [-25,-25,0,0] @ [0, 0.55, 0.6167, 1] */
@keyframes upi-vis-toast-copy {
  0%,
  55% {
    opacity: 0;
    transform: translateX(-25px);
  }
  61.67%,
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

.upi-vis:not(.upi-vis--motion) .upi-vis__area,
.upi-vis:not(.upi-vis--motion) .upi-vis__curve-path,
.upi-vis:not(.upi-vis--motion) .upi-vis__toast,
.upi-vis:not(.upi-vis--motion) .upi-vis__toast-icon,
.upi-vis:not(.upi-vis--motion) .upi-vis__toast-copy {
  opacity: 1;
  transform: none;
}
.upi-vis:not(.upi-vis--motion) .upi-vis__curve-path {
  stroke-dasharray: 1 1;
}

@media (prefers-reduced-motion: reduce) {
  .upi-vis__area,
  .upi-vis__curve-path,
  .upi-vis__toast,
  .upi-vis__toast-icon,
  .upi-vis__toast-copy {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
  .upi-vis__curve-path {
    stroke-dasharray: 1 1 !important;
  }
}
</style>
