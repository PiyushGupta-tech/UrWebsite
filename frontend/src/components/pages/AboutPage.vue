<script setup>
import { computed, onMounted, ref } from "vue";
import AboutHeroGraphic from "./AboutHeroGraphic.vue";
import AboutEcoPanel from "./AboutEcoPanel.vue";
import AboutEcoTip from "./AboutEcoTip.vue";
import { provideAboutEco } from "@/composables/useAboutEco.js";
import { useReveal } from "@/composables/useReveal.js";

const props = defineProps({
  page: { type: Object, required: true },
});

const introParagraphs = computed(() =>
  Array.isArray(props.page.intro) ? props.page.intro : [props.page.intro]
);

const heroReady = ref(false);

provideAboutEco(heroReady);
useReveal(".about-reveal");

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});
</script>

<template>
  <main class="about">
    <!-- Hero -->
    <section class="about-hero section--tight" :class="{ 'about-hero--ready': heroReady }">
      <div class="about-hero__glow" aria-hidden="true" />
      <div class="container about-hero__layout">
        <div class="about-hero__copy">
          <h1 class="about-hero__title">{{ page.title }}</h1>
          <p
            v-for="(para, index) in introParagraphs"
            :key="index"
            class="about-hero__intro"
          >
            {{ para }}
          </p>
          <div class="about-hero__rule" aria-hidden="true" />
        </div>
        <div class="about-hero__visual">
          <AboutHeroGraphic class="about-hero__graphic" />
          <AboutEcoTip />
          <AboutEcoPanel class="about-hero__eco-panel" />
        </div>
      </div>
    </section>

    <!-- Story articles -->
    <section class="section about-story">
      <div class="container about-story__grid">
        <article
          v-for="(block, index) in page.blocks"
          :key="block.heading"
          class="about-article about-reveal"
          :data-delay="index"
        >
          <span class="about-article__index" aria-hidden="true">
            {{ String(index + 1).padStart(2, "0") }}
          </span>
          <div class="about-article__body">
            <h2>{{ block.heading }}</h2>
            <p>{{ block.body }}</p>
            <h3 v-if="block.bullets_heading" class="about-article__subhead">
              {{ block.bullets_heading }}
            </h3>
            <ul v-if="block.bullets?.length" class="about-article__list">
              <li v-for="b in block.bullets" :key="b">{{ b }}</li>
            </ul>
            <p v-if="block.closing" class="about-article__closing">{{ block.closing }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Partners -->
    <section class="section about-panel">
      <div class="container">
        <header class="about-panel__head about-reveal">
          <p class="eyebrow">Partner spotlight</p>
          <h2 class="about-panel__title">Built with leaders who scale</h2>
        </header>
        <div class="about-partners">
          <article
            v-for="(partner, index) in page.partners"
            :key="partner.name"
            class="about-partner about-reveal"
            :data-delay="index + 1"
          >
            <h3>{{ partner.name }}</h3>
            <p>{{ partner.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Offerings -->
    <section class="section about-offerings-section">
      <div class="container">
        <header class="about-panel__head about-reveal">
          <p class="eyebrow">What We Offer</p>
          <h2 class="about-panel__title">Payments That Grow With You</h2>
        </header>
        <p v-if="page.offerings_intro" class="about-offerings__intro about-reveal">
          {{ page.offerings_intro }}
        </p>
        <div class="about-offerings">
          <article
            v-for="(item, index) in page.offerings"
            :key="item.title"
            class="about-offering about-reveal"
            :data-delay="index"
          >
            <span class="about-offering__dot" aria-hidden="true" />
            <h3>{{ item.title }}</h3>
            <p>{{ item.body }}</p>
            <h4 v-if="item.bullets_heading" class="about-offering__subhead">
              {{ item.bullets_heading }}
            </h4>
            <ul v-if="item.bullets?.length" class="about-offering__list">
              <li v-for="b in item.bullets" :key="b">{{ b }}</li>
            </ul>
          </article>
        </div>
        <p v-if="page.offerings_closing" class="about-offerings__closing about-reveal">
          {{ page.offerings_closing }}
        </p>
      </div>
    </section>

    <!-- Closing -->
    <section class="section about-panel">
      <div class="container about-closing">
        <article
          v-for="(section, index) in page.closing_sections"
          :key="section.heading"
          class="about-closing__card about-reveal"
          :data-delay="index"
        >
          <h2>{{ section.heading }}</h2>
          <p>{{ section.body }}</p>
        </article>
      </div>
    </section>

    <!-- Tagline -->
    <section class="about-tagline about-reveal">
      <div class="container about-tagline__inner">
        <p class="about-tagline__text">{{ page.tagline }}</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.about {
  --about-navy: #1a365d;
  --about-cyan: #06b6d4;
  --about-gradient: linear-gradient(135deg, var(--about-navy) 0%, var(--about-cyan) 100%);
}

/* Hero */
.about-hero {
  position: relative;
  overflow: visible;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
}

.about-hero__glow {
  position: absolute;
  top: 50%;
  right: 8%;
  width: min(420px, 42vw);
  height: min(420px, 42vw);
  transform: translateY(-50%);
  background: radial-gradient(
    circle,
    rgba(6, 182, 212, 0.1) 0%,
    rgba(26, 54, 93, 0.04) 50%,
    transparent 72%
  );
  animation: about-glow-drift 14s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 0;
}

@keyframes about-glow-drift {
  from {
    transform: translate(0, 0) scale(1);
  }
  to {
    transform: translate(-6%, 8%) scale(1.08);
  }
}

.about-hero__layout {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 28px;
  align-items: start;
  padding-block: 8px 16px;
}

.about-hero__copy {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 520px;
  align-self: start;
}

.about-hero__visual {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
  width: 100%;
  max-width: 384px;
  justify-self: center;
  align-self: center;
}

.about-hero__eco-panel {
  margin-top: 4px;
}

.about-hero__graphic {
  width: 100%;
}

@media (min-width: 900px) {
  .about-hero__layout {
    grid-template-columns: 1.05fr 0.95fr;
    gap: 36px;
    min-height: 0;
    align-items: center;
  }

  .about-hero__copy {
    align-self: start;
  }

  .about-hero__visual {
    justify-self: center;
    align-self: center;
  }
}

.about-hero__title {
  margin: 0 0 16px;
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.1;
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.6s ease 0.05s,
    transform 0.6s ease 0.05s;
}

.about-hero__intro {
  margin: 0;
  font-size: 18px;
  line-height: 1.65;
  color: var(--text-secondary);
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.6s ease 0.12s,
    transform 0.6s ease 0.12s;
}

.about-hero__intro + .about-hero__intro {
  margin-top: 1.15em;
}

.about-hero__rule {
  margin-top: 28px;
  height: 3px;
  width: 0;
  max-width: 120px;
  border-radius: var(--radius-pill);
  background: var(--about-gradient);
  transition: width 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.28s;
}

.about-hero--ready .about-hero__title,
.about-hero--ready .about-hero__intro {
  opacity: 1;
  transform: translateY(0);
}

.about-hero--ready .about-hero__rule {
  width: 120px;
}

/* Scroll reveal */
.about-reveal {
  opacity: 0;
  transform: translateY(20px);
}

.about-reveal.is-visible {
  animation: about-reveal-in 0.65s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  animation-delay: calc(var(--delay, 0) * 0.08s);
}

.about-reveal[data-delay="0"] {
  --delay: 0;
}
.about-reveal[data-delay="1"] {
  --delay: 1;
}
.about-reveal[data-delay="2"] {
  --delay: 2;
}
.about-reveal[data-delay="3"] {
  --delay: 3;
}

@keyframes about-reveal-in {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Story articles */
.about-story__grid {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 820px;
}

.about-article {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 24px;
  padding: 32px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}

.about-article::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--about-gradient);
  transform: scaleY(0);
  transform-origin: top;
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1) 0.15s;
}

.about-article.is-visible::before {
  transform: scaleY(1);
}

.about-article__index {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--about-cyan);
  padding-top: 4px;
}

.about-article__body h2 {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--about-navy);
}

.about-article__body p {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
}

.about-article__subhead {
  margin: 20px 0 12px;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--about-navy);
}

.about-article__closing {
  margin-top: 20px;
}

.about-article__list {
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.about-article__list li {
  position: relative;
  padding-left: 18px;
  font-size: 15px;
  line-height: 1.55;
  color: var(--text-secondary);
}

.about-article__list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--about-gradient);
}

/* Panel sections */
.about-panel {
  background: var(--bg-muted);
  border-block: 1px solid var(--border);
}

.about-panel__head {
  max-width: 560px;
  margin-bottom: 32px;
}

.about-panel__title {
  margin: 0;
  font-size: clamp(24px, 3.5vw, 32px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

/* Partners */
.about-partners {
  display: grid;
  gap: 20px;
}

@media (min-width: 768px) {
  .about-partners {
    grid-template-columns: repeat(2, 1fr);
  }
}

.about-partner {
  padding: 28px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.about-partner.is-visible:hover {
  transform: translateY(-4px);
  border-color: rgba(6, 182, 212, 0.35);
  box-shadow: 0 12px 32px rgba(26, 54, 93, 0.08);
}

.about-partner h3 {
  margin: 0 0 10px;
  font-size: 18px;
  font-weight: 700;
  color: var(--about-navy);
}

.about-partner p {
  margin: 0;
  font-size: 14px;
  line-height: 1.65;
  color: var(--text-secondary);
}

/* Offerings */
.about-offerings__intro,
.about-offerings__closing {
  margin: 0;
  max-width: 820px;
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
}

.about-offerings__intro {
  margin: 0 auto 32px;
  text-align: center;
}

.about-offerings__closing {
  margin: 32px auto 0;
  text-align: center;
  font-weight: 500;
  color: var(--text-primary);
}

.about-offerings {
  display: grid;
  gap: 20px;
}

@media (min-width: 768px) {
  .about-offerings {
    grid-template-columns: repeat(2, 1fr);
  }
}

.about-offering {
  padding: 28px 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  transition: border-color 0.25s ease;
}

.about-offering.is-visible:hover {
  border-color: rgba(26, 54, 93, 0.2);
}

.about-offering__dot {
  display: block;
  width: 10px;
  height: 10px;
  margin-bottom: 16px;
  border-radius: 50%;
  background: var(--about-gradient);
  animation: about-dot-pulse 2.5s ease-in-out infinite;
}

.about-offering.is-visible .about-offering__dot {
  animation-play-state: running;
}

@keyframes about-dot-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.75;
  }
}

.about-offering h3 {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 700;
  color: var(--about-navy);
}

.about-offering p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.about-offering__subhead {
  margin: 16px 0 10px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--about-navy);
}

.about-offering__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.about-offering__list li {
  position: relative;
  padding-left: 16px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.about-offering__list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--about-cyan);
}

/* Closing */
.about-closing {
  display: grid;
  gap: 24px;
}

@media (min-width: 768px) {
  .about-closing {
    grid-template-columns: repeat(2, 1fr);
  }
}

.about-closing__card {
  padding: 32px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
}

.about-closing__card h2 {
  margin: 0 0 12px;
  font-size: 20px;
  font-weight: 700;
  color: var(--about-navy);
}

.about-closing__card p {
  margin: 0;
  font-size: 15px;
  line-height: 1.65;
  color: var(--text-secondary);
}

/* Tagline */
.about-tagline {
  padding: 64px 0;
  background: var(--about-gradient);
  color: #fff;
  text-align: center;
  overflow: hidden;
}

.about-tagline__inner {
  position: relative;
}

.about-tagline__text {
  margin: 0;
  font-size: clamp(22px, 4vw, 30px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.about-tagline.is-visible .about-tagline__text {
  animation: about-tagline-in 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes about-tagline-in {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .about-article {
    grid-template-columns: 1fr;
    gap: 12px;
    padding: 24px;
  }

  .about-article__index {
    font-size: 12px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .about-hero__glow {
    animation: none;
  }

  .about-hero__title,
  .about-hero__intro {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .about-hero__rule {
    width: 120px;
    transition: none;
  }

  .about-reveal {
    opacity: 1;
    transform: none;
  }

  .about-reveal.is-visible {
    animation: none;
  }

  .about-article::before {
    transform: scaleY(1);
  }

  .about-offering__dot {
    animation: none;
  }

  .about-partner.is-visible:hover {
    transform: none;
  }
}
</style>
