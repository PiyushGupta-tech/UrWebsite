<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: { type: String, default: "Configure Your Platform" },
});

const ASSET = "/images/figma-white-label/cfg";
/**
 * Figma 274:2182 — Frame 2147225859 (492×243)
 * Artboard is drawn at 2× (984×486) then scaled down so 6–8px type
 * isn’t inflated by browser minimum font-size (which was overflowing the card).
 * Cursor aims at live nav/toggle centers.
 *
 * Visible blue screen fill (screen-wrap × inset) — scale to match Brand’s blue card.
 * Brand: wrap = 64.41% × 71.38% of 744×476, inset 0.
 * Cfg: wrap 580×380 @ (232,24), inset 8.49% / 9.66% / 3.62% / 8.97%.
 */
const BRAND_ART_W = 744;
const BRAND_ART_H = 476;
const BRAND_BLUE_W = 744 * (1 - 0.3559);
const BLUE_LEFT = 232 + 580 * 0.0897;
const BLUE_TOP = 24 + 380 * 0.0849;
const BLUE_W = 580 * (1 - 0.0966 - 0.0897);
const BLUE_H = 380 * (1 - 0.0849 - 0.0362);

const reduceMotion = ref(false);
const activeNav = ref(0);
const clicking = ref(false);
/** Cursor tip in card-local CSS px (2× space) */
const cursor = reactive({ x: 92, y: 98 });

const rootRef = ref(null);
const cardRef = ref(null);
const navItemRefs = ref([]);
const rowToggleRefs = ref([]);
const scale = ref(0.5);
const offsetX = ref(0);
const offsetY = ref(0);

const NAV = ["Features", "Payments", "Orchestration", "Checkout Type"];

const PANELS = [
  {
    label: "Enable Features",
    rows: [
      { label: "Payment Gateway", on: true },
      { label: "Payouts System", on: true },
      { label: "Auto-Reconcile", on: true },
      { label: "Monthly Reports", on: false },
    ],
  },
  {
    label: "Enable Features",
    rows: [
      { label: "UPI", on: true },
      { label: "Cards", on: true },
      { label: "Net Banking", on: true },
      { label: "Smart Routing", on: false },
    ],
  },
  {
    label: "Enable Features",
    rows: [
      { label: "Smart Routing", on: true },
      { label: "Failover Rules", on: true },
      { label: "Cascade Retry", on: false },
      { label: "Load Balance", on: true },
    ],
  },
  {
    label: "Enable Features",
    rows: [
      { label: "Hosted Checkout", on: true },
      { label: "Embedded Widget", on: true },
      { label: "Custom API", on: false },
      { label: "QR Payments", on: true },
    ],
  },
];

const panelState = ref(PANELS.map((p) => p.rows.map((r) => ({ ...r }))));

const currentPanel = computed(() => ({
  label: PANELS[activeNav.value].label,
  rows: panelState.value[activeNav.value],
}));

function setNavRef(el, i) {
  if (el) navItemRefs.value[i] = el;
}

function setToggleRef(el, i) {
  if (el) rowToggleRefs.value[i] = el;
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

async function clickEl(el, holdMs = 160) {
  if (!el) return;
  aimAt(el);
  await wait(300);
  clicking.value = true;
  await wait(holdMs);
  clicking.value = false;
  await wait(120);
}

function resetPanels() {
  panelState.value = PANELS.map((p) => p.rows.map((r) => ({ ...r })));
}

function setToggle(navIdx, rowIdx, on) {
  panelState.value[navIdx][rowIdx].on = on;
}

function flipToggle(navIdx, rowIdx) {
  panelState.value[navIdx][rowIdx].on = !panelState.value[navIdx][rowIdx].on;
}

function updateScale() {
  const root = rootRef.value;
  if (!root) return;
  // Match Brand step's dark-blue screen width; keep X aligned with Brand blue
  const brandScale = Math.min(
    root.clientWidth / BRAND_ART_W,
    root.clientHeight / BRAND_ART_H,
  );
  const next = (BRAND_BLUE_W * brandScale) / BLUE_W;
  scale.value = next;
  const brandOx = (root.clientWidth - BRAND_ART_W * brandScale) / 2;
  const brandBlueLeft = brandOx + BRAND_ART_W * 0.3559 * brandScale;
  // Nudge left so Analytics clears the steps wire / "02" number
  offsetX.value = brandBlueLeft - BLUE_LEFT * next - 28;
  // Vertically center the blue screen in the slot (cards overhang; overflow visible)
  const blueH = BLUE_H * next;
  offsetY.value = (root.clientHeight - blueH) / 2 - BLUE_TOP * next;
}

async function runSequence() {
  if (reduceMotion.value) return;
  clearTimers();
  resetPanels();
  activeNav.value = 0;
  await nextTick();

  await clickEl(navItemRefs.value[0]);
  activeNav.value = 0;
  await nextTick();

  await clickEl(rowToggleRefs.value[3], 200);
  setToggle(0, 3, true);
  await wait(450);

  await clickEl(navItemRefs.value[1]);
  activeNav.value = 1;
  await nextTick();
  await wait(250);
  await clickEl(rowToggleRefs.value[3], 200);
  setToggle(1, 3, true);
  await wait(450);

  await clickEl(navItemRefs.value[2]);
  activeNav.value = 2;
  await nextTick();
  await wait(250);
  await clickEl(rowToggleRefs.value[2], 200);
  flipToggle(2, 2);
  await wait(450);

  await clickEl(navItemRefs.value[3]);
  activeNav.value = 3;
  await nextTick();
  await wait(250);
  await clickEl(rowToggleRefs.value[2], 200);
  flipToggle(3, 2);
  await wait(900);

  loopTimer = setTimeout(() => runSequence(), 400);
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
    class="wl-cfg"
    :class="{ 'wl-cfg--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div
      class="wl-cfg__artboard"
      aria-hidden="true"
      :style="{ transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})` }"
    >
      <!-- 274:2183 @ 116,12 → ×2 -->
      <div class="wl-cfg__screen-wrap">
        <div class="wl-cfg__screen">
          <div class="wl-cfg__screen-fill">
            <img
              class="wl-cfg__grid"
              :src="`${ASSET}/grid.svg`"
              alt=""
              width="840"
              height="450"
              draggable="false"
            />
            <span class="wl-cfg__pulse wl-cfg__pulse--a">
              <img :src="`${ASSET}/pulse-a.svg`" alt="" width="146" height="146" />
              <img :src="`${ASSET}/pulse-a1.svg`" alt="" width="106" height="106" />
              <img :src="`${ASSET}/pulse-a2.svg`" alt="" width="20" height="20" />
            </span>
            <span class="wl-cfg__pulse wl-cfg__pulse--b">
              <img :src="`${ASSET}/pulse-b.svg`" alt="" width="44" height="44" />
              <img :src="`${ASSET}/pulse-b1.svg`" alt="" width="28" height="28" />
              <img :src="`${ASSET}/pulse-b2.svg`" alt="" width="14" height="14" />
            </span>
            <span class="wl-cfg__pulse wl-cfg__pulse--c">
              <img :src="`${ASSET}/pulse-c.svg`" alt="" width="102" height="102" />
              <img :src="`${ASSET}/pulse-c1.svg`" alt="" width="54" height="54" />
              <img :src="`${ASSET}/pulse-c2.svg`" alt="" width="28" height="28" />
            </span>
            <div class="wl-cfg__screen-overlay" />
          </div>
        </div>
      </div>

      <!-- 274:2222 @ 297,0 → ×2 -->
      <div class="wl-cfg__analytics">
        <p class="wl-cfg__analytics-title">Analytics Overview</p>
        <div class="wl-cfg__analytics-body">
          <img
            class="wl-cfg__donut"
            :src="`${ASSET}/donut.svg`"
            alt=""
            width="128"
            height="128"
          />
          <div class="wl-cfg__legends">
            <div class="wl-cfg__legend">
              <img :src="`${ASSET}/legend-green.svg`" alt="" width="12" height="12" />
              <span>Cards (65%)</span>
            </div>
            <div class="wl-cfg__legend">
              <img :src="`${ASSET}/legend-blue.svg`" alt="" width="12" height="12" />
              <span>UPI (25%)</span>
            </div>
            <div class="wl-cfg__legend">
              <img :src="`${ASSET}/legend-orange.svg`" alt="" width="12" height="12" />
              <span>Net Banking</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 274:2186 @ 0,96 221×129 → ×2 = 442×258 -->
      <div ref="cardRef" class="wl-cfg__card">
        <img
          class="wl-cfg__mac"
          :src="`${ASSET}/mac-buttons.svg`"
          alt=""
          width="42"
          height="10"
        />
        <p class="wl-cfg__title">Platform Settings</p>
        <div class="wl-cfg__split">
          <nav class="wl-cfg__nav">
            <span
              v-for="(item, i) in NAV"
              :key="item"
              :ref="(el) => setNavRef(el, i)"
              class="wl-cfg__nav-item"
              :class="{ 'wl-cfg__nav-item--active': activeNav === i }"
            >
              {{ item }}
            </span>
          </nav>
          <div class="wl-cfg__panel">
            <p class="wl-cfg__panel-label">{{ currentPanel.label }}</p>
            <div
              v-for="(row, ri) in currentPanel.rows"
              :key="row.label"
              class="wl-cfg__row"
            >
              <span>{{ row.label }}</span>
              <span
                :ref="(el) => setToggleRef(el, ri)"
                class="wl-cfg__toggle"
                :class="{ 'wl-cfg__toggle--on': row.on }"
              >
                <span class="wl-cfg__knob" />
              </span>
            </div>
          </div>
        </div>

        <div
          v-show="!reduceMotion"
          class="wl-cfg__cursor"
          :class="{ 'wl-cfg__cursor--click': clicking }"
          :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
        >
          <img
            src="/images/figma-white-label/settings-cursor.svg"
            alt=""
            width="20"
            height="20"
          />
          <span v-show="clicking" class="wl-cfg__click-ring" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wl-cfg {
  position: relative;
  width: min(100%, 498px);
  aspect-ratio: 498 / 280;
  margin-inline: auto;
  /* Match Brand: blue-equal scale can overhang the slot; don't clip cards */
  overflow: visible;
  line-height: normal;
  background: transparent;
}

.wl-cfg__artboard {
  position: absolute;
  left: 0;
  top: 0;
  width: 984px;
  height: 486px;
  transform-origin: top left;
}

.wl-cfg__screen-wrap {
  position: absolute;
  left: 232px;
  top: 24px;
  width: 580px;
  height: 380px;
  z-index: 0;
}

.wl-cfg__screen {
  position: absolute;
  inset: 8.49% 9.66% 3.62% 8.97%;
  overflow: hidden;
  border-radius: 32px;
}

.wl-cfg__screen-fill {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.wl-cfg__grid {
  position: absolute;
  left: 50%;
  top: calc(50% - 44px);
  width: 1680px;
  height: auto;
  transform: translate(-50%, -50%);
  pointer-events: none;
  opacity: 0.85;
}

.wl-cfg__pulse {
  position: absolute;
  display: grid;
  place-items: center;
  pointer-events: none;
  mix-blend-mode: screen;
}

.wl-cfg__pulse img {
  position: absolute;
  display: block;
  max-width: none;
}

.wl-cfg__pulse--a {
  left: calc(50% - 12px);
  top: 50%;
  width: 146px;
  height: 146px;
  transform: translate(-50%, -50%);
}
.wl-cfg__pulse--a img:nth-child(1) {
  width: 146px;
  height: 146px;
}
.wl-cfg__pulse--a img:nth-child(2) {
  width: 106px;
  height: 106px;
}
.wl-cfg__pulse--a img:nth-child(3) {
  width: 20px;
  height: 20px;
}

.wl-cfg__pulse--b {
  left: calc(50% + 20px);
  top: calc(50% - 36px);
  width: 44px;
  height: 44px;
  transform: translate(-50%, -50%);
}
.wl-cfg__pulse--b img:nth-child(1) {
  width: 44px;
  height: 44px;
}
.wl-cfg__pulse--b img:nth-child(2) {
  width: 28px;
  height: 28px;
}
.wl-cfg__pulse--b img:nth-child(3) {
  width: 14px;
  height: 14px;
}

.wl-cfg__pulse--c {
  left: calc(50% - 46px);
  top: calc(50% + 50px);
  width: 102px;
  height: 102px;
  transform: translate(-50%, -50%);
}
.wl-cfg__pulse--c img:nth-child(1) {
  width: 102px;
  height: 102px;
}
.wl-cfg__pulse--c img:nth-child(2) {
  width: 54px;
  height: 54px;
}
.wl-cfg__pulse--c img:nth-child(3) {
  width: 28px;
  height: 28px;
}

.wl-cfg--motion .wl-cfg__pulse--a {
  animation: wl-cfg-pulse 2.8s ease-in-out infinite;
}
.wl-cfg--motion .wl-cfg__pulse--b {
  animation: wl-cfg-pulse 2.8s ease-in-out 0.6s infinite;
}
.wl-cfg--motion .wl-cfg__pulse--c {
  animation: wl-cfg-pulse 2.8s ease-in-out 1.2s infinite;
}

@keyframes wl-cfg-pulse {
  0%,
  100% {
    opacity: 0.75;
    transform: translate(-50%, -50%) scale(0.92);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.06);
  }
}

.wl-cfg__screen-overlay {
  position: absolute;
  inset: 0;
  background: rgba(56, 127, 245, 0.1);
  mix-blend-mode: color-burn;
  pointer-events: none;
}

.wl-cfg__analytics {
  position: absolute;
  /* Nudged left of Figma 297×2 so it clears the steps wire */
  left: 548px;
  top: 0;
  width: 390px;
  height: 258px;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px;
  box-sizing: border-box;
  border-radius: 24px;
  background: #ffffff;
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 2px 3px rgba(0, 0, 0, 0.1);
}

.wl-cfg__analytics-title {
  margin: 0;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 24px;
  font-weight: 700;
  line-height: normal;
  color: #252b37;
  white-space: nowrap;
}

.wl-cfg__analytics-body {
  display: flex;
  align-items: center;
  gap: 32px;
}

.wl-cfg__donut {
  display: block;
  width: 128px;
  height: 128px;
  flex-shrink: 0;
}

.wl-cfg__legends {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.wl-cfg__legend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 20px;
  font-weight: 400;
  line-height: normal;
  color: #535862;
  white-space: nowrap;
}

.wl-cfg__legend img {
  display: block;
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}

.wl-cfg__card {
  position: absolute;
  left: 0;
  top: 192px;
  width: 442px;
  height: 258px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 23px;
  box-sizing: border-box;
  border-radius: 18.6px;
  background: #ffffff;
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 2px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.wl-cfg__mac {
  display: block;
  width: 42px;
  height: 9.3px;
  flex-shrink: 0;
}

.wl-cfg__title {
  margin: 0;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  color: #252b37;
  white-space: nowrap;
}

.wl-cfg__split {
  display: flex;
  gap: 18.6px;
  flex: 1 1 auto;
  min-height: 0;
  height: 152px;
}

.wl-cfg__nav {
  display: flex;
  flex-direction: column;
  gap: 7px;
  width: 140px;
  flex-shrink: 0;
}

.wl-cfg__nav-item {
  display: flex;
  align-items: center;
  box-sizing: border-box;
  height: 30px;
  padding: 7px 9px;
  border-radius: 7px;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 12.8px;
  font-weight: 500;
  line-height: normal;
  color: #535862;
  white-space: nowrap;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    font-weight 0.2s ease;
}

.wl-cfg__nav-item--active {
  background: #d8f3dc;
  font-weight: 700;
  color: #1b4332;
}

.wl-cfg__panel {
  display: flex;
  flex-direction: column;
  gap: 11.6px;
  flex: 1;
  min-width: 0;
}

.wl-cfg__panel-label {
  margin: 0;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 12.8px;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
  color: #1b4332;
  white-space: nowrap;
}

.wl-cfg__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  height: 21px;
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 15.1px;
  font-weight: 500;
  line-height: normal;
  color: #252b37;
  white-space: nowrap;
}

.wl-cfg__toggle {
  position: relative;
  flex-shrink: 0;
  width: 39.5px;
  height: 21px;
  border-radius: 10.5px;
  background: #d1d5db;
  box-sizing: border-box;
  padding: 2.3px;
  transition: background 0.22s ease;
}

.wl-cfg__toggle--on {
  background: #2d6a4f;
}

.wl-cfg__knob {
  display: block;
  width: 16.3px;
  height: 16.3px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
  transform: translateX(0);
  transition: transform 0.22s ease;
}

.wl-cfg__toggle--on .wl-cfg__knob {
  transform: translateX(18.6px);
}

/* Tip ≈ (2.5, 2.5) in 20×20 (2× of 10×10 tip at 1.25) */
.wl-cfg__cursor {
  position: absolute;
  z-index: 6;
  width: 20px;
  height: 20px;
  margin-left: -2.5px;
  margin-top: -2.5px;
  pointer-events: none;
  transition:
    left 0.45s cubic-bezier(0.45, 0, 0.2, 1),
    top 0.45s cubic-bezier(0.45, 0, 0.2, 1),
    transform 0.12s ease;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.35));
}

.wl-cfg__cursor img {
  display: block;
  width: 20px;
  height: 20px;
}

.wl-cfg__cursor--click {
  transform: scale(0.82);
  transform-origin: 2.5px 2.5px;
}

.wl-cfg__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(45, 106, 79, 0.85);
  animation: wl-cfg-ring 0.28s ease-out forwards;
}

@keyframes wl-cfg-ring {
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
  .wl-cfg__cursor,
  .wl-cfg__nav-item,
  .wl-cfg__toggle,
  .wl-cfg__knob,
  .wl-cfg__pulse--a,
  .wl-cfg__pulse--b,
  .wl-cfg__pulse--c {
    transition: none;
    animation: none;
  }
}
</style>
