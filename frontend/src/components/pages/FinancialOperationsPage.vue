<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import FoiBaasDiagram from "./FoiBaasDiagram.vue";
import FoiShowcaseCarousel from "./FoiShowcaseCarousel.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);

const advantageCards = computed(() => props.page?.advantages?.cards || []);
const showcaseCards = computed(() => props.page?.showcase?.cards || []);

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});

/** Mid CTA card metrics that count up from 0 whenever the section scrolls into view. */
const MID_COUNTS = {
  accounts: { value: 12480, decimals: 0 },
  success: { value: 98.7, decimals: 1, suffix: "%" },
  processed: { value: 18.2, decimals: 1, prefix: "+", suffix: "%" },
};
const MID_COUNT_MS = 1400;
/** Share of the section that must be visible before the count starts. */
const MID_COUNT_THRESHOLD = 0.4;

const canAnimateCounts =
  typeof window !== "undefined" &&
  "IntersectionObserver" in window &&
  !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function formatMidCount(key, progress) {
  const { value, decimals, prefix = "", suffix = "" } = MID_COUNTS[key];
  const number = (value * progress).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return `${prefix}${number}${suffix}`;
}

const midFinal = Object.fromEntries(
  Object.keys(MID_COUNTS).map((key) => [key, formatMidCount(key, 1)]),
);
const midSection = ref(null);
const midProgress = ref(canAnimateCounts ? 0 : 1);
const midCounts = computed(() => {
  const eased = 1 - (1 - midProgress.value) ** 3;
  return Object.fromEntries(
    Object.keys(MID_COUNTS).map((key) => [key, formatMidCount(key, eased)]),
  );
});

let midFrame = 0;
let midPlayed = false;
let midObserver = null;

function playMidCounts() {
  cancelAnimationFrame(midFrame);
  const start = performance.now();
  const step = (now) => {
    midProgress.value = Math.min(1, (now - start) / MID_COUNT_MS);
    if (midProgress.value < 1) midFrame = requestAnimationFrame(step);
  };
  midFrame = requestAnimationFrame(step);
}

if (canAnimateCounts) {
  midObserver = new IntersectionObserver(
    (entries) => {
      const entry = entries[entries.length - 1];
      if (!entry.isIntersecting) {
        cancelAnimationFrame(midFrame);
        midPlayed = false;
        midProgress.value = 0;
      } else if (!midPlayed && entry.intersectionRatio >= MID_COUNT_THRESHOLD) {
        midPlayed = true;
        playMidCounts();
      }
    },
    { threshold: [0, MID_COUNT_THRESHOLD] },
  );

  watch(
    midSection,
    (el, previous) => {
      if (previous) midObserver.unobserve(previous);
      if (el) midObserver.observe(el);
    },
    { flush: "post" },
  );
}

onBeforeUnmount(() => {
  cancelAnimationFrame(midFrame);
  midObserver?.disconnect();
});
</script>

<template>
  <main class="foi-page">
    <!-- Hero — Figma 385:7923 (1440×629) -->
    <section class="foi-hero" :class="{ 'foi-hero--ready': heroReady }">
      <div class="foi-hero__bg" aria-hidden="true">
        <img
          class="foi-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="foi-hero__inner">
        <p v-if="page.eyebrow" class="foi-hero__eyebrow">{{ page.eyebrow }}</p>
        <h1 class="foi-hero__title">{{ page.title }}</h1>
        <p class="foi-hero__intro">{{ page.intro }}</p>
        <RouterLink to="/contact" class="foi-hero__cta">
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

    <!-- Infra heading — Figma 405:3124 (821×172 @ x=310) -->
    <section v-if="page.infra" class="foi-section foi-section--infra">
      <div class="foi-section__head foi-section__head--center">
        <h2 class="foi-section__title">{{ page.infra.title }}</h2>
        <p class="foi-section__body">{{ page.infra.body }}</p>
      </div>
    </section>

    <!-- BAAS diagram — Figma 391:11616 (1291×813 @ x=75) -->
    <section v-if="page.diagram" class="foi-section foi-section--diagram">
      <FoiBaasDiagram
        :image="page.diagram.image"
        :alt="page.diagram.image_alt || page.infra?.title || page.title"
      />
    </section>

    <!-- Advantages — Figma 405:3132 (1202×608 @ x=119) -->
    <section v-if="page.advantages" class="foi-section foi-section--advantages">
      <div class="foi-advantages">
        <div class="foi-advantages__head">
          <h2 class="foi-advantages__title">{{ page.advantages.title }}</h2>
          <p class="foi-advantages__body">{{ page.advantages.body }}</p>
        </div>

        <div class="foi-advantages__grid" aria-label="Operational advantages">
          <article
            v-for="(card, index) in advantageCards"
            :key="card.title"
            class="foi-advantages__card"
          >
            <img
              class="foi-advantages__bullet"
              :src="
                index % 2 === 0
                  ? '/images/figma-financial-ops/icons/bullet-a.svg'
                  : '/images/figma-financial-ops/icons/bullet-b.svg'
              "
              alt=""
              width="28"
              height="28"
              decoding="async"
            />
            <h3 class="foi-advantages__card-title">{{ card.title }}</h3>
            <p class="foi-advantages__card-body">{{ card.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Showcase carousel — Skiper49 inverted coverflow on Figma cards -->
    <section v-if="page.showcase" class="foi-section foi-section--showcase">
      <div class="foi-showcase">
        <div class="foi-section__head foi-section__head--center">
          <h2 class="foi-section__title">{{ page.showcase.title }}</h2>
          <p class="foi-section__body">{{ page.showcase.body }}</p>
        </div>

        <div class="foi-carousel">
          <div class="foi-carousel__stage" aria-live="polite">
            <FoiShowcaseCarousel
              :cards="showcaseCards"
              :initial-slide="1"
              :autoplay-delay="5000"
            />
          </div>
        </div>
      </div>
    </section>
    <!-- Mid CTA — Figma 385:8558 (1440×557) -->
    <section v-if="page.mid_cta" ref="midSection" class="foi-mid">
      <div class="foi-mid__frame">
        <div class="foi-mid__stage">
          <!-- Soft teal glows (CSS radial — fades to transparent, no hard box edge) -->
          <div class="foi-mid__glow foi-mid__glow--left" aria-hidden="true" />
          <div class="foi-mid__glow foi-mid__glow--right" aria-hidden="true" />

          <!-- Connector lines -->
          <img
            class="foi-mid__line foi-mid__line--left"
            src="/images/figma-financial-ops/mid/line-left.svg"
            alt=""
            width="128"
            height="2"
            decoding="async"
            aria-hidden="true"
          />
          <div class="foi-mid__line foi-mid__line--mid" aria-hidden="true">
            <img
              src="/images/figma-financial-ops/mid/line-mid.svg"
              alt=""
              width="128"
              height="147"
              decoding="async"
            />
          </div>
          <div class="foi-mid__line foi-mid__line--right-top" aria-hidden="true">
            <img
              src="/images/figma-financial-ops/mid/line-right-top.svg"
              alt=""
              width="60"
              height="215"
              decoding="async"
            />
          </div>
          <img
            class="foi-mid__line foi-mid__line--right-bottom"
            src="/images/figma-financial-ops/mid/line-right-bottom.svg"
            alt=""
            width="150"
            height="265"
            decoding="async"
            aria-hidden="true"
          />

          <!-- Floating cards -->
          <article class="foi-mid__card foi-mid__card--accounts">
            <div class="foi-mid__card-icon" aria-hidden="true">
              <img
                src="/images/figma-financial-ops/mid/icon-account.svg"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
            </div>
            <div class="foi-mid__card-copy">
              <p class="foi-mid__card-label">Virtual Accounts</p>
              <p class="foi-mid__card-value">
                <span class="foi-mid__count">
                  <span class="foi-mid__count-size" aria-hidden="true">{{ midFinal.accounts }}</span>
                  <span class="foi-mid__count-live">{{ midCounts.accounts }}</span>
                </span>
                Active Accounts
              </p>
            </div>
          </article>

          <article class="foi-mid__card foi-mid__card--transactions">
            <div class="foi-mid__card-icon" aria-hidden="true">
              <img
                src="/images/figma-financial-ops/mid/icon-transaction.svg"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
            </div>
            <div class="foi-mid__card-copy">
              <p class="foi-mid__card-label">Transactions</p>
              <p class="foi-mid__card-value">
                <span class="foi-mid__count">
                  <span class="foi-mid__count-size" aria-hidden="true">{{ midFinal.success }}</span>
                  <span class="foi-mid__count-live">{{ midCounts.success }}</span>
                </span>
                Success Rate
              </p>
            </div>
          </article>

          <article class="foi-mid__card foi-mid__card--dashboard">
            <div class="foi-mid__dash-head">
              <img
                src="/images/figma-financial-ops/mid/icon-dashboard.svg"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
              <p>Operational Dashboard</p>
            </div>
            <div class="foi-mid__dash-rule" aria-hidden="true" />
            <div class="foi-mid__avatars">
              <img
                src="/images/figma-financial-ops/mid/avatar-1.jpg"
                alt=""
                width="32"
                height="32"
                decoding="async"
              />
              <img
                src="/images/figma-financial-ops/mid/avatar-2.jpg"
                alt=""
                width="32"
                height="32"
                decoding="async"
              />
            </div>
            <div class="foi-mid__card-copy">
              <p class="foi-mid__card-label">Processed this month</p>
              <p class="foi-mid__card-value foi-mid__card-value--semi">
                <span class="foi-mid__count">
                  <span class="foi-mid__count-size" aria-hidden="true">{{ midFinal.processed }}</span>
                  <span class="foi-mid__count-live">{{ midCounts.processed }}</span>
                </span>
              </p>
            </div>
            <div class="foi-mid__progress" aria-hidden="true">
              <span class="foi-mid__progress-fill" />
            </div>
          </article>

          <!-- Center copy + CTA -->
          <div class="foi-mid__copy">
            <div class="foi-mid__copy-text">
              <h2 class="foi-mid__title">
                Build the Financial Infrastructure<br />
                Your Business Needs
              </h2>
              <p class="foi-mid__body">
                Connect your products to scalable financial infrastructure and create
                smarter, more connected financial experiences.
              </p>
            </div>
            <RouterLink to="/contact" class="foi-mid__cta">
              <span>{{ page.mid_cta.cta_label || "Talk to Expert" }}</span>
              <img
                src="/images/figma-financial-ops/mid/cta-arrow.svg"
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
  </main>
</template>

<style scoped>
.foi-page {
  --foi-ink: #252b37;
  --foi-muted: #535862;
  --foi-teal: #097495;
  --foi-surface: #f8fafc;
  background: #ffffff;
  color: var(--foi-ink);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

/* —— Hero 385:7923 —— */
.foi-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.foi-hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.foi-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.foi-hero__inner {
  position: relative;
  z-index: 1;
  width: min(808px, calc(100% - 48px));
  margin: 0 auto;
  padding: 80px 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0;
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.55s ease,
    transform 0.55s ease;
}

.foi-hero--ready .foi-hero__inner {
  opacity: 1;
  transform: none;
}

.foi-hero__eyebrow {
  margin: 0 0 18px;
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  background: transparent;
  font-size: 12px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 1.7836px;
  text-transform: uppercase;
  color: #0292b8;
}

.foi-hero__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--foi-ink);
  text-transform: capitalize;
}

.foi-hero__intro {
  margin: 12px 0 0;
  max-width: 669px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.56px;
  color: var(--foi-muted);
}

.foi-hero__cta {
  margin-top: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: var(--foi-teal);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.foi-hero__cta:hover {
  background: #075f7a;
}

/* —— Shared section chrome —— */
.foi-section {
  width: min(1291px, calc(100% - 48px));
  margin-inline: auto;
}

.foi-section__head--center {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  width: min(821px, 100%);
  margin-inline: auto;
}

.foi-section__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--foi-ink);
  white-space: pre-line;
}

.foi-section__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--foi-muted);
  white-space: pre-line;
}

.foi-section--infra {
  margin-top: 100px;
  padding-top: 0;
  padding-bottom: 0;
}

.foi-section--diagram {
  margin-top: 56px;
  display: flex;
  justify-content: center;
  padding-inline: 10px;
}

/* —— Advantages 405:3132 —— */
.foi-section--advantages {
  margin-top: 100px;
  width: min(1202px, calc(100% - 48px));
}

.foi-advantages {
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.foi-advantages__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 48px;
}

.foi-advantages__title {
  margin: 0;
  width: min(690px, 100%);
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--foi-ink);
}

.foi-advantages__body {
  margin: 0;
  width: min(389px, 100%);
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  color: var(--foi-muted);
  flex-shrink: 0;
}

.foi-advantages__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 48px 24px;
  padding: 40px 24px;
  background: var(--foi-surface);
  border-radius: 16px;
}

.foi-advantages__card {
  position: relative;
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.foi-advantages__card:not(:nth-child(3n))::after {
  content: "";
  position: absolute;
  top: 50%;
  right: -12px;
  width: 1px;
  height: 148px;
  transform: translateY(-50%);
  background: #e4e7ec;
}

.foi-advantages__bullet {
  display: block;
  width: 28px;
  height: 28px;
  margin-bottom: 16px;
}

.foi-advantages__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: var(--foi-ink);
}

.foi-advantages__card-body {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  color: var(--foi-muted);
}
/* —— Showcase carousel (Skiper49 inverted coverflow) —— */
.foi-section--showcase {
  margin-top: 100px;
  width: min(1206px, calc(100% - 48px));
}

.foi-showcase {
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.foi-carousel {
  width: 100%;
}

.foi-carousel__stage {
  position: relative;
  width: 100%;
  min-height: 505px;
  overflow: visible;
}

/* —— Mid CTA 385:8558 (1440×557 artboard) —— */
.foi-mid {
  /* Title sits 163px into the artboard — pull up so dots → title = 150px */
  margin-top: calc(150px - 163px);
  width: 100%;
  /* Let glows fade past the artboard into the page white */
  overflow: visible;
}

.foi-mid__frame {
  width: 100%;
  display: flex;
  justify-content: center;
  overflow: visible;
}

.foi-mid__stage {
  position: relative;
  width: 1440px;
  height: 557px;
  flex-shrink: 0;
  transform-origin: top center;
  overflow: visible;
}

/* Soft glows — pure radial fade to transparent (no SVG canvas cutoff) */
.foi-mid__glow {
  position: absolute;
  width: 560px;
  height: 560px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
  background: radial-gradient(
    circle at center,
    rgba(9, 116, 149, 0.22) 0%,
    rgba(9, 116, 149, 0.12) 28%,
    rgba(9, 116, 149, 0.05) 48%,
    rgba(9, 116, 149, 0.015) 62%,
    transparent 72%
  );
}

.foi-mid__glow--left {
  left: 246px;
  bottom: 38px;
}

.foi-mid__glow--right {
  left: 649px;
  bottom: 16px;
}

.foi-mid__line {
  position: absolute;
  z-index: 1;
  pointer-events: none;
  display: block;
}

.foi-mid__line--left {
  left: 0;
  top: 373px;
  width: 128px;
  height: 2px;
}

/* Figma: -rotate-90 wrapper at left 251 / top 189 */
.foi-mid__line--mid {
  left: 251px;
  top: 189px;
  width: 146.5px;
  height: 128px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.foi-mid__line--mid img {
  width: 128px;
  height: 146.5px;
  transform: rotate(-90deg);
  flex-shrink: 0;
}

.foi-mid__line--right-top {
  left: 1225px;
  top: 142px;
  width: 215px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.foi-mid__line--right-top img {
  width: 60px;
  height: 215px;
  transform: rotate(-90deg);
  flex-shrink: 0;
}

.foi-mid__line--right-bottom {
  left: 1057.5px;
  top: 301px;
  width: 150px;
  height: 264.5px;
}

.foi-mid__copy {
  position: absolute;
  left: 386px;
  top: 163px;
  z-index: 2;
  width: 681px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  text-align: center;
}

.foi-mid__copy-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.foi-mid__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--foi-ink);
}

.foi-mid__body {
  margin: 0;
  max-width: 100%;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: var(--foi-muted);
}

.foi-mid__cta {
  position: relative;
  z-index: 5;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: var(--foi-teal);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.foi-mid__cta:hover {
  background: #075f7a;
}

.foi-mid__card {
  position: absolute;
  z-index: 4;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(9, 116, 149, 0.1);
  overflow: hidden;
}

/* 48px left of Figma so the card clears the body copy (starts at x≈420). */
.foi-mid__card--accounts {
  left: 112px;
  top: 269px;
  width: 283px;
}

.foi-mid__card--transactions {
  left: 80px;
  top: 381px;
  width: 257px;
}

.foi-mid__card--dashboard {
  left: 1090px;
  top: 193px;
  width: 270px;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.foi-mid__card-icon {
  width: 48px;
  height: 48px;
  border-radius: 24px;
  background: var(--foi-surface);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.foi-mid__card-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-start;
  min-width: 0;
}

.foi-mid__card-label {
  margin: 0;
  font-size: 12px;
  font-weight: 500;
  line-height: normal;
  color: var(--foi-muted);
}

.foi-mid__card-value {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  color: var(--foi-ink);
}

.foi-mid__card-value--semi {
  font-weight: 600;
}

/*
 * A hidden copy of the final value holds the layout width; the live value is
 * overlaid, so the words after it never shift while counting.
 */
.foi-mid__count {
  position: relative;
  display: inline-block;
}

.foi-mid__count-size {
  visibility: hidden;
}

.foi-mid__count-live {
  position: absolute;
  top: 0;
  left: 0;
  white-space: nowrap;
}

.foi-mid__dash-head {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  font-size: 16px;
  font-weight: 500;
  color: var(--foi-ink);
}

.foi-mid__dash-head p {
  margin: 0;
  white-space: nowrap;
}

.foi-mid__dash-rule {
  width: 100%;
  height: 1px;
  background: #e4e7ec;
}

.foi-mid__avatars {
  display: flex;
  align-items: flex-start;
}

.foi-mid__avatars img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ffffff;
}

.foi-mid__avatars img + img {
  margin-left: -2px;
}

.foi-mid__progress {
  width: 138px;
  height: 7px;
  border-radius: 8px;
  background: #f8f8f8;
  overflow: hidden;
}

/* Resting fill is Figma's 97 of 138px; the loop sweeps it fuller and back. */
.foi-mid__progress-fill {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  background: var(--foi-teal);
  clip-path: inset(0 29.71% 0 0 round 8px);
  animation: foi-mid-progress 2.4s cubic-bezier(0.42, 0, 0.58, 1) infinite alternate;
}

@keyframes foi-mid-progress {
  from {
    clip-path: inset(0 85% 0 0 round 8px);
  }
  to {
    clip-path: inset(0 0 0 0 round 8px);
  }
}

/* Scale full artboard down on narrower desktops */
@media (max-width: 1440px) and (min-width: 901px) {
  .foi-mid {
    margin-top: calc(100px - 163px * (100vw / 1440));
  }

  .foi-mid__stage {
    transform: scale(calc(100vw / 1440));
    margin-bottom: calc(557px * (100vw / 1440 - 1));
  }
}

@media (max-width: 1100px) {
  .foi-advantages__head {
    flex-direction: column;
    gap: 16px;
  }

  .foi-advantages__body {
    width: 100%;
  }

  .foi-advantages__card:not(:nth-child(3n))::after {
    display: none;
  }
}

@media (max-width: 900px) {
  .foi-hero {
    min-height: 0;
  }

  .foi-hero__title,
  .foi-section__title,
  .foi-advantages__title {
    font-size: 32px;
    line-height: 42px;
  }

  .foi-advantages__grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .foi-section--infra,
  .foi-section--diagram,
  .foi-section--advantages,
  .foi-section--showcase {
    margin-top: 64px;
  }

  .foi-carousel__stage {
    min-height: min(420px, 70vw);
  }

  .foi-mid {
    margin-top: 150px;
  }

  .foi-mid__frame {
    overflow: visible;
    padding: 0 20px;
  }

  .foi-mid__stage {
    width: 100%;
    height: auto;
    transform: none;
    margin-bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
    padding: 24px 0 8px;
  }

  .foi-mid__glow,
  .foi-mid__line {
    display: none;
  }

  .foi-mid__copy {
    position: relative;
    left: auto;
    top: auto;
    width: 100%;
    max-width: 560px;
    order: 1;
    gap: 24px;
  }

  .foi-mid__title {
    font-size: 28px;
    line-height: 36px;
  }

  .foi-mid__card {
    position: relative;
    left: auto !important;
    top: auto !important;
    width: 100%;
    max-width: 320px;
    order: 2;
  }

  .foi-mid__card--dashboard {
    order: 3;
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-hero__inner {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .foi-mid__progress-fill {
    animation: none;
  }
}
</style>
