<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import HomeHeroDiagram from "@/components/HomeHeroDiagram.vue";

const props = defineProps({
  hero: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  site: { type: Object, default: null },
});

function splitWords(text) {
  return String(text || "").trim().split(/\s+/).filter(Boolean);
}

/* Split so each word can blur in on its own. */
const headlineWords = computed(() => splitWords(props.hero.headline));
const leadWords = computed(() => splitWords(props.hero.subheadline));
</script>

<template>
  <!-- Figma home 975:8531 — centred copy above the full-width infrastructure graphic -->
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
        <div
          class="home-hero__copy"
          :style="{ '--word-count': headlineWords.length, '--lead-count': leadWords.length }"
        >
          <div class="home-hero__text">
            <h1 class="home-hero__title">
              <template v-for="(word, i) in headlineWords" :key="i">
                <span class="home-hero__word" :style="{ '--i': i }">{{ word }}</span>{{ i < headlineWords.length - 1 ? " " : "" }}
              </template>
            </h1>
            <p class="home-hero__lead">
              <template v-for="(word, i) in leadWords" :key="i">
                <span class="home-hero__word home-hero__word--lead" :style="{ '--i': i }">{{ word }}</span
                >{{ i < leadWords.length - 1 ? " " : "" }}
              </template>
            </p>
          </div>
          <RouterLink to="/contact" class="home-hero__cta">
            <span class="home-hero__cta-label">{{ hero.cta_primary || "Talk to an Expert" }}</span>
            <img
              class="home-hero__cta-arrow"
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
  width: 100%;
  min-height: 0;
  padding-top: 40px;
}

.home-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  margin: 0 auto;
}

.home-hero__text {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  text-align: center;
}

.home-hero__title {
  margin: 0;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -1.26px;
  color: var(--home-ink);
  text-wrap: balance;
}

.home-hero__word {
  display: inline-block;
}

.home-hero__lead {
  max-width: 760px;
  margin: 0 auto;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.56px;
  color: var(--home-muted);
}

/* The nav's "Talk to an Expert" button at 70% size. */
.home-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 2.8px;
  min-width: 108.5px;
  height: 36.4px;
  padding: 0 11.2px;
  box-sizing: border-box;
  border-radius: 5.6px;
  background: var(--home-teal);
  color: #ffffff;
  font-size: 11.2px;
  font-weight: 700;
  letter-spacing: -0.224px;
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}

.home-hero__cta:hover {
  opacity: 0.92;
  color: #ffffff;
}

.home-hero__cta-label {
  display: inline-flex;
  align-items: center;
  line-height: 1;
}

.home-hero__cta-arrow {
  display: block;
  flex-shrink: 0;
  width: 12.6px;
  height: 12.6px;
}

.home-hero__visual {
  display: flex;
  justify-content: center;
  width: 100%;
  min-width: 0;
}

.home-hero__diagram {
  width: 100%;
  max-width: 1180px;
  margin-inline: auto;
}

/*
 * Laptop: the diagram sits 10px under the CTA and is also capped by the viewport height
 * left under the copy (nav clearance + stage padding + one-line title + two-line lead +
 * CTA + gaps), leaving 10px above the viewport bottom. It scales itself from its width.
 */
@media (min-width: 1201px) {
  .home-hero__stage {
    --home-diagram-gap: 10px;
    gap: var(--home-diagram-gap);
  }

  .home-hero__visual .home-hero__diagram {
    --home-diagram-top: calc(
      var(--home-nav-clearance) + 40px + var(--ur-heading-lg, 42px) * 1.15 + 12px + 48px + 32px + 36.4px +
        var(--home-diagram-gap)
    );
    max-width: min(1180px, max(760px, calc((100svh - var(--home-diagram-top) - 10px) * 1180 / 512)));
  }
}

/* Tablet: centered stack (Figma iPad 208:3123) */
@media (max-width: 1200px) {
  .home-hero__inner {
    padding: 120px 40px 0;
    min-height: auto;
  }

  .home-hero__stage {
    gap: 40px;
    padding-top: 0;
  }

  .home-hero__copy {
    gap: 24px;
    max-width: 570px;
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
    min-width: 142px;
    height: 40px;
    padding: 0 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  .home-hero__cta-arrow {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 700px) {
  .home-hero__inner {
    padding: 104px 19px 0;
  }

  .home-hero__stage {
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
}

/*
 * Entrance: headline words blur in one after another, the lead follows with a
 * tighter stagger (it has ~3x the words), then the CTA pops up.
 */
@media (prefers-reduced-motion: no-preference) {
  .home-hero__word {
    animation: home-hero-word-in 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
    animation-delay: calc(0.1s + var(--i) * 0.08s);
  }

  .home-hero__word--lead {
    animation-delay: calc(0.1s + var(--word-count) * 0.08s + var(--i) * 0.03s);
  }

  .home-hero__cta {
    animation: home-hero-cta-in 0.7s cubic-bezier(0.34, 1.4, 0.64, 1) both;
    animation-delay: calc(0.4s + var(--word-count) * 0.08s + var(--lead-count) * 0.03s);
  }
}

@keyframes home-hero-word-in {
  from {
    opacity: 0;
    filter: blur(10px);
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    filter: blur(0);
    transform: none;
  }
}

@keyframes home-hero-cta-in {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.8);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>
