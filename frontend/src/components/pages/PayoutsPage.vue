<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import MetricCards from "@/components/MetricCards.vue";
import PayoutsHeroGraphic from "./PayoutsHeroGraphic.vue";
import PayoutsPlatformDiagram from "./PayoutsPlatformDiagram.vue";
import UpiPathSection from "./UpiPathSection.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);
const platformReady = ref(false);
const controlRef = ref(null);
const controlStackRef = ref(null);
const controlProgress = ref(0);
const controlReduceMotion = ref(false);
let controlRaf = 0;

const stats = computed(() => props.page?.stats || []);
const featureCards = computed(() => props.page?.features?.cards || []);
const controlCards = computed(() => props.page?.control?.cards || []);
const controlCount = computed(() => Math.max(controlCards.value.length, 1));

/**
 * Skiper16-style sticky card stack (scroll progress → scale).
 * Inspired by https://skiper-ui.com/v1/skiper16 — adapted for Vue (no framer-motion/lenis).
 * Section title scrolls normally; only cards stick + scale.
 */
function navOffsetPx() {
  if (typeof window === "undefined") return 129;
  const raw = getComputedStyle(document.documentElement)
    .getPropertyValue("--page-nav-offset")
    .trim();
  const fromPage = controlRef.value
    ? getComputedStyle(controlRef.value).getPropertyValue("--page-nav-offset").trim()
    : "";
  const n = Number.parseFloat(fromPage || raw || "129");
  return Number.isFinite(n) ? n : 129;
}

function mapRange(value, [inMin, inMax], [outMin, outMax]) {
  if (value <= inMin) return outMin;
  if (value >= inMax) return outMax;
  const t = (value - inMin) / Math.max(inMax - inMin, 1e-6);
  return outMin + (outMax - outMin) * t;
}

const CONTROL_SCALE_STEP = 0.05;
const CONTROL_STACK_PEEK = 14;

function controlTargetScale(i) {
  const n = controlCount.value;
  // Equal steps: e.g. 3 cards → 0.90 / 0.95 / 1
  return Math.max(0.85, 1 - (n - i - 1) * CONTROL_SCALE_STEP);
}

function controlCardScale(i) {
  if (controlReduceMotion.value) return 1;
  const n = controlCount.value;
  const step = n <= 1 ? 1 : 1 / n;
  return mapRange(controlProgress.value, [i * step, 1], [1, controlTargetScale(i)]);
}

function controlCardStyle(i) {
  const scale = controlCardScale(i);
  // Equal pixel peeks between layers (keeps the stack proportional)
  return {
    transform: `translateY(${i * CONTROL_STACK_PEEK}px) scale(${scale})`,
    transformOrigin: "top center",
  };
}

function controlSlotStyle(i) {
  return { zIndex: i + 1 };
}

function syncControlProgress() {
  const el = controlStackRef.value || controlRef.value;
  if (!el || controlReduceMotion.value) {
    controlProgress.value = 0;
    return;
  }
  const nav = navOffsetPx();
  const rect = el.getBoundingClientRect();
  // Progress over the card stack only (title is normal page flow)
  const start = window.scrollY + rect.top - nav;
  const end = window.scrollY + rect.bottom - window.innerHeight;
  const total = Math.max(end - start, 1);
  controlProgress.value = Math.min(1, Math.max(0, (window.scrollY - start) / total));
}

function onControlScroll() {
  cancelAnimationFrame(controlRaf);
  controlRaf = requestAnimationFrame(syncControlProgress);
}

onMounted(async () => {
  requestAnimationFrame(() => {
    heroReady.value = true;
    platformReady.value = true;
  });
  controlReduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  await nextTick();
  syncControlProgress();
  window.addEventListener("scroll", onControlScroll, { passive: true });
  window.addEventListener("resize", onControlScroll);
});

onBeforeUnmount(() => {
  cancelAnimationFrame(controlRaf);
  window.removeEventListener("scroll", onControlScroll);
  window.removeEventListener("resize", onControlScroll);
});

watch([controlRef, controlStackRef], () => {
  syncControlProgress();
});

watch(controlCount, async () => {
  await nextTick();
  syncControlProgress();
});
</script>

<template>
  <main class="po-page">
    <!-- Hero — Figma 370:3264 -->
    <section class="po-hero" :class="{ 'po-hero--ready': heroReady }">
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
        <div class="po-hero__copy">
          <p v-if="page.eyebrow" class="po-hero__eyebrow">{{ page.eyebrow }}</p>
          <h1 class="po-hero__title">{{ page.title }}</h1>
          <p class="po-hero__intro">{{ page.intro }}</p>
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

        <div class="po-hero__visual">
          <PayoutsHeroGraphic
            :ready="heroReady"
            :alt="page.hero_image_alt || 'Distribute funds across recipients'"
          />
        </div>
      </div>
    </section>

    <!-- Stats — shared MetricCards (Collections card treatment) -->
    <section
      v-if="stats.length"
      class="po-stats"
      aria-label="Payout performance metrics"
    >
      <MetricCards :items="stats" aria-label="Payout performance metrics" />
    </section>

    <!-- Platform — Figma 385:7109 (heading 385:7102 + diagram) -->
    <section v-if="page.platform" class="po-section po-section--platform">
      <div class="po-platform-head">
        <h2 class="po-platform-head__title">{{ page.platform.title }}</h2>
        <p class="po-platform-head__body">{{ page.platform.body }}</p>
      </div>
      <PayoutsPlatformDiagram
        :ready="platformReady"
        :alt="page.platform.image_alt || page.platform.title"
      />
    </section>

    <!-- Features — Figma 385:7086 -->
    <section v-if="page.features" class="po-section po-section--features">
      <div class="po-section__head">
        <h2 class="po-section__title">{{ page.features.title }}</h2>
        <p class="po-section__body">{{ page.features.body }}</p>
      </div>
      <div class="po-features" aria-label="Payout operation features">
        <article
          v-for="card in featureCards"
          :key="card.title"
          class="po-features__card"
        >
          <div class="po-features__icon">
            <img
              :src="card.icon"
              alt=""
              width="55"
              height="55"
              decoding="async"
            />
          </div>
          <h3 class="po-features__title">{{ card.title }}</h3>
          <p class="po-features__body">{{ card.body }}</p>
        </article>
      </div>
    </section>

    <!-- Path — Figma 385:6824 -->
    <UpiPathSection v-if="page.path" :path="page.path" />

    <!-- Control — Figma 413:6482 — normal scrolling title + Skiper16 card stack -->
    <section
      v-if="page.control"
      ref="controlRef"
      class="po-section po-section--control"
      :class="{ 'po-section--control-static': controlReduceMotion }"
      :style="{ '--po-control-steps': String(controlCount) }"
    >
      <div class="po-section__head po-section__head--control">
        <h2 class="po-section__title po-section__title--control">
          {{ page.control.title }}
        </h2>
        <p class="po-section__body po-section__body--control">
          {{ page.control.body }}
        </p>
      </div>

      <div
        ref="controlStackRef"
        class="po-control-stack"
        aria-label="Payout control capabilities"
      >
        <template v-for="(card, i) in controlCards" :key="card.title">
          <div class="po-control-slot" :style="controlSlotStyle(i)">
            <article
              class="po-control__card"
              :class="{ 'po-control__card--reverse': i % 2 === 1 }"
              :style="controlCardStyle(i)"
            >
              <div class="po-control__copy">
                <h3 class="po-control__title">{{ card.title }}</h3>
                <p class="po-control__body">{{ card.body }}</p>
              </div>
              <div class="po-control__visual">
                <img
                  class="po-control__media"
                  :src="card.image"
                  :alt="card.image_alt || card.title"
                  :width="card.image_width || 765"
                  :height="card.image_height || 411"
                  decoding="async"
                  loading="lazy"
                />
              </div>
            </article>
          </div>
          <div
            v-if="i < controlCount - 1"
            class="po-control-runway"
            aria-hidden="true"
          />
        </template>
      </div>
    </section>
  </main>
</template>

<style scoped>
.po-page {
  width: 100%;
  background: #ffffff;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #1e2a3b;
}

/* —— Hero —— */
.po-hero {
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

.po-hero__bg {
  position: absolute;
  inset: 0;
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
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  /*
   Figma 370:3264 (1440×813):
   copy @ x=90 w=516 · graphic @ x=629 w=779.64
   → left inset 90, right inset ~31, gap 23
  */
  /* Band between navbar and viewport bottom */
  min-height: calc(100svh - var(--page-nav-offset, 129px));
  padding: 0 31px 0 90px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 516fr) minmax(0, 780fr);
  column-gap: 23px;
  align-items: center;
}

.po-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: center;
  max-width: 516px;
  width: 100%;
}

.po-hero__eyebrow {
  margin: 0 0 18px;
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
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

.po-hero__title {
  margin: 0 0 12px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
  text-transform: capitalize;
}

.po-hero__intro {
  margin: 0 0 40px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
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
}

.po-hero__visual {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  align-self: center;
  min-width: 0;
  width: 100%;
  height: auto;
  max-height: calc(100svh - var(--page-nav-offset, 129px));
  margin: 0;
  padding: 0;
  overflow: visible;
}

/* —— Stats strip spacing (cards styled by MetricCards) —— */
.po-stats {
  width: 100%;
  max-width: 1208px;
  margin: 0 auto;
  padding: 24px 24px 0;
  box-sizing: border-box;
}

/* —— Shared section —— */
.po-section {
  max-width: 1291px;
  margin: 96px auto 0;
  padding: 0 24px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
}

.po-section--platform {
  max-width: none;
  width: 100%;
  /* 100px from stats section to platform title */
  margin-top: 100px;
  /* Figma: heading → diagram gap = 172 − 116 = 56 */
  gap: 56px;
  min-height: 0;
  justify-content: flex-start;
  padding-block: 0 24px;
}

/* Figma 385:7102 — Tablet_Heading (do not scale with the graphic) */
.po-platform-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(744px, 100%);
  text-align: center;
  flex-shrink: 0;
}

.po-platform-head__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
  text-transform: capitalize;
}

.po-platform-head__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.po-section__head {
  width: min(810px, 100%);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.po-section__title {
  margin: 0;
  font-size: clamp(28px, 3.5vw, 40px);
  font-weight: 700;
  line-height: 1.25;
  color: #1e2a3b;
  text-transform: capitalize;
}

.po-section__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 26px;
  color: #475569;
}

/* —— Features —— */
.po-features {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1167px;
}

.po-features__card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 242px;
  padding: 24px 20px;
  box-sizing: border-box;
  border: 1px solid #e9eaeb;
  border-radius: 12px;
  background: #ffffff;
}

.po-features__icon {
  width: 55px;
  height: 55px;
}

.po-features__icon img {
  display: block;
  width: 55px;
  height: 55px;
  object-fit: contain;
}

.po-features__title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  line-height: 24px;
  color: #1e2a3b;
}

.po-features__body {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: #64748b;
}

/* —— Control — title scrolls with page; cards sticky-stack (Skiper16) —— */
.po-section--control {
  --po-control-card-max-h: 451px;
  --po-control-steps: 3;
  --po-control-sticky-top: var(--page-nav-offset, 129px);
  --po-control-runway: 40vh;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1291px;
  margin: 96px auto 0;
  padding: 0 24px;
  box-sizing: border-box;
}

/* Normal in-flow copy — not sticky, not a floating panel */
.po-section__head--control {
  position: static;
  z-index: auto;
  width: min(810px, 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin: 0 0 40px;
  padding: 0;
  text-align: center;
  background: transparent;
}

.po-section__title--control {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.po-section__body--control {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.po-control-stack {
  position: relative;
  width: 100%;
  max-width: 1249px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding-bottom: 0;
}

.po-control-slot {
  position: sticky;
  top: calc(var(--po-control-sticky-top) + 20px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: auto;
  min-height: 0;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Scroll distance between cards — not after the last one */
.po-control-runway {
  flex: 0 0 auto;
  width: 100%;
  height: var(--po-control-runway);
  pointer-events: none;
}

.po-control__card {
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 64px;
  width: 100%;
  height: min(
    var(--po-control-card-max-h),
    calc(100svh - var(--po-control-sticky-top) - 48px)
  );
  max-height: min(
    var(--po-control-card-max-h),
    calc(100svh - var(--po-control-sticky-top) - 48px)
  );
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #ebebeb;
  border-radius: 24px;
  background: #fafafa;
  overflow: hidden;
  box-shadow:
    0 1px 2px rgba(16, 24, 40, 0.04),
    0 12px 32px rgba(16, 24, 40, 0.1);
  will-change: transform;
}

.po-control__card--reverse {
  flex-direction: row-reverse;
}

@media (prefers-reduced-motion: reduce) {
  .po-section--control,
  .po-section--control-static {
    padding-bottom: 0;
  }

  .po-control-stack {
    gap: 24px;
    padding-bottom: 0;
  }

  .po-control-slot {
    position: static;
    min-height: 0;
    margin-bottom: 0;
  }

  .po-control-runway {
    display: none;
  }

  .po-control__card {
    height: auto;
    max-height: none;
    transform: none !important;
  }
}

.po-control__copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  width: 371px;
  flex-shrink: 0;
}

.po-control__title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 24px;
  color: #252b37;
}

.po-control__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #535862;
}

.po-control__visual {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  min-height: 0;
  height: 100%;
  max-height: 100%;
}

.po-control__media {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
  pointer-events: none;
  user-select: none;
}

@media (max-width: 1200px) {
  .po-hero__inner {
    padding: 0 24px 0 48px;
    column-gap: 16px;
    grid-template-columns: minmax(0, 516fr) minmax(0, 780fr);
    min-height: calc(100svh - var(--page-nav-offset, 129px));
  }

  .po-hero__copy {
    max-width: none;
  }

  .po-hero__title {
    font-size: 36px;
    line-height: 48px;
  }

  .po-stats {
    padding-left: 48px;
    padding-right: 48px;
  }

  .po-features {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .po-hero__inner {
    grid-template-columns: 1fr;
    padding: 40px 24px 48px;
    min-height: 0;
  }

  .po-hero__copy {
    max-width: none;
  }

  .po-hero {
    min-height: 0;
  }

  .po-hero__title {
    font-size: 32px;
    line-height: 42px;
  }

  .po-hero__visual {
    justify-content: center;
    margin-top: 0;
  }

  .po-stats {
    padding-left: 24px;
    padding-right: 24px;
  }

  .po-section {
    margin-top: 64px;
    padding-left: 24px;
    padding-right: 24px;
  }

  .po-section--platform {
    margin-top: 100px;
    gap: 40px;
    padding-block: 0 24px;
  }

  .po-features {
    grid-template-columns: 1fr;
  }

  .po-section--control {
    height: auto;
    margin-top: 64px;
    padding-bottom: 0;
  }

  .po-section__head--control {
    position: static;
    padding: 0 0 24px;
  }

  .po-control-stack {
    gap: 24px;
    padding-bottom: 0;
  }

  .po-control-runway {
    display: none;
  }

  .po-control-slot {
    position: static;
    min-height: 0;
    margin-bottom: 0;
  }

  .po-control__card,
  .po-control__card--reverse {
    position: relative;
    inset: auto;
    z-index: auto;
    flex-direction: column;
    height: auto;
    min-height: 0;
    max-height: none;
    gap: 28px;
    padding: 28px 20px;
    margin-bottom: 0;
    transform: none !important;
    box-shadow: none;
  }

  .po-control__copy {
    width: 100%;
  }

  .po-control__visual {
    max-height: none;
    width: 100%;
  }

  .po-control__media {
    max-height: 360px;
    width: 100%;
  }

  .po-section__title--control {
    font-size: 32px;
    line-height: 42px;
  }
}
</style>
