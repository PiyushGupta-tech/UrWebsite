<script setup>
import { nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: { type: String, default: "Customize Your Brand" },
});

/**
 * Figma 274:4227 (Customize graphic) + 770:2574 Brand Card Flow Animation
 * 11.5s loop (get_motion_context):
 *  ~15%: click + → logo (State-2)
 *  ~35%: purple swatch scales to selected (State-3)
 *  ~55–80%: type manyar.com in steps m → man → manyar → manyar.com (State-4)
 *  ~95%: reset → State-1
 *
 * Drawn at 2× then scaled (avoids browser min-font on tiny type).
 */
const ASSET = "/images/figma-white-label/brand";
const ART_W = 744; // 372 × 2
const ART_H = 476; // 238 × 2
const CYCLE_MS = 11500;

const SWATCHES = [
  { id: "blue", src: "swatch-blue.svg" },
  { id: "green", src: "swatch-green.svg" },
  { id: "purple", src: "swatch-purple.svg" },
  { id: "orange", src: "swatch-orange.svg" },
  { id: "red", src: "swatch-red.svg" },
];

const TYPE_STEPS = ["m", "man", "manyar", "manyar.com"];

const reduceMotion = ref(false);
const showLogo = ref(false);
const purpleSelected = ref(false);
const purplePulse = ref(false);
const domainText = ref("yourbrand.com");
const showCheck = ref(true);
const showCaret = ref(false);
const clicking = ref(false);
const cursor = reactive({ x: 384, y: 138 });

const rootRef = ref(null);
const cardRef = ref(null);
const plusRef = ref(null);
const purpleRef = ref(null);
const domainRef = ref(null);
const scale = ref(0.5);
const offsetX = ref(0);
const offsetY = ref(0);

function setPurpleRef(el) {
  purpleRef.value = el || null;
}

function aimAt(el) {
  const card = cardRef.value;
  if (!card || !el) return;
  const c = card.getBoundingClientRect();
  const r = el.getBoundingClientRect();
  const s = scale.value || 1;
  cursor.x = (r.left + r.width / 2 - c.left) / s;
  cursor.y = (r.top + r.height / 2 - c.top) / s;
}

let timers = [];
let loopTimer = null;
let resizeObserver = null;

function clearTimers() {
  timers.forEach((id) => clearTimeout(id));
  timers = [];
  if (loopTimer) {
    clearTimeout(loopTimer);
    loopTimer = null;
  }
}

function wait(ms) {
  return new Promise((resolve) => {
    timers.push(setTimeout(resolve, ms));
  });
}

function at(pct) {
  return Math.round((pct / 100) * CYCLE_MS);
}

async function clickEl(el, holdMs = 140) {
  if (!el) return;
  aimAt(el);
  await wait(280);
  clicking.value = true;
  await wait(holdMs);
  clicking.value = false;
  await wait(80);
}

function updateScale() {
  const root = rootRef.value;
  if (!root) return;
  const sx = root.clientWidth / ART_W;
  const sy = root.clientHeight / ART_H;
  const next = Math.min(sx, sy);
  scale.value = next;
  offsetX.value = (root.clientWidth - ART_W * next) / 2;
  offsetY.value = (root.clientHeight - ART_H * next) / 2;
}

function resetState() {
  showLogo.value = false;
  purpleSelected.value = false;
  purplePulse.value = false;
  domainText.value = "yourbrand.com";
  showCheck.value = true;
  showCaret.value = false;
  cursor.x = 384;
  cursor.y = 138;
}

async function runSequence() {
  if (reduceMotion.value) return;
  clearTimers();
  resetState();
  await nextTick();

  const start = performance.now();
  async function until(pct) {
    const remaining = at(pct) - (performance.now() - start);
    if (remaining > 0) await wait(remaining);
  }

  // ~9–15%: move to plus, click → logo (State-2)
  await until(8.7);
  await clickEl(plusRef.value, 160);
  showLogo.value = true;

  // ~34%: purple swatch select (State-3) — scale pulse then settle
  await until(33.9);
  await clickEl(purpleRef.value, 160);
  purplePulse.value = true;
  await wait(200);
  purplePulse.value = false;
  purpleSelected.value = true;

  // ~54%: domain field → type manyar.com (State-4)
  await until(53.9);
  await clickEl(domainRef.value, 120);
  domainText.value = "";
  showCheck.value = false;
  showCaret.value = true;

  const typeStarts = [62.61, 67.83, 73.04, 80];
  for (let i = 0; i < TYPE_STEPS.length; i += 1) {
    await until(typeStarts[i]);
    domainText.value = TYPE_STEPS[i];
  }
  showCaret.value = false;
  showCheck.value = true;

  // Hold through ~95%, then reset to State-1
  await until(95.2);
  resetState();
  await until(100);

  loopTimer = setTimeout(() => runSequence(), 80);
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  nextTick(() => {
    updateScale();
    if (typeof ResizeObserver !== "undefined" && rootRef.value) {
      resizeObserver = new ResizeObserver(updateScale);
      resizeObserver.observe(rootRef.value);
    }
    if (!reduceMotion.value) runSequence();
  });
});

onBeforeUnmount(() => {
  clearTimers();
  resizeObserver?.disconnect();
});
</script>

<template>
  <div
    ref="rootRef"
    class="wl-brand"
    :class="{ 'wl-brand--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div
      class="wl-brand__artboard"
      aria-hidden="true"
      :style="{ transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})` }"
    >
      <!-- Blue screen — Figma inset 35.59% L / 0 T / 0 R / 28.62% B -->
      <div class="wl-brand__screen-wrap">
        <div class="wl-brand__screen">
          <div class="wl-brand__screen-fill">
            <img
              class="wl-brand__grid"
              :src="`${ASSET}/grid.svg`"
              alt=""
              width="1432"
              height="766"
              draggable="false"
            />
            <span class="wl-brand__pulse wl-brand__pulse--main">
              <img :src="`${ASSET}/pulse-a.svg`" alt="" width="218" height="218" />
              <img :src="`${ASSET}/pulse-b.svg`" alt="" width="117" height="117" />
            </span>
            <img
              class="wl-brand__shield"
              :src="`${ASSET}/shield.svg`"
              alt=""
              width="160"
              height="160"
              draggable="false"
            />
            <span class="wl-brand__pulse wl-brand__pulse--sm">
              <img :src="`${ASSET}/pulse-sm-a.svg`" alt="" width="37" height="37" />
              <img :src="`${ASSET}/pulse-sm-b.svg`" alt="" width="23" height="23" />
              <img :src="`${ASSET}/pulse-sm-c.svg`" alt="" width="12" height="12" />
            </span>
            <div class="wl-brand__overlay" />
          </div>
        </div>
      </div>

      <!-- Brand card — inset 26.54% T / 41.37% R / 0 B / 0 L → 436×350 @ 2× -->
      <div ref="cardRef" class="wl-brand__card">
        <img
          class="wl-brand__mac"
          :src="`${ASSET}/mac-buttons.svg`"
          alt=""
          width="46"
          height="10"
        />
        <p class="wl-brand__title">Your Brand</p>

        <div class="wl-brand__logo-box">
          <img
            v-if="showLogo"
            class="wl-brand__logo-img"
            :src="`${ASSET}/logo.png`"
            alt=""
            width="28"
            height="30"
          />
          <span v-else class="wl-brand__logo-placeholder">YOUR LOGO</span>
          <button
            ref="plusRef"
            type="button"
            class="wl-brand__plus"
            tabindex="-1"
            aria-hidden="true"
          >
            <img :src="`${ASSET}/plus.svg`" alt="" width="16" height="16" />
          </button>
        </div>

        <div
          class="wl-brand__section wl-brand__section--color"
          :class="{ 'wl-brand__section--shifted': showLogo }"
        >
          <p class="wl-brand__label">Choose primary color</p>
          <div class="wl-brand__swatches">
            <span
              v-for="(sw, i) in SWATCHES"
              :key="sw.id"
              :ref="i === 2 ? setPurpleRef : undefined"
              class="wl-brand__swatch"
              :class="{
                'wl-brand__swatch--selected': i === 2 && purpleSelected,
                'wl-brand__swatch--pulse': i === 2 && purplePulse,
              }"
            >
              <img :src="`${ASSET}/${sw.src}`" alt="" width="26" height="26" />
            </span>
          </div>
        </div>

        <div
          class="wl-brand__section wl-brand__section--domain"
          :class="{ 'wl-brand__section--shifted': showLogo }"
        >
          <p class="wl-brand__label">Your Domain</p>
          <div ref="domainRef" class="wl-brand__domain">
            <span class="wl-brand__domain-text">
              {{ domainText }}<span v-show="showCaret" class="wl-brand__caret" />
            </span>
            <img
              v-show="showCheck"
              class="wl-brand__check"
              :src="`${ASSET}/check.svg`"
              alt=""
              width="18"
              height="18"
            />
          </div>
        </div>

        <div
          v-show="!reduceMotion"
          class="wl-brand__cursor"
          :class="{ 'wl-brand__cursor--click': clicking }"
          :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
        >
          <img :src="`${ASSET}/cursor.svg`" alt="" width="20" height="20" />
          <span v-show="clicking" class="wl-brand__click-ring" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wl-brand {
  position: relative;
  width: min(100%, 498px);
  aspect-ratio: 498 / 280;
  margin-inline: auto;
  overflow: visible;
  line-height: normal;
  background: transparent;
}

.wl-brand__artboard {
  position: absolute;
  left: 0;
  top: 0;
  width: 744px;
  height: 476px;
  transform-origin: top left;
}

.wl-brand__screen-wrap {
  position: absolute;
  left: 35.59%;
  top: 0;
  right: 0;
  bottom: 28.62%;
  z-index: 0;
}

.wl-brand__screen {
  position: absolute;
  inset: 0;
  overflow: hidden;
  border-radius: 18px;
}

.wl-brand__screen-fill {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.wl-brand__grid {
  position: absolute;
  left: 50%;
  top: calc(50% - 96px);
  width: 1432px;
  height: auto;
  transform: translate(-50%, -50%);
  opacity: 0.85;
  pointer-events: none;
}

.wl-brand__shield {
  position: absolute;
  left: calc(50% + 56px);
  top: calc(50% + 10px);
  width: 160px;
  height: 160px;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.wl-brand__pulse {
  position: absolute;
  display: grid;
  place-items: center;
  pointer-events: none;
  mix-blend-mode: screen;
}

.wl-brand__pulse img {
  position: absolute;
  display: block;
  max-width: none;
}

.wl-brand__pulse--main {
  left: calc(50% + 55px);
  top: calc(50% + 10px);
  width: 218px;
  height: 218px;
  transform: translate(-50%, -50%);
}

.wl-brand__pulse--sm {
  left: calc(50% + 71px);
  top: calc(50% - 99px);
  width: 37px;
  height: 37px;
  transform: translate(-50%, -50%);
}

.wl-brand--motion .wl-brand__pulse--main {
  animation: wl-brand-pulse 2.8s ease-in-out infinite;
}

@keyframes wl-brand-pulse {
  0%,
  100% {
    opacity: 0.75;
    transform: translate(-50%, -50%) scale(0.94);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.05);
  }
}

.wl-brand__overlay {
  position: absolute;
  inset: 0;
  background: rgba(56, 127, 245, 0.1);
  mix-blend-mode: color-burn;
  pointer-events: none;
}

.wl-brand__card {
  position: absolute;
  left: 0;
  top: 126px;
  width: 436px;
  height: 350px;
  z-index: 2;
  box-sizing: border-box;
  padding: 26px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 2px 3px rgba(0, 0, 0, 0.1);
}

.wl-brand__mac {
  display: block;
  width: 46px;
  height: 10px;
}

.wl-brand__title {
  position: absolute;
  left: 26px;
  top: 56px;
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
}

.wl-brand__logo-box {
  position: absolute;
  left: 26px;
  right: 26px;
  top: 99px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 46px;
  padding: 15px;
  box-sizing: border-box;
  border: 1.3px dashed #e5e7eb;
  border-radius: 10px;
}

.wl-brand__logo-placeholder {
  font-family: Manrope, system-ui, sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
}

.wl-brand__logo-img {
  display: block;
  width: 28px;
  height: 30px;
  object-fit: contain;
}

.wl-brand__plus {
  display: grid;
  place-items: center;
  width: 16px;
  height: 16px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: default;
  flex-shrink: 0;
}

.wl-brand__plus img {
  display: block;
  width: 16px;
  height: 16px;
}

.wl-brand__section {
  position: absolute;
  left: 26px;
  right: 26px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wl-brand__section--color {
  top: 168px;
}

.wl-brand__section--domain {
  top: 242px;
}

.wl-brand__section--color.wl-brand__section--shifted {
  top: 180px;
}

.wl-brand__section--domain.wl-brand__section--shifted {
  top: 254px;
}

.wl-brand__label {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #252b37;
  white-space: nowrap;
}

.wl-brand__swatches {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 36px;
}

.wl-brand__swatch {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  transition: transform 0.28s cubic-bezier(0.45, 0, 0.2, 1);
}

.wl-brand__swatch img {
  display: block;
  width: 26px;
  height: 26px;
}

.wl-brand__swatch--pulse {
  transform: scale(1.4);
}

.wl-brand__swatch--selected {
  transform: scale(1.25);
}

.wl-brand__domain {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 384px;
  max-width: 100%;
  height: 40px;
  padding: 0 13px;
  box-sizing: border-box;
  border: 1.3px solid #e5e7eb;
  border-radius: 8px;
  background: #fafbfa;
}

.wl-brand__domain-text {
  display: inline-flex;
  align-items: center;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #535862;
  white-space: nowrap;
}

.wl-brand__caret {
  display: inline-block;
  width: 1.5px;
  height: 14px;
  margin-left: 1px;
  background: #252b37;
  animation: wl-brand-caret 0.9s step-end infinite;
}

@keyframes wl-brand-caret {
  50% {
    opacity: 0;
  }
}

.wl-brand__check {
  display: block;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.wl-brand__cursor {
  position: absolute;
  z-index: 8;
  width: 20px;
  height: 20px;
  margin-left: -2px;
  margin-top: -2px;
  pointer-events: none;
  transition:
    left 0.5s cubic-bezier(0.45, 0, 0.2, 1),
    top 0.5s cubic-bezier(0.45, 0, 0.2, 1),
    transform 0.12s ease;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.35));
}

.wl-brand__cursor img {
  display: block;
  width: 20px;
  height: 20px;
}

.wl-brand__cursor--click {
  transform: scale(0.82);
  transform-origin: 2px 2px;
}

.wl-brand__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.85);
  animation: wl-brand-ring 0.28s ease-out forwards;
}

@keyframes wl-brand-ring {
  from {
    transform: scale(0.4);
    opacity: 0.95;
  }
  to {
    transform: scale(1.8);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .wl-brand__cursor,
  .wl-brand__swatch,
  .wl-brand__pulse--main,
  .wl-brand__caret {
    transition: none;
    animation: none;
  }
}
</style>
