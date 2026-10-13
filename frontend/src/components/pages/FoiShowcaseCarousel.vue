<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import * as FoiPayinFlowGraphic from "./FoiPayinFlowGraphic.vue";
import * as FoiPayoutFlowGraphic from "./FoiPayoutFlowGraphic.vue";
import * as FoiReconciliationFlowGraphic from "./FoiReconciliationFlowGraphic.vue";
import * as FoiVisibilityFlowGraphic from "./FoiVisibilityFlowGraphic.vue";

const props = defineProps({
  cards: { type: Array, default: () => [] },
  /** Start on this logical card index (Figma default: Collections = 1) */
  initialSlide: { type: Number, default: 1 },
  autoplayDelay: { type: Number, default: 5000 },
});

const TRANSITION_MS = 900;
/** Phones show every card stacked, so the carousel stops cycling there. */
const PHONE_QUERY = "(max-width: 767px)";

/**
 * Cards whose static image is replaced by an animated Figma graphic. Each
 * module exports LOOP_MS and PLAYBACK_MS; autoplay holds a card until its
 * play-through has finished.
 */
const ANIMATED_GRAPHICS = {
  collections: FoiPayinFlowGraphic,
  payout: FoiPayoutFlowGraphic,
  reconciliation: FoiReconciliationFlowGraphic,
  visibility: FoiVisibilityFlowGraphic,
};

const reduceMotion =
  typeof window !== "undefined" &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const slides = computed(() => props.cards || []);
const count = computed(() => slides.value.length);
const activeIndex = ref(0);
const hovered = ref(false);
const isPhone = ref(false);
let phoneMql = null;
/** Park unused cards on this side so the next enter is always a short slide */
const parkSide = ref("back-right");
const snapIds = ref(new Set());
/** Per-card remount counter; bumping it restarts that card's animation. */
const playRuns = ref({});
let playStartedAt = 0;
let timer = null;
let busy = false;
let settleTimer = null;

function clampInitial() {
  const n = count.value;
  if (!n) {
    activeIndex.value = 0;
    return;
  }
  activeIndex.value = Math.min(Math.max(props.initialSlide, 0), n - 1);
  parkSide.value = "back-right";
}

function stopAutoplay() {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
}

/**
 * Time until the centre card may move on: the end of its current animated
 * play-through, or the plain autoplay delay for static cards.
 */
function remainingHold() {
  const graphic = ANIMATED_GRAPHICS[slides.value[activeIndex.value]?.id];
  if (!graphic) return props.autoplayDelay;
  const { LOOP_MS, PLAYBACK_MS } = graphic;
  const elapsed = (performance.now() - playStartedAt) % LOOP_MS;
  return elapsed <= PLAYBACK_MS ? PLAYBACK_MS - elapsed : LOOP_MS - elapsed + PLAYBACK_MS;
}

function scheduleAdvance(delay) {
  stopAutoplay();
  if (reduceMotion || hovered.value || isPhone.value || count.value < 2) return;
  timer = window.setTimeout(() => {
    timer = null;
    if (busy) scheduleAdvance(TRANSITION_MS);
    else next();
  }, delay);
}

function startAutoplay() {
  scheduleAdvance(remainingHold());
}

/** Restart the centre card's animation so it always plays from the top. */
function replayCenter() {
  const key = activeIndex.value;
  playRuns.value = { ...playRuns.value, [key]: (playRuns.value[key] || 0) + 1 };
  playStartedAt = performance.now();
}

function slotFor(index) {
  const n = count.value;
  if (!n) return "back-right";
  const rel = ((index - activeIndex.value) % n + n) % n;
  if (rel === 0) return "center";
  if (rel === 1) return "right";
  if (rel === n - 1) return "left";
  return parkSide.value;
}

function wait(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

/**
 * After a move finishes, silently move invisible parked cards to the
 * entry side for the next autoplay step — never mid-animation.
 */
async function reparkSilent(nextPark) {
  if (count.value <= 3) {
    parkSide.value = nextPark;
    return;
  }

  const parked = [];
  for (let i = 0; i < count.value; i += 1) {
    const rel = ((i - activeIndex.value) % count.value + count.value) % count.value;
    if (rel > 1 && rel < count.value - 1) parked.push(i);
  }
  if (!parked.length) {
    parkSide.value = nextPark;
    return;
  }

  snapIds.value = new Set(parked);
  parkSide.value = nextPark;
  await nextTick();
  void document.body.offsetHeight;
  await nextTick();
  snapIds.value = new Set();
}

async function advance(dir) {
  const n = count.value;
  if (n < 2 || busy) return;
  busy = true;

  // Ensure parked cards sit on the entry side BEFORE we animate (already there
  // after previous repark; on first move from mount they're at back-right).
  if (dir === 1 && parkSide.value !== "back-right" && n > 3) {
    await reparkSilent("back-right");
  } else if (dir === -1 && parkSide.value !== "back-left" && n > 3) {
    await reparkSilent("back-left");
  }

  activeIndex.value = (activeIndex.value + dir + n) % n;

  const duration = reduceMotion ? 0 : TRANSITION_MS;
  if (settleTimer) clearTimeout(settleTimer);
  await wait(duration);

  // Prep entry side for the following move in the same direction
  await reparkSilent(dir === 1 ? "back-right" : "back-left");
  busy = false;
}

function next() {
  return advance(1);
}

function prev() {
  return advance(-1);
}

function onCenterEnter() {
  hovered.value = true;
  stopAutoplay();
}

function onCenterLeave() {
  hovered.value = false;
  startAutoplay();
}

function onPhoneChange(e) {
  isPhone.value = e.matches;
  startAutoplay();
}

onMounted(() => {
  playStartedAt = performance.now();
  phoneMql = window.matchMedia(PHONE_QUERY);
  isPhone.value = phoneMql.matches;
  phoneMql.addEventListener("change", onPhoneChange);
  clampInitial();
  startAutoplay();
});

watch(activeIndex, () => {
  replayCenter();
  startAutoplay();
});

watch(count, () => {
  clampInitial();
  startAutoplay();
});

watch(
  () => props.autoplayDelay,
  () => startAutoplay(),
);

onBeforeUnmount(() => {
  phoneMql?.removeEventListener("change", onPhoneChange);
  stopAutoplay();
  if (settleTimer) clearTimeout(settleTimer);
});
</script>

<template>
  <div
    class="foi-coverflow"
    :class="{ 'foi-coverflow--static': reduceMotion }"
  >
    <div class="foi-coverflow__stage" aria-live="polite">
      <button
        v-if="count > 1"
        type="button"
        class="foi-coverflow__nav foi-coverflow__nav--prev"
        aria-label="Previous card"
        @click="prev()"
      >
        <span aria-hidden="true">‹</span>
      </button>

      <article
        v-for="(card, index) in slides"
        :key="card.id || card.title"
        class="foi-coverflow__card"
        :class="[
          `foi-coverflow__card--${slotFor(index)}`,
          { 'foi-coverflow__card--snap': snapIds.has(index) },
        ]"
        :data-card="card.id"
        :aria-hidden="!isPhone && slotFor(index) !== 'center'"
      >
        <component
          :is="ANIMATED_GRAPHICS[card.id].default"
          v-if="ANIMATED_GRAPHICS[card.id]"
          :key="playRuns[index] || 0"
          :alt="card.image_alt || card.title"
        />
        <img
          v-else
          class="foi-coverflow__img"
          :src="card.image"
          :alt="card.image_alt || card.title"
          :width="card.image_width || 576"
          :height="card.image_height || 505"
          decoding="async"
          loading="lazy"
          draggable="false"
        />
      </article>

      <div
        class="foi-coverflow__hover-zone"
        aria-hidden="true"
        @mouseenter="onCenterEnter"
        @mouseleave="onCenterLeave"
      />

      <button
        v-if="count > 1"
        type="button"
        class="foi-coverflow__nav foi-coverflow__nav--next"
        aria-label="Next card"
        @click="next()"
      >
        <span aria-hidden="true">›</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.foi-coverflow {
  width: 100%;
  --foi-teal: #097495;
  /* Smooth decelerate — no snap feeling */
  --foi-ease: cubic-bezier(0.16, 1, 0.3, 1);
  --foi-dur: 0.9s;
  --foi-card-w: min(576px, 52vw);
  --foi-card-h: 505px;
  padding: 0;
}

.foi-coverflow__stage {
  position: relative;
  width: 100%;
  height: var(--foi-card-h);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}

.foi-coverflow__card {
  position: absolute;
  top: 50%;
  left: 50%;
  width: var(--foi-card-w);
  height: var(--foi-card-h);
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  border: 1px solid #d5d7da;
  border-radius: 32px;
  background: #fafafa;
  overflow: hidden;
  box-shadow:
    0 4px 16px rgba(15, 23, 42, 0.06),
    0 12px 32px rgba(15, 23, 42, 0.08);
  transform-origin: center center;
  transition:
    transform var(--foi-dur) var(--foi-ease),
    opacity var(--foi-dur) var(--foi-ease),
    box-shadow var(--foi-dur) var(--foi-ease);
  will-change: transform, opacity;
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
}

.foi-coverflow__card--snap {
  transition: none !important;
}

.foi-coverflow__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  user-select: none;
  -webkit-user-drag: none;
}

.foi-coverflow__card--center {
  z-index: 3;
  opacity: 1;
  box-shadow:
    0 8px 24px rgba(15, 23, 42, 0.08),
    0 20px 48px rgba(15, 23, 42, 0.1);
  transform: translate3d(-50%, -50%, 0) scale(1);
}

/* Softer side offset — shorter travel = smoother feel */
.foi-coverflow__card--left {
  z-index: 2;
  opacity: 0.96;
  transform: translate3d(-50%, -50%, 0) translate3d(-36%, 0, 0) scale(0.68);
}

.foi-coverflow__card--right {
  z-index: 2;
  opacity: 0.96;
  transform: translate3d(-50%, -50%, 0) translate3d(36%, 0, 0) scale(0.68);
}

.foi-coverflow__card--back-left {
  z-index: 1;
  opacity: 0;
  pointer-events: none;
  box-shadow: none;
  transform: translate3d(-50%, -50%, 0) translate3d(-62%, 0, 0) scale(0.58);
}

.foi-coverflow__card--back-right {
  z-index: 1;
  opacity: 0;
  pointer-events: none;
  box-shadow: none;
  transform: translate3d(-50%, -50%, 0) translate3d(62%, 0, 0) scale(0.58);
}

.foi-coverflow__hover-zone {
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 4;
  width: var(--foi-card-w);
  height: var(--foi-card-h);
  transform: translate(-50%, -50%);
  cursor: default;
}

.foi-coverflow__nav {
  position: absolute;
  top: 50%;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 1px solid #e4e7ec;
  border-radius: 50%;
  background: #fff;
  color: var(--foi-teal);
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
  transform: translateY(-50%);
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.foi-coverflow__nav:hover {
  background: #f8fafc;
  border-color: var(--foi-teal);
  box-shadow: 0 8px 22px rgba(9, 116, 149, 0.12);
}

.foi-coverflow__nav:focus-visible {
  outline: 2px solid var(--foi-teal);
  outline-offset: 2px;
}

.foi-coverflow__nav--prev {
  left: 0;
}

.foi-coverflow__nav--next {
  right: 0;
}

.foi-coverflow__nav span {
  display: block;
  margin-top: -2px;
}

.foi-coverflow--static .foi-coverflow__card {
  transition: none;
}

@media (max-width: 900px) {
  .foi-coverflow {
    --foi-card-w: min(420px, 86vw);
    --foi-card-h: min(420px, 72vw);
  }

  .foi-coverflow__card--left {
    transform: translate3d(-50%, -50%, 0) translate3d(-44%, 0, 0) scale(0.58);
  }

  .foi-coverflow__card--right {
    transform: translate3d(-50%, -50%, 0) translate3d(44%, 0, 0) scale(0.58);
  }

  .foi-coverflow__nav {
    width: 36px;
    height: 36px;
    font-size: 24px;
  }

  .foi-coverflow__nav--prev {
    left: 4px;
  }

  .foi-coverflow__nav--next {
    right: 4px;
  }
}

@media (max-width: 767px) {
  .foi-coverflow__stage {
    height: auto;
    flex-direction: column;
    align-items: stretch;
    gap: 24px;
  }

  .foi-coverflow__stage .foi-coverflow__card {
    position: relative;
    top: auto;
    left: auto;
    z-index: auto;
    width: 100%;
    height: auto;
    aspect-ratio: 361 / 322;
    border-radius: 20px;
    opacity: 1;
    pointer-events: auto;
    box-shadow: none;
    transform: none;
    transition: none;
  }

  .foi-coverflow__card[data-card="collections"] {
    order: 1;
  }

  .foi-coverflow__card[data-card="payout"] {
    order: 2;
  }

  .foi-coverflow__card[data-card="visibility"] {
    order: 3;
  }

  .foi-coverflow__card[data-card="reconciliation"] {
    order: 4;
  }

  .foi-coverflow__nav,
  .foi-coverflow__hover-zone {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-coverflow__card {
    transition: none;
  }
}
</style>
