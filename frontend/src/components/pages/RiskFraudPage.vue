<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import RfDetectIpGraphic from "./RfDetectIpGraphic.vue";
import RfDetectLocationsGraphic from "./RfDetectLocationsGraphic.vue";
import RfDetectPatternsGraphic from "./RfDetectPatternsGraphic.vue";
import RfDetectTransactionsGraphic from "./RfDetectTransactionsGraphic.vue";
import RfSecureDiagram from "./RfSecureDiagram.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const SAFER_INTERVAL = 3500;
const SAFER_HEIGHT = 307;
const SAFER_NUM_SIZE = 55;
const SAFER_NUM_GAP = 16;
const SAFER_TEXT_WIDTH = 492;
const SAFER_NUM_TOP_FALLBACK = 46.5;

const heroReady = ref(false);
const saferReady = ref(false);
const saferActive = ref(0);
const saferPaused = ref(false);
const saferReduceMotion = ref(false);
const saferInteracted = ref(false);
const saferRowRef = ref(null);
/** Per-step landing Y — measured at final text width so it never re-settles mid-expand */
const saferNumTops = ref([]);
let saferTimer = null;

const growthCards = computed(() => props.page?.growth?.cards || []);
const detectCards = computed(() => props.page?.detect?.cards || []);
/** Detect-card images replaced by an animated inline version of the same artwork. */
const DETECT_GRAPHICS = {
  "/images/figma-risk-fraud/illustration-container.svg": RfDetectIpGraphic,
  "/images/figma-risk-fraud/Frame%202147226663.svg": RfDetectPatternsGraphic,
  "/images/figma-risk-fraud/Frame%202147226808.svg": RfDetectTransactionsGraphic,
  "/images/figma-risk-fraud/Frame%202147226810.svg": RfDetectLocationsGraphic,
};
const saferItems = computed(() => {
  const items = props.page?.safer?.items || [];
  return items.map((item) => ({
    ...item,
    num: item.num || item.number,
  }));
});
const saferOthers = computed(() => Math.max(saferItems.value.length - 1, 0));

function stopSaferCycle() {
  if (saferTimer) clearInterval(saferTimer);
  saferTimer = null;
}

function startSaferCycle() {
  stopSaferCycle();
  if (
    saferReduceMotion.value ||
    saferPaused.value ||
    saferInteracted.value ||
    saferItems.value.length < 2
  ) {
    return;
  }
  saferTimer = window.setInterval(() => {
    const next = (saferActive.value + 1) % saferItems.value.length;
    ensureSaferNumTop(next);
    saferActive.value = next;
  }, SAFER_INTERVAL);
}

function numTopFor(index) {
  return saferNumTops.value[index] ?? SAFER_NUM_TOP_FALLBACK;
}

/**
 * Measure title+body at the expanded 492px width so wrapping (and thus
 * vertical center) matches the final card — never the collapsed pill width.
 */
function measureStepTextHeight(textEl) {
  if (!textEl) return 0;
  const style = textEl.style;
  const prev = {
    width: style.width,
    maxWidth: style.maxWidth,
    position: style.position,
    visibility: style.visibility,
    height: style.height,
    display: style.display,
    opacity: style.opacity,
    transform: style.transform,
    pointerEvents: style.pointerEvents,
  };
  style.width = `${SAFER_TEXT_WIDTH}px`;
  style.maxWidth = `${SAFER_TEXT_WIDTH}px`;
  style.position = "absolute";
  style.left = "0";
  style.top = "0";
  style.visibility = "hidden";
  style.height = "auto";
  style.display = "flex";
  style.opacity = "1";
  style.transform = "none";
  style.pointerEvents = "none";
  const height = textEl.offsetHeight;
  style.width = prev.width;
  style.maxWidth = prev.maxWidth;
  style.position = prev.position;
  style.left = "";
  style.top = "";
  style.visibility = prev.visibility;
  style.height = prev.height;
  style.display = prev.display;
  style.opacity = prev.opacity;
  style.transform = prev.transform;
  style.pointerEvents = prev.pointerEvents;
  return height;
}

/** Final Y for the number so num + text sit vertically centered after expand. */
function ensureSaferNumTop(index) {
  if (saferNumTops.value[index] != null) return saferNumTops.value[index];

  const row = saferRowRef.value;
  if (!row || typeof window === "undefined") return SAFER_NUM_TOP_FALLBACK;
  if (window.matchMedia("(max-width: 1200px)").matches) return SAFER_NUM_TOP_FALLBACK;

  const step = row.querySelectorAll(".rf-safer__step")[index];
  const text = step?.querySelector(".rf-safer__step-text");
  const textH = measureStepTextHeight(text);
  if (!textH) return SAFER_NUM_TOP_FALLBACK;

  const contentH = SAFER_NUM_SIZE + SAFER_NUM_GAP + textH;
  const top = Math.max(20, (SAFER_HEIGHT - contentH) / 2);
  const rounded = Math.round(top * 10) / 10;
  const next = saferNumTops.value.slice();
  next[index] = rounded;
  saferNumTops.value = next;
  return rounded;
}

function syncAllSaferNumTops() {
  // Clear cache so resize/font changes remeasure at final width
  saferNumTops.value = [];
  for (let i = 0; i < saferItems.value.length; i += 1) {
    ensureSaferNumTop(i);
  }
}

function selectSafer(index, { fromUser = true } = {}) {
  if (fromUser) {
    saferInteracted.value = true;
    stopSaferCycle();
  }
  // Lock landing Y before morph — no post-expand correction/settle
  ensureSaferNumTop(index);
  saferActive.value = index;
  if (!fromUser) startSaferCycle();
}

function pauseSafer() {
  saferPaused.value = true;
  stopSaferCycle();
}

function resumeSafer() {
  saferPaused.value = false;
  if (!saferInteracted.value) startSaferCycle();
}

function onSaferHover(index) {
  if (saferReduceMotion.value) return;
  if (!saferInteracted.value && index === 0 && saferActive.value === 0) return;
  selectSafer(index, { fromUser: true });
}

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
    saferReady.value = true;
    syncAllSaferNumTops();
  });
  // Fonts can change text wrap — remeasure once ready
  if (typeof document !== "undefined" && document.fonts?.ready) {
    document.fonts.ready.then(() => syncAllSaferNumTops()).catch(() => {});
  }
  saferReduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startSaferCycle();
  window.addEventListener("resize", syncAllSaferNumTops);
});

onBeforeUnmount(() => {
  stopSaferCycle();
  if (typeof window !== "undefined") {
    window.removeEventListener("resize", syncAllSaferNumTops);
  }
});

watch(saferItems, async () => {
  await nextTick();
  if (!saferInteracted.value) startSaferCycle();
  syncAllSaferNumTops();
});
</script>

<template>
  <main class="rf-page">
    <!-- Hero — Figma 466:32442 (1440×865) -->
    <section class="rf-hero" :class="{ 'rf-hero--ready': heroReady }">
      <div class="rf-hero__bg" aria-hidden="true">
        <img
          class="rf-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="rf-hero__inner">
        <div class="rf-hero__copy">
          <p v-if="page.eyebrow" class="rf-hero__eyebrow">{{ page.eyebrow }}</p>
          <h1 class="rf-hero__title">{{ page.title }}</h1>
          <p class="rf-hero__intro">{{ page.intro }}</p>
          <RouterLink to="/contact" class="rf-hero__cta">
            <span>{{ page.cta_label || "Talk to Expert" }}</span>
            <img
              src="/images/figma-contact/nav-arrow.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
        </div>

        <div class="rf-hero__visual">
          <img
            class="rf-hero__graphic"
            src="/images/figma-risk-fraud/Frame%202147226977.svg?v=2"
            :alt="page.hero_image_alt || page.title"
            width="612"
            height="463"
            decoding="async"
          />
        </div>
      </div>
    </section>

    <!-- Secure — Figma 466:32438 + 466:32441 -->
    <section v-if="page.secure" class="rf-section rf-section--secure">
      <div class="rf-section__head rf-section__head--secure">
        <h2 class="rf-section__title rf-section__title--secure">
          {{ page.secure.title }}
        </h2>
        <p class="rf-section__body rf-section__body--secure">
          {{ page.secure.body }}
        </p>
      </div>
      <RfSecureDiagram
        :image="page.secure.image"
        :alt="page.secure.image_alt || page.secure.title"
      />
    </section>

    <!-- Growth — Figma 538:5121 cards (682×550, 2×2) -->
    <section v-if="page.growth" class="rf-section rf-section--growth">
      <div class="rf-growth">
        <div class="rf-growth__copy">
          <h2 class="rf-growth__title">{{ page.growth.title }}</h2>
          <p class="rf-growth__body">{{ page.growth.body }}</p>
        </div>

        <div class="rf-growth__cards" aria-label="Risk growth capabilities">
          <article
            v-for="card in growthCards"
            :key="card.title"
            class="rf-growth__card"
          >
            <div class="rf-growth__icon" aria-hidden="true">
              <img
                :src="card.icon"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
            </div>
            <h3 class="rf-growth__card-title">{{ card.title }}</h3>
            <p class="rf-growth__card-body">{{ card.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Detect — Figma 466:32789 (1052 × 1236) -->
    <section v-if="page.detect" class="rf-section rf-section--detect">
      <div class="rf-section__head rf-section__head--detect">
        <h2 class="rf-section__title rf-section__title--detect">
          {{ page.detect.title }}
        </h2>
        <p class="rf-section__body rf-section__body--detect">
          {{ page.detect.body }}
        </p>
      </div>
      <div class="rf-detect" aria-label="Risk detection capabilities">
        <article
          v-for="card in detectCards"
          :key="card.title"
          class="rf-detect__card"
        >
          <div class="rf-detect__visual">
            <component
              :is="DETECT_GRAPHICS[card.image]"
              v-if="DETECT_GRAPHICS[card.image]"
              class="rf-detect__img"
            />
            <img
              v-else
              class="rf-detect__img"
              :src="card.image"
              alt=""
              :width="card.image_width || 466"
              :height="card.image_height || 373"
              decoding="async"
              loading="lazy"
            />
          </div>
          <div class="rf-detect__text">
            <h3 class="rf-detect__title">{{ card.title }}</h3>
            <p class="rf-detect__body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Safer — matches Orchestration po-control accordion (1074×307) -->
    <section
      v-if="page.safer"
      class="rf-safer"
      :class="{ 'rf-safer--ready': saferReady }"
      :style="{ '--rf-safer-others': String(saferOthers) }"
      @mouseenter="pauseSafer"
      @mouseleave="resumeSafer"
      @focusin="pauseSafer"
      @focusout="resumeSafer"
    >
      <div class="rf-safer__head">
        <h2 class="rf-safer__heading">{{ page.safer.title }}</h2>
        <p class="rf-safer__intro">{{ page.safer.body }}</p>
      </div>
      <div
        ref="saferRowRef"
        class="rf-safer__row"
        role="tablist"
        aria-label="Safer financial operations"
      >
        <button
          v-for="(step, index) in saferItems"
          :key="step.num"
          type="button"
          class="rf-safer__step"
          :class="{ 'rf-safer__step--active': saferActive === index }"
          :style="{ '--rf-num-top-expanded': `${numTopFor(index)}px` }"
          role="tab"
          :aria-selected="saferActive === index"
          :aria-label="`${step.num}. ${step.title}`"
          @click="selectSafer(index)"
          @mouseenter="onSaferHover(index)"
          @focus="onSaferHover(index)"
        >
          <!-- Absolute num rides left:50% as width morphs → diagonal travel -->
          <span class="rf-safer__num" aria-hidden="true">{{ step.num }}</span>
          <span class="rf-safer__cluster">
            <!-- Ghost slot keeps final vertical center stable during expand -->
            <span class="rf-safer__num-slot" aria-hidden="true" />
            <span class="rf-safer__step-text">
              <span class="rf-safer__step-title">{{ step.title }}</span>
              <span class="rf-safer__step-body">{{ step.body }}</span>
            </span>
          </span>
        </button>
      </div>
    </section>
  </main>
</template>

<style scoped>
.rf-page {
  width: 100%;
  background: #ffffff;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #1e2a3b;
}

/* —— Hero — Figma 466:32442 —— */
.rf-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  min-height: 100svh;
  box-sizing: border-box;
  overflow: hidden;
  background: #ffffff;
}

.rf-hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.rf-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.rf-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  /*
   Figma 466:32465 / 466:32475:
   copy @ x=105 w=516 · graphic @ x=660 w=705.87
   → left 105, right ~74, gap 39
  */
  min-height: calc(100svh - var(--page-nav-offset, 129px));
  padding: 0 74px 0 105px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 516fr) minmax(0, 706fr);
  column-gap: 39px;
  align-items: center;
}

.rf-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: center;
  max-width: 516px;
  width: 100%;
  transform: translateY(calc(var(--page-nav-offset, 129px) / -2));
  opacity: 0;
  transition: opacity 0.6s ease;
}

.rf-hero--ready .rf-hero__copy {
  opacity: 1;
}

.rf-hero__eyebrow {
  margin: 0 0 18px;
  display: inline-flex;
  align-items: center;
  padding: 9px 17px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  background: transparent;
  color: #0292b8;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.78px;
  line-height: 20px;
  text-transform: uppercase;
}

.rf-hero__title {
  margin: 0 0 12px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
  text-transform: capitalize;
}

.rf-hero__intro {
  margin: 0 0 40px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.56px;
  color: #535862;
}

.rf-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  box-sizing: border-box;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.rf-hero__cta:hover {
  background: #0a86ad;
}

.rf-hero__cta img {
  display: block;
}

.rf-hero__visual {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  align-self: stretch;
  min-width: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.rf-hero__graphic {
  display: block;
  width: 100%;
  max-width: 612px;
  height: auto;
  aspect-ratio: 612 / 463;
  object-fit: contain;
  object-position: center;
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.7s ease,
    transform 0.7s ease;
}

.rf-hero--ready .rf-hero__graphic {
  opacity: 1;
  transform: translateY(0);
}

/* —— Shared section —— */
.rf-section {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rf-section__head {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rf-section__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.rf-section__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* —— Secure — Figma 466:32438 (962) + 466:32441 (1291×841) —— */
.rf-section--secure {
  margin-top: 0;
  gap: 72px;
  padding-top: 0;
}

.rf-section__head--secure {
  width: min(962px, 100%);
  margin-top: 0;
  gap: 20px;
}

.rf-section__title--secure {
  max-width: 905px;
  margin-inline: auto;
}

/* —— Growth — Figma 538:5121 (cards 682×550, 2×2) —— */
.rf-section--growth {
  margin-top: 96px;
  padding: 0 24px;
  box-sizing: border-box;
  max-width: 1440px;
}

.rf-growth {
  /* copy ~544 + gap + cards 682 */
  width: min(1312px, 100%);
  margin-inline: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 86px;
}

.rf-growth__copy {
  width: 544px;
  max-width: 100%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}

.rf-growth__title {
  margin: 0;
  width: 100%;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.rf-growth__body {
  margin: 0;
  width: 100%;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.rf-growth__cards {
  width: 682px;
  flex-shrink: 0;
  display: grid;
  grid-template-columns: repeat(2, 329px);
  grid-template-rows: repeat(2, 263px);
  gap: 24px;
}

.rf-growth__card {
  width: 329px;
  height: 263px;
  padding: 32px 20px 20px;
  box-sizing: border-box;
  border-radius: 12px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
  gap: 12px;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.25s ease;
}

.rf-growth__card:hover {
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

.rf-growth__icon {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 13.284px;
  border-radius: 6.642px;
  background: #097495;
  flex-shrink: 0;
}

.rf-growth__icon img {
  display: block;
  width: 28px;
  height: 28px;
}

.rf-growth__card-title {
  margin: 0;
  width: 100%;
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  letter-spacing: 0.6px;
  color: #252b37;
}

.rf-growth__card-body {
  margin: 0;
  width: 100%;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.48px;
  color: #535862;
}

/* —— Detect — Figma 466:32789 / 466:32793 (1052 × 1056) —— */
.rf-section--detect {
  margin-top: 108px;
  gap: 56px; /* heading 124 + gap to grid = 180 → ~56 after head height */
}

.rf-section__head--detect {
  width: min(962px, 100%);
  gap: 20px; /* 76 - 56 = 20 */
}

.rf-section__title--detect {
  font-size: 42px;
  line-height: 56px;
  color: #252b37;
}

.rf-section__body--detect {
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.rf-detect {
  width: min(1052px, 100%);
  display: grid;
  grid-template-columns: repeat(2, 514px);
  gap: 24px;
  justify-content: center;
}

.rf-detect__card {
  width: 514px;
  min-height: 513px;
  margin: 0;
  padding: 24px;
  box-sizing: border-box;
  border: 1px solid #e9eaeb;
  border-radius: 12px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.rf-detect__visual {
  width: 466px;
  max-width: 100%;
  height: 373px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.rf-detect__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
}

.rf-detect__text {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.rf-detect__title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 32px;
  color: #252b37;
}

.rf-detect__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* —— Safer — matches Orchestration po-control (1074×307) —— */
.rf-safer {
  --rf-safer-inactive: 104px;
  --rf-safer-gap: 24px;
  --rf-safer-others: 3;
  --rf-safer-height: 307px;
  --rf-num-size: 55px;
  --rf-num-top-expanded: 46.5px;
  --rf-num-gap: 16px;
  --rf-active-inset: 20px;
  --rf-dur-in: 0.5s;
  --rf-dur-big: 1s;
  --rf-ease-out: cubic-bezier(0.6, 0.6, 0, 1);
  width: 100%;
  max-width: 1074px;
  margin: 100px auto 0;
  padding: 0 0 40px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 72px;
}

.rf-safer__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: min(788px, 100%);
  text-align: center;
}

.rf-safer__heading {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.rf-safer__intro {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.rf-safer__row {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: var(--rf-safer-gap);
  width: 100%;
  height: var(--rf-safer-height);
}

.rf-safer__step {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: var(--rf-safer-inactive);
  flex: 0 0 var(--rf-safer-inactive);
  height: 100%;
  padding: 24px;
  box-sizing: border-box;
  border: 0;
  border-radius: 48px;
  background: #f8fafc;
  color: #252b37;
  cursor: pointer;
  font: inherit;
  overflow: hidden;
  will-change: width, flex-basis, background;
  transition:
    background var(--rf-dur-in) ease,
    color var(--rf-dur-in) ease,
    border-radius var(--rf-dur-in) var(--rf-ease-out),
    padding var(--rf-dur-big) var(--rf-ease-out),
    width var(--rf-dur-big) var(--rf-ease-out),
    flex-basis var(--rf-dur-big) var(--rf-ease-out),
    box-shadow var(--rf-dur-in) ease;
}

.rf-safer:not(.rf-safer--ready) .rf-safer__step,
.rf-safer:not(.rf-safer--ready) .rf-safer__num {
  transition: none;
}

.rf-safer__step--active {
  width: calc(
    100% - ((var(--rf-safer-inactive) + var(--rf-safer-gap)) * var(--rf-safer-others))
  );
  flex-basis: calc(
    100% - ((var(--rf-safer-inactive) + var(--rf-safer-gap)) * var(--rf-safer-others))
  );
  min-width: 0;
  /* Flex-center the cluster so num+text share one stable vertical midpoint */
  justify-content: center;
  align-items: center;
  padding: var(--rf-active-inset);
  border-radius: 48px;
  background: #097495;
  color: #ffffff;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.1),
    0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

/*
 * Cluster = ghost num slot + text. Fixed 492px width matches Figma 434:2838
 * so wrap/height (and vertical center) stay stable while the card width morphs.
 */
.rf-safer__cluster {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--rf-num-gap);
  width: min(492px, 100%);
  max-width: 100%;
  min-height: 0;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  height: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
}

.rf-safer__step--active .rf-safer__cluster {
  height: auto;
  opacity: 1;
  overflow: visible;
  pointer-events: auto;
}

.rf-safer__num-slot {
  flex-shrink: 0;
  width: var(--rf-num-size);
  height: var(--rf-num-size);
  visibility: hidden;
  pointer-events: none;
}

/*
 * Number circle: absolute to the step so left:50% tracks the width morph (X)
 * while transform Y animates bottom → precomputed center top (diagonal).
 * --rf-num-top-expanded is locked before expand so nothing settles afterward.
 */
.rf-safer__num {
  position: absolute;
  left: 50%;
  z-index: 2;
  top: var(--rf-num-top-expanded);
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--rf-num-size);
  height: var(--rf-num-size);
  /* Inactive: sit at pill bottom. (height − padding − size) − top */
  transform: translate(
    -50%,
    calc(var(--rf-safer-height) - 24px - var(--rf-num-size) - var(--rf-num-top-expanded))
  );
  margin: 0;
  padding: 0;
  border: 0;
  border-radius: 32px;
  background: #00b7db;
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 32px;
  text-align: center;
  pointer-events: none;
  will-change: transform;
  transition:
    transform var(--rf-dur-big) var(--rf-ease-out),
    background var(--rf-dur-in) ease,
    color var(--rf-dur-in) ease,
    border-radius var(--rf-dur-in) var(--rf-ease-out);
}

.rf-safer__step:nth-child(even) .rf-safer__num {
  background: #0292b8;
}

.rf-safer__step--active .rf-safer__num {
  transform: translate(-50%, 0);
  background: #00b7db;
  color: #ffffff;
}

.rf-safer__step-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  width: 100%;
  max-width: 492px;
  text-align: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0s ease-in;
}

.rf-safer__step--active .rf-safer__step-text {
  opacity: 1;
  pointer-events: auto;
  /* Fade only — no translateY settle that reads as “falling into center” */
  transition: opacity var(--rf-dur-in) ease-in 0.35s;
}

.rf-safer__step-title {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  line-height: 42px;
  color: #fafafa;
  text-wrap: balance;
}

.rf-safer__step-body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #ffffff;
  max-width: 492px;
  text-wrap: balance;
}

@media (prefers-reduced-motion: reduce) {
  .rf-safer__step,
  .rf-safer__step-text,
  .rf-safer__num,
  .rf-safer__step--active .rf-safer__step-text {
    transition: none !important;
  }
}

@media (max-width: 1100px) {
  .rf-hero__inner {
    padding: 48px 40px 64px;
    grid-template-columns: 1fr;
    gap: 40px;
    min-height: auto;
  }

  .rf-hero__copy {
    transform: none;
    max-width: 640px;
  }

  .rf-hero__visual {
    justify-content: center;
  }

  .rf-growth {
    flex-direction: column;
    align-items: flex-start;
    gap: 48px;
  }

  .rf-growth__copy {
    width: 100%;
  }

  .rf-growth__cards {
    width: min(682px, 100%);
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-template-rows: none;
  }

  .rf-growth__card {
    width: 100%;
    height: auto;
    min-height: 263px;
  }

  .rf-detect {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    width: 100%;
  }

  .rf-detect__card {
    width: 100%;
    min-height: 0;
  }

  .rf-detect__visual {
    width: 100%;
    height: auto;
    aspect-ratio: 466 / 373;
  }
}

@media (max-width: 1200px) {
  .rf-safer {
    padding-left: 20px;
    padding-right: 20px;
  }

  .rf-safer__row {
    flex-direction: column;
    height: auto;
    min-height: 0;
    gap: 12px;
  }

  .rf-safer__step,
  .rf-safer__step--active {
    position: relative;
    width: 100% !important;
    flex: 0 0 auto !important;
    flex-basis: auto !important;
    height: auto;
    min-height: 0;
    border-radius: 28px;
    padding: 20px;
    will-change: auto;
  }

  .rf-safer__step {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
  }

  .rf-safer__cluster {
    position: static;
    height: auto !important;
    opacity: 1 !important;
    overflow: visible;
    margin-top: 0 !important;
    width: 100%;
    pointer-events: auto;
  }

  .rf-safer__num-slot {
    display: none;
  }

  .rf-safer__num {
    position: static !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    flex-shrink: 0;
    width: 55px;
    height: 55px;
    will-change: auto;
    transition: background var(--rf-dur-in) ease, color var(--rf-dur-in) ease;
  }

  .rf-safer__step--active .rf-safer__num {
    background: #00b7db;
    transform: none !important;
  }

  .rf-safer__step-text {
    opacity: 1 !important;
    transform: none !important;
    pointer-events: auto;
    width: 100%;
    padding: 0;
    gap: 8px;
    transition: none !important;
  }

  .rf-safer__step:not(.rf-safer__step--active) {
    min-height: 72px;
    padding: 12px 16px;
  }

  .rf-safer__step:not(.rf-safer__step--active) .rf-safer__cluster,
  .rf-safer__step:not(.rf-safer__step--active) .rf-safer__step-text {
    display: none;
  }

  .rf-safer__step--active {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }

  .rf-safer__step--active .rf-safer__cluster {
    width: min(492px, 100%);
  }

  .rf-safer__step--active .rf-safer__step-body {
    color: #ffffff;
  }
}

@media (max-width: 700px) {
  .rf-hero__inner {
    padding: 32px 20px 48px;
  }

  .rf-hero__title,
  .rf-section__title,
  .rf-growth__title,
  .rf-safer__heading {
    font-size: 28px;
    line-height: 36px;
  }

  .rf-growth__cards {
    grid-template-columns: 1fr;
  }

  .rf-growth__card {
    min-height: 0;
  }

  .rf-detect {
    grid-template-columns: 1fr;
  }

  .rf-safer {
    padding-left: 20px;
    padding-right: 20px;
  }

  .rf-safer__step-title {
    font-size: 24px;
    line-height: 32px;
  }

  .rf-safer__step-body {
    font-size: 14px;
  }
}
</style>
