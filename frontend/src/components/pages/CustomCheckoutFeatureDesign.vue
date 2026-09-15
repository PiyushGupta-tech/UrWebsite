<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

/** Figma 283:8983 — Design Your Experience graphic */
const COLORS = [
  { id: "blue", hex: "#1A73E8", label: "#1A73E8" },
  { id: "teal", hex: "#097495", label: "#097495" },
  { id: "indigo", hex: "#0A54E9", label: "#0A54E9" },
  { id: "purple", hex: "#8854D0", label: "#8854D0" },
  { id: "pink", hex: "#FF4DFF", label: "#FF4DFF" },
  { id: "orange", hex: "#FF9F43", label: "#FF9F43" },
];

const activeIndex = ref(0);
const paused = ref(false);
let timer = null;
let reduceMotion = false;

const accent = computed(() => COLORS[activeIndex.value].hex);
const accentLabel = computed(() => COLORS[activeIndex.value].label);

function select(index) {
  activeIndex.value = index;
  restart();
}

function next() {
  activeIndex.value = (activeIndex.value + 1) % COLORS.length;
}

function restart() {
  stop();
  if (reduceMotion || paused.value) return;
  timer = window.setInterval(next, 2400);
}

function stop() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
}

onMounted(() => {
  reduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  restart();
});

onBeforeUnmount(stop);
</script>

<template>
  <div
    class="cfd"
    :style="{ '--cfd-accent': accent }"
    @mouseenter="paused = true; stop()"
    @mouseleave="paused = false; restart()"
  >
    <div class="cfd__screen">
      <div class="cfd__grid" />
      <div class="cfd__shield" aria-hidden="true">
        <img
          src="/images/figma-custom-checkout/features/design-shield.svg"
          alt=""
          width="126"
          height="126"
          decoding="async"
        />
      </div>
      <!-- Dotted ripples — Figma groups near icon (top-right + bottom-left) -->
      <div class="cfd__ripple cfd__ripple--a" aria-hidden="true">
        <span class="cfd__ripple-core" />
        <span class="cfd__ripple-ring" />
        <span class="cfd__ripple-ring" />
      </div>
      <div class="cfd__ripple cfd__ripple--b" aria-hidden="true">
        <span class="cfd__ripple-core" />
        <span class="cfd__ripple-ring" />
        <span class="cfd__ripple-ring" />
      </div>
    </div>

    <article class="cfd__settings">
      <p class="cfd__settings-title">Brand Settings</p>

      <label class="cfd__field">
        <span>Logo</span>
        <div class="cfd__input cfd__input--logo">ACME</div>
      </label>

      <div class="cfd__field">
        <span>Primary Color</span>
        <div class="cfd__swatches" role="listbox" aria-label="Primary color">
          <button
            v-for="(color, index) in COLORS"
            :key="color.id"
            type="button"
            class="cfd__swatch"
            :class="{ 'cfd__swatch--active': index === activeIndex }"
            :style="{ '--swatch': color.hex }"
            :aria-selected="index === activeIndex"
            :aria-label="`Select ${color.id}`"
            role="option"
            @click="select(index)"
          />
        </div>
        <div class="cfd__input cfd__input--color">
          <span class="cfd__dot" />
          <span>{{ accentLabel }}</span>
        </div>
      </div>

      <label class="cfd__field">
        <span>Font</span>
        <div class="cfd__input cfd__input--font">
          <span>Inter</span>
          <span class="cfd__chevron" />
        </div>
      </label>

      <div class="cfd__field">
        <span>Layout</span>
        <div class="cfd__layouts">
          <div class="cfd__layout cfd__layout--active">
            <span class="cfd__layout-bar" />
            <span class="cfd__layout-line" />
            <span class="cfd__layout-line cfd__layout-line--sm" />
          </div>
          <div class="cfd__layout">
            <span class="cfd__layout-col" />
            <span class="cfd__layout-stack">
              <i /><i /><i />
            </span>
          </div>
        </div>
      </div>
    </article>

    <article class="cfd__preview">
      <header class="cfd__preview-head">
        <span>ACME</span>
        <span class="cfd__dots" />
      </header>
      <div class="cfd__preview-body">
        <p class="cfd__preview-title">Checkout</p>
        <div class="cfd__preview-steps">
          <span class="cfd__preview-step cfd__preview-step--active">
            <i>1</i> Cart
          </span>
          <span>2. Details</span>
          <span>3. Payment</span>
        </div>
        <span class="cfd__skel" />
        <div class="cfd__fieldbox">
          <span class="cfd__skel cfd__skel--sm" />
        </div>
        <div class="cfd__pay">Pay Now</div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.cfd {
  --cfd-accent: #1a73e8;
  position: relative;
  width: 100%;
  aspect-ratio: 586 / 427;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

.cfd__screen {
  position: absolute;
  left: 12.58%;
  right: 21.14%;
  top: 17.33%;
  bottom: 18.74%;
  overflow: hidden;
  border-radius: 16px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.cfd__grid {
  position: absolute;
  inset: -25%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 24px 24px;
}

.cfd__shield {
  position: absolute;
  left: 50%;
  top: 48%;
  width: min(42%, 126px);
  transform: translate(-50%, -50%);
  filter: drop-shadow(0 0 18px rgba(180, 230, 255, 0.35));
  animation: cfd-glow 3.2s ease-in-out infinite;
  z-index: 1;
}

.cfd__shield img {
  display: block;
  width: 100%;
  height: auto;
}

.cfd__ripple {
  position: absolute;
  z-index: 0;
  width: 12px;
  height: 12px;
  pointer-events: none;
}

.cfd__ripple--a {
  left: 62%;
  top: 22%;
}

.cfd__ripple--b {
  left: 28%;
  top: 68%;
}

.cfd__ripple-core {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(220, 245, 255, 0.95) 0%,
    rgba(180, 230, 255, 0.5) 45%,
    rgba(180, 230, 255, 0) 72%
  );
  filter: blur(4px);
  box-shadow: 0 0 12px 4px rgba(180, 230, 255, 0.35);
}

.cfd__ripple-ring {
  position: absolute;
  left: 50%;
  top: 50%;
  border: 1.5px dotted rgba(180, 230, 255, 0.55);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: cfd-dotted-ring 3.2s ease-out infinite;
}

.cfd__ripple--a .cfd__ripple-ring:nth-child(2) {
  animation-delay: 0s;
}

.cfd__ripple--a .cfd__ripple-ring:nth-child(3) {
  animation-delay: 1.1s;
}

.cfd__ripple--b .cfd__ripple-ring:nth-child(2) {
  animation-delay: 0.5s;
}

.cfd__ripple--b .cfd__ripple-ring:nth-child(3) {
  animation-delay: 1.6s;
}

.cfd__settings {
  position: absolute;
  z-index: 3;
  left: 0;
  top: 34.7%;
  width: 30.7%;
  padding: 14px;
  box-sizing: border-box;
  border-radius: 16px;
  background: #ffffff;
  box-shadow:
    0 1px 1px rgba(0, 0, 0, 0.1),
    0 1px 1.5px rgba(0, 0, 0, 0.1);
  animation: cfd-float 5s ease-in-out infinite;
}

.cfd__settings-title {
  margin: 0 0 12px;
  font-size: clamp(10px, 1.7vw, 12px);
  font-weight: 700;
}

.cfd__field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 10px;
  font-size: clamp(8px, 1.3vw, 9px);
  font-weight: 600;
  color: #535862;
}

.cfd__input {
  display: flex;
  align-items: center;
  height: 28px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: clamp(9px, 1.4vw, 10px);
  color: #252b37;
  background: #fff;
}

.cfd__input--logo {
  font-weight: 700;
  color: var(--cfd-accent);
  transition: color 0.4s ease;
}

.cfd__input--color {
  gap: 6px;
  font-weight: 500;
}

.cfd__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--cfd-accent);
  transition: background 0.4s ease;
}

.cfd__input--font {
  justify-content: space-between;
}

.cfd__chevron {
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid #6b7280;
}

.cfd__swatches {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 4px;
}

.cfd__swatch {
  width: 14px;
  height: 14px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: var(--swatch);
  cursor: pointer;
  box-shadow: 0 0 0 0 transparent;
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.cfd__swatch--active {
  transform: scale(1.08);
  box-shadow: 0 0 0 2px #fff, 0 0 0 3.5px var(--swatch);
}

.cfd__layouts {
  display: flex;
  gap: 8px;
}

.cfd__layout {
  width: 48px;
  height: 34px;
  padding: 3px;
  box-sizing: border-box;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
}

.cfd__layout--active {
  border: 1.5px solid var(--cfd-accent);
  background: #f8f9fc;
  transition: border-color 0.4s ease;
}

.cfd__layout-bar {
  display: block;
  height: 6px;
  border-radius: 2px;
  background: var(--cfd-accent);
  transition: background 0.4s ease;
}

.cfd__layout-line {
  display: block;
  height: 5px;
  margin-top: 3px;
  border-radius: 1px;
  background: #e5e7eb;
}

.cfd__layout-line--sm {
  width: 45%;
}

.cfd__layout-col {
  display: inline-block;
  width: 12px;
  height: 24px;
  border-radius: 2px;
  background: #e5e7eb;
  vertical-align: top;
}

.cfd__layout-stack {
  display: inline-flex;
  flex-direction: column;
  gap: 2px;
  margin-left: 4px;
  vertical-align: top;
}

.cfd__layout-stack i {
  display: block;
  width: 18px;
  height: 6px;
  border-radius: 1px;
  background: #e5e7eb;
}

.cfd__preview {
  position: absolute;
  z-index: 3;
  left: 53.2%;
  top: 0;
  width: 46.8%;
  height: 61.4%;
  overflow: hidden;
  border-radius: 16px;
  background: #ffffff;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px rgba(0, 0, 0, 0.1);
  animation: cfd-float 5.6s ease-in-out infinite reverse;
}

.cfd__preview-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 38px;
  padding: 0 16px;
  background: var(--cfd-accent);
  color: #fff;
  font-size: clamp(11px, 1.9vw, 13px);
  font-weight: 700;
  transition: background 0.4s ease;
}

.cfd__dots {
  width: 24px;
  height: 6px;
  background:
    radial-gradient(circle, #fff 1.5px, transparent 2px) 0 50% / 8px 6px repeat-x;
}

.cfd__preview-body {
  padding: 18px 16px 14px;
}

.cfd__preview-title {
  margin: 0 0 10px;
  font-size: clamp(11px, 1.8vw, 12px);
  font-weight: 600;
}

.cfd__preview-steps {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
  font-size: clamp(8px, 1.3vw, 9px);
  color: #6b7280;
}

.cfd__preview-step--active {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--cfd-accent);
  font-weight: 600;
  transition: color 0.4s ease;
}

.cfd__preview-step--active i {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 12px;
  height: 12px;
  border-radius: 6px;
  background: var(--cfd-accent);
  color: #fff;
  font-style: normal;
  font-size: 8px;
  font-weight: 700;
  transition: background 0.4s ease;
}

.cfd__skel {
  display: block;
  width: 48%;
  height: 12px;
  margin-bottom: 12px;
  border-radius: 4px;
  background: #e2e6ef;
  transform-origin: left center;
  animation: cfd-skel-grow 2.4s ease-in-out infinite;
}

.cfd__skel--sm {
  width: 40%;
  height: 8px;
  margin: 0;
  animation-duration: 2.8s;
  animation-delay: 0.35s;
}

.cfd__fieldbox {
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid #e2e6ef;
  border-radius: 4px;
}

.cfd__pay {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  border-radius: 8px;
  background: var(--cfd-accent);
  color: #fff;
  font-size: clamp(10px, 1.6vw, 11px);
  font-weight: 700;
  transition: background 0.4s ease;
}

@keyframes cfd-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes cfd-glow {
  0%,
  100% {
    opacity: 0.85;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.04);
  }
}

@keyframes cfd-dotted-ring {
  0% {
    width: 12px;
    height: 12px;
    opacity: 0.7;
  }
  100% {
    width: 110px;
    height: 110px;
    opacity: 0;
  }
}

@keyframes cfd-skel-grow {
  0%,
  100% {
    transform: scaleX(0.55);
  }
  50% {
    transform: scaleX(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .cfd__settings,
  .cfd__preview,
  .cfd__shield,
  .cfd__ripple-ring,
  .cfd__skel {
    animation: none;
  }

  .cfd__skel {
    transform: none;
  }
}
</style>
