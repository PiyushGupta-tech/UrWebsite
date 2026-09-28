<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import UpiPathSection from "./UpiPathSection.vue";
import ReconciliationClarityDiagram from "./ReconciliationClarityDiagram.vue";
import RcExceptionGraphic from "./RcExceptionGraphic.vue";
import RcMatchingGraphic from "./RcMatchingGraphic.vue";
import RcReconciledGraphic from "./RcReconciledGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);

const featureCards = computed(() => props.page?.features?.cards || []);
const showcaseRows = computed(() => props.page?.showcase?.rows || []);
/** Showcase images replaced by an animated inline version of the same artwork. */
const SHOWCASE_GRAPHICS = {
  "/images/figma-reconciliation/Frame%202147226717.svg": RcMatchingGraphic,
  "/images/figma-reconciliation/Group%201171275349.svg": RcReconciledGraphic,
  "/images/figma-reconciliation/Frame%202147226952.svg?v=2": RcExceptionGraphic,
};

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});
</script>

<template>
  <main class="rc-page">
    <!-- Hero — Figma 461:7155 -->
    <section class="rc-hero" :class="{ 'rc-hero--ready': heroReady }">
      <div class="rc-hero__bg" aria-hidden="true">
        <img
          class="rc-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="rc-hero__inner">
        <div class="rc-hero__copy">
          <p v-if="page.eyebrow" class="rc-hero__eyebrow">{{ page.eyebrow }}</p>
          <h1 class="rc-hero__title">{{ page.title }}</h1>
          <p class="rc-hero__intro">{{ page.intro }}</p>
          <RouterLink to="/contact" class="rc-hero__cta">
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

        <div class="rc-hero__visual">
          <img
            class="rc-hero__graphic"
            src="/images/figma-reconciliation/Frame%202147226845.svg"
            :alt="page.hero_image_alt || page.title"
            width="563"
            height="492"
            decoding="async"
          />
        </div>
      </div>
    </section>

    <!-- Clarity — Figma 652:9451 -->
    <section v-if="page.clarity" class="rc-section rc-section--clarity">
      <div class="rc-section__head rc-section__head--center">
        <h2 class="rc-section__title">{{ page.clarity.title }}</h2>
        <p class="rc-section__body">{{ page.clarity.body }}</p>
      </div>
      <div class="rc-clarity__diagram">
        <ReconciliationClarityDiagram
          :image="page.clarity.image"
          :alt="page.clarity.image_alt || page.clarity.title"
          :width="page.clarity.image_width || 1291"
          :height="page.clarity.image_height || 627"
        />
      </div>
    </section>

    <!-- Features — Figma 461:7615 -->
    <section v-if="page.features" class="rc-section rc-section--features">
      <div class="rc-features">
        <div class="rc-features__copy">
          <h2 class="rc-features__title">{{ page.features.title }}</h2>
          <p class="rc-features__body">{{ page.features.body }}</p>
        </div>

        <div class="rc-features__cards" aria-label="Reconciliation capabilities">
          <article
            v-for="card in featureCards"
            :key="card.title"
            class="rc-features__card"
          >
            <div class="rc-features__icon" aria-hidden="true">
              <img
                :src="card.icon"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
            </div>
            <h3 class="rc-features__card-title">{{ card.title }}</h3>
            <p class="rc-features__card-body">{{ card.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Path — Figma 461:7587 (shared UpiPathSection orbits + animated badges) -->
    <UpiPathSection
      v-if="page.path"
      :path="page.path"
      aria-label="Reconciliation path"
    />

    <!-- Showcase rows — Figma 652:8971 -->
    <section v-if="page.showcase" class="rc-section rc-section--showcase">
      <div class="rc-section__head rc-section__head--center">
        <h2 class="rc-section__title">{{ page.showcase.title }}</h2>
        <p class="rc-section__body">{{ page.showcase.body }}</p>
      </div>

      <div class="rc-showcase" aria-label="Reconciliation showcase">
        <article
          v-for="row in showcaseRows"
          :key="row.title"
          class="rc-showcase__row"
          :class="`rc-showcase__row--${row.side || 'left'}`"
        >
          <div class="rc-showcase__visual">
            <component
              :is="SHOWCASE_GRAPHICS[row.image]"
              v-if="SHOWCASE_GRAPHICS[row.image]"
              class="rc-showcase__img"
              :alt="row.image_alt || row.title"
            />
            <img
              v-else
              class="rc-showcase__img"
              :src="row.image"
              :alt="row.image_alt || row.title"
              :width="row.image_width || 640"
              :height="row.image_height || 363"
              decoding="async"
              loading="lazy"
            />
          </div>
          <div class="rc-showcase__copy">
            <h3 class="rc-showcase__title">{{ row.title }}</h3>
            <p class="rc-showcase__body">{{ row.body }}</p>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.rc-page {
  width: 100%;
  background: #ffffff;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

/* —— Hero — Figma 461:7155 —— */
.rc-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.rc-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.rc-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.rc-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  min-height: calc(100svh - var(--page-nav-offset, 129px));
  padding: 0 74px 40px 119px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 517fr) minmax(0, 559fr);
  column-gap: 126px;
  align-items: center;
}

.rc-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: center;
  max-width: 517px;
  width: 100%;
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.55s ease,
    transform 0.55s ease;
}

.rc-hero--ready .rc-hero__copy {
  opacity: 1;
  transform: none;
}

.rc-hero__eyebrow {
  margin: 0 0 18px;
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  font-size: 12px;
  font-weight: 700;
  line-height: 20px;
  letter-spacing: 1.78px;
  text-transform: uppercase;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.rc-hero__title {
  margin: 0 0 12px;
  font-size: 42px;
  font-weight: 700;
  line-height: 1.2;
  color: #252b37;
  text-transform: capitalize;
}

.rc-hero__intro {
  margin: 0 0 40px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.56px;
  color: #535862;
}

.rc-hero__cta {
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

.rc-hero__cta:hover {
  background: #0a86ad;
}

.rc-hero__cta img {
  display: block;
}

.rc-hero__visual {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  min-width: 0;
  width: 100%;
}

.rc-hero__graphic {
  display: block;
  width: 100%;
  max-width: 563px;
  height: auto;
  aspect-ratio: 563 / 492;
  object-fit: contain;
  object-position: center;
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.7s ease,
    transform 0.7s ease;
}

.rc-hero--ready .rc-hero__graphic {
  opacity: 1;
  transform: none;
}

/* —— Shared section —— */
.rc-section {
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  padding: 0 75px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rc-section__head {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: min(809px, 100%);
}

.rc-section__head--center {
  align-items: center;
  text-align: center;
}

.rc-section__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.rc-section__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* —— Clarity —— */
.rc-section--clarity {
  margin-top: 96px;
  gap: 48px;
}

.rc-clarity__diagram {
  width: min(1291px, 100%);
}

/* —— Features —— */
.rc-section--features {
  margin-top: 96px;
  padding: 0 75px;
}

.rc-features {
  width: min(1275px, 100%);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 86px;
}

.rc-features__copy {
  width: 485px;
  max-width: 100%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rc-features__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.rc-features__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.rc-features__cards {
  width: 682px;
  flex-shrink: 0;
  display: grid;
  grid-template-columns: repeat(2, 329px);
  grid-template-rows: repeat(2, 263px);
  gap: 24px;
}

.rc-features__card {
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

.rc-features__card:hover {
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

.rc-features__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 54.57px;
  height: 54.57px;
  padding: 13.284px;
  box-sizing: border-box;
  border-radius: 6.642px;
  background: #097495;
  flex-shrink: 0;
}

.rc-features__icon img {
  display: block;
  width: 28px;
  height: 28px;
}

.rc-features__card-title {
  margin: 0;
  width: 100%;
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  color: #252b37;
}

.rc-features__card-body {
  margin: 0;
  width: 100%;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.48px;
  color: #535862;
}

/* —— Showcase —— */
.rc-section--showcase {
  margin-top: 72px;
  margin-bottom: 40px;
  gap: 56px;
}

.rc-showcase {
  width: min(1218px, 100%);
  display: flex;
  flex-direction: column;
  gap: 80px;
}

.rc-showcase__row {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  align-items: center;
  gap: 64px;
}

.rc-showcase__row--right {
  grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr);
}

.rc-showcase__row--right .rc-showcase__visual {
  order: 2;
}

.rc-showcase__row--right .rc-showcase__copy {
  order: 1;
}

.rc-showcase__visual {
  width: 100%;
  display: flex;
  justify-content: center;
}

.rc-showcase__img {
  display: block;
  width: 100%;
  max-width: 640px;
  height: auto;
}

.rc-showcase__copy {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 488px;
}

.rc-showcase__title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  line-height: 36px;
  color: #252b37;
}

.rc-showcase__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

@media (max-width: 1200px) {
  .rc-hero__inner {
    grid-template-columns: 1fr;
    column-gap: 40px;
    padding: 48px 40px 64px;
    min-height: 0;
  }

  .rc-hero__copy {
    max-width: 640px;
  }

  .rc-hero__visual {
    justify-content: center;
  }

  .rc-features {
    flex-direction: column;
    align-items: flex-start;
    gap: 40px;
  }

  .rc-features__cards {
    width: 100%;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-template-rows: auto;
  }

  .rc-features__card {
    width: 100%;
    height: auto;
    min-height: 220px;
  }

  .rc-showcase__row,
  .rc-showcase__row--right {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .rc-showcase__row--right .rc-showcase__visual,
  .rc-showcase__row--right .rc-showcase__copy {
    order: initial;
  }
}

@media (max-width: 720px) {
  .rc-hero__inner,
  .rc-section,
  .rc-section--features {
    padding-inline: 20px;
  }

  .rc-hero__title,
  .rc-section__title,
  .rc-features__title {
    font-size: 32px;
    line-height: 42px;
  }

  .rc-features__cards {
    grid-template-columns: 1fr;
  }
}
</style>
