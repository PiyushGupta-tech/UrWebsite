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
        src="/images/herobg.svg"
        alt=""
        width="1440"
        height="600"
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
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.home-hero__bg img {
  display: block;
  position: absolute;
  left: 50%;
  top: 0;
  width: 100%;
  min-width: 100%;
  height: 100%;
  min-height: 100%;
  transform: translateX(-50%);
  object-fit: cover;
  object-position: center top;
}

.home-hero__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: var(--ur-page-max, 1440px);
  margin: 0 auto;
  min-height: max(560px, calc(100svh - var(--home-trust-peek)));
  padding: var(--home-nav-clearance) var(--ur-gutter) 0;
  box-sizing: border-box;
}

.home-hero__stage {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(280px, 545px) minmax(280px, 1fr);
  align-items: center;
  gap: clamp(24px, 3vw, 40px);
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
  font-size: var(--ur-heading-lg, 42px);
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
  /* Keep diagram in flow so section gap below isn’t eaten by a transform */
  margin-top: 24px;
}

/* Tablet: centered stack (Figma iPad 208:3123) */
@media (max-width: 1200px) {
  .home-hero__inner {
    padding: 120px 40px 0;
    min-height: auto;
  }

  .home-hero__stage {
    grid-template-columns: 1fr;
    gap: 40px;
    max-width: 673px;
    margin-inline: auto;
  }

  .home-hero__copy {
    align-items: center;
    gap: 24px;
    max-width: 570px;
    margin: 0 auto;
  }

  .home-hero__text {
    gap: 12px;
    text-align: center;
  }

  .home-hero__title {
    font-size: 34px;
    line-height: 42px;
    letter-spacing: -0.8px;
  }

  .home-hero__lead {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0;
    text-align: center;
  }

  .home-hero__cta {
    width: auto;
    min-width: 142px;
    height: 40px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -0.28px;
  }

  .home-hero__visual {
    padding-top: 0;
  }

  .home-hero__diagram {
    width: min(100%, 674px);
    max-height: none;
    transform: none;
    margin-top: 0;
    margin-inline: auto;
  }
}

@media (max-width: 700px) {
  .home-hero__inner {
    padding: 104px 19px 0;
  }

  .home-hero__stage {
    max-width: none;
    gap: 32px;
  }

  .home-hero__copy {
    max-width: 353px;
  }

  .home-hero__title {
    font-size: 28px;
    line-height: 1.15;
  }

  .home-hero__lead {
    font-size: 14px;
    line-height: 1.56;
  }

  .home-hero__diagram {
    width: min(100%, 324px);
    max-height: 240px;
  }
}
</style>
