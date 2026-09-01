<script setup>
import { RouterLink } from "vue-router";

defineProps({
  hero: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  site: { type: Object, default: null },
});
</script>

<template>
  <section class="home-hero" aria-label="Hero">
    <div class="home-hero__bg" aria-hidden="true">
      <img
        src="/images/figma-contact/hero-bg@2x.png"
        alt=""
        width="1440"
        height="628"
        decoding="async"
      />
    </div>

    <!-- Figma node 1:5338 — centered copy -->
    <div class="home-hero__copy">
      <div class="home-hero__badges">
        <span
          v-for="(badge, index) in hero.compliance_badges || []"
          :key="badge"
          class="home-hero__badge-item"
        >
          <img
            v-if="index > 0"
            class="home-hero__badge-sep"
            src="/images/figma-home/hero-badge-sep.svg"
            alt=""
            width="1"
            height="18"
          />
          {{ badge }}
        </span>
      </div>

      <div class="home-hero__body">
        <div class="home-hero__text">
          <h1 class="home-hero__title">{{ hero.headline }}</h1>
          <p class="home-hero__lead">{{ hero.subheadline }}</p>
        </div>

        <RouterLink to="/contact" class="home-hero__cta">
          {{ hero.cta_primary || "Talk to Expert" }}
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

    <!-- Figma hero float graphics -->
    <img
      class="home-hero__float home-hero__float--mdr"
      src="/images/figma-home/Group%201171275340.svg"
      alt=""
      width="175"
      height="92"
      loading="lazy"
      decoding="async"
      aria-hidden="true"
    />
    <img
      class="home-hero__float home-hero__float--payout"
      src="/images/figma-home/Frame%202147225794.svg"
      alt=""
      width="176"
      height="78"
      loading="lazy"
      decoding="async"
      aria-hidden="true"
    />
    <img
      class="home-hero__float home-hero__float--routing"
      src="/images/figma-home/Frame%202147225799.svg"
      alt=""
      width="175"
      height="58"
      loading="lazy"
      decoding="async"
      aria-hidden="true"
    />
    <img
      class="home-hero__float home-hero__float--uptime"
      src="/images/figma-home/Frame%202147225798.svg"
      alt=""
      width="166"
      height="76"
      loading="lazy"
      decoding="async"
      aria-hidden="true"
    />
  </section>
</template>

<style scoped>
.home-hero {
  --home-ink: #252b37;
  --home-muted: #535862;
  --home-teal: #097495;
  --home-teal-border: #0292b8;
  position: relative;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  min-height: 548px;
  padding-bottom: 0;
  box-sizing: border-box;
  overflow: hidden;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-hero__bg {
  position: absolute;
  inset: 0 auto auto 50%;
  transform: translateX(-50%);
  width: 1440px;
  height: 560px;
  pointer-events: none;
  z-index: 0;
}

.home-hero__bg img {
  display: block;
  width: 1440px;
  height: 560px;
  object-fit: cover;
  object-position: center top;
}

/* Figma 1:5338 */
.home-hero__copy {
  position: absolute;
  left: 50%;
  top: 200px;
  z-index: 2;
  width: 611px;
  max-width: calc(100% - 48px);
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  text-align: center;
}

/* Figma 1:5339 */
.home-hero__badges {
  display: inline-flex;
  align-items: flex-end;
  gap: 12px;
  padding: 8px 12px;
  border: 1px solid var(--home-teal-border);
  border-radius: 29px;
}

.home-hero__badge-item {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 1.78px;
  text-transform: uppercase;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.home-hero__badge-sep {
  display: block;
  width: 1px;
  height: 18px;
  flex-shrink: 0;
}

/* Figma 1:5343 */
.home-hero__body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  width: 100%;
}

.home-hero__text {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.home-hero__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  letter-spacing: -1.26px;
  color: var(--home-ink);
}

.home-hero__lead {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.56px;
  color: var(--home-muted);
}

/* Figma 1:5347 */
.home-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: var(--home-teal);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  box-sizing: border-box;
}

.home-hero__cta:hover {
  background: #086681;
}

.home-hero__cta img {
  width: 18px;
  height: 18px;
  filter: brightness(0) invert(1);
}

.home-hero__float {
  position: absolute;
  z-index: 1;
  display: block;
  height: auto;
  pointer-events: none;
}

/* Figma Group 1171275340 — Low MDR + arrow */
.home-hero__float--mdr {
  left: 128px;
  top: 280px;
  width: 175px;
}

/* Figma Frame 2147225794 — Recent Payout */
.home-hero__float--payout {
  left: 176px;
  top: 468px;
  width: 176px;
}

/* Figma Frame 2147225799 — Smart Routing */
.home-hero__float--routing {
  left: 1162px;
  top: 276px;
  width: 175px;
}

/* Figma Frame 2147225798 — Core Uptime */
.home-hero__float--uptime {
  left: 1094px;
  top: 468px;
  width: 166px;
}

@media (max-width: 1280px) {
  .home-hero__float--routing {
    left: auto;
    right: 103px;
    top: 276px;
  }

  .home-hero__float--uptime {
    left: auto;
    right: 180px;
    top: 468px;
  }
}

@media (max-width: 1100px) {
  .home-hero {
    min-height: 500px;
  }

  .home-hero__float {
    display: none;
  }
}

@media (max-width: 768px) {
  .home-hero {
    min-height: auto;
    padding-bottom: 48px;
  }

  .home-hero__copy {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    margin: 0 auto;
    padding: 168px 24px 0;
  }

  .home-hero__title {
    font-size: 32px;
    letter-spacing: -0.8px;
  }

  .home-hero__body {
    gap: 28px;
  }
}
</style>
