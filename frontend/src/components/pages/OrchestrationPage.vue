<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import MetricCards from "@/components/MetricCards.vue";
import { useLoopSlider } from "@/composables/useLoopSlider.js";
import { useScaledArt } from "@/composables/useScaledArt.js";
import OrchestrationLayerVisual from "./OrchestrationLayerVisual.vue";
import PaymentOrchestrationHeroGraphic from "./PaymentOrchestrationHeroGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  relatedLinks: { type: Array, default: () => [] },
});

const CONTROL_INTERVAL = 3500;

const heroReady = ref(false);
const activeControl = ref(0);
const controlPaused = ref(false);
const controlReduceMotion = ref(false);
const controlInteracted = ref(false);
const controlReady = ref(false);
let controlTimer = null;

const controlRowRef = ref(null);
const registerArtFrame = useScaledArt("po");

const growthCards = computed(() => props.page?.growth?.cards || []);
const growthLeft = computed(() => [growthCards.value[0], growthCards.value[1]].filter(Boolean));
const growthRight = computed(() => [growthCards.value[2], growthCards.value[3]].filter(Boolean));
const controlSteps = computed(() => props.page?.control?.steps || []);
const controlOthers = computed(() => Math.max(controlSteps.value.length - 1, 0));
const controlCount = computed(() => controlSteps.value.length);
const {
  slide: controlSlide,
  snapping: controlSnapping,
  onTrackTransitionEnd: onControlTrackEnd,
} = useLoopSlider(activeControl, controlCount);
const pageStats = computed(() => props.page?.stats || []);

function startControlCycle() {
  stopControlCycle();
  if (
    controlReduceMotion.value ||
    controlPaused.value ||
    controlInteracted.value ||
    controlSteps.value.length < 2
  ) {
    return;
  }
  controlTimer = window.setInterval(() => {
    activeControl.value = (activeControl.value + 1) % controlSteps.value.length;
  }, CONTROL_INTERVAL);
}

function stopControlCycle() {
  if (controlTimer) clearInterval(controlTimer);
  controlTimer = null;
}

function selectControl(index, { fromUser = true } = {}) {
  if (fromUser) {
    controlInteracted.value = true;
    stopControlCycle();
  }
  activeControl.value = index;
  if (!fromUser) startControlCycle();
}

/** Phone arrows: step through the cards, wrapping at either end. */
function stepControl(dir) {
  const count = controlSteps.value.length;
  if (count < 2) return;
  selectControl((activeControl.value + dir + count) % count);
}

function pauseControl() {
  controlPaused.value = true;
  stopControlCycle();
}

function resumeControl() {
  controlPaused.value = false;
  if (!controlInteracted.value) startControlCycle();
}

function onControlHover(index) {
  if (controlReduceMotion.value) return;
  // Match Primer: first meaningful hover owns the accordion and stops autoplay.
  if (!controlInteracted.value && index === 0 && activeControl.value === 0) return;
  selectControl(index, { fromUser: true });
}

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
    controlReady.value = true;
  });
  controlReduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startControlCycle();
});

onBeforeUnmount(() => {
  stopControlCycle();
});

watch(controlSteps, async () => {
  await nextTick();
  if (!controlInteracted.value) startControlCycle();
});
</script>

<template>
  <main class="po-page po-page--orchestration">
    <!-- Hero + stats — Figma 330:1482 -->
    <section class="po-hero">
      <div class="po-hero__bg" aria-hidden="true">
        <img
          class="po-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="po-hero__inner">
        <div class="po-hero__row">
          <div class="po-hero__copy">
            <p v-if="page.eyebrow" class="po-hero__eyebrow">{{ page.eyebrow }}</p>
            <div class="po-hero__cta-block">
              <div class="po-hero__text">
                <h1 class="po-hero__title">{{ page.title }}</h1>
                <p class="po-hero__intro">{{ page.intro }}</p>
              </div>
              <RouterLink to="/contact" class="po-hero__cta">
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
          </div>
          <div :ref="registerArtFrame" class="po-hero__graphic">
            <div class="po-hero__art">
              <PaymentOrchestrationHeroGraphic :ready="heroReady" />
            </div>
          </div>
        </div>

        <MetricCards
          v-if="pageStats.length"
          class="po-hero__metrics"
          :items="pageStats"
          :ready="heroReady"
          aria-label="Orchestration outcomes"
        />
      </div>
    </section>

    <!-- One layer — Figma 330:1521 -->
    <section v-if="page.layer" class="po-layer">
      <div class="po-layer__head">
        <h2 class="po-layer__title">{{ page.layer.title }}</h2>
        <p class="po-layer__body">{{ page.layer.body }}</p>
      </div>
      <div class="po-layer__visual">
        <OrchestrationLayerVisual
          class="po-layer__media"
          :src="page.layer.image"
          :alt="page.layer.image_alt || page.layer.title"
          :width="page.layer.image_width || 1240"
          :height="page.layer.image_height || 782"
        />
      </div>
    </section>

    <!-- Growth — Figma 296:3175 -->
    <section v-if="page.growth" class="po-growth">
      <div class="po-growth__copy">
        <h2 class="po-growth__title">{{ page.growth.title }}</h2>
        <p class="po-growth__body">{{ page.growth.body }}</p>
      </div>
      <div class="po-growth__cols" aria-label="Business growth outcomes">
        <div class="po-growth__col po-growth__col--left">
          <article
            v-for="card in growthLeft"
            :key="card.title"
            class="po-growth__card"
          >
            <div class="po-growth__icon" :class="{ 'po-growth__icon--bare': card.framed }">
              <img
                :src="card.icon"
                alt=""
                :width="card.icon_width || 26"
                :height="card.icon_height || 26"
                decoding="async"
              />
            </div>
            <div class="po-growth__card-text">
              <h3 class="po-growth__card-title">{{ card.title }}</h3>
              <p class="po-growth__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
        <div class="po-growth__col">
          <article
            v-for="card in growthRight"
            :key="card.title"
            class="po-growth__card"
          >
            <div class="po-growth__icon" :class="{ 'po-growth__icon--bare': card.framed }">
              <img
                :src="card.icon"
                alt=""
                :width="card.icon_width || 26"
                :height="card.icon_height || 26"
                decoding="async"
              />
            </div>
            <div class="po-growth__card-text">
              <h3 class="po-growth__card-title">{{ card.title }}</h3>
              <p class="po-growth__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Routing — Figma 330:1469 -->
    <section v-if="page.routing" class="po-routing">
      <div class="po-routing__head">
        <h2 class="po-routing__title">{{ page.routing.title }}</h2>
        <p class="po-routing__body">{{ page.routing.body }}</p>
      </div>
      <div class="po-routing__grid" aria-label="Routing strategies">
        <article
          v-for="card in page.routing.cards || []"
          :key="card.title"
          class="po-routing__card"
        >
          <div class="po-routing__visual">
            <img
              class="po-routing__media"
              :src="card.image"
              :alt="card.image_alt || card.title"
              width="466"
              height="373"
              decoding="async"
              loading="lazy"
            />
          </div>
          <div class="po-routing__card-text">
            <h3 class="po-routing__card-title">{{ card.title }}</h3>
            <p class="po-routing__card-body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Control — Primer-style fluid accordion (width/flex morph + staggered fades). -->
    <section
      v-if="page.control"
      class="po-control"
      :class="{ 'po-control--ready': controlReady }"
      :style="{ '--po-control-others': String(controlOthers) }"
      @mouseenter="pauseControl"
      @mouseleave="resumeControl"
      @focusin="pauseControl"
      @focusout="resumeControl"
    >
      <div class="po-control__head">
        <h2 class="po-control__title">{{ page.control.title }}</h2>
        <p class="po-control__body">{{ page.control.body }}</p>
      </div>
      <div
        ref="controlRowRef"
        class="po-control__row"
        :class="{ 'po-control__row--snap': controlSnapping }"
        :style="{ '--po-slide': String(controlSlide) }"
        role="tablist"
        aria-label="Transaction control"
        @transitionend="onControlTrackEnd"
      >
        <button
          v-for="(step, index) in controlSteps"
          :key="step.num"
          type="button"
          class="po-control__step"
          :class="{
            'po-control__step--active': activeControl === index,
          }"
          role="tab"
          :aria-selected="activeControl === index"
          :aria-label="`${step.num}. ${step.title}`"
          @click="selectControl(index)"
          @mouseenter="onControlHover(index)"
          @focus="onControlHover(index)"
        >
          <span class="po-control__num" aria-hidden="true">{{ step.num }}</span>
          <span class="po-control__stack">
            <span class="po-control__step-text">
              <span class="po-control__step-title">{{ step.title }}</span>
              <span class="po-control__step-body">{{ step.body }}</span>
            </span>
          </span>
        </button>
        <!-- Phone slider only: copy of the first card so wrapping keeps sliding forward. -->
        <div
          v-if="controlSteps.length > 2"
          class="po-control__step po-control__step--active po-control__step--clone"
          aria-hidden="true"
        >
          <span class="po-control__num">{{ controlSteps[0].num }}</span>
          <span class="po-control__stack">
            <span class="po-control__step-text">
              <span class="po-control__step-title">{{ controlSteps[0].title }}</span>
              <span class="po-control__step-body">{{ controlSteps[0].body }}</span>
            </span>
          </span>
        </div>
      </div>
      <div v-if="controlSteps.length > 1" class="po-control__nav">
        <button
          type="button"
          class="po-control__arrow po-control__arrow--prev"
          aria-label="Previous step"
          @click="stepControl(-1)"
        >
          <img
            src="/images/figma-collections/experiences/arrow-up-dark.svg"
            alt=""
            width="12"
            height="13"
            decoding="async"
          />
        </button>
        <button
          type="button"
          class="po-control__arrow po-control__arrow--next"
          aria-label="Next step"
          @click="stepControl(1)"
        >
          <img
            src="/images/figma-collections/experiences/arrow-up-white.svg"
            alt=""
            width="14"
            height="14"
            decoding="async"
          />
        </button>
      </div>
    </section>
  </main>
</template>

<style scoped>
.po-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

/* —— Hero — Figma 330:1482 / 321:6601 —— */
.po-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.po-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.po-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.po-hero__inner {
  /* Side padding matches title inset (100px) on both edges. */
  --po-hero-side: 100px;
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  /* Bottom pad so card drop-shadows aren’t clipped by .po-hero overflow */
  padding: 72px var(--po-hero-side) 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 100px;
}

.po-hero__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(32px, 8vw, 143px);
  width: 100%;
  min-height: 475px;
}

.po-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 18px;
  flex: 0 1 545px;
  width: min(545px, 100%);
  min-width: 0;
}

.po-hero__eyebrow {
  margin: 0;
  padding: 8px 16px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  font-size: 12px;
  font-weight: 700;
  line-height: 20px;
  letter-spacing: 1.7836px;
  text-transform: uppercase;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.po-hero__cta-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 40px;
  width: 100%;
}

.po-hero__text {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.po-hero__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 1.27;
  letter-spacing: -1.26px;
  text-transform: capitalize;
  color: #252b37;
}

.po-hero__intro {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.56px;
  color: #535862;
}

.po-hero__cta {
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

.po-hero__cta:hover {
  background: #0a86ad;
}

.po-hero__cta img {
  display: block;
  width: 18px;
  height: 18px;
}

.po-hero__graphic {
  flex: 0 1 520px;
  width: min(520px, 100%);
  max-width: 520px;
  min-width: 0;
}

.po-hero__art {
  width: 100%;
}

/* —— One layer — Figma 330:1521 —— */
.po-layer {
  max-width: 1440px;
  margin: 84px auto 0;
  padding: 0 100px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.po-layer__head,
.po-routing__head,
.po-control__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: min(788px, 100%);
  text-align: center;
}

.po-layer__title,
.po-growth__title,
.po-routing__title,
.po-control__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.po-layer__body,
.po-growth__body,
.po-routing__body,
.po-control__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.po-layer__visual {
  width: 100%;
  max-width: 1240px;
  border-radius: 14.141px;
  overflow: hidden;
}

.po-layer__media {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 1240 / 782;
  object-fit: cover;
  border: 0;
  pointer-events: none;
}

/* —— Growth — Figma 296:3175 —— */
.po-growth {
  max-width: 1440px;
  margin: 100px auto 0;
  padding: 0 100px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 86px;
}

.po-growth__copy {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 544px;
  max-width: 100%;
  flex-shrink: 0;
}

.po-growth__cols {
  display: flex;
  gap: 36px;
  width: 610px;
  max-width: 100%;
  flex-shrink: 0;
}

.po-growth__col {
  display: flex;
  flex-direction: column;
  gap: 36px;
  width: 287px;
  max-width: 100%;
}

.po-growth__col--left {
  padding-top: 73px;
}

.po-growth__card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  width: 287px;
  min-height: 179px;
  height: auto;
  padding: 20px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 14.141px;
  /* Match about-purpose__card default + hover (Figma 722:7669 / 722:7640) */
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.25s ease;
}

.po-growth__card:hover {
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

.po-growth__icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-shrink: 0;
  padding: 13.284px;
  box-sizing: border-box;
  background: rgba(9, 116, 149, 0.1);
  border-radius: 6.642px;
}

.po-growth__icon--bare {
  padding: 0;
  background: transparent;
  border-radius: 0;
}

.po-growth__icon img {
  display: block;
  object-fit: contain;
}

.po-growth__card-text {
  display: flex;
  flex-direction: column;
  gap: 7px;
  width: 100%;
  min-width: 0;
}

.po-growth__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.48px;
  color: #252b37;
}

.po-growth__card-body {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: #535862;
}

/* —— Routing — Figma 330:1469 —— */
.po-routing {
  max-width: 1052px;
  margin: 100px auto 0;
  padding: 0 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.po-routing__grid {
  display: grid;
  grid-template-columns: repeat(2, 514px);
  gap: 24px;
  width: 100%;
  justify-content: center;
}

.po-routing__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 514px;
  min-height: 513px;
  padding: 24px;
  box-sizing: border-box;
  background: #ffffff;
  border: 0;
  box-shadow: inset 0 0 0 1px #e9eaeb;
  border-radius: 12px;
}

.po-routing__visual {
  width: 466px;
  height: 373px;
  max-width: 100%;
}

.po-routing__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  border: 0;
  pointer-events: none;
}

.po-routing__card-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.po-routing__card-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 32px;
  color: #252b37;
}

.po-routing__card-body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* —— Control — Figma 296:3218 dimensions + fluid width morph —— */
.po-control {
  /* Figma: inactive 104, gap 24, active 690 → row 1074 */
  --po-control-inactive: 104px;
  --po-control-gap: 24px;
  --po-control-others: 3;
  --po-control-height: 307px;
  --po-num-size: 55px;
  --po-num-top-expanded: 46.5px;
  --po-num-gap: 16px;
  --po-active-inset: 20px;
  --po-dur-in: 0.5s;
  --po-dur-big: 1s;
  --po-ease-out: cubic-bezier(0.6, 0.6, 0, 1);
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

.po-control__row {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: var(--po-control-gap);
  width: 100%;
  height: var(--po-control-height);
}

.po-control__step {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* Explicit lengths only — auto/flex-grow cannot animate fluidly. */
  width: var(--po-control-inactive);
  flex: 0 0 var(--po-control-inactive);
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
    background var(--po-dur-in) ease,
    color var(--po-dur-in) ease,
    border-radius var(--po-dur-in) var(--po-ease-out),
    padding var(--po-dur-big) var(--po-ease-out),
    width var(--po-dur-big) var(--po-ease-out),
    flex-basis var(--po-dur-big) var(--po-ease-out),
    box-shadow var(--po-dur-in) ease;
}

.po-control:not(.po-control--ready) .po-control__step,
.po-control:not(.po-control--ready) .po-control__num {
  transition: none;
}

.po-control__step--active {
  /* Figma active width 690 = 1074 − 3×104 − 3×24 */
  width: calc(
    100% - ((var(--po-control-inactive) + var(--po-control-gap)) * var(--po-control-others))
  );
  flex-basis: calc(
    100% - ((var(--po-control-inactive) + var(--po-control-gap)) * var(--po-control-others))
  );
  min-width: 0;
  /* Pin from the number landing Y so gap under the circle stays constant */
  justify-content: flex-start;
  align-items: center;
  padding: var(--po-active-inset);
  border-radius: 48px;
  background: #097495;
  color: #ffffff;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.1),
    0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

/*
 * Figma 296:3224 — num lands at 46.5px; copy is offset by numSize + --po-num-gap
 * so the space under the circle is always 16px (not affected by text height).
 */
.po-control__stack {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 0;
  width: min(388px, 100%);
  max-width: 100%;
  min-height: 0;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  /* Inactive: collapse so only the absolute number shows at the pill bottom */
  height: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
}

.po-control__step--active .po-control__stack {
  height: auto;
  opacity: 1;
  overflow: visible;
  pointer-events: auto;
  /*
   * Absolute num `top` is relative to the step padding box.
   * Flow content starts after --po-active-inset, so this margin places text at
   * numTop + numSize + gap → constant 16px under the circle.
   */
  margin-top: calc(
    var(--po-num-top-expanded) - var(--po-active-inset) + var(--po-num-size) +
      var(--po-num-gap)
  );
}

.po-control__num {
  position: absolute;
  left: 50%;
  z-index: 2;
  /* Expanded landing Y (Figma stack top). Contracted offset applied via translateY. */
  top: var(--po-num-top-expanded);
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--po-num-size);
  height: var(--po-num-size);
  /* Inactive: shift down to pill bottom → (307 − 24 − 55) − 46.5 = 181.5 */
  transform: translate(
    -50%,
    calc(var(--po-control-height) - 24px - var(--po-num-size) - var(--po-num-top-expanded))
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
    transform var(--po-dur-big) var(--po-ease-out),
    background var(--po-dur-in) ease,
    color var(--po-dur-in) ease,
    border-radius var(--po-dur-in) var(--po-ease-out);
}

.po-control__step:nth-child(even) .po-control__num {
  background: #0292b8;
}

/* Expanded — settle at stack top; X travels with the width morph (diagonal). */
.po-control__step--active .po-control__num {
  transform: translate(-50%, 0);
  background: #00b7db;
  color: #ffffff;
}

.po-control__step-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  /* Fixed Figma copy width so line breaks don’t reflow while the card morphs */
  width: 388px;
  max-width: 388px;
  text-align: center;
  opacity: 0;
  transform: translateY(12px);
  pointer-events: none;
  transition:
    transform 0s var(--po-ease-out),
    opacity 0s ease-in;
}

.po-control__step--active .po-control__step-text {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
  /* Fade in after the width morph has mostly settled */
  transition:
    transform var(--po-dur-in) var(--po-ease-out) 0.55s,
    opacity var(--po-dur-in) ease-in 0.55s;
}

.po-control__step-title {
  margin: 0;
  width: 100%;
  /* Figma 296:3228 / 719:7438 — fixed 87px title band */
  height: 87px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  line-height: 42px;
  color: #fafafa;
}

.po-control__step-body {
  margin: 0;
  width: 100%;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.56px;
  /* Figma 296:3229 (in-page); variants use rgba(255,255,255,0.8) */
  color: #e9eaeb;
}

/* Phone only: the row shows one card, so arrows step through the rest. */
.po-control__nav {
  display: none;
}

.po-control__step.po-control__step--clone {
  display: none;
}

@media (prefers-reduced-motion: reduce) {
  .po-growth__card,
  .po-control__step,
  .po-control__step-text,
  .po-control__num,
  .po-control__step--active .po-control__step-text {
    transition: none !important;
  }
}

@media (max-width: 1114px) {
  .po-control {
    padding-left: 20px;
    padding-right: 20px;
  }
}

@media (max-width: 1280px) {
  .po-hero__inner,
  .po-layer,
  .po-growth {
    padding-left: 56px;
    padding-right: 56px;
  }

  .po-hero__row {
    gap: 48px;
  }

  .po-growth {
    gap: 48px;
  }
}

@media (max-width: 1200px) {
  .po-hero__row,
  .po-growth {
    flex-wrap: wrap;
    justify-content: center;
  }

  .po-hero__copy,
  .po-hero__graphic,
  .po-growth__copy,
  .po-growth__cols {
    width: 100%;
    flex: 1 1 auto;
  }

  .po-hero__graphic {
    flex-basis: 552px;
  }

  .po-growth__col--left {
    padding-top: 0;
  }

  .po-routing__grid {
    grid-template-columns: 1fr;
  }

  .po-routing__card {
    width: min(514px, 100%);
    margin-inline: auto;
  }

  .po-control__row {
    flex-direction: column;
    height: auto;
    min-height: 0;
    gap: 12px;
  }

  .po-control__step,
  .po-control__step--active {
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

  .po-control__step {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
  }

  .po-control__stack {
    position: static;
    height: auto !important;
    opacity: 1 !important;
    overflow: visible;
    padding-top: 0 !important;
    width: 100%;
    pointer-events: auto;
  }

  .po-control__num {
    position: static !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    flex-shrink: 0;
    width: 55px;
    height: 55px;
    font-size: 20px;
    will-change: auto;
    transition: background var(--po-dur-in) ease, color var(--po-dur-in) ease;
  }

  .po-control__step--active .po-control__num {
    top: auto !important;
    width: var(--po-num-size);
    height: var(--po-num-size);
    border-radius: 32px;
    background: #00b7db;
    transform: none !important;
  }

  .po-control__step-text {
    opacity: 1 !important;
    transform: none !important;
    pointer-events: auto;
    width: 100%;
    padding: 0;
    gap: 8px;
    transition: none !important;
  }

  .po-control__step:not(.po-control__step--active) {
    min-height: 72px;
    padding: 12px 16px;
  }

  .po-control__step:not(.po-control__step--active) .po-control__stack,
  .po-control__step:not(.po-control__step--active) .po-control__step-text {
    display: none;
  }

  .po-control__step--active {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }

  .po-control__step--active .po-control__stack {
    width: min(388px, 100%);
  }

  .po-control__step--active .po-control__step-text {
    height: auto;
    margin-top: 0;
    padding-top: 0;
  }

  .po-control__step--active .po-control__step-body {
    color: #e9eaeb;
  }
}

@media (max-width: 700px) {
  .po-hero__inner,
  .po-layer,
  .po-growth,
  .po-control {
    padding-left: 20px;
    padding-right: 20px;
  }

  .po-hero__title,
  .po-layer__title,
  .po-growth__title,
  .po-routing__title,
  .po-control__title {
    font-size: 32px;
    line-height: 42px;
  }

  .po-growth__cols {
    flex-direction: column;
    align-items: center;
  }

  .po-control__step-title {
    font-size: 24px;
    line-height: 32px;
  }

  .po-control__step-body {
    font-size: 14px;
  }
}

/* —— Phone — Figma 1149:6639 (393 frame, 16px gutters, 100px between sections) —— */
@media (max-width: 767px) {
  .po-hero__title,
  .po-layer__title,
  .po-growth__title,
  .po-routing__title,
  .po-control__title {
    font-size: 28px;
    line-height: 36px;
  }

  .po-hero__title,
  .po-layer__title,
  .po-growth__title,
  .po-routing__title {
    letter-spacing: -0.84px;
  }

  .po-hero__intro,
  .po-layer__body,
  .po-growth__body,
  .po-routing__body,
  .po-control__body {
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0;
  }

  .po-control__body {
    letter-spacing: 0.56px;
  }

  .po-layer__head,
  .po-routing__head,
  .po-control__head,
  .po-growth__copy {
    gap: 12px;
  }

  /* Hero: chip 91px under the navbar; bottom padding keeps the metric card shadows unclipped */
  .po-hero__inner {
    padding: 91px 16px 24px;
    gap: 100px;
  }

  .po-hero__row {
    flex-direction: column;
    gap: 24px;
    min-height: 0;
  }

  .po-hero__copy {
    flex: none;
    align-items: center;
    gap: 24px;
    text-align: center;
  }

  .po-hero__cta-block {
    align-items: center;
    gap: 24px;
  }

  .po-hero__cta {
    height: 40px;
    padding: 0 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  /* Graphic is drawn at its desktop width and scaled to the column (useScaledArt). */
  .po-hero__graphic {
    flex: none;
    width: calc(100% - 4px);
    max-width: none;
    height: var(--po-art-height, auto);
  }

  .po-hero__art {
    width: 520px;
    transform: scale(var(--po-art-scale, 1));
    transform-origin: 0 0;
  }

  .po-hero .po-hero__metrics {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 144px));
    justify-content: center;
    gap: 18px 40px;
  }

  .po-hero__metrics :deep(.ur-metrics__card) {
    height: auto;
    min-height: 115px;
    padding: 12px;
    gap: 8px;
    border: 0;
    border-radius: 8px;
    box-shadow:
      0 12px 16px -4px rgba(10, 13, 18, 0.1),
      0 4px 6px -2px rgba(10, 13, 18, 0.05);
  }

  .po-hero__metrics :deep(.ur-metrics__value) {
    min-height: 40px;
    font-size: 32px;
    line-height: 40px;
    letter-spacing: -0.96px;
    color: #252b37;
  }

  /* Two-line label box so every value sits at the same height */
  .po-hero__metrics :deep(.ur-metrics__label) {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 40px;
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0;
    white-space: normal;
  }

  /* Metrics → layer is 64px; 24px of it is the hero's shadow padding. */
  .po-layer {
    margin-top: 40px;
    padding: 0 16px;
    gap: 36px;
  }

  .po-layer__visual {
    width: calc(100% - 8px);
    border-radius: 6.38px;
  }

  .po-growth,
  .po-routing,
  .po-control {
    margin-top: 100px;
    padding: 0 16px;
  }

  .po-growth {
    flex-direction: column;
    gap: 36px;
  }

  .po-growth__copy {
    flex: none;
    text-align: center;
  }

  .po-growth__cols {
    flex: none;
    flex-direction: column;
    width: min(322px, 100%);
    gap: 24px;
  }

  /* Columns dissolve so the cards read row by row, as in Figma. */
  .po-growth__col {
    display: contents;
  }

  .po-growth__col--left .po-growth__card:nth-child(1) {
    order: 1;
  }

  .po-growth__col:not(.po-growth__col--left) .po-growth__card:nth-child(1) {
    order: 2;
  }

  .po-growth__col--left .po-growth__card:nth-child(2) {
    order: 3;
  }

  .po-growth__col:not(.po-growth__col--left) .po-growth__card:nth-child(2) {
    order: 4;
  }

  .po-growth__card {
    justify-content: center;
    gap: 12px;
    width: 100%;
    min-height: 197px;
    border-radius: 12px;
  }

  .po-growth__icon {
    padding: 12px;
    border-radius: 4px;
  }

  .po-growth__card-text {
    gap: 8px;
  }

  .po-growth__card-title {
    line-height: 20px;
  }

  .po-growth__card-body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.36px;
  }

  .po-routing {
    gap: 36px;
  }

  .po-routing__card {
    width: 100%;
    min-height: 410px;
    padding: 20px;
    box-shadow:
      inset 0 0 0 1px #f4f4f4,
      0 1px 1px rgba(0, 0, 0, 0.1),
      0 1px 1.5px rgba(0, 0, 0, 0.1);
  }

  .po-routing__visual {
    width: 100%;
    height: auto;
    aspect-ratio: 466 / 373;
  }

  .po-routing__card-text,
  .po-control__step-text {
    gap: 8px;
  }

  .po-routing__card-title,
  .po-control__step-title {
    font-size: 16px;
    font-weight: 700;
    line-height: 20px;
  }

  .po-routing__card-body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.48px;
  }

  /* Head → card 36px (24 gap + 12 margin), card → arrows 24px. */
  .po-control {
    padding-bottom: 0;
    gap: 24px;
    overflow-x: hidden;
    overflow-x: clip;
  }

  .po-control__head {
    margin-bottom: 12px;
  }

  /* One card wide track that slides like the testimonials carousel. */
  .po-control__row {
    flex-direction: row;
    justify-content: flex-start;
    align-items: stretch;
    gap: 16px;
    transform: translateX(calc(-1 * var(--po-slide, 0) * (100% + 16px)));
    transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
    will-change: transform;
  }

  .po-control__row--snap {
    transition: none;
  }

  /* Every card wears the active look so neighbours slide in already styled. */
  .po-control__row .po-control__step {
    display: flex;
    flex: 0 0 100% !important;
    width: 100% !important;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 160px;
    padding: 10px;
    gap: 8px;
    border-radius: 24px;
    background: #097495;
    color: #ffffff;
    box-shadow:
      0 0.523px 1.046px -0.523px rgba(0, 0, 0, 0.1),
      0 0.523px 1.57px 0 rgba(0, 0, 0, 0.1);
    transition: none;
  }

  .po-control__row .po-control__step .po-control__stack {
    display: flex;
    width: 100%;
    margin-top: 0;
  }

  .po-control__row .po-control__step .po-control__step-text {
    display: flex;
  }

  .po-control__row .po-control__step .po-control__num {
    width: 28px;
    height: 28px;
    border-radius: 16px;
    background: #00b7db;
    font-size: 12px;
    line-height: 15px;
  }

  .po-control__step-title {
    height: auto;
  }

  .po-control__row .po-control__step .po-control__step-body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.48px;
    color: #e9eaeb;
  }

  .po-control__nav {
    display: flex;
    justify-content: center;
    gap: 20px;
  }

  .po-control__arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 28px;
    padding: 0;
    border: 0;
    border-radius: 14px;
    cursor: pointer;
  }

  .po-control__arrow--prev {
    border: 0.5px solid #e5e7eb;
    background: #ffffff;
  }

  .po-control__arrow--prev img {
    width: 11.9px;
    height: 13.03px;
    transform: rotate(-90deg);
  }

  .po-control__arrow--next {
    background: #097495;
  }

  .po-control__arrow--next img {
    width: 13.54px;
    height: 13.54px;
    transform: rotate(90deg);
  }

  .po-control__arrow:focus-visible {
    outline: 2px solid #097495;
    outline-offset: 2px;
  }
}

@media (max-width: 767px) and (prefers-reduced-motion: reduce) {
  .po-control__row {
    transition: none;
  }
}
</style>

<style>
/* Shared closing sits outside this component; only this page's phone rhythm uses Figma's 100px gaps.
   Payouts also roots at .po-page, hence the modifier. */
@media (max-width: 767px) {
  .page-view:has(> .po-page.po-page--orchestration) > .site-closing > * + * {
    margin-top: 100px;
  }
}
</style>
