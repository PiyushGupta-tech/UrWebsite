<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import UpiPathSection from "./UpiPathSection.vue";
import UdPlatformDiagram from "./UdPlatformDiagram.vue";
import UdCascadingGraphic from "./UdCascadingGraphic.vue";
import UdVisibilityGraphic from "./UdVisibilityGraphic.vue";
import UdInsightsGraphic from "./UdInsightsGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);
const activeControl = ref(0);

const controlCards = computed(() => props.page?.control?.cards || []);
const featureRows = computed(() => props.page?.features?.rows || []);

function featureGraphic(row) {
  const src = String(row?.image || "");
  if (src.includes("visibility-graphic")) return "visibility";
  if (src.includes("cascading-graphic")) return "cascading";
  if (src.includes("insights-graphic")) return "insights";
  return null;
}

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});
</script>

<template>
  <main class="ud-page">
    <!-- Hero — Figma 689:2746 -->
    <section class="ud-hero" :class="{ 'ud-hero--ready': heroReady }">
      <div class="ud-hero__bg" aria-hidden="true">
        <img
          class="ud-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="ud-hero__inner">
        <p v-if="page.eyebrow" class="ud-hero__eyebrow">{{ page.eyebrow }}</p>
        <h1 class="ud-hero__title">{{ page.title }}</h1>
        <p class="ud-hero__intro">{{ page.intro }}</p>
        <RouterLink to="/contact" class="ud-hero__cta">
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
    </section>

    <!-- Platform — Figma 689:2851 -->
    <section v-if="page.platform" class="ud-section ud-section--platform">
      <div class="ud-section__head ud-section__head--center">
        <h2 class="ud-section__title">{{ page.platform.title }}</h2>
        <p class="ud-section__body">{{ page.platform.body }}</p>
      </div>
      <div class="ud-platform">
        <UdPlatformDiagram
          :image="page.platform.image"
          :alt="page.platform.image_alt || page.platform.title"
          :width="page.platform.image_width || 1291"
          :height="page.platform.image_height || 523"
        />
      </div>
    </section>

    <!-- Control cards — Figma 689:3335 -->
    <section v-if="page.control" class="ud-section ud-section--control">
      <div class="ud-section__head ud-section__head--center">
        <h2 class="ud-section__title ud-section__title--capitalize">
          {{ page.control.title }}
        </h2>
        <p class="ud-section__body">{{ page.control.body }}</p>
      </div>

      <div class="ud-control" aria-label="Payment control capabilities">
        <article
          v-for="(card, index) in controlCards"
          :key="card.title"
          class="ud-control__card"
          :class="{ 'ud-control__card--active': activeControl === index }"
          @mouseenter="activeControl = index"
          @focusin="activeControl = index"
        >
          <div class="ud-control__icon" aria-hidden="true">
            <img
              class="ud-control__icon-img"
              :src="card.icon"
              alt=""
              :width="card.icon_width || 28"
              :height="card.icon_height || 28"
              decoding="async"
            />
          </div>
          <div class="ud-control__text">
            <h3 class="ud-control__title">{{ card.title }}</h3>
            <p class="ud-control__body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Feature rows — Figma 689:3374 -->
    <section v-if="page.features" class="ud-section ud-section--features">
      <div class="ud-section__head ud-section__head--center">
        <h2 class="ud-section__title">{{ page.features.title }}</h2>
        <p class="ud-section__body">{{ page.features.body }}</p>
      </div>

      <div class="ud-features">
        <article
          v-for="(row, index) in featureRows"
          :key="row.title"
          class="ud-features__row"
          :class="{ 'ud-features__row--reverse': index % 2 === 1 }"
        >
          <div class="ud-features__visual">
            <UdVisibilityGraphic
              v-if="featureGraphic(row) === 'visibility'"
              :alt="row.image_alt || row.title"
            />
            <UdCascadingGraphic
              v-else-if="featureGraphic(row) === 'cascading'"
              :alt="row.image_alt || row.title"
            />
            <UdInsightsGraphic
              v-else-if="featureGraphic(row) === 'insights'"
              :alt="row.image_alt || row.title"
            />
            <img
              v-else
              :src="row.image"
              :alt="row.image_alt || row.title"
              :width="row.image_width || 704"
              :height="row.image_height || 352"
              decoding="async"
              loading="lazy"
            />
          </div>
          <div class="ud-features__copy">
            <h3 class="ud-features__title">{{ row.title }}</h3>
            <p class="ud-features__body">{{ row.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Path — Figma 689:3998 -->
    <UpiPathSection
      v-if="page.path"
      :path="page.path"
      :phone-home-offsets="{ trend: 0.2 }"
      aria-label="Unified dashboard operations path"
    />
  </main>
</template>

<style scoped>
.ud-page {
  width: 100%;
  background: #ffffff;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
  --ud-ink: #252b37;
  --ud-muted: #535862;
  --ud-brand: #097495;
}

/* —— Hero —— */
.ud-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  min-height: 594px;
  box-sizing: border-box;
  overflow: hidden;
  background: #ffffff;
}

.ud-hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.ud-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.ud-hero__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0;
  width: min(1240px, calc(100% - 48px));
  margin: 0 auto;
  padding: 100px 0 80px;
  box-sizing: border-box;
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.7s ease,
    transform 0.7s ease;
}

.ud-hero--ready .ud-hero__inner {
  opacity: 1;
  transform: none;
}

.ud-hero__eyebrow {
  margin: 0 0 16px;
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

.ud-hero__title {
  margin: 0;
  width: max-content;
  max-width: 100%;
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  color: var(--ud-ink);
  white-space: nowrap;
}

.ud-hero__intro {
  margin: 12px 0 0;
  max-width: 669px;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.96px;
  color: var(--ud-muted);
}

.ud-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  margin-top: 40px;
  padding: 16px;
  border-radius: 8px;
  background: var(--ud-brand);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  box-sizing: border-box;
  transition: background 0.2s ease;
}

.ud-hero__cta:hover {
  background: #075f7a;
}

.ud-hero__cta img {
  display: block;
}

/* —— Shared sections —— */
.ud-section {
  width: min(1291px, calc(100% - 48px));
  margin-inline: auto;
  box-sizing: border-box;
}

.ud-section__head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ud-section__head--center {
  align-items: center;
  text-align: center;
  margin-inline: auto;
}

.ud-section__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--ud-ink);
}

.ud-section__title--capitalize {
  text-transform: capitalize;
}

.ud-section__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--ud-muted);
}

/* —— Platform —— */
.ud-section--platform {
  margin-top: 0;
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.ud-section--platform .ud-section__head {
  width: min(941px, 100%);
}

.ud-platform {
  width: 100%;
  line-height: 0;
}

.ud-platform__img {
  display: block;
  width: 100%;
  height: auto;
  max-width: 1291px;
  margin-inline: auto;
}

/* —— Control cards —— */
.ud-section--control {
  margin-top: 100px;
  width: min(1204px, calc(100% - 48px));
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.ud-section--control .ud-section__head {
  width: min(809px, 100%);
}

.ud-control {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  align-items: stretch;
}

.ud-control__card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 272px;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e9eaeb;
  background: #ffffff;
  box-sizing: border-box;
  overflow: hidden;
  transition:
    border-color 0.35s ease,
    box-shadow 0.35s ease;
}

.ud-control__card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: #097495;
  border-radius: 16px 16px 0 0;
  transform: scaleY(0);
  transform-origin: top center;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
}

.ud-control__card--active {
  border-color: transparent;
  box-shadow: 0 0 80px rgba(0, 0, 0, 0.06);
}

.ud-control__card--active::before {
  transform: scaleY(1);
}

.ud-control__icon {
  position: relative;
  width: 55px;
  height: 55px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #097495;
  /* Footprint fixed at 55×55; inactive reads as 48px circle via scale */
  transform: scale(0.8727);
  transform-origin: center center;
  will-change: border-radius, transform;
  transition:
    border-radius 0.55s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

.ud-control__card--active .ud-control__icon {
  border-radius: 6.642px;
  transform: scale(1);
}

.ud-control__icon-img {
  display: block;
  max-width: 28px;
  max-height: 28px;
  transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

.ud-control__card--active .ud-control__icon-img {
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .ud-control__icon,
  .ud-control__icon-img {
    transition-duration: 0.01ms;
  }
}

.ud-control__text {
  display: flex;
  flex-direction: column;
  gap: 7px;
  width: 100%;
  min-width: 0;
}

.ud-control__title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: var(--ud-ink);
}

.ud-control__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: var(--ud-muted);
  height: calc(24px * 5);
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 5;
}

/* —— Features —— */
.ud-section--features {
  margin-top: 100px;
  width: min(1200px, calc(100% - 48px));
  display: flex;
  flex-direction: column;
  gap: 56px;
  padding-bottom: 40px;
}

.ud-section--features .ud-section__head {
  width: min(844px, 100%);
}

.ud-features {
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.ud-features__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 48px;
}

.ud-features__row--reverse {
  flex-direction: row-reverse;
}

.ud-features__visual {
  flex: 1 1 570px;
  min-width: 0;
  line-height: 0;
}

.ud-features__visual img {
  display: block;
  width: 100%;
  height: auto;
  max-width: 704px;
}

.ud-features__visual :deep(.ud-vis) {
  width: 100%;
  max-width: 571px;
}

.ud-features__visual :deep(.ud-casc) {
  width: 100%;
  max-width: 709px;
}

.ud-features__visual :deep(.ud-ins) {
  width: 100%;
  max-width: 600px;
}

.ud-features__copy {
  flex: 0 1 480px;
  max-width: 480px;
  min-width: min(360px, 100%);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ud-features__title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: 32px;
  color: var(--ud-ink);
}

.ud-features__body {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: var(--ud-muted);
  opacity: 0.8;
}

@media (max-width: 1100px) {
  .ud-hero__title {
    white-space: normal;
    width: auto;
  }

  .ud-control {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .ud-features__row,
  .ud-features__row--reverse {
    flex-direction: column;
    align-items: stretch;
    gap: 28px;
  }

  .ud-features__copy {
    max-width: none;
    min-width: 0;
  }
}

@media (max-width: 720px) {
  .ud-hero__title,
  .ud-section__title {
    font-size: 32px;
    line-height: 40px;
  }

  .ud-hero__intro,
  .ud-section__body {
    letter-spacing: 0.4px;
  }

  .ud-control {
    grid-template-columns: 1fr;
  }

  .ud-section,
  .ud-section--control,
  .ud-section--features {
    width: calc(100% - 32px);
  }
}

/* —— Phone — Figma 931:5011 —— */
@media (max-width: 767px) {
  .ud-page {
    margin-bottom: -44px;
  }

  /* Hero: chip 41px under the navbar */
  .ud-hero {
    min-height: 0;
  }

  .ud-hero__inner {
    width: calc(100% - 32px);
    padding: 33px 0 0;
  }

  .ud-hero__eyebrow {
    margin-bottom: 24px;
  }

  .ud-hero__title,
  .ud-section__title {
    font-size: 28px;
    line-height: 36px;
    letter-spacing: -0.84px;
  }

  .ud-hero__intro,
  .ud-section__body {
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0;
  }

  .ud-hero__cta {
    height: 40px;
    margin-top: 24px;
    padding: 0 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  .ud-section,
  .ud-section--control,
  .ud-section--features {
    width: calc(100% - 32px);
  }

  .ud-section--platform {
    margin-top: 56px;
  }

  .ud-section--control,
  .ud-section--features {
    margin-top: 56px;
  }

  .ud-section--platform,
  .ud-section--control,
  .ud-section--features {
    gap: 36px;
  }

  .ud-platform {
    width: calc(100% - 8px);
    margin-inline: auto;
  }

  /* Control: stacked cards, 44px icons */
  .ud-control {
    gap: 24px;
  }

  .ud-control__card {
    height: auto;
    padding: 19px;
    gap: 16px;
  }

  .ud-control__icon,
  .ud-control__card--active .ud-control__icon {
    width: 44px;
    height: 44px;
    transform: none;
  }

  .ud-control__card--active .ud-control__icon {
    border-radius: 5.779px;
  }

  .ud-control__icon-img {
    max-width: 20px;
    max-height: 20px;
  }

  .ud-control__text {
    gap: 8px;
  }

  .ud-control__title,
  .ud-features__title {
    font-size: 16px;
    font-weight: 600;
    line-height: 20px;
  }

  .ud-control__body {
    height: auto;
    font-size: 12px;
    line-height: 18px;
  }

  /* Features: graphic over copy */
  .ud-section--features {
    padding-bottom: 0;
  }

  .ud-features {
    gap: 36px;
  }

  .ud-features__row,
  .ud-features__row--reverse {
    gap: 24px;
  }

  .ud-features__visual,
  .ud-features__copy {
    flex: none;
  }

  .ud-features__copy {
    gap: 8px;
  }

  .ud-features__title {
    letter-spacing: -0.48px;
  }

  .ud-features__body {
    font-size: 12px;
    line-height: 18px;
    letter-spacing: 0.48px;
    opacity: 1;
  }

  /* Path: Figma's ring frame starts 56px under the features; the cropped stage begins 62px into it. */
  .ud-page :deep(.upi-path) {
    margin-top: 118px;
    padding: 0 16px;
  }

  /* Copy is taller than the stage at narrow widths, so let it run into the gap below. */
  .ud-page :deep(.upi-path__stage) {
    overflow: visible;
  }

  .ud-page :deep(.upi-path__copy) {
    top: 0;
    width: max(234px, 64.8%);
    gap: 12px;
  }

  .ud-page :deep(.upi-path__title) {
    font-size: 16px;
    font-weight: 600;
    line-height: 20px;
    color: #252b37;
  }

  .ud-page :deep(.upi-path__body) {
    font-size: 12px;
    line-height: 18px;
    color: #535862;
  }

  .ud-page :deep(.upi-path__badge) {
    width: 16px;
    border-width: 0.5px;
  }
}
</style>

<style>
/* Shared closing sits outside this component; only this page's phone rhythm uses Figma's 56px gaps. */
@media (max-width: 767px) {
  .page-view:has(> .ud-page) > .site-closing > * + * {
    margin-top: 56px;
  }
}
</style>
