<script setup>
import { RouterLink } from "vue-router";
import HomeHeroDiagram from "@/components/HomeHeroDiagram.vue";

defineProps({
  hero: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  site: { type: Object, default: null },
});
</script>

<template>
  <!-- Figma home 1:5281 — left copy + right product diagram; navbar unchanged -->
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

    <div class="home-hero__inner">
      <div class="home-hero__stage">
        <div class="home-hero__copy">
          <div class="home-hero__text">
            <h1 class="home-hero__title">{{ hero.headline }}</h1>
            <p class="home-hero__lead">{{ hero.subheadline }}</p>
          </div>
          <RouterLink to="/contact" class="home-hero__cta">
            {{ hero.cta_primary || "Talk to an Expert" }}
            <img
              src="/images/figma-contact/nav-arrow.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
        </div>

        <div class="home-hero__visual">
          <HomeHeroDiagram class="home-hero__diagram" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-hero {
  --home-ink: #252b37;
  --home-muted: #535862;
  --home-teal: #097495;
  --home-nav-clearance: 129px;
  --home-trust-peek: 80px;
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  overflow: hidden;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-hero__bg {
  position: absolute;
  inset: 0 auto auto 50%;
  transform: translateX(-50%);
  width: max(100%, 1440px);
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.home-hero__bg img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.home-hero__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  min-height: max(560px, calc(100svh - var(--home-trust-peek)));
  padding: var(--home-nav-clearance) 102px 48px;
  box-sizing: border-box;
}

.home-hero__stage {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(280px, 545px) minmax(280px, 1fr);
  align-items: center;
  gap: 40px;
  width: 100%;
  min-height: 0;
}

.home-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 40px;
  max-width: 545px;
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
  line-height: 1.15;
  letter-spacing: -1.26px;
  color: var(--home-ink);
}

.home-hero__lead {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.56px;
  color: var(--home-muted);
}

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
  filter: brightness(1.05);
}

.home-hero__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  padding-top: 12px;
}

.home-hero__diagram {
  display: block;
  width: min(100%, 604px);
  height: auto;
  max-height: 454px;
  transform: translateY(24px);
}

@media (max-width: 1100px) {
  .home-hero__inner {
    padding: 113px 40px 40px;
    min-height: auto;
  }

  .home-hero__stage {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .home-hero__copy {
    max-width: 640px;
  }

  .home-hero__diagram {
    max-height: 360px;
    transform: translateY(12px);
  }
}

@media (max-width: 768px) {
  .home-hero__inner {
    padding: 100px 24px 32px;
  }

  .home-hero__title {
    font-size: 32px;
    letter-spacing: -0.8px;
  }

  .home-hero__cta {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .home-hero__inner {
    min-height: auto;
    padding: 104px 19px 28px;
  }

  .home-hero__stage {
    gap: 40px;
  }

  .home-hero__copy {
    align-items: center;
    gap: 24px;
    max-width: 353px;
    margin: 0 auto;
  }

  .home-hero__text {
    gap: 10px;
    text-align: center;
  }

  .home-hero__title {
    font-size: 44px;
    line-height: 1.04;
    letter-spacing: -1.1px;
  }

  .home-hero__lead {
    font-size: 16px;
    line-height: 1.56;
    letter-spacing: 0;
    text-align: center;
  }

  .home-hero__cta {
    width: auto;
    min-width: 142px;
    height: 40px;
    padding: 10px 16px;
    font-size: 16px;
  }

  .home-hero__visual {
    padding-top: 0;
  }

  .home-hero__diagram {
    width: min(100%, 324px);
    max-height: 240px;
    transform: none;
  }
}
</style>
