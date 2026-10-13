<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { useScaledArt } from "@/composables/useScaledArt.js";
import HyperCheckoutShowcaseGraphic from "./HyperCheckoutShowcaseGraphic.vue";
import HyperCheckoutSmarterGraphic from "./HyperCheckoutSmarterGraphic.vue";
import HyperCheckoutTrustGraphic from "./HyperCheckoutTrustGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  relatedLinks: { type: Array, default: () => [] },
});

const TRUST_INTERVAL = 10000;

const activeTrust = ref(0);
const trustReduceMotion = ref(false);
let trustTimer = null;

const trustCards = computed(() => props.page?.trust?.cards || []);

function trustAlt(card) {
  return card.image_alt || card.title || props.page?.trust?.image_alt || "";
}

function startTrustCycle() {
  stopTrustCycle();
  if (trustReduceMotion.value || trustCards.value.length < 2) return;
  trustTimer = window.setInterval(() => {
    activeTrust.value = (activeTrust.value + 1) % trustCards.value.length;
  }, TRUST_INTERVAL);
}

function stopTrustCycle() {
  if (trustTimer) clearInterval(trustTimer);
  trustTimer = null;
}

/** A manual pick shows immediately and restarts the dwell time on that card. */
function selectTrust(index) {
  activeTrust.value = index;
  startTrustCycle();
}

/** Hover/focus: pause tab auto-advance only — graphics keep looping. */
function pauseTrustTabs() {
  stopTrustCycle();
}

function resumeTrustTabs() {
  startTrustCycle();
}

onMounted(() => {
  trustReduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startTrustCycle();
});

onBeforeUnmount(stopTrustCycle);

/** Phones draw the showcase stage at its desktop width and scale it to the column. */
const registerArtFrame = useScaledArt("hc");
</script>

<template>
  <main class="hc-page">
    <!-- Hero — Figma 285:9609 / 285:9653 -->
    <section class="hc-hero">
      <div class="hc-hero__bg" aria-hidden="true">
        <img
          class="hc-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="hc-hero__inner">
        <div class="hc-hero__copy">
          <p v-if="page.eyebrow" class="hc-hero__eyebrow">{{ page.eyebrow }}</p>
          <div class="hc-hero__cta-block">
            <div class="hc-hero__text">
              <h1 class="hc-hero__title">{{ page.title }}</h1>
              <p class="hc-hero__intro">{{ page.intro }}</p>
            </div>
            <RouterLink to="/contact" class="hc-hero__cta">
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
      </div>
    </section>

    <!-- Showcase — Figma 296:1744 -->
    <section v-if="page.showcase" class="hc-showcase">
      <div class="hc-showcase__head">
        <h2 class="hc-showcase__title">{{ page.showcase.title }}</h2>
        <p class="hc-showcase__body">{{ page.showcase.body }}</p>
      </div>
      <div :ref="registerArtFrame" class="hc-showcase__visual">
        <div class="hc-showcase__art">
          <HyperCheckoutShowcaseGraphic />
        </div>
      </div>
    </section>

    <!-- Smarter features — Figma 296:1397 -->
    <section v-if="page.smarter" class="hc-smarter">
      <div class="hc-smarter__head">
        <h2 class="hc-smarter__title">{{ page.smarter.title }}</h2>
        <p class="hc-smarter__body">{{ page.smarter.body }}</p>
      </div>

      <div class="hc-smarter__row">
        <div class="hc-smarter__visual">
          <HyperCheckoutSmarterGraphic
            :alt="page.smarter.image_alt || page.smarter.title"
          />
        </div>
        <div class="hc-smarter__cards" aria-label="Checkout features">
          <article
            v-for="card in page.smarter.cards || []"
            :key="card.title"
            class="hc-smarter__card"
          >
            <div class="hc-smarter__icon">
              <img :src="card.icon" alt="" width="28" height="28" decoding="async" />
            </div>
            <div class="hc-smarter__card-text">
              <h3 class="hc-smarter__card-title">{{ card.title }}</h3>
              <p class="hc-smarter__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Journey grid — Figma 285:10096 -->
    <section v-if="page.journey" class="hc-journey">
      <div class="hc-journey__head">
        <h2 class="hc-journey__title">{{ page.journey.title }}</h2>
        <p class="hc-journey__body">{{ page.journey.body }}</p>
      </div>
      <div class="hc-journey__grid" aria-label="Payment journey benefits">
        <article
          v-for="card in page.journey.cards || []"
          :key="card.title"
          class="hc-journey__card"
        >
          <div class="hc-journey__icon">
            <img :src="card.icon" alt="" width="28" height="28" decoding="async" />
          </div>
          <div class="hc-journey__card-text">
            <h3 class="hc-journey__card-title">{{ card.title }}</h3>
            <p class="hc-journey__card-body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Trust / capabilities — Figma 296:1980 -->
    <section v-if="page.trust" class="hc-trust">
      <div class="hc-trust__head">
        <h2 class="hc-trust__title">{{ page.trust.title }}</h2>
        <p class="hc-trust__body">{{ page.trust.body }}</p>
      </div>

      <div
        class="hc-trust__row"
        @mouseenter="pauseTrustTabs"
        @mouseleave="resumeTrustTabs"
        @focusin="pauseTrustTabs"
        @focusout="resumeTrustTabs"
      >
        <div
          class="hc-trust__tabs"
          role="tablist"
          aria-label="Checkout capabilities"
        >
          <button
            v-for="(card, index) in trustCards"
            :key="card.title"
            type="button"
            :id="`hc-trust-tab-${index}`"
            class="hc-trust__tab"
            :class="{ 'hc-trust__tab--active': activeTrust === index }"
            role="tab"
            :aria-selected="activeTrust === index"
            aria-controls="hc-trust-panel"
            @click="selectTrust(index)"
          >
            <span
              class="hc-trust__tab-icon"
              aria-hidden="true"
              :style="{ WebkitMaskImage: `url(${card.icon})`, maskImage: `url(${card.icon})` }"
            />
            <span class="hc-trust__tab-text">
              <span class="hc-trust__tab-title">{{ card.title }}</span>
              <span class="hc-trust__tab-body">{{ card.body }}</span>
            </span>
          </button>
        </div>
        <!-- Animated storyboard graphic (Figma 841:*); crossfade stays inside the graphic. -->
        <div
          id="hc-trust-panel"
          class="hc-trust__visual"
          role="tabpanel"
          :aria-labelledby="`hc-trust-tab-${activeTrust}`"
        >
          <HyperCheckoutTrustGraphic
            :active-index="activeTrust"
            :alt="trustAlt(trustCards[activeTrust] || {})"
          />
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.hc-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

/* —— Hero — Figma 285:9609 —— */
.hc-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.hc-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.hc-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.hc-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  min-height: 0;
  padding: 80px 56px 100px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.hc-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: min(804px, 100%);
  text-align: center;
}

.hc-hero__eyebrow {
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

.hc-hero__cta-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  width: min(808px, 100%);
}

.hc-hero__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(815px, 100%);
  text-align: center;
}

.hc-hero__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  text-transform: capitalize;
  color: #252b37;
}

.hc-hero__intro {
  margin: 0;
  max-width: 669px;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-hero__cta {
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

.hc-hero__cta:hover {
  background: #0a86ad;
}

.hc-hero__cta img {
  display: block;
  width: 18px;
  height: 18px;
}

/* —— Showcase — Figma 296:1744 —— */
.hc-showcase {
  max-width: 1291px;
  margin: 0 auto;
  padding: 0 74.5px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.hc-showcase__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(914px, 100%);
  text-align: center;
}

.hc-showcase__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.hc-showcase__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-showcase__visual {
  width: 100%;
  border-radius: 14.141px;
  overflow: hidden;
}

.hc-showcase__art > :deep(.hc-stage) {
  display: block;
  width: 100%;
}

/* —— Smarter — Figma 296:1397 —— */
.hc-smarter {
  /* Figma row 296:1396 is 1126 wide; 56px of padding sits either side of it. */
  max-width: 1238px;
  margin: 100px auto 0;
  padding: 0 56px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.hc-smarter__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(662px, 100%);
  text-align: center;
}

.hc-smarter__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.hc-smarter__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-smarter__row {
  display: flex;
  align-items: center;
  gap: 100px;
  width: 100%;
}

/* Figma 296:1395 / 744:8012 — 471.22 x 620.53. */
.hc-smarter__visual {
  flex: 0 1 471px;
  min-width: 0;
}

.hc-smarter__visual :deep(.hc-smart) {
  display: block;
  width: 100%;
  max-width: 471px;
  aspect-ratio: 471 / 621;
  height: auto;
  margin-inline: 0;
}

/* Legacy static SVG bleed (kept for fallbacks). */
.hc-smarter__visual > img {
  display: block;
  width: 112.6861%;
  max-width: none;
  height: auto;
  margin: -4.2708% -8.6968% -13.0177% -3.9892%;
}

/* Figma 296:1370 — 555 x 556 (4 cards of 124 + 3 gaps of 20). */
.hc-smarter__cards {
  flex: 1 1 555px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 555px;
  min-width: 0;
}

.hc-smarter__card {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  width: 100%;
  min-height: 124px;
  padding: 20px 24px;
  box-sizing: border-box;
  background: rgba(9, 116, 149, 0.05);
  border: 2px solid #097495;
  border-radius: 12px;
}

.hc-smarter__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 10px;
  box-sizing: border-box;
  background: #097495;
  border-radius: 4px;
}

.hc-smarter__icon img {
  display: block;
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.hc-smarter__card-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.hc-smarter__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.48px;
  color: #097495;
}

.hc-smarter__card-body {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.42px;
  color: #535862;
}

/* —— Journey — Figma 285:10096 —— */
.hc-journey {
  /* Figma's top row is three 363px cards with 32px gaps (1153); 56px either side. */
  max-width: 1265px;
  margin: 100px auto 0;
  padding: 0 56px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.hc-journey__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(797px, 100%);
  text-align: center;
}

.hc-journey__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
  color: #252b37;
}

.hc-journey__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-journey__grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px 32px;
  width: 100%;
}

/* Figma 285:10100 — 363x202, icon over centred text with no card surface. */
.hc-journey__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: min(363px, 100%);
  min-height: 202px;
  /* Figma's body text nodes are 349 wide; the browser needs ~352 to keep the
     longest one on three lines, so the side padding is kept narrow. */
  padding: 20px 4px;
  box-sizing: border-box;
}

.hc-journey__icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-shrink: 0;
  padding: 13.284px;
  box-sizing: border-box;
  background: rgba(9, 116, 149, 0.1);
  border-radius: 6.642px;
}

.hc-journey__icon img {
  display: block;
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.hc-journey__card-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  text-align: center;
}

.hc-journey__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.48px;
  color: #252b37;
}

.hc-journey__card-body {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: #535862;
}

/* —— Trust — Figma 296:1980 —— */
.hc-trust {
  max-width: 1254px;
  margin: 100px auto 0;
  padding: 0 56px 40px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.hc-trust__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(679px, 100%);
  text-align: center;
}

.hc-trust__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
  color: #252b37;
}

.hc-trust__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-trust__row {
  display: flex;
  align-items: center;
  gap: 83px;
  width: 100%;
}

.hc-trust__tabs {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: min(499px, 100%);
  flex-shrink: 0;
}

.hc-trust__tab {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  width: 100%;
  min-height: 146px;
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #d5d7da;
  border-radius: 12px;
  background: #ffffff;
  text-align: left;
  cursor: pointer;
  font: inherit;
  color: inherit;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.hc-trust__tab--active {
  background: #097495;
  border-color: #097495;
}

.hc-trust__tab-icon {
  display: block;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  background: #252b37;
  -webkit-mask-size: contain;
  mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
}

.hc-trust__tab--active .hc-trust__tab-icon {
  background: #ffffff;
}

.hc-trust__tab-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.hc-trust__tab-title {
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  letter-spacing: 0.6px;
  color: #252b37;
}

.hc-trust__tab-body {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.hc-trust__tab--active .hc-trust__tab-title {
  color: #ffffff;
}

.hc-trust__tab--active .hc-trust__tab-body {
  color: rgba(255, 255, 255, 0.8);
}

/* Fixed box: graphics have different aspect ratios; keep the row height stable. */
.hc-trust__visual {
  position: relative;
  flex: 1 1 0;
  min-width: 0;
  max-width: 672px;
  aspect-ratio: 706 / 644;
}

.hc-trust__visual :deep(.hc-trust-g) {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

@media (prefers-reduced-motion: reduce) {
  .hc-trust__visual :deep(.hc-trust-g__frame) {
    transition: none;
    transform: none;
  }
}

@media (max-width: 1200px) {
  .hc-hero__inner {
    padding: 64px 40px 100px;
    min-height: 0;
  }

  .hc-hero__title,
  .hc-showcase__title,
  .hc-smarter__title,
  .hc-journey__title,
  .hc-trust__title {
    font-size: 32px;
    line-height: 1.25;
  }

  .hc-showcase,
  .hc-smarter,
  .hc-journey,
  .hc-trust {
    padding-left: 40px;
    padding-right: 40px;
  }

  .hc-smarter__row,
  .hc-trust__row {
    flex-direction: column;
    gap: 40px;
  }

  .hc-smarter__visual,
  .hc-smarter__cards,
  .hc-trust__tabs,
  .hc-trust__visual {
    width: 100%;
    max-width: none;
  }

  /* Stacked: flex-basis would size the height, and the bleed compensation
     would push the artwork outside the viewport. */
  .hc-smarter__visual,
  .hc-smarter__cards {
    flex: 0 1 auto;
  }

  .hc-smarter__visual {
    max-width: 471px;
    margin: 0 auto;
  }

  .hc-smarter__visual > img {
    width: 100%;
    margin: 0;
  }

  .hc-smarter__visual :deep(.hc-smart) {
    max-width: 100%;
  }

  .hc-journey__grid {
    justify-content: stretch;
  }

  .hc-journey__card {
    width: calc(50% - 16px);
  }
}

@media (max-width: 700px) {
  .hc-hero__inner {
    padding: 48px 20px 100px;
  }

  .hc-hero__title {
    font-size: 28px;
  }

  .hc-hero__intro {
    font-size: 14px;
    line-height: 22px;
  }

  .hc-showcase {
    margin-top: 0;
  }

  .hc-showcase,
  .hc-smarter,
  .hc-journey,
  .hc-trust {
    padding-left: 20px;
    padding-right: 20px;
  }

  .hc-smarter,
  .hc-journey,
  .hc-trust {
    margin-top: 48px;
  }

  .hc-showcase__title,
  .hc-smarter__title,
  .hc-journey__title,
  .hc-trust__title {
    font-size: 26px;
    line-height: 1.3;
  }

  .hc-journey__grid {
    display: flex;
  }

  .hc-journey__card {
    width: 100%;
  }

  .hc-smarter__card {
    min-height: 0;
  }

  .hc-trust__tab {
    min-height: 0;
  }
}

@media (max-width: 767px) {
  .hc-page {
    margin-bottom: -44px;
  }

  /* Hero: chip 41px under the navbar */
  .hc-hero__inner {
    padding: 33px 16px 0;
  }

  .hc-hero__copy {
    gap: 24px;
    width: 100%;
  }

  .hc-hero__cta-block {
    gap: 24px;
  }

  .hc-hero__title,
  .hc-showcase__title,
  .hc-smarter__title,
  .hc-journey__title,
  .hc-trust__title {
    font-size: 28px;
    line-height: 36px;
    letter-spacing: -0.84px;
  }

  .hc-hero__intro,
  .hc-showcase__body,
  .hc-smarter__body,
  .hc-journey__body,
  .hc-trust__body {
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0;
  }

  .hc-hero__cta {
    height: 40px;
    padding: 0 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  /* Shared section rhythm */
  .hc-showcase,
  .hc-smarter,
  .hc-journey,
  .hc-trust {
    margin-top: 56px;
    padding: 0 16px;
    gap: 36px;
  }

  /* Showcase stage is drawn at its desktop width and scaled to the column (useScaledArt). */
  .hc-showcase__visual {
    height: var(--hc-art-height, auto);
    border-radius: calc(14.141px * var(--hc-art-scale, 1));
  }

  .hc-showcase__art {
    width: 1142px;
    transform: scale(var(--hc-art-scale, 1));
    transform-origin: 0 0;
  }

  /* Smarter: cards first, then the phone graphic */
  .hc-smarter__row {
    gap: 56px;
  }

  .hc-smarter__cards {
    order: -1;
    gap: 16px;
  }

  .hc-smarter__visual {
    width: 100%;
    max-width: none;
  }

  .hc-smarter__card {
    gap: 20px;
    padding: 19px 16px;
  }

  .hc-smarter__card-title,
  .hc-journey__card-title,
  .hc-trust__tab-title {
    font-size: 16px;
    line-height: 20px;
    letter-spacing: 0.48px;
  }

  .hc-smarter__card-body,
  .hc-trust__tab-body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.36px;
  }

  /* Journey: one centred card per row */
  .hc-journey {
    gap: 56px;
  }

  .hc-journey__card {
    padding: 20px 0;
  }

  .hc-journey__card-body {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0.36px;
  }

  /* Trust: graphic first, then the tabs */
  .hc-trust {
    padding-bottom: 0;
  }

  .hc-trust__row {
    gap: 24px;
  }

  .hc-trust__visual {
    order: -1;
  }

  .hc-trust__tabs {
    gap: 24px;
  }

  .hc-trust__tab {
    min-height: 125px;
  }
}
</style>

<style>
/* Shared closing sits outside this component; only this page's phone rhythm uses Figma's 56px gaps. */
@media (max-width: 767px) {
  .page-view:has(> .hc-page) > .site-closing > * + * {
    margin-top: 56px;
  }
}
</style>
