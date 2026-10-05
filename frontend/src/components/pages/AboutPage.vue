<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import PartnersMarquee from "@/components/PartnersMarquee.vue";
import AboutPartnersGraphic from "@/components/pages/AboutPartnersGraphic.vue";
import {
  animateStatValues,
  formatStatValue,
  parseStatValue,
} from "@/composables/useCountUp.js";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const ASSETS = "/images/figma-about-v2";
const PARTNERS_STAGE_WIDTH = 866;

const valueIcons = {
  users: `${ASSETS}/icon-users.svg`,
  star: `${ASSETS}/icon-star.svg`,
  "shield-check": `${ASSETS}/icon-shield-check.svg`,
  zap: `${ASSETS}/icon-zap.svg`,
};

const partnersSection = ref(null);
const partnersZoom = ref(1);
let partnersObserver = null;

function updatePartnersZoom() {
  const el = partnersSection.value;
  if (!el) return;
  partnersZoom.value = Math.min(1, el.clientWidth / PARTNERS_STAGE_WIDTH);
}

const openLeader = ref(null);

/* Touch and pen have no hover, so a tap toggles the bio; mouse users get it on hover. */
function onLeaderTap(event, leader) {
  if (event.pointerType === "mouse" || !leader.bio) return;
  openLeader.value = openLeader.value === leader.name ? null : leader.name;
}

const STATS_DURATION = 1800;
const statsEl = ref(null);
const statDisplays = ref([]);
let statsObserver = null;
let cancelStats = null;

/* Single-digit whole values ("1Cr") count through tenths so they visibly grow; the last frame is exact. */
function statsForCounting() {
  return (props.page.stats || []).map((stat) => {
    const parsed = parseStatValue(stat.value);
    if (parsed.fixed === undefined && parsed.decimals === 0 && parsed.target < 10) {
      return { ...parsed, decimals: 1, tenths: true };
    }
    return parsed;
  });
}

function formatFrame(value, parsed) {
  return parsed.tenths ? value.replace(/\.0(?=\D*$)/, "") : value;
}

function showFinalStats() {
  statDisplays.value = (props.page.stats || []).map((stat) => stat.value);
}

function setupStatsCountUp() {
  statsObserver?.disconnect();
  statsObserver = null;
  cancelStats?.();
  cancelStats = null;

  const stats = props.page.stats || [];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!stats.length || reduceMotion || typeof IntersectionObserver === "undefined" || !statsEl.value) {
    showFinalStats();
    return;
  }

  const parsed = statsForCounting();
  statDisplays.value = parsed.map((p) => formatFrame(formatStatValue(p, 0), p));

  statsObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      statsObserver?.disconnect();
      statsObserver = null;
      cancelStats = animateStatValues(parsed, {
        duration: STATS_DURATION,
        onFrame: (values) => {
          statDisplays.value = values.map((value, i) => formatFrame(value, parsed[i]));
        },
        onComplete: showFinalStats,
      });
    },
    { threshold: 0.25, rootMargin: "0px 0px -8% 0px" },
  );
  statsObserver.observe(statsEl.value);
}

watch(
  () => (props.page.stats || []).map((s) => `${s.label}:${s.value}`).join("|"),
  async () => {
    await nextTick();
    setupStatsCountUp();
  },
);

onMounted(() => {
  updatePartnersZoom();
  if (typeof ResizeObserver !== "undefined" && partnersSection.value) {
    partnersObserver = new ResizeObserver(updatePartnersZoom);
    partnersObserver.observe(partnersSection.value);
  }
  setupStatsCountUp();
});

onBeforeUnmount(() => {
  partnersObserver?.disconnect();
  partnersObserver = null;
  statsObserver?.disconnect();
  cancelStats?.();
});
</script>

<template>
  <main class="about-page">
    <section class="about-hero">
      <div class="about-hero__bg" aria-hidden="true">
        <img
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="about-hero__inner">
        <div class="about-hero__copy">
          <div class="about-hero__text">
            <h1 class="about-hero__title">{{ page.hero_title || page.title }}</h1>
            <p class="about-hero__intro">{{ page.intro }}</p>
          </div>
          <RouterLink to="/contact" class="about-hero__cta">
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

        <div class="about-trust">
          <PartnersMarquee
            title="Trusted by Leading Businesses"
            :partners="page.merchant_partners || []"
            variant="merchants"
          />
        </div>
      </div>
    </section>

    <div class="about-body">
      <section class="about-overview">
        <h2 class="about-overview__title">{{ page.overview_title }}</h2>
        <div class="about-overview__copy">
          <p class="about-overview__body">{{ page.overview_body }}</p>
          <dl v-if="page.stats?.length" ref="statsEl" class="about-overview__stats">
            <div v-for="(stat, i) in page.stats" :key="stat.label" class="about-overview__stat">
              <dt>{{ stat.label }}</dt>
              <dd>
                <span aria-hidden="true">{{ statDisplays[i] ?? stat.value }}</span>
                <span class="about-overview__sr">{{ stat.value }}</span>
              </dd>
            </div>
          </dl>
        </div>
      </section>

      <section v-if="page.mission || page.vision" class="about-mission">
        <div class="about-mission__inner">
          <div v-if="page.mission" class="about-mission__col about-mission__col--mission">
            <span class="about-mission__icon" aria-hidden="true">
              <img :src="`${ASSETS}/icon-mission.svg`" alt="" width="32" height="32" decoding="async" />
            </span>
            <h2 class="about-mission__title">{{ page.mission.title }}</h2>
            <p class="about-mission__body">{{ page.mission.body }}</p>
          </div>
          <span class="about-mission__divider" aria-hidden="true">
            <img :src="`${ASSETS}/mission-divider.svg`" alt="" width="223" height="1" decoding="async" />
          </span>
          <div v-if="page.vision" class="about-mission__col about-mission__col--vision">
            <span class="about-mission__icon" aria-hidden="true">
              <img :src="`${ASSETS}/icon-vision.svg`" alt="" width="32" height="32" decoding="async" />
            </span>
            <h2 class="about-mission__title">{{ page.vision.title }}</h2>
            <p class="about-mission__body">{{ page.vision.body }}</p>
          </div>
        </div>
      </section>

      <section class="about-journey">
        <div class="about-journey__intro">
          <div class="about-journey__head">
            <h2 class="about-journey__title">{{ page.journey_title }}</h2>
            <p class="about-journey__lead">{{ page.journey_intro }}</p>
          </div>
          <img
            class="about-journey__photo"
            :src="`${ASSETS}/journey-handshake.png`"
            alt="Business partners shaking hands over a laptop showing payment reports"
            width="1200"
            height="630"
            loading="lazy"
            decoding="async"
          />
        </div>

        <ol class="about-journey__timeline">
          <li v-for="(step, index) in page.journey || []" :key="step.title" class="about-journey__step">
            <span class="about-journey__node" aria-hidden="true">{{ index + 1 }}</span>
            <h3 class="about-journey__step-title">{{ step.title }}</h3>
            <p class="about-journey__step-body">{{ step.body }}</p>
          </li>
        </ol>
      </section>

      <section
        ref="partnersSection"
        class="about-partners"
        :style="{ '--partners-zoom': partnersZoom }"
      >
        <div class="about-partners__stage">
          <AboutPartnersGraphic class="about-partners__graphic" />
        </div>
        <div class="about-partners__copy-layer">
          <div class="about-partners__copy-frame">
            <div class="about-partners__copy">
              <h2 class="about-partners__title">{{ page.partnerships_title }}</h2>
              <p class="about-partners__intro">{{ page.partnerships_intro }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="about-leaders" aria-labelledby="about-leaders-title">
        <div class="about-leaders__head">
          <h2 id="about-leaders-title" class="about-leaders__title">{{ page.leaders_title }}</h2>
          <p class="about-leaders__intro">{{ page.leaders_intro }}</p>
        </div>

        <div class="about-leaders__grid">
          <article
            v-for="leader in page.leaders || []"
            :key="leader.name"
            class="about-leaders__card"
            :class="{ 'about-leaders__card--open': openLeader === leader.name }"
            :tabindex="leader.bio ? 0 : undefined"
            @pointerup="onLeaderTap($event, leader)"
          >
            <img
              class="about-leaders__photo"
              :src="leader.image"
              :alt="leader.name"
              width="406"
              height="424"
              loading="lazy"
              decoding="async"
            />
            <div class="about-leaders__caption" :class="{ 'about-leaders__caption--bio': leader.bio }">
              <span class="about-leaders__spacer" aria-hidden="true" />
              <div class="about-leaders__person">
                <h3 class="about-leaders__name">{{ leader.name }}</h3>
                <p class="about-leaders__role">
                  <span class="about-leaders__role-text">{{ leader.role }}</span>
                  <span v-if="leader.bio" class="about-leaders__role-text about-leaders__role-text--caps" aria-hidden="true">
                    {{ leader.role }}
                  </span>
                </p>
              </div>
              <p v-if="leader.bio" class="about-leaders__bio">{{ leader.bio }}</p>
              <span class="about-leaders__spacer about-leaders__spacer--end" aria-hidden="true" />
            </div>
          </article>
        </div>
      </section>

      <section class="about-values" aria-labelledby="about-values-title">
        <div class="about-values__head">
          <h2 id="about-values-title" class="about-values__title">{{ page.values_title }}</h2>
          <p class="about-values__intro">{{ page.values_intro }}</p>
        </div>

        <div class="about-values__row">
          <div v-for="value in page.values || []" :key="value.title" class="about-values__col">
            <span class="about-values__letter" aria-hidden="true">{{ value.letter }}</span>
            <article class="about-values__card">
              <span class="about-values__icon" aria-hidden="true">
                <img :src="valueIcons[value.icon]" alt="" width="32" height="32" decoding="async" />
              </span>
              <div class="about-values__copy">
                <h3 class="about-values__card-title">{{ value.title }}</h3>
                <p class="about-values__card-body">{{ value.body }}</p>
              </div>
            </article>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.about-page {
  --about-ink: #252b37;
  --about-muted: #535862;
  --about-teal: #097495;
  --about-gradient: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  --about-font: "Manrope", "DM Sans", system-ui, sans-serif;
  --about-gutter: 56px;
  --about-gap: 100px;
  font-family: var(--about-font);
  background: #ffffff;
  color: var(--about-ink);
  margin-top: -129px;
  overflow-x: clip;
  max-width: 100%;
}

/* ---------- Hero ---------- */

/* the background runs past the hero box so its fade isn't cut off; .about-page clips sideways */
.about-hero {
  position: relative;
  width: 100%;
}

.about-hero__bg {
  position: absolute;
  inset: 0 0 auto;
  height: 680px;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.about-hero__bg img {
  display: block;
  position: absolute;
  left: 50%;
  top: 0;
  width: 100%;
  min-width: 1440px;
  height: 100%;
  transform: translateX(-50%);
  object-fit: cover;
  object-position: center top;
}

.about-hero__inner {
  position: relative;
  z-index: 1;
  max-width: var(--ur-page-max, 1440px);
  margin: 0 auto;
  padding: 209px var(--about-gutter) 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 100px;
}

.about-hero__copy {
  width: 789px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  text-align: center;
}

.about-hero__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.about-hero__title {
  margin: 0;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.26px;
}

.about-hero__intro {
  max-width: 611px;
  margin: 0;
  font-size: 14px;
  line-height: normal;
  letter-spacing: 0.56px;
  color: var(--about-muted);
}

.about-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: var(--about-teal);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  line-height: 1;
  text-decoration: none;
  box-sizing: border-box;
}

.about-hero__cta img {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.about-hero__cta:hover {
  filter: brightness(1.05);
}

.about-trust {
  width: 1051px;
  max-width: 100%;
  min-height: 141px;
}

.about-trust :deep(.partners) {
  padding-top: 0;
  padding-bottom: 0;
  border-block: 0;
  background: transparent;
}

.about-trust :deep(.partners__title) {
  margin: 0 0 32px;
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  line-height: 32px;
  text-transform: none;
  letter-spacing: normal;
  color: var(--about-ink);
}

.about-trust :deep(.partners__scroll) {
  gap: 48px;
  align-items: center;
}

.about-trust :deep(.partners__pill) {
  width: 140px;
  min-width: 140px;
  height: 48px;
  padding: 0;
  background: transparent;
  border: 0;
  border-radius: 0;
}

.about-trust :deep(.partners__logo),
.about-trust :deep(.partners__logo--lg) {
  width: 100% !important;
  height: 40px !important;
  max-width: 140px !important;
  object-fit: contain;
  object-position: center;
}

/* ---------- Body ---------- */

.about-body {
  position: relative;
  z-index: 1;
  width: min(1328px, calc(100% - 2 * var(--about-gutter)));
  margin: 0 auto;
  padding-top: var(--about-gap);
  display: flex;
  flex-direction: column;
  gap: var(--about-gap);
}

.about-overview__title,
.about-journey__title,
.about-partners__title,
.about-leaders__title,
.about-values__title {
  margin: 0;
  font-size: var(--ur-heading-md, 40px);
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.2px;
  color: var(--about-ink);
}

/* Overview */

.about-overview {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 486fr) minmax(0, 612fr);
  gap: clamp(48px, 7vw, 102px);
  align-items: start;
}

.about-overview__copy {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.about-overview__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  color: var(--about-muted);
}

.about-overview__stats {
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 16px 46px;
}

.about-overview__stat {
  min-width: 160px;
  display: flex;
  flex-direction: column-reverse;
  gap: 4px;
}

.about-overview__stat dd {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -0.96px;
  color: var(--about-ink);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.about-overview__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

.about-overview__stat dt {
  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
  white-space: nowrap;
}

/* Mission & vision */

.about-mission {
  min-height: 395px;
  padding: 66px 48px;
  box-sizing: border-box;
  border-radius: 24px;
  background: var(--about-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.about-mission__inner {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 1px minmax(0, 1fr);
  gap: clamp(40px, 5.35vw, 77px);
  align-items: start;
}

.about-mission__col {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
}

.about-mission__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 62px;
  height: 62px;
  border-radius: 31px;
  background: #f5f5f5;
}

.about-mission__icon img {
  width: 32px;
  height: 32px;
}

.about-mission__title {
  margin: 0;
  font-size: var(--ur-heading-md, 40px);
  font-weight: 700;
  line-height: 56px;
  color: #ffffff;
}

.about-mission__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #ffffff;
}

.about-mission__divider {
  position: relative;
  align-self: center;
  width: 1px;
  height: 223px;
}

.about-mission__divider img {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 223px;
  height: 1px;
  max-width: none;
  transform: translate(-50%, -50%) rotate(90deg);
}

/* Journey */

.about-journey {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 476fr) minmax(0, 556fr);
  gap: clamp(56px, 12.4vw, 178px);
  align-items: start;
}

.about-journey__intro {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.about-journey__head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.about-journey__lead {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-journey__photo {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 1920 / 918;
  border-radius: 12px;
  object-fit: cover;
}

.about-journey__timeline {
  list-style: none;
  margin: 0;
  padding: 0 0 0 65px;
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.about-journey__step {
  --journey-gap: 60px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* rail runs from just inside this node to just inside the next one */
.about-journey__step:not(:last-child)::after {
  content: "";
  position: absolute;
  left: -46px;
  top: 37px;
  width: 3px;
  height: calc(100% + var(--journey-gap) - 33px);
  background: var(--about-teal);
}

.about-journey__node {
  position: absolute;
  z-index: 1;
  left: -65px;
  top: 0;
  width: 41px;
  height: 41px;
  border-radius: 8px;
  background: var(--about-teal);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
  color: #ffffff;
}

.about-journey__step-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: 32px;
  color: var(--about-ink);
}

.about-journey__step-body {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  color: var(--about-muted);
  opacity: 0.8;
}

/* Partnerships */

.about-partners {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.about-partners__stage {
  display: flex;
  justify-content: center;
}

.about-partners__graphic {
  flex-shrink: 0;
  zoom: var(--partners-zoom, 1);
}

.about-partners__copy-layer {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  pointer-events: none;
}

.about-partners__copy-frame {
  position: relative;
  flex-shrink: 0;
  width: 866px;
  height: 806px;
  zoom: var(--partners-zoom, 1);
}

.about-partners__copy {
  position: absolute;
  left: calc(50% - 4.04px);
  top: 297px;
  width: 478px;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  pointer-events: auto;
}

.about-partners__title {
  width: 351px;
  max-width: 100%;
}

.about-partners__intro {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

/* Leaders */

.about-leaders {
  width: min(872px, 100%);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 36px;
}

.about-leaders__head {
  max-width: 738px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.about-leaders__intro {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-leaders__grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 406px));
  justify-content: center;
  gap: 60px;
}

.about-leaders__card {
  --open: 0;
  --leader-ease: cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
  aspect-ratio: 406 / 424;
  border-radius: 24px;
  overflow: hidden;
  background: #d4d4d8;
}

@media (hover: hover) {
  .about-leaders__card:hover {
    --open: 1;
  }
}

.about-leaders__card:focus-visible,
.about-leaders__card--open {
  --open: 1;
}

.about-leaders__card:focus-visible {
  outline: 2px solid var(--about-ink);
  outline-offset: 4px;
}

.about-leaders__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Full-card glass panel parked so only its 82px strip shows; --open slides it up over the photo (Figma 1003:9116). */
.about-leaders__caption {
  position: absolute;
  inset: 0;
  box-sizing: border-box;
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 0 0 24px 24px;
  background: rgba(255, 255, 255, 0.2);
  -webkit-backdrop-filter: blur(28.5px);
  backdrop-filter: blur(28.5px);
  transform: translateY(calc(100% - 82px));
}

.about-leaders__caption--bio {
  border-radius: calc(var(--open) * 24px) calc(var(--open) * 24px) 24px 24px;
  transform: translateY(calc((1 - var(--open)) * (100% - 82px)));
  transition:
    transform 0.6s var(--leader-ease),
    border-radius 0.6s var(--leader-ease);
}

.about-leaders__spacer {
  flex: 0 0 0;
}

.about-leaders__spacer--end {
  flex-grow: 1;
}

.about-leaders__caption--bio .about-leaders__spacer:not(.about-leaders__spacer--end) {
  flex-grow: var(--open);
  transition: flex-grow 0.6s var(--leader-ease);
}

.about-leaders__person {
  display: flex;
  flex-direction: column;
  gap: calc(4px + var(--open) * 4px);
  transition: gap 0.6s var(--leader-ease);
}

.about-leaders__name {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 24px;
  color: #fafafa;
}

.about-leaders__role {
  display: grid;
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  line-height: 22px;
  color: #ffffff;
  opacity: 0.8;
}

.about-leaders__role-text {
  grid-area: 1 / 1;
}

.about-leaders__caption--bio .about-leaders__role-text {
  opacity: calc(1 - var(--open));
  transition: opacity 0.3s ease;
}

.about-leaders__caption--bio .about-leaders__role-text--caps {
  font-size: 15px;
  text-transform: uppercase;
  opacity: var(--open);
}

.about-leaders__bio {
  margin: 24px 0 0;
  font-size: 15px;
  font-weight: 500;
  line-height: 22px;
  color: #ffffff;
  opacity: calc(var(--open) * 0.8);
  transform: translateY(calc((1 - var(--open)) * 12px));
  transition:
    opacity 0.4s ease,
    transform 0.6s var(--leader-ease);
  transition-delay: calc(var(--open) * 0.15s);
}

@media (prefers-reduced-motion: reduce) {
  .about-leaders__caption--bio,
  .about-leaders__caption--bio .about-leaders__spacer,
  .about-leaders__person,
  .about-leaders__role-text,
  .about-leaders__bio {
    transition: none;
  }
}

/* Core values */

.about-values {
  min-height: 860px;
  padding: 60px 70px;
  box-sizing: border-box;
  border-radius: 24px;
  background: var(--about-gradient);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 36px;
  overflow: hidden;
}

.about-values__head {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: center;
}

.about-values__title {
  color: #ffffff;
}

.about-values__intro {
  margin: 0;
  font-size: 20px;
  line-height: 28px;
  letter-spacing: 0.8px;
  color: rgba(255, 255, 255, 0.8);
}

.about-values__row {
  display: grid;
  grid-template-columns: 282px 316px 313px 291px;
  justify-content: center;
  gap: 12px;
  width: 100%;
}

.about-values__col {
  --letter-x: 50%;
  --card-x: 0px;
  position: relative;
  height: 548px;
}

.about-values__col:nth-child(1) {
  --letter-x: 140px;
}

.about-values__col:nth-child(2) {
  --letter-x: 153px;
  --card-x: 21px;
}

.about-values__col:nth-child(3) {
  --letter-x: 156.5px;
  --card-x: 16px;
}

.about-values__col:nth-child(4) {
  --letter-x: 151.5px;
  --card-x: 11px;
}

.about-values__letter {
  position: absolute;
  left: var(--letter-x);
  top: 181.5px;
  height: 363px;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Arimo", Arial, sans-serif;
  font-size: 480px;
  font-weight: 400;
  line-height: normal;
  color: transparent;
  -webkit-text-stroke: 3px #ffffff;
  opacity: 0.08;
  pointer-events: none;
  user-select: none;
}

.about-values__card {
  position: absolute;
  left: var(--card-x);
  top: 248px;
  width: 280px;
  height: 300px;
  box-sizing: border-box;
  padding: 64px 24px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 140px 140px 12px 12px;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  -webkit-backdrop-filter: blur(5px);
  backdrop-filter: blur(5px);
}

.about-values__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  padding: 12px;
  box-sizing: border-box;
}

.about-values__icon img {
  width: 32px;
  height: 32px;
}

.about-values__copy {
  width: 220.713px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
}

.about-values__card-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  letter-spacing: -0.24px;
  color: #ffffff;
}

.about-values__card-body {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
  color: rgba(255, 255, 255, 0.8);
}

/* ---------- Narrow laptop: the four value cards share the row evenly ---------- */

@media (max-width: 1367px) {
  .about-overview__stats {
    column-gap: 40px;
  }

  .about-overview__stat {
    min-width: 0;
  }

  .about-values {
    padding-inline: 32px;
  }

  .about-values__row {
    grid-template-columns: repeat(4, minmax(0, 280px));
  }

  .about-values__col {
    --letter-x: 50%;
    --card-x: 0px;
  }

  .about-values__col:nth-child(n) {
    --letter-x: 50%;
    --card-x: 0px;
  }

  .about-values__card {
    width: 100%;
    padding-inline: 20px;
  }

  .about-values__letter {
    font-size: clamp(300px, 35vw, 480px);
  }
}

@media (max-width: 1200px) {
  .about-page {
    --about-gutter: var(--ur-gutter, 48px);
    margin-top: -82px;
  }

  .about-hero__inner {
    padding-top: 160px;
  }

  .about-hero__title,
  .about-overview__title,
  .about-journey__title,
  .about-partners__title,
  .about-leaders__title,
  .about-values__title,
  .about-mission__title {
    line-height: 1.3;
  }

  .about-values__card-title {
    font-size: 20px;
  }
}

/* ---------- Desktop: fixed overview title size; values panel compact enough to fit a laptop viewport ---------- */

@media (min-width: 1025px) {
  .about-overview__title {
    font-size: 40px;
  }

  .about-values {
    min-height: 0;
    padding-block: 48px;
    gap: 28px;
  }

  .about-values__col {
    height: 446px;
  }

  .about-values__letter {
    top: 148px;
    height: 296px;
    font-size: clamp(300px, 35vw, 400px);
  }

  .about-values__card {
    top: 196px;
    height: 250px;
    padding-top: 56px;
    padding-bottom: 32px;
    gap: 16px;
  }
}

/* ---------- Tablet ---------- */

@media (min-width: 768px) and (max-width: 1024px) {
  .about-page {
    --about-gap: 86px;
  }

  .about-hero__inner {
    padding-top: 162px;
    gap: 86px;
  }

  .about-hero__title {
    letter-spacing: -1.08px;
  }

  .about-overview {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .about-overview__title {
    max-width: 640px;
  }

  .about-mission {
    min-height: 0;
    padding: 48px 32px;
  }

  .about-mission__inner {
    grid-template-columns: minmax(0, 1fr) 1px minmax(0, 1fr);
    gap: 32px;
  }

  .about-journey {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
    gap: 40px;
  }

  .about-journey__timeline,
  .about-journey__step {
    --journey-gap: 40px;
  }

  .about-journey__timeline {
    gap: 40px;
  }

  .about-journey__step-title {
    font-size: 20px;
    line-height: 28px;
  }

  .about-leaders__grid {
    gap: clamp(24px, calc(-48px + 9.375vw), 48px);
  }

  .about-values {
    min-height: 0;
    padding: 48px 32px;
  }

  .about-values__row {
    grid-template-columns: repeat(2, minmax(0, 280px));
    row-gap: 24px;
    column-gap: clamp(24px, calc(-72px + 12.5vw), 56px);
  }

  .about-values__letter {
    font-size: 480px;
  }

  .about-values__card-title {
    font-size: 24px;
  }
}

/* ---------- Phone ---------- */

@media (max-width: 767px) {
  .about-page {
    --about-gap: 56px;
  }

  .about-hero__inner {
    padding-top: 128px;
    gap: 48px;
  }

  .about-hero__title {
    line-height: 1.25;
    letter-spacing: -1.08px;
  }

  .about-hero__cta {
    height: 44px;
    padding: 12px 16px;
    font-size: 14px;
  }

  .about-trust :deep(.partners__title) {
    margin-bottom: 16px;
    font-size: 20px;
    line-height: 28px;
  }

  .about-overview {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .about-overview__body {
    font-size: 16px;
    line-height: 24px;
  }

  .about-overview__stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
  }

  .about-overview__stat {
    min-width: 0;
    gap: 0;
    justify-content: flex-end;
  }

  .about-overview__stat dd {
    font-size: 24px;
    line-height: 36px;
  }

  .about-overview__stat dt {
    font-size: 13px;
    line-height: 18px;
    letter-spacing: 0.2px;
    white-space: normal;
  }

  .about-mission {
    min-height: 0;
    padding: 32px 20px;
  }

  .about-mission__inner {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .about-mission__divider {
    width: 100%;
    height: 1px;
  }

  .about-mission__divider img {
    width: 100%;
    transform: translate(-50%, -50%);
  }

  .about-mission__body {
    font-size: 14px;
    line-height: 22px;
  }

  .about-journey {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .about-journey__timeline,
  .about-journey__step {
    --journey-gap: 32px;
  }

  .about-journey__timeline {
    gap: 32px;
    padding-left: 56px;
  }

  .about-journey__step:not(:last-child)::after {
    left: -38.5px;
    top: 33px;
    height: calc(100% + var(--journey-gap) - 29px);
  }

  .about-journey__node {
    left: -56px;
    width: 36px;
    height: 36px;
    font-size: 20px;
  }

  .about-journey__step-title {
    font-size: 18px;
    line-height: 26px;
  }

  .about-journey__step {
    gap: 6px;
  }

  .about-partners {
    gap: 20px;
  }

  .about-partners__copy-layer {
    position: static;
    display: block;
    order: -1;
    pointer-events: auto;
  }

  .about-partners__copy-frame {
    width: 100%;
    height: auto;
    zoom: 1;
  }

  .about-partners__copy {
    position: static;
    width: auto;
    transform: none;
  }

  .about-partners__title {
    width: auto;
  }

  .about-partners__intro {
    font-size: 14px;
    line-height: 22px;
  }

  .about-leaders {
    gap: 28px;
  }

  .about-leaders__intro,
  .about-journey__lead {
    font-size: 14px;
    line-height: 22px;
  }

  .about-leaders__grid {
    grid-template-columns: minmax(0, 406px);
    gap: 24px;
  }

  .about-values {
    min-height: 0;
    padding: 40px 20px;
    gap: 28px;
  }

  .about-values__intro {
    font-size: 16px;
    line-height: 24px;
    letter-spacing: 0.4px;
  }

  .about-values__row {
    grid-template-columns: minmax(0, 280px);
    gap: 16px;
  }

  .about-values__col {
    height: 420px;
  }

  .about-values__letter {
    top: 130px;
    height: 260px;
    font-size: 340px;
  }

  .about-values__card {
    top: 150px;
    height: 270px;
    padding: 56px 20px 32px;
  }
}

@media (max-width: 480px) {
  .about-page {
    margin-top: -88px;
  }
}
</style>
