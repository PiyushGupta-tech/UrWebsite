<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { useScaledArt } from "@/composables/useScaledArt.js";
import CustomCheckoutShowcaseGraphic from "./CustomCheckoutShowcaseGraphic.vue";
import CustomCheckoutFeatureBranding from "./CustomCheckoutFeatureBranding.vue";
import CustomCheckoutFeatureMethods from "./CustomCheckoutFeatureMethods.vue";
import CustomCheckoutFeatureDesign from "./CustomCheckoutFeatureDesign.vue";

const props = defineProps({
  page: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  relatedLinks: { type: Array, default: () => [] },
});

const featureGraphics = {
  branding: CustomCheckoutFeatureBranding,
  methods: CustomCheckoutFeatureMethods,
  design: CustomCheckoutFeatureDesign,
};

/** Figma 283:9211 left col (offset): cards 0,2; right col 283:9228: cards 1,3 */
const benefitsLeft = computed(() => {
  const cards = props.page?.benefits?.cards || [];
  return [cards[0], cards[2]].filter(Boolean);
});
const benefitsRight = computed(() => {
  const cards = props.page?.benefits?.cards || [];
  return [cards[1], cards[3]].filter(Boolean);
});

/** Phones draw each graphic at its desktop width and scale it to the column. */
const registerArtFrame = useScaledArt("cc");
</script>

<template>
  <main class="cc-page">
    <!-- Hero — Figma 283:8546 / 283:8642 -->
    <section class="cc-hero">
      <div class="cc-hero__bg" aria-hidden="true">
        <img
          class="cc-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="cc-hero__inner">
        <div class="cc-hero__copy">
          <p v-if="page.eyebrow" class="cc-hero__eyebrow">{{ page.eyebrow }}</p>
          <div class="cc-hero__cta-block">
            <div class="cc-hero__text">
              <h1 class="cc-hero__title">{{ page.title }}</h1>
              <p class="cc-hero__intro">{{ page.intro }}</p>
            </div>
            <RouterLink to="/contact" class="cc-hero__cta">
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

    <!-- Showcase — Figma 283:8649 + 283:8650 -->
    <section v-if="page.showcase" class="cc-showcase">
      <div class="cc-showcase__head">
        <h2 class="cc-showcase__title">{{ page.showcase.title }}</h2>
        <p class="cc-showcase__body">{{ page.showcase.body }}</p>
      </div>
      <div :ref="registerArtFrame" class="cc-showcase__visual">
        <div class="cc-showcase__art">
          <CustomCheckoutShowcaseGraphic />
        </div>
      </div>
    </section>

    <!-- Features — Figma 283:8844 -->
    <section v-if="page.features" class="cc-features">
      <div class="cc-features__head">
        <h2 class="cc-features__title">{{ page.features.title }}</h2>
        <p class="cc-features__body">{{ page.features.body }}</p>
      </div>

      <div class="cc-features__list">
        <div
          v-for="item in page.features.items || []"
          :key="item.title"
          class="cc-features__row"
          :class="{ 'cc-features__row--reverse': item.reverse }"
        >
          <div class="cc-features__visual">
            <div
              v-if="item.graphic && featureGraphics[item.graphic]"
              :ref="registerArtFrame"
              class="cc-features__frame"
            >
              <div class="cc-features__art">
                <component :is="featureGraphics[item.graphic]" :aria-label="item.title" />
              </div>
            </div>
            <img
              v-else
              :src="item.image"
              :alt="item.title"
              :width="item.image_width || 616"
              :height="item.image_height || 351"
              decoding="async"
            />
          </div>
          <div class="cc-features__copy">
            <h3 class="cc-features__name">{{ item.title }}</h3>
            <p class="cc-features__desc">{{ item.body }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits — Figma 283:9206 -->
    <section v-if="page.benefits" class="cc-benefits">
      <div class="cc-benefits__copy">
        <h2 class="cc-benefits__title">{{ page.benefits.title }}</h2>
        <p class="cc-benefits__body">{{ page.benefits.body }}</p>
      </div>
      <div class="cc-benefits__cards" aria-label="Benefits">
        <div class="cc-benefits__col cc-benefits__col--offset">
          <article
            v-for="card in benefitsLeft"
            :key="card.title"
            class="cc-benefits__card"
          >
            <div class="cc-benefits__icon">
              <img :src="card.icon" alt="" width="26" height="26" decoding="async" />
            </div>
            <div class="cc-benefits__card-text">
              <h3 class="cc-benefits__card-title">{{ card.title }}</h3>
              <p class="cc-benefits__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
        <div class="cc-benefits__col">
          <article
            v-for="card in benefitsRight"
            :key="card.title"
            class="cc-benefits__card"
          >
            <div class="cc-benefits__icon">
              <img :src="card.icon" alt="" width="26" height="26" decoding="async" />
            </div>
            <div class="cc-benefits__card-text">
              <h3 class="cc-benefits__card-title">{{ card.title }}</h3>
              <p class="cc-benefits__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.cc-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

/* —— Hero — Figma 283:8546 (1440×600) —— */
.cc-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.cc-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.cc-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.cc-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  min-height: min(471px, calc(100svh - var(--page-nav-offset, 129px)));
  padding: 80px 56px 48px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.cc-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: min(804px, 100%);
  text-align: center;
}

.cc-hero__eyebrow {
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

.cc-hero__cta-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  width: min(808px, 100%);
}

.cc-hero__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(815px, 100%);
  text-align: center;
}

.cc-hero__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  text-transform: capitalize;
  color: #252b37;
}

.cc-hero__intro {
  margin: 0;
  max-width: 669px;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.cc-hero__cta {
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

.cc-hero__cta:hover {
  background: #0a86ad;
}

.cc-hero__cta img {
  display: block;
  width: 18px;
  height: 18px;
}

/* —— Showcase — Figma 283:8649 + 283:8650 —— */
.cc-showcase {
  max-width: 1291px;
  margin: 56px auto 0;
  padding: 0 74.5px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.cc-showcase__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(914px, 100%);
  text-align: center;
}

.cc-showcase__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.cc-showcase__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.cc-showcase__visual {
  width: 100%;
  border-radius: 14.141px;
  overflow: hidden;
}

/* —— Features — Figma 283:8844 —— */
.cc-features {
  max-width: 1212px;
  margin: 100px auto 0;
  padding: 0 56px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.cc-features__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(788px, 100%);
  text-align: center;
}

.cc-features__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.cc-features__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.cc-features__list {
  display: flex;
  flex-direction: column;
  gap: 36px;
  width: 100%;
}

.cc-features__row {
  display: flex;
  align-items: center;
  gap: 96px;
  width: 100%;
}

.cc-features__row--reverse {
  flex-direction: row-reverse;
  gap: 48px;
}

.cc-features__visual {
  flex: 0 1 auto;
  width: min(637px, 52%);
}

.cc-features__visual > img {
  display: block;
  width: 100%;
  height: auto;
}

.cc-features__visual > :not(img) {
  display: block;
  width: 100%;
}

.cc-features__copy {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 480px;
  min-width: 0;
}

.cc-features__name {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: 32px;
  color: #1c1f25;
}

.cc-features__desc {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: #535862;
  opacity: 0.8;
}

/* —— Benefits — Figma 283:9206 —— */
.cc-benefits {
  max-width: 1440px;
  margin: 100px auto 0;
  padding: 0 114px 40px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 544px) minmax(0, 610px);
  gap: 86px;
  align-items: center;
  justify-content: center;
}

.cc-benefits__copy {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 544px;
}

.cc-benefits__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.cc-benefits__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.cc-benefits__cards {
  position: relative;
  width: 100%;
  max-width: 610px;
  height: 467px;
  justify-self: end;
}

.cc-benefits__col {
  position: absolute;
  top: 0;
  width: 287px;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.cc-benefits__col--offset {
  left: 0;
  top: 73px;
}

.cc-benefits__col:not(.cc-benefits__col--offset) {
  left: 323px;
  top: 0;
}

.cc-benefits__card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  min-height: 179px;
  padding: 20px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 14.141px;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.25s ease;
}

.cc-benefits__card:hover {
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

@media (prefers-reduced-motion: reduce) {
  .cc-benefits__card {
    transition: none;
  }
}

.cc-benefits__icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-shrink: 0;
  width: fit-content;
  padding: 13.284px;
  box-sizing: border-box;
  background: rgba(9, 116, 149, 0.1);
  border-radius: 6.642px;
}

.cc-benefits__icon img {
  display: block;
  width: 26px;
  height: 26px;
  object-fit: contain;
}

.cc-benefits__card-text {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.cc-benefits__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.48px;
  color: #252b37;
}

.cc-benefits__card-body {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: #535862;
}

@media (max-width: 1200px) {
  .cc-hero__inner {
    padding: 64px 40px 40px;
    min-height: 0;
  }

  .cc-hero__title,
  .cc-showcase__title,
  .cc-features__title {
    font-size: 32px;
    line-height: 1.25;
  }

  .cc-benefits__title {
    font-size: 42px;
    line-height: 56px;
  }

  .cc-showcase,
  .cc-features,
  .cc-benefits {
    padding-left: 40px;
    padding-right: 40px;
  }

  .cc-features__row,
  .cc-features__row--reverse {
    flex-direction: column;
    gap: 32px;
  }

  .cc-features__visual {
    width: 100%;
  }

  .cc-features__copy {
    max-width: none;
  }

  .cc-benefits {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .cc-benefits__cards {
    height: auto;
    max-width: none;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    justify-self: stretch;
  }

  .cc-benefits__col {
    position: static;
    width: auto;
    gap: 24px;
  }

  .cc-benefits__col--offset {
    top: auto;
  }
}

@media (max-width: 700px) {
  .cc-hero__inner {
    padding: 48px 20px 32px;
  }

  .cc-hero__title {
    font-size: 28px;
  }

  .cc-hero__intro {
    font-size: 14px;
    line-height: 22px;
  }

  .cc-showcase,
  .cc-features,
  .cc-benefits {
    margin-top: 48px;
    padding-left: 20px;
    padding-right: 20px;
  }

  .cc-showcase__title,
  .cc-features__title {
    font-size: 26px;
    line-height: 1.3;
  }

  .cc-benefits__title {
    font-size: 42px;
    line-height: 1.3;
  }

  .cc-features__name {
    font-size: 20px;
    line-height: 28px;
  }

  .cc-benefits__cards {
    grid-template-columns: 1fr;
  }

  .cc-benefits {
    padding-bottom: 24px;
  }
}

@media (max-width: 767px) {
  .cc-page {
    margin-bottom: -44px;
  }

  /* Hero: chip 41px under the navbar */
  .cc-hero__inner {
    min-height: 0;
    padding: 33px 16px 0;
  }

  .cc-hero__copy {
    gap: 24px;
    width: 100%;
  }

  .cc-hero__cta-block {
    gap: 24px;
  }

  .cc-hero__title,
  .cc-showcase__title,
  .cc-features__title,
  .cc-benefits__title {
    font-size: 28px;
    line-height: 36px;
    letter-spacing: -0.84px;
  }

  .cc-hero__intro,
  .cc-showcase__body,
  .cc-features__body,
  .cc-benefits__body {
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0;
  }

  .cc-hero__cta {
    height: 40px;
    padding: 0 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  /* Shared section rhythm */
  .cc-showcase,
  .cc-features,
  .cc-benefits {
    margin-top: 56px;
    padding: 0 16px;
    gap: 36px;
  }

  .cc-showcase__head,
  .cc-features__head,
  .cc-benefits__copy {
    gap: 12px;
  }

  /* Graphics are drawn at their desktop width and scaled to the column (useScaledArt). */
  .cc-showcase__visual {
    height: var(--cc-art-height, auto);
    border-radius: calc(14.141px * var(--cc-art-scale, 1));
  }

  .cc-showcase__art,
  .cc-features__art {
    transform: scale(var(--cc-art-scale, 1));
    transform-origin: 0 0;
  }

  .cc-showcase__art {
    width: 1142px;
  }

  .cc-features__frame {
    height: var(--cc-art-height, auto);
  }

  .cc-features__art {
    width: 572px;
  }

  /* Features: graphic over copy */
  .cc-features__row,
  .cc-features__row--reverse {
    gap: 24px;
  }

  .cc-features__copy {
    gap: 8px;
  }

  .cc-features__name {
    font-size: 16px;
    font-weight: 700;
    line-height: 20px;
    letter-spacing: -0.48px;
    color: #252b37;
  }

  .cc-features__desc {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.48px;
    opacity: 1;
  }

  /* Benefits: centred heading over one column of cards in data order */
  .cc-benefits {
    padding-bottom: 0;
  }

  .cc-benefits__copy {
    max-width: none;
    text-align: center;
  }

  .cc-benefits__cards {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: calc(100% - 2px);
    justify-self: center;
  }

  .cc-benefits__col {
    display: contents;
  }

  .cc-benefits__col--offset .cc-benefits__card:nth-child(1) {
    order: 1;
  }

  .cc-benefits__col:not(.cc-benefits__col--offset) .cc-benefits__card:nth-child(1) {
    order: 2;
  }

  .cc-benefits__col--offset .cc-benefits__card:nth-child(2) {
    order: 3;
  }

  .cc-benefits__col:not(.cc-benefits__col--offset) .cc-benefits__card:nth-child(2) {
    order: 4;
  }

  .cc-benefits__card {
    justify-content: center;
    gap: 12px;
    min-height: 0;
    border-radius: 12px;
  }

  .cc-benefits__icon {
    align-items: center;
    width: 52px;
    height: 52px;
    padding: 12px;
    border-radius: 4px;
  }

  .cc-benefits__card-text {
    gap: 8px;
  }

  .cc-benefits__card-title {
    line-height: 20px;
  }

  .cc-benefits__card-body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.36px;
  }
}
</style>

<style>
/* Shared closing sits outside this component; only this page's phone rhythm uses Figma's 56px gaps. */
@media (max-width: 767px) {
  .page-view:has(> .cc-page) > .site-closing > * + * {
    margin-top: 56px;
  }
}
</style>
