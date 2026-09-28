<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: { type: String, default: "Launch Under Your Brand" },
});

const ASSET = "/images/figma-white-label/launch";
/**
 * Figma 274:2252 — Launch Under Your Brand
 * Storyboard (Frame 1 → 2 → 3 → 5):
 * 1) Cursor clicks “Last 30 Days” dropdown
 * 2) Menu opens; hover/select “Last 15 Days” (grey highlight)
 * 3) Selection applies; stats + bars update
 * 5) Cursor reopens menu, picks “Last Week”; stats + bars update
 * Loop.
 *
 * Drawn at 2× (632×530) then scaled so tiny Figma type isn’t min-font clamped.
 *
 * Visible blue screen fill (screen-wrap × inset) — scale to match Brand’s blue card.
 * Brand: wrap = 64.41% × 71.38% of 744×476, inset 0.
 * Launch: wrap 580×380 @ (52,0), inset 0 / 0 / 10.81% / 17.41%.
 */
const BRAND_ART_W = 744;
const BRAND_ART_H = 476;
const BRAND_BLUE_W = 744 * (1 - 0.3559);
const BLUE_LEFT = 52 + 580 * 0.1741;
const BLUE_TOP = 0;
const BLUE_W = 580 * (1 - 0.1741);
const BAR_MAX = 42; // tallest Figma bar (frame 5 Fri)

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const MENU = ["Last 15 Days", "Last Week", "Yesterday", "Last 30 Days"];

const PERIODS = {
  "Last 30 Days": {
    stats: [
      { label: "Total Transactions", value: "24,780", change: "↑ 12.5%" },
      { label: "Success Rate", value: "98.6%", change: "↑ 8.2%" },
      { label: "Total Revenue", value: "₹12.6M", change: "↑ 15.3%" },
    ],
    // Figma 274:2252 / Frame 1 bar heights
    bars: [22.37, 30.76, 16.78, 25.16, 33.55, 27.96, 19.57],
  },
  "Last 15 Days": {
    stats: [
      { label: "Total Transactions", value: "5,340", change: "↑ 10.5%" },
      { label: "Success Rate", value: "99.5%", change: "↑ 6.8%" },
      { label: "Total Revenue", value: "₹2.74M", change: "↑ 11.2%" },
    ],
    // Frame 3
    bars: [14, 22, 31, 36, 19, 36, 14],
  },
  "Last Week": {
    stats: [
      { label: "Total Transactions", value: "11,263", change: "↑ 9.5%" },
      { label: "Success Rate", value: "89.1%", change: "↑ 7.4%" },
      { label: "Total Revenue", value: "₹6.67M", change: "↑ 09.2%" },
    ],
    // Frame 5
    bars: [31, 13, 19, 30, 42, 18, 28],
  },
};

const reduceMotion = ref(false);
const selected = ref("Last 30 Days");
const menuOpen = ref(false);
const hoverOption = ref("");
const clicking = ref(false);
const cursor = reactive({ x: 540, y: 100 });

const rootRef = ref(null);
const dashRef = ref(null);
const dropdownRef = ref(null);
const optionRefs = ref([]);
const scale = ref(0.5);
const offsetX = ref(0);
const offsetY = ref(0);

const current = computed(() => PERIODS[selected.value] || PERIODS["Last 30 Days"]);

const barPercents = computed(() =>
  current.value.bars.map((h) => Math.max(8, (h / BAR_MAX) * 100)),
);

function setOptionRef(el, i) {
  if (el) optionRefs.value[i] = el;
}

function aimAt(el) {
  const dash = dashRef.value;
  if (!dash || !el) return;
  const d = dash.getBoundingClientRect();
  const r = el.getBoundingClientRect();
  const s = scale.value || 1;
  cursor.x = (r.left + r.width / 2 - d.left) / s;
  cursor.y = (r.top + r.height / 2 - d.top) / s;
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
  await wait(320);
  clicking.value = true;
  await wait(holdMs);
  clicking.value = false;
  await wait(100);
}

function updateScale() {
  const root = rootRef.value;
  if (!root) return;
  // Match Brand step's dark-blue screen size + slot position
  const brandScale = Math.min(
    root.clientWidth / BRAND_ART_W,
    root.clientHeight / BRAND_ART_H,
  );
  const next = (BRAND_BLUE_W * brandScale) / BLUE_W;
  scale.value = next;
  const brandOx = (root.clientWidth - BRAND_ART_W * brandScale) / 2;
  const brandOy = (root.clientHeight - BRAND_ART_H * brandScale) / 2;
  // Brand blue sits at left 35.59%, top 0 within its artboard
  const brandBlueLeft = brandOx + BRAND_ART_W * 0.3559 * brandScale;
  const brandBlueTop = brandOy;
  offsetX.value = brandBlueLeft - BLUE_LEFT * next;
  offsetY.value = brandBlueTop - BLUE_TOP * next;
}

function applyPeriod(label) {
  selected.value = label;
  menuOpen.value = false;
  hoverOption.value = "";
}

async function runSequence() {
  if (reduceMotion.value) return;
  clearTimers();
  selected.value = "Last 30 Days";
  menuOpen.value = false;
  hoverOption.value = "";
  await nextTick();

  // 1) Click dropdown (Frame 1 → 2)
  await clickEl(dropdownRef.value);
  menuOpen.value = true;
  await nextTick();
  await wait(280);

  // 2) Hover + select Last 15 Days
  const opt15 = optionRefs.value[0];
  aimAt(opt15);
  hoverOption.value = "Last 15 Days";
  await wait(400);
  await clickEl(opt15, 180);
  applyPeriod("Last 15 Days");
  await wait(1100);

  // 3) Open again → Last Week (Frame 5)
  await clickEl(dropdownRef.value);
  menuOpen.value = true;
  await nextTick();
  await wait(280);

  const optWeek = optionRefs.value[1];
  aimAt(optWeek);
  hoverOption.value = "Last Week";
  await wait(400);
  await clickEl(optWeek, 180);
  applyPeriod("Last Week");
  await wait(1400);

  // Reset toward Frame 1 look, then loop
  await clickEl(dropdownRef.value);
  menuOpen.value = true;
  await nextTick();
  await wait(200);
  const opt30 = optionRefs.value[3];
  aimAt(opt30);
  hoverOption.value = "Last 30 Days";
  await wait(350);
  await clickEl(opt30, 160);
  applyPeriod("Last 30 Days");
  await wait(700);

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
    else selected.value = "Last 30 Days";
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
    class="wl-launch"
    :class="{ 'wl-launch--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div
      class="wl-launch__artboard"
      aria-hidden="true"
      :style="{ transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})` }"
    >
      <!-- Blue screen — Figma 274:2253 @ 26,0 290×190 → ×2 -->
      <div class="wl-launch__screen-wrap">
        <div class="wl-launch__screen">
          <div class="wl-launch__screen-fill">
            <img
              class="wl-launch__grid"
              :src="`${ASSET}/grid.svg`"
              alt=""
              width="1460"
              height="780"
              draggable="false"
            />
            <img
              class="wl-launch__wave"
              :src="`${ASSET}/wave.svg`"
              alt=""
              width="1204"
              height="270"
              draggable="false"
            />
            <img
              class="wl-launch__chart-a"
              :src="`${ASSET}/chart-line-a.svg`"
              alt=""
              width="1204"
              height="262"
              draggable="false"
            />
            <span class="wl-launch__pulse">
              <img :src="`${ASSET}/pulse-a.svg`" alt="" width="176" height="176" />
              <img :src="`${ASSET}/pulse-b.svg`" alt="" width="124" height="124" />
              <img :src="`${ASSET}/pulse-c.svg`" alt="" width="62" height="62" />
              <img :src="`${ASSET}/pulse-d.svg`" alt="" width="21" height="21" />
            </span>
            <div class="wl-launch__overlay" />
          </div>
        </div>
      </div>

      <!-- Dashboard — 744:6792 @ 11,101 295×167 → ×2 -->
      <div ref="dashRef" class="wl-launch__dash">
        <header class="wl-launch__header">
          <div class="wl-launch__brand">
            <img
              :src="`${ASSET}/logo-mark.svg`"
              alt=""
              width="18"
              height="18"
            />
            <span>YOUR LOGO&nbsp;&nbsp;I&nbsp;&nbsp;YOUR COLORS</span>
          </div>
          <div class="wl-launch__user">
            <img
              class="wl-launch__avatar"
              :src="`${ASSET}/avatar.png`"
              alt=""
              width="18"
              height="18"
            />
            <span>Admin</span>
          </div>
        </header>

        <div class="wl-launch__body">
          <div class="wl-launch__toolbar">
            <p class="wl-launch__metrics-label">Metrics</p>
            <div class="wl-launch__dd-wrap">
              <button
                ref="dropdownRef"
                type="button"
                class="wl-launch__dropdown"
                :class="{ 'wl-launch__dropdown--open': menuOpen }"
                tabindex="-1"
              >
                <span>{{ selected }}</span>
                <img
                  :src="`${ASSET}/chevron.svg`"
                  alt=""
                  width="24"
                  height="24"
                />
              </button>

              <div
                v-show="menuOpen"
                class="wl-launch__menu"
                role="listbox"
              >
                <span
                  v-for="(opt, i) in MENU"
                  :key="opt"
                  :ref="(el) => setOptionRef(el, i)"
                  class="wl-launch__option"
                  :class="{
                    'wl-launch__option--hover': hoverOption === opt,
                    'wl-launch__option--active': selected === opt,
                  }"
                >
                  {{ opt }}
                </span>
              </div>
            </div>
          </div>

          <div class="wl-launch__stats">
            <article
              v-for="stat in current.stats"
              :key="stat.label"
              class="wl-launch__stat"
            >
              <p class="wl-launch__stat-label">{{ stat.label }}</p>
              <p class="wl-launch__stat-value">{{ stat.value }}</p>
              <p class="wl-launch__stat-change">{{ stat.change }}</p>
            </article>
          </div>

          <div class="wl-launch__chart">
            <p class="wl-launch__chart-title">Transaction Overview</p>
            <div class="wl-launch__bars">
              <div
                v-for="(day, i) in DAYS"
                :key="day"
                class="wl-launch__bar-col"
              >
                <div
                  class="wl-launch__bar"
                  :style="{ height: `${barPercents[i]}%` }"
                />
                <span>{{ day }}</span>
              </div>
            </div>
          </div>
        </div>

        <div
          v-show="!reduceMotion"
          class="wl-launch__cursor"
          :class="{ 'wl-launch__cursor--click': clicking }"
          :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
        >
          <img :src="`${ASSET}/cursor.svg`" alt="" width="16" height="16" />
          <span v-show="clicking" class="wl-launch__click-ring" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wl-launch {
  position: relative;
  width: min(100%, 498px);
  aspect-ratio: 498 / 280;
  margin-inline: auto;
  /* Match Brand: blue-equal scale can overhang the slot; don't clip screen/dash */
  overflow: visible;
  line-height: normal;
  background: transparent;
}

.wl-launch__artboard {
  position: absolute;
  left: 0;
  top: 0;
  width: 632px;
  height: 530px;
  transform-origin: top left;
}

.wl-launch__screen-wrap {
  position: absolute;
  left: 52px;
  top: 0;
  width: 580px;
  height: 380px;
  z-index: 0;
}

.wl-launch__screen {
  position: absolute;
  inset: 0 0 10.81% 17.41%;
  overflow: hidden;
  border-radius: 32px;
}

.wl-launch__screen-fill {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.wl-launch__grid {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 1460px;
  height: auto;
  transform: translate(-50%, -50%);
  opacity: 0.85;
  pointer-events: none;
}

.wl-launch__wave,
.wl-launch__chart-a {
  position: absolute;
  left: 55%;
  top: 48%;
  width: 1204px;
  height: auto;
  transform: translate(-50%, -50%);
  pointer-events: none;
  opacity: 0.9;
}

.wl-launch__pulse {
  position: absolute;
  left: calc(50% - 76px);
  top: calc(50% + 5px);
  width: 176px;
  height: 176px;
  display: grid;
  place-items: center;
  transform: translate(-50%, -50%);
  mix-blend-mode: screen;
  pointer-events: none;
}

.wl-launch__pulse img {
  position: absolute;
  display: block;
  max-width: none;
}

.wl-launch--motion .wl-launch__pulse {
  animation: wl-launch-pulse 2.8s ease-in-out infinite;
}

@keyframes wl-launch-pulse {
  0%,
  100% {
    opacity: 0.75;
    transform: translate(-50%, -50%) scale(0.92);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.05);
  }
}

.wl-launch__overlay {
  position: absolute;
  inset: 0;
  background: rgba(56, 127, 245, 0.1);
  mix-blend-mode: color-burn;
  pointer-events: none;
}

.wl-launch__dash {
  position: absolute;
  left: 22px;
  top: 202px;
  width: 590px;
  height: 334px;
  z-index: 2;
  overflow: visible;
  border-radius: 18px;
  background: #ffffff;
  box-shadow:
    0 2px 4px -2px rgba(0, 0, 0, 0.1),
    0 2px 6px rgba(0, 0, 0, 0.1);
}

.wl-launch__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  padding: 0 18px;
  box-sizing: border-box;
  background: #1b4332;
  /* Match dash radius (Figma 8.947 × 2) so top corners stay curved */
  border-radius: 18px 18px 0 0;
}

.wl-launch__brand,
.wl-launch__user {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #ffffff;
  font-family: Manrope, Inter, system-ui, sans-serif;
  white-space: nowrap;
}

.wl-launch__brand {
  font-size: 12px;
  font-weight: 700;
}

.wl-launch__brand img {
  display: block;
  width: 18px;
  height: 18px;
}

.wl-launch__user {
  font-family: Inter, Manrope, system-ui, sans-serif;
  font-size: 11px;
  font-weight: 600;
}

.wl-launch__avatar {
  display: block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  object-fit: cover;
}

.wl-launch__body {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 12px 16px 16px;
  box-sizing: border-box;
}

.wl-launch__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.wl-launch__metrics-label {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #252b37;
}

.wl-launch__dd-wrap {
  position: relative;
  z-index: 4;
}

.wl-launch__dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 132px;
  height: 40px;
  padding: 0 16px;
  box-sizing: border-box;
  border: 1.6px solid #e2e8f0;
  border-radius: 4px;
  background: #ffffff;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #535862;
  cursor: default;
  white-space: nowrap;
}

.wl-launch__dropdown img {
  display: block;
  width: 24px;
  height: 24px;
  transition: transform 0.2s ease;
}

.wl-launch__dropdown--open img {
  transform: rotate(180deg);
}

.wl-launch__menu {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  width: 132px;
  padding: 14px;
  box-sizing: border-box;
  border-radius: 8px;
  background: #ffffff;
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.1),
    0 1px 3px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 5;
}

.wl-launch__option {
  display: block;
  padding: 8px;
  border-radius: 4px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.2;
  color: #535862;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease;
}

.wl-launch__option--hover,
.wl-launch__option--active {
  background: #e5e7eb;
  color: #252b37;
}

.wl-launch__stats {
  display: flex;
  gap: 20px;
  width: 100%;
}

.wl-launch__stat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 13px;
  box-sizing: border-box;
  border: 1.1px solid #e5e7eb;
  border-radius: 9px;
  background: #fafbfa;
  min-width: 0;
}

.wl-launch__stat-label {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  color: #535862;
  white-space: nowrap;
}

.wl-launch__stat-value {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
  transition: opacity 0.25s ease;
}

.wl-launch__stat-change {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 600;
  color: #2d6a4f;
  white-space: nowrap;
}

.wl-launch__chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.wl-launch__chart-title {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
}

.wl-launch__bars {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 36px;
  height: 67px;
  width: 100%;
  padding: 0 18px;
  box-sizing: border-box;
}

.wl-launch__bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 7px;
  height: 100%;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #535862;
  white-space: nowrap;
}

.wl-launch__bar {
  width: 16px;
  border-radius: 3.4px 3.4px 0 0;
  background: #2d6a4f;
  transition: height 0.55s cubic-bezier(0.45, 0, 0.2, 1);
}

.wl-launch__cursor {
  position: absolute;
  z-index: 8;
  width: 16px;
  height: 16px;
  margin-left: -2px;
  margin-top: -2px;
  pointer-events: none;
  transition:
    left 0.45s cubic-bezier(0.45, 0, 0.2, 1),
    top 0.45s cubic-bezier(0.45, 0, 0.2, 1),
    transform 0.12s ease;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.35));
}

.wl-launch__cursor img {
  display: block;
  width: 16px;
  height: 16px;
}

.wl-launch__cursor--click {
  transform: scale(0.82);
  transform-origin: 2px 2px;
}

.wl-launch__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid rgba(45, 106, 79, 0.85);
  animation: wl-launch-ring 0.28s ease-out forwards;
}

@keyframes wl-launch-ring {
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
  .wl-launch__cursor,
  .wl-launch__bar,
  .wl-launch__option,
  .wl-launch__dropdown img,
  .wl-launch__pulse {
    transition: none;
    animation: none;
  }
}
</style>
