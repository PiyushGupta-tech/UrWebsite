<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Parent and child MID hierarchy with transaction volume drill-down",
  },
});

/**
 * Figma 722:7877 — Transaction Volume period storyboard.
 * Cursor opens the period dropdown and cycles report values.
 * Hierarchy backdrop: cascading-graphic.svg (static card covered by live card).
 */
const ASSET = "/images/figma-unified-dashboard/features/cascading";
const ART_W = 709;
const ART_H = 357;

const MENU = ["Last 15 Days", "Last Week", "Yesterday", "Last 30 Days"];

const PERIODS = {
  "Last 30 Days": [
    { id: "parent", label: "Parent MID (MID001)", icon: "building.svg", tone: "blue", value: "₹24.8M", change: "12%" },
    { id: "c1", label: "MID001-01", icon: "bag-blue.svg", tone: "blue", value: "₹8.4M", change: "10%" },
    { id: "c2", label: "MID001-02", icon: "bag-green.svg", tone: "green", value: "₹10.2M", change: "16%" },
    { id: "c3", label: "MID001-03", icon: "bag-purple.svg", tone: "purple", value: "₹6.1M", change: "9%" },
  ],
  "Last 15 Days": [
    { id: "parent", label: "Parent MID (MID001)", icon: "building.svg", tone: "blue", value: "₹22.8M", change: "11.1%" },
    { id: "c1", label: "MID001-01", icon: "bag-blue.svg", tone: "blue", value: "₹9.6M", change: "12%" },
    { id: "c2", label: "MID001-02", icon: "bag-green.svg", tone: "green", value: "₹7.8M", change: "8%" },
    { id: "c3", label: "MID001-03", icon: "bag-purple.svg", tone: "purple", value: "₹5.4M", change: "14%" },
  ],
  "Last Week": [
    { id: "parent", label: "Parent MID (MID001)", icon: "building.svg", tone: "blue", value: "₹3.40M", change: "7.9%" },
    { id: "c1", label: "MID001-01", icon: "bag-blue.svg", tone: "blue", value: "₹1.42M", change: "7%" },
    { id: "c2", label: "MID001-02", icon: "bag-green.svg", tone: "green", value: "₹1.16M", change: "11%" },
    { id: "c3", label: "MID001-03", icon: "bag-purple.svg", tone: "purple", value: "₹0.82M", change: "5%" },
  ],
  Yesterday: [
    { id: "parent", label: "Parent MID (MID001)", icon: "building.svg", tone: "blue", value: "₹12.30M", change: "9.9%" },
    { id: "c1", label: "MID001-01", icon: "bag-blue.svg", tone: "blue", value: "₹5.10M", change: "9%" },
    { id: "c2", label: "MID001-02", icon: "bag-green.svg", tone: "green", value: "₹4.20M", change: "13%" },
    { id: "c3", label: "MID001-03", icon: "bag-purple.svg", tone: "purple", value: "₹3.00M", change: "7%" },
  ],
};

const reduceMotion = ref(false);
const selected = ref("Last 30 Days");
const menuOpen = ref(false);
const hoverOption = ref("");
const clicking = ref(false);
const valuesFlash = ref(false);
const cursor = reactive({ x: 640, y: 90 });

const rootRef = ref(null);
const dropdownRef = ref(null);
const optionRefs = ref([]);

const rows = computed(() => PERIODS[selected.value] || PERIODS["Last 30 Days"]);

let timers = [];
let loopTimer = null;

function setOptionRef(el, i) {
  if (el) optionRefs.value[i] = el;
}

function aimAt(el) {
  const root = rootRef.value;
  if (!root || !el) return;
  const rBox = root.getBoundingClientRect();
  const tBox = el.getBoundingClientRect();
  const sx = rBox.width / ART_W;
  const sy = rBox.height / ART_H;
  cursor.x = (tBox.left + tBox.width / 2 - rBox.left) / sx;
  cursor.y = (tBox.top + tBox.height / 2 - rBox.top) / sy;
}

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
  await wait(280);
  clicking.value = true;
  await wait(holdMs);
  clicking.value = false;
  await wait(90);
}

function applyPeriod(label) {
  selected.value = label;
  menuOpen.value = false;
  hoverOption.value = "";
  valuesFlash.value = true;
  timers.push(
    setTimeout(() => {
      valuesFlash.value = false;
    }, 420),
  );
}

async function pickOption(index, label) {
  await clickEl(dropdownRef.value);
  menuOpen.value = true;
  await nextTick();
  await wait(220);
  const opt = optionRefs.value[index];
  aimAt(opt);
  hoverOption.value = label;
  await wait(380);
  await clickEl(opt, 170);
  applyPeriod(label);
  await wait(1100);
}

async function runSequence() {
  if (reduceMotion.value) return;
  clearTimers();
  selected.value = "Last 30 Days";
  menuOpen.value = false;
  hoverOption.value = "";
  valuesFlash.value = false;
  await nextTick();

  // Frame 1→2→3: open menu, pick Last 15 Days
  await pickOption(0, "Last 15 Days");
  // Frame 4: Last Week
  await pickOption(1, "Last Week");
  // Frame 5: Yesterday
  await pickOption(2, "Yesterday");
  // Return to Last 30 Days
  await pickOption(3, "Last 30 Days");
  await wait(600);

  loopTimer = setTimeout(() => runSequence(), 350);
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  nextTick(() => {
    if (!reduceMotion.value) runSequence();
    else selected.value = "Last 30 Days";
  });
});

onBeforeUnmount(clearTimers);
</script>

<template>
  <div
    ref="rootRef"
    class="ud-casc"
    :class="{ 'ud-casc--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="ud-casc__backdrop"
      src="/images/figma-unified-dashboard/features/cascading-graphic.svg"
      alt=""
      width="709"
      height="357"
      decoding="async"
    />

    <!-- Live Transaction Volume card — covers static card in backdrop -->
    <article class="ud-casc__card" aria-hidden="true">
      <div class="ud-casc__header">
        <p class="ud-casc__title">Transaction Volume</p>
        <button
          ref="dropdownRef"
          type="button"
          class="ud-casc__dropdown"
          tabindex="-1"
        >
          <span>{{ selected }}</span>
          <img :src="`${ASSET}/chevron.svg`" alt="" width="12" height="12" />
        </button>
      </div>

      <div
        v-show="menuOpen"
        class="ud-casc__menu"
      >
        <div
          v-for="(opt, i) in MENU"
          :key="opt"
          :ref="(el) => setOptionRef(el, i)"
          class="ud-casc__menu-item"
          :class="{ 'ud-casc__menu-item--hover': hoverOption === opt }"
        >
          {{ opt }}
        </div>
      </div>

      <div class="ud-casc__rows" :class="{ 'ud-casc__rows--flash': valuesFlash }">
        <div
          v-for="row in rows"
          :key="row.id"
          class="ud-casc__row"
        >
          <div class="ud-casc__row-left">
            <span
              class="ud-casc__icon"
              :class="`ud-casc__icon--${row.tone}`"
            >
              <img :src="`${ASSET}/${row.icon}`" alt="" width="12" height="12" />
            </span>
            <span
              class="ud-casc__label"
              :class="{ 'ud-casc__label--strong': row.id === 'parent' }"
            >
              {{ row.label }}
            </span>
          </div>
          <div class="ud-casc__row-right">
            <span class="ud-casc__value">{{ row.value }}</span>
            <span class="ud-casc__change">
              <img :src="`${ASSET}/arrow-up.svg`" alt="" width="8" height="8" />
              {{ row.change }}
            </span>
          </div>
        </div>
      </div>

      <div class="ud-casc__banner">
        <span class="ud-casc__banner-icon">
          <img :src="`${ASSET}/eye.svg`" alt="" width="12" height="12" />
        </span>
        <p>Drill down from parent to merchant in seconds.</p>
      </div>
    </article>

    <div
      v-show="!reduceMotion"
      class="ud-casc__cursor"
      :class="{ 'ud-casc__cursor--click': clicking }"
      :style="{ left: `${cursor.x}px`, top: `${cursor.y}px` }"
    >
      <img :src="`${ASSET}/cursor.svg`" alt="" width="18" height="18" />
      <span v-show="clicking" class="ud-casc__click-ring" />
    </div>
  </div>
</template>

<style scoped>
.ud-casc {
  position: relative;
  width: 100%;
  aspect-ratio: 709 / 357;
  overflow: visible;
  line-height: normal;
  background: transparent;
  container-type: size;
}

.ud-casc__backdrop {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  pointer-events: none;
  user-select: none;
}

/* Exact cover of baked-in card in cascading-graphic.svg (rect 399 78.36 307×274.78) */
.ud-casc__card {
  position: absolute;
  left: calc(399 / 709 * 100%);
  top: calc(78.36 / 357 * 100%);
  width: calc(307 / 709 * 100%);
  height: calc(274.78 / 357 * 100%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  padding: 20px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  box-shadow:
    0 1px 2px rgba(16, 24, 40, 0.06),
    0 4px 12px rgba(16, 24, 40, 0.08);
}

.ud-casc__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}

.ud-casc__title {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(10px, 3.4cqw, 12px);
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
}

.ud-casc__dropdown {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border: 0.8px solid #e2e8f0;
  border-radius: 2px;
  background: #ffffff;
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(7px, 2.3cqw, 8px);
  font-weight: 600;
  color: #535862;
  white-space: nowrap;
  cursor: default;
  pointer-events: none;
}

.ud-casc__dropdown img {
  display: block;
  width: 12px;
  height: 12px;
}

.ud-casc__menu {
  position: absolute;
  top: 48px;
  right: 20px;
  z-index: 4;
  width: 80px;
  padding: 6px;
  box-sizing: border-box;
  border: 1px solid #e2e8f0;
  border-radius: 2px;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(16, 24, 40, 0.08);
}

.ud-casc__menu-item {
  padding: 4px;
  border-radius: 2px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(7px, 2.3cqw, 8px);
  font-weight: 600;
  color: #535862;
  white-space: nowrap;
}

.ud-casc__menu-item--hover {
  background: rgba(83, 88, 98, 0.1);
}

.ud-casc__rows {
  display: flex;
  flex-direction: column;
  gap: 13px;
  flex: 1;
  min-height: 0;
  margin-top: 18px;
  transition: opacity 0.25s ease;
}

.ud-casc__rows--flash {
  animation: ud-casc-flash 0.42s ease;
}

.ud-casc__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.ud-casc__row-left,
.ud-casc__row-right {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.ud-casc__row-right {
  flex-shrink: 0;
}

.ud-casc__icon {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 2px;
  flex-shrink: 0;
}

.ud-casc__icon--blue {
  background: #eef4ff;
}
.ud-casc__icon--green {
  background: #e6fbf3;
}
.ud-casc__icon--purple {
  background: #f5f3ff;
}

.ud-casc__icon img {
  display: block;
  width: 12px;
  height: 12px;
}

.ud-casc__label {
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(8px, 2.8cqw, 10px);
  font-weight: 500;
  color: #535862;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ud-casc__label--strong {
  font-weight: 600;
  color: #252b37;
}

.ud-casc__value {
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(8px, 2.8cqw, 10px);
  font-weight: 700;
  color: #252b37;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.ud-casc__change {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(8px, 2.8cqw, 10px);
  font-weight: 600;
  color: #00c286;
  white-space: nowrap;
}

.ud-casc__change img {
  display: block;
  width: 8px;
  height: 8px;
}

.ud-casc__banner {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-top: auto;
  padding: 10px 12px;
  border-radius: 8px;
  background: rgba(9, 116, 149, 0.1);
}

.ud-casc__banner-icon {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(9, 116, 149, 0.1);
  flex-shrink: 0;
}

.ud-casc__banner-icon img {
  display: block;
  width: 12px;
  height: 12px;
}

.ud-casc__banner p {
  margin: 0;
  font-family: Manrope, system-ui, sans-serif;
  font-size: clamp(8px, 2.8cqw, 10px);
  font-weight: 600;
  line-height: 1.4;
  color: #097495;
}

.ud-casc__cursor {
  position: absolute;
  z-index: 5;
  width: 18px;
  height: 18px;
  margin-left: -2px;
  margin-top: -2px;
  pointer-events: none;
  transition:
    left 0.32s ease-in-out,
    top 0.32s ease-in-out;
}

.ud-casc__cursor img {
  display: block;
  width: 18px;
  height: 18px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.25));
}

.ud-casc__cursor--click {
  transform: scale(0.88);
}

.ud-casc__click-ring {
  position: absolute;
  left: 0;
  top: 0;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(9, 116, 149, 0.45);
  border-radius: 50%;
  animation: ud-casc-ring 0.28s ease-out;
}

@keyframes ud-casc-flash {
  0% {
    opacity: 0.35;
  }
  100% {
    opacity: 1;
  }
}

@keyframes ud-casc-ring {
  from {
    transform: scale(0.6);
    opacity: 0.8;
  }
  to {
    transform: scale(1.6);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ud-casc__cursor,
  .ud-casc__rows--flash {
    animation: none !important;
    transition: none !important;
  }
}
</style>
