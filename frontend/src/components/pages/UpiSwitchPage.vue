<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import UpiArchitectureDiagram from "./UpiArchitectureDiagram.vue";
import UpiPathSection from "./UpiPathSection.vue";
import UpiCapsConnectivityGraphic from "./UpiCapsConnectivityGraphic.vue";
import UpiCapsRoutingGraphic from "./UpiCapsRoutingGraphic.vue";
import UpiCapsVisibilityGraphic from "./UpiCapsVisibilityGraphic.vue";
import UpiCapsScaleGraphic from "./UpiCapsScaleGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);

const featureCards = computed(() => props.page?.features?.cards || []);
const capabilityCards = computed(() => props.page?.capabilities?.cards || []);

function capGraphic(card) {
  const title = String(card?.title || "").toLowerCase();
  if (title.includes("connectivity")) return "connectivity";
  if (title.includes("routing")) return "routing";
  if (title.includes("visibility")) return "visibility";
  if (title.includes("scale")) return "scale";
  return null;
}

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});
</script>

<template>
  <main class="upi-page">
    <!-- Hero — Figma 466:17722 -->
    <section class="upi-hero" :class="{ 'upi-hero--ready': heroReady }">
      <div class="upi-hero__bg" aria-hidden="true">
        <img
          class="upi-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="upi-hero__inner">
        <div class="upi-hero__copy">
          <p v-if="page.eyebrow" class="upi-hero__eyebrow">{{ page.eyebrow }}</p>
          <div class="upi-hero__cta-block">
            <div class="upi-hero__text">
              <h1 class="upi-hero__title">{{ page.title }}</h1>
              <p class="upi-hero__intro">{{ page.intro }}</p>
            </div>
            <RouterLink to="/contact" class="upi-hero__cta">
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

    <!-- Architecture — Figma 466:17859 / diagram 296:2487 (composed parts) -->
    <section v-if="page.architecture" class="upi-arch">
      <div class="upi-arch__head">
        <h2 class="upi-arch__title">{{ page.architecture.title }}</h2>
        <p class="upi-arch__body">{{ page.architecture.body }}</p>
      </div>
      <div class="upi-arch__visual">
        <UpiArchitectureDiagram
          :ready="heroReady"
          :alt="page.architecture.image_alt || page.architecture.title"
        />
      </div>
    </section>

    <!-- Features — Figma 466:18031 -->
    <section v-if="page.features" class="upi-features">
      <div class="upi-features__head">
        <h2 class="upi-features__title">{{ page.features.title }}</h2>
        <p class="upi-features__body">{{ page.features.body }}</p>
      </div>
      <div class="upi-features__grid" aria-label="UPI Switch features">
        <article
          v-for="card in featureCards"
          :key="card.title"
          class="upi-features__card"
        >
          <div class="upi-features__icon">
            <img
              :src="card.icon"
              alt=""
              :width="card.icon_width || 28"
              :height="card.icon_height || 28"
              decoding="async"
            />
          </div>
          <div class="upi-features__card-text">
            <h3 class="upi-features__card-title">{{ card.title }}</h3>
            <p class="upi-features__card-body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Path — Figma 466:18065 -->
    <UpiPathSection v-if="page.path" :path="page.path" />

    <!-- Capabilities — Figma 466:18096 -->
    <section v-if="page.capabilities" class="upi-caps">
      <div class="upi-caps__head">
        <h2 class="upi-caps__title">{{ page.capabilities.title }}</h2>
        <p class="upi-caps__body">{{ page.capabilities.body }}</p>
      </div>
      <div class="upi-caps__grid" aria-label="UPI Switch capabilities">
        <article
          v-for="card in capabilityCards"
          :key="card.title"
          class="upi-caps__card"
        >
          <div class="upi-caps__visual">
            <UpiCapsConnectivityGraphic
              v-if="capGraphic(card) === 'connectivity'"
              :alt="card.image_alt || card.title"
            />
            <UpiCapsRoutingGraphic
              v-else-if="capGraphic(card) === 'routing'"
              :alt="card.image_alt || card.title"
            />
            <UpiCapsVisibilityGraphic
              v-else-if="capGraphic(card) === 'visibility'"
              :alt="card.image_alt || card.title"
            />
            <UpiCapsScaleGraphic
              v-else-if="capGraphic(card) === 'scale'"
              :alt="card.image_alt || card.title"
            />
            <img
              v-else
              class="upi-caps__media"
              :src="card.image"
              :alt="card.image_alt || card.title"
              :width="card.image_width || 466"
              :height="card.image_height || 373"
              decoding="async"
              loading="lazy"
            />
          </div>
          <div class="upi-caps__card-text">
            <h3 class="upi-caps__card-title">{{ card.title }}</h3>
            <p class="upi-caps__card-body">{{ card.body }}</p>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.upi-page {
  width: 100%;
  background: #ffffff;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

/* —— Hero — Figma 466:17722 —— */
.upi-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.upi-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.upi-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.upi-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  padding: 80px 100px 120px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upi-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: min(809px, 100%);
  text-align: center;
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.55s ease,
    transform 0.55s ease;
}

.upi-hero--ready .upi-hero__copy {
  opacity: 1;
  transform: none;
}

.upi-hero__eyebrow {
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

.upi-hero__cta-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  width: 100%;
}

.upi-hero__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.upi-hero__title {
  margin: 0;
  width: min(809px, 100%);
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  text-transform: capitalize;
  color: #252b37;
}

.upi-hero__intro {
  margin: 0;
  width: min(669px, 100%);
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.64px;
  color: #535862;
}

.upi-hero__cta {
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

.upi-hero__cta:hover {
  background: #0a86ad;
}

.upi-hero__cta img {
  display: block;
}

/* —— Architecture — Figma 466:17859 —— */
.upi-arch {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 74.5px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.upi-arch__head,
.upi-features__head,
.upi-caps__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.upi-arch__head {
  width: min(662px, 100%);
}

.upi-arch__title,
.upi-features__title,
.upi-caps__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
  color: #252b37;
}

.upi-arch__body,
.upi-features__body,
.upi-caps__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.upi-arch__visual {
  position: relative;
  width: 100%;
  max-width: 1291px;
}

/* —— Features — Figma 466:18031 —— */
.upi-features {
  max-width: 1440px;
  margin: 100px auto 0;
  padding: 0 123.5px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.upi-features__head {
  width: min(649px, 100%);
}

.upi-features__grid {
  display: flex;
  gap: 24px;
  width: 100%;
  max-width: 1193px;
  justify-content: center;
}

.upi-features__card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  width: 285px;
  min-height: 164px;
}

.upi-features__icon {
  display: flex;
  align-items: flex-start;
  padding: 13.284px;
  border-radius: 6.642px;
  background: rgba(9, 116, 149, 0.1);
}

.upi-features__icon img {
  display: block;
  width: 28px;
  height: 28px;
}

.upi-features__card-text {
  display: flex;
  flex-direction: column;
  gap: 7px;
  width: 100%;
}

.upi-features__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: #252b37;
}

.upi-features__card-body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #535862;
}

/* —— Capabilities — Figma 466:18096 —— */
.upi-caps {
  max-width: 1052px;
  margin: 100px auto 40px;
  padding: 0 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.upi-caps__head {
  width: min(810px, 100%);
}

.upi-caps__grid {
  /* Figma 316:1934 — 2×2, 514 cards, 24 gap */
  display: grid;
  grid-template-columns: repeat(2, 514px);
  gap: 24px;
  width: 1052px;
  max-width: 100%;
  justify-content: center;
}

.upi-caps__card {
  /* Figma 296:2660 — 514 × 511, p24, gap12, r12 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 514px;
  height: 511px;
  max-width: 100%;
  min-height: 511px;
  max-height: 511px;
  padding: 24px;
  box-sizing: border-box;
  border: 1px solid #e9eaeb;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(10, 13, 18, 0.05);
}

.upi-caps__visual {
  /* Figma 296:2661 — exact 466 × 373.02 visual slot; no inner frame */
  position: relative;
  display: block;
  flex: 0 0 auto;
  width: 466px;
  height: 373.02px;
  max-width: 100%;
  overflow: hidden;
  border: 0;
  outline: none;
  box-shadow: none;
  background: transparent;
  line-height: 0;
  isolation: isolate;
}

.upi-caps__visual :deep(.upi-conn),
.upi-caps__visual :deep(.upi-route),
.upi-caps__visual :deep(.upi-vis),
.upi-caps__visual :deep(.upi-scale) {
  width: 100%;
  height: 100%;
}

.upi-caps__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  border: none;
  outline: none;
  box-shadow: none;
  background: transparent;
  pointer-events: none;
}

.upi-caps__card-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
  width: 100%;
}

.upi-caps__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: #252b37;
}

.upi-caps__card-body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #535862;
}

@media (max-width: 1200px) {
  .upi-hero__inner,
  .upi-arch,
  .upi-features {
    padding-left: 48px;
    padding-right: 48px;
  }

  .upi-features__grid {
    flex-wrap: wrap;
  }

  .upi-features__card {
    width: calc(50% - 12px);
    min-width: 240px;
  }

  .upi-caps__grid {
    grid-template-columns: repeat(2, minmax(280px, 1fr));
  }

  .upi-caps__card {
    width: 100%;
    height: auto;
    min-height: 0;
    max-height: none;
  }

  .upi-caps__visual {
    width: 100%;
    height: auto;
    aspect-ratio: 466 / 373.02;
    min-height: 0;
  }
}

@media (max-width: 900px) {
  .upi-hero__inner {
    padding: 48px 24px 80px;
  }

  .upi-arch,
  .upi-features,
  .upi-caps {
    padding-left: 24px;
    padding-right: 24px;
  }

  .upi-arch__title,
  .upi-features__title,
  .upi-caps__title,
  .upi-hero__title {
    font-size: 32px;
    line-height: 42px;
  }

  .upi-features__grid {
    flex-direction: column;
  }

  .upi-features__card {
    width: 100%;
    min-height: 0;
  }

  .upi-caps__grid {
    grid-template-columns: 1fr;
  }
}
</style>
