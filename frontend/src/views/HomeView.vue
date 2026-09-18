<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import { fetchHomepage } from "@/api/client";
import { applySeo } from "@/utils/seo";
import HeroSection from "@/components/HeroSection.vue";
import ProblemTrio from "@/components/ProblemTrio.vue";
import PartnersMarquee from "@/components/PartnersMarquee.vue";
import HomeEcosystem from "@/components/HomeEcosystem.vue";
import HomePerform from "@/components/HomePerform.vue";
import HomeProducts from "@/components/HomeProducts.vue";
import HomeClosing from "@/components/HomeClosing.vue";
import {
  animateStatValues,
  formatStatValue,
  parseStatValue,
} from "@/composables/useCountUp.js";
import { scheduleScrollRestore } from "@/utils/scrollRestoration.js";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

function readHomepageBootstrap() {
  const el = document.getElementById("homepage-bootstrap");
  if (!el?.textContent) return null;
  try {
    return JSON.parse(el.textContent);
  } catch {
    return null;
  }
}

const bootstrap = readHomepageBootstrap();
const data = ref(bootstrap);
const error = ref(null);
const loading = ref(!bootstrap);
const trustStatsRef = ref(null);
const hasAnimatedStats = ref(false);
const statDisplays = ref([]);
let statsObserver = null;
let cancelStatAnimation = null;

const parsedStats = computed(() =>
  (data.value?.stats || []).map((stat) => parseStatValue(stat.value)),
);

function setFinalStatValues() {
  statDisplays.value = (data.value?.stats || []).map((stat) => stat.value);
}

function resetStatValues() {
  statDisplays.value = parsedStats.value.map((parsed) => formatStatValue(parsed, 0));
}

function runStatsCountUp() {
  if (hasAnimatedStats.value || !parsedStats.value.length) return;
  hasAnimatedStats.value = true;
  cancelStatAnimation?.();
  cancelStatAnimation = animateStatValues(parsedStats.value, {
    duration: 1800,
    onFrame: (values) => {
      statDisplays.value = values;
    },
    onComplete: setFinalStatValues,
  });
}

function setupStatsObserver() {
  statsObserver?.disconnect();

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setFinalStatValues();
    return;
  }

  statsObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      runStatsCountUp();
      statsObserver?.disconnect();
    },
    { threshold: 0.25, rootMargin: "0px 0px -8% 0px" },
  );

  if (trustStatsRef.value) {
    statsObserver.observe(trustStatsRef.value);
  }
}

onMounted(async () => {
  if (bootstrap) {
    applySeo(bootstrap.seo, bootstrap.structured_data);
    resetStatValues();
    loading.value = false;
    await nextTick();
    setupStatsObserver();
    scheduleScrollRestore();
    return;
  }
  try {
    data.value = await fetchHomepage();
    applySeo(data.value.seo, data.value.structured_data);
    resetStatValues();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
    await nextTick();
    setupStatsObserver();
    scheduleScrollRestore();
  }
});

onUnmounted(() => {
  statsObserver?.disconnect();
  cancelStatAnimation?.();
});
</script>

<template>
  <div v-if="loading" class="page-loading">
    <div class="loading-screen__spinner" />
  </div>

  <div v-else-if="error" class="page-loading page-loading--error">
    <p>{{ error }}</p>
  </div>

  <main v-else class="home-page">
    <HeroSection :hero="data.hero" :site="data.site" />

    <section class="home-trust" aria-label="Trust and performance">
      <div class="home-trust__top">
        <div class="home-trust__intro">
          <h2 class="home-trust__title">Trusted by Leading Businesses</h2>
          <PartnersMarquee
            :partners="data.merchant_partners || []"
            variant="merchants"
            :show-title="false"
          />
        </div>
        <div class="home-trust__rule" aria-hidden="true" />
      </div>

      <div ref="trustStatsRef" class="home-trust__stats">
        <div
          v-for="(stat, index) in data.stats || []"
          :key="stat.label"
          class="home-trust__stat"
        >
          <span class="home-trust__stat-value">{{ statDisplays[index] || stat.value }}</span>
          <span class="home-trust__stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </section>

    <ProblemTrio :problem="data.problem_trio" />
    <HomeEcosystem v-if="data.ecosystem" :section="data.ecosystem" />
    <HomePerform v-if="data.perform" :section="data.perform" />

    <section class="home-banks">
      <PartnersMarquee
        title="Partnered with leading banks and Partners"
        :partners="data.banking_partners || []"
        variant="banks"
      />
    </section>

    <HomeProducts v-if="data.products" :section="data.products" />
    <HomeClosing v-if="data.closing" :section="data.closing" />
  </main>
</template>

<style scoped>
.home-page {
  margin-top: -129px;
  background: #ffffff;
  overflow-x: clip;
  max-width: 100%;
}

/* Consistent gap between major homepage sections.
   Use margin-block-start so section roots can still use margin-inline: auto. */
.home-page > * + * {
  margin-block-start: var(--ur-section-gap);
}

/* Hero diagram → trust title (Figma: ~100 desktop / 120 iPad / 100 phone) */
.home-page > .home-hero + .home-trust {
  margin-block-start: 100px;
}

/* Match spacing below metrics to spacing above clients */
.home-page > .home-trust + * {
  margin-block-start: 100px;
}

.home-trust {
  max-width: 1280px;
  margin-inline: auto;
  padding: 0 var(--ur-gutter);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

/* Figma 1:5372 — title, logos, divider */
.home-trust__top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  width: 100%;
}

.home-trust__intro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  width: 100%;
}

.home-trust :deep(.partners) {
  width: 100%;
  padding-top: 0;
  padding-bottom: 0;
  border-block: 0;
  background: transparent;
}

.home-trust :deep(.partners .container) {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

.home-trust :deep(.partners__scroll) {
  gap: 48px;
  align-items: center;
}

.home-trust :deep(.partners__pill) {
  width: 140px;
  min-width: 140px;
  height: 48px;
  padding: 0;
  background: transparent;
  border: 0;
  border-radius: 0;
}

.home-trust :deep(.partners__logo-stack) {
  width: 100%;
}

.home-trust :deep(.partners__logo),
.home-trust :deep(.partners__logo--lg) {
  width: 100% !important;
  height: 40px !important;
  max-width: 140px !important;
  object-fit: contain;
  object-position: center;
}

.home-trust__title {
  margin: 0;
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  line-height: 32px;
  color: #252b37;
}

.home-trust__rule {
  width: 100%;
  height: 1px;
  background: #eceef2;
}

/* Figma 1:5384 — stats row */
.home-trust__stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 93px;
  width: 100%;
  max-width: 1120px;
}

.home-trust__stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  min-width: 0;
}

.home-trust__stat-value {
  display: block;
  font-size: 44px;
  font-weight: 600;
  line-height: 72px;
  letter-spacing: -1.68px;
  color: #252b37;
  white-space: nowrap;
}

.home-trust__stat-label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  line-height: 32px;
  color: #414651;
}

.home-banks :deep(.partners) {
  padding-top: 0;
  padding-bottom: 0;
  border-block: 0;
  background: transparent;
}

.home-banks :deep(.partners__title) {
  margin: 0 0 24px;
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  line-height: 32px;
  text-transform: none;
  letter-spacing: normal;
  color: #252b37;
}

.home-banks :deep(.partners__scroll) {
  gap: 48px;
  align-items: center;
}

.home-banks :deep(.partners__pill) {
  width: 140px;
  min-width: 140px;
  height: 48px;
  padding: 0;
  background: transparent;
  border: 0;
  border-radius: 0;
}

.home-banks :deep(.partners__logo),
.home-banks :deep(.partners__logo--lg) {
  width: 100% !important;
  height: 40px !important;
  max-width: 140px !important;
  object-fit: contain;
  object-position: center;
}

.home-banks {
  max-width: 1280px;
  margin-inline: auto;
  padding: 0 var(--ur-gutter);
}

.page-loading {
  min-height: 40vh;
  display: grid;
  place-items: center;
}

.page-loading--error {
  color: #c0392b;
}

.loading-screen__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Tablet: Figma iPad — single-row stats (gap 120), compact logos */
@media (max-width: 1200px) {
  .home-page {
    margin-top: -82px;
  }

  .home-page > .home-hero + .home-trust,
  .home-page > .home-trust + * {
    margin-block-start: 100px;
  }

  .home-trust,
  .home-banks {
    max-width: 1024px;
    padding: 0 70px;
  }

  /* Figma 208:3156 — intro gap 16 + pb 12 + border, then 44 to stats */
  .home-trust {
    gap: 44px;
  }

  .home-trust__top {
    gap: 0;
  }

  .home-trust__intro {
    gap: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #d5d7da;
  }

  .home-trust__rule {
    display: none;
  }

  .home-trust__title {
    font-size: 16px;
    line-height: 24px;
    font-weight: 500;
  }

  .home-trust :deep(.partners),
  .home-trust :deep(.partners .container),
  .home-trust :deep(.partners__track) {
    line-height: 0;
  }

  .home-trust :deep(.partners__scroll) {
    gap: 64px;
    justify-content: flex-start;
  }

  .home-trust :deep(.partners__pill) {
    width: 120px;
    min-width: 120px;
    height: 34px;
  }

  .home-trust :deep(.partners__logo),
  .home-trust :deep(.partners__logo--lg) {
    width: 100% !important;
    height: 28px !important;
    max-width: 120px !important;
  }

  .home-trust__stats {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: clamp(32px, 8vw, 120px);
    width: 100%;
    max-width: 868px;
  }

  .home-trust__stat {
    flex: 0 1 auto;
    max-width: 137px;
  }

  .home-trust__stat-value {
    font-size: 36px;
    line-height: 44px;
    letter-spacing: -1.08px;
  }

  .home-trust__stat-label {
    font-size: 16px;
    line-height: 24px;
    font-weight: 600;
  }
}

@media (max-width: 700px) {
  .home-page {
    margin-top: -88px;
  }

  .home-page > .home-hero + .home-trust,
  .home-page > .home-trust + * {
    margin-block-start: 80px;
  }

  .home-trust,
  .home-banks {
    padding: 0 19px;
  }

  .home-banks {
    padding-top: 0;
  }

  /* Phone: compact title→logos; rule sits close under logo belt */
  .home-trust {
    gap: 24px;
  }

  .home-trust__top {
    gap: 16px;
    width: 100%;
  }

  .home-trust__intro {
    gap: 12px;
    padding-bottom: 0;
    border-bottom: 0;
  }

  .home-trust__rule {
    display: block;
  }

  .home-trust__title {
    font-size: 16px;
    line-height: 24px;
    font-weight: 500;
  }

  .home-banks :deep(.partners__title) {
    font-size: 24px;
    line-height: 1.33;
  }

  .home-trust__stats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    max-width: 327px;
    gap: 26px 36px;
  }

  .home-trust__stat {
    max-width: none;
  }

  .home-trust :deep(.partners__scroll),
  .home-banks :deep(.partners__scroll) {
    gap: 28px;
  }

  .home-trust :deep(.partners__pill),
  .home-banks :deep(.partners__pill) {
    width: 112px;
    min-width: 112px;
    height: 36px;
  }

  .home-trust :deep(.partners__logo),
  .home-trust :deep(.partners__logo--lg),
  .home-banks :deep(.partners__logo),
  .home-banks :deep(.partners__logo--lg) {
    height: 26px !important;
    max-width: 112px !important;
  }

  .home-trust__stat-value {
    font-size: 36px;
    line-height: 1.2;
    letter-spacing: -1px;
  }

  .home-trust__stat-label {
    font-size: 14px;
    line-height: 1.5;
  }
}
</style>
