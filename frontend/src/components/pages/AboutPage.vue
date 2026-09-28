<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import PartnersMarquee from "@/components/PartnersMarquee.vue";
import AboutHeroGraphic from "@/components/pages/AboutHeroGraphic.vue";
import AboutEcoPanel from "@/components/pages/AboutEcoPanel.vue";
import { provideAboutEco } from "@/composables/useAboutEco.js";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
const heroParagraphs = computed(() => props.page.hero_paragraphs || [props.page.intro]);

const pillarIcons = {
  handshake: "/images/figma-about/icon-handshake.svg",
  performance: "/images/figma-about/icon-performance.svg",
  link: "/images/figma-about/icon-link.svg",
  growth: "/images/figma-about/icon-growth.svg",
};

const openPrinciple = ref(0);
const openFaq = ref(0);
const aboutEcoReady = ref(false);
provideAboutEco(aboutEcoReady);

const leftPillars = computed(() => (props.page.pillars || []).slice(0, 2));
const rightPillars = computed(() => (props.page.pillars || []).slice(2, 4));

function togglePrinciple(index) {
  openPrinciple.value = openPrinciple.value === index ? -1 : index;
}

onMounted(() => {
  aboutEcoReady.value = true;
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
          <h1 class="about-hero__title">{{ page.title }}</h1>
          <div class="about-hero__intros">
            <p
              v-for="(paragraph, index) in heroParagraphs"
              :key="index"
              class="about-hero__intro"
            >
              {{ paragraph }}
            </p>
          </div>
          <RouterLink to="/contact" class="about-hero__cta">
            <span>{{ page.cta_label || "Talk to an Expert" }}</span>
            <img
              src="/images/figma-contact/nav-arrow.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
        </div>

        <div class="about-hero__visual" aria-label="Payments ecosystem overview">
          <AboutHeroGraphic class="about-hero__graphic" />
          <AboutEcoPanel class="about-hero__panel" />
        </div>
      </div>
    </section>

    <section class="about-trust">
      <PartnersMarquee
        title="Trusted by Leading Businesses"
        :partners="page.merchant_partners || []"
        variant="merchants"
      />
    </section>

    <section class="about-purpose">
      <div class="about-purpose__head">
        <h2 class="about-purpose__title">{{ page.purpose_title }}</h2>
        <p class="about-purpose__intro">{{ page.purpose_intro }}</p>
      </div>

      <div class="about-purpose__grid">
        <div class="about-purpose__col">
          <article
            v-for="item in leftPillars"
            :key="item.title"
            class="about-purpose__card"
          >
            <span class="about-purpose__icon-wrap" aria-hidden="true">
              <img
                :src="pillarIcons[item.icon]"
                alt=""
                width="24"
                height="24"
                decoding="async"
              />
            </span>
            <h3 class="about-purpose__card-title">{{ item.title }}</h3>
            <p class="about-purpose__card-body">{{ item.body }}</p>
          </article>
        </div>

        <figure class="about-purpose__photo">
          <img
            src="/images/figma-about/team-photo@2x.png"
            alt="Urbanrupee team collaborating in the office"
            width="347"
            height="424"
            loading="lazy"
            decoding="async"
          />
        </figure>

        <div class="about-purpose__col">
          <article
            v-for="item in rightPillars"
            :key="item.title"
            class="about-purpose__card"
          >
            <span class="about-purpose__icon-wrap" aria-hidden="true">
              <img
                :src="pillarIcons[item.icon]"
                alt=""
                width="24"
                height="24"
                decoding="async"
              />
            </span>
            <h3 class="about-purpose__card-title">{{ item.title }}</h3>
            <p class="about-purpose__card-body">{{ item.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="about-leaders" aria-label="Leadership team">
      <div class="about-leaders__head">
        <h2 class="about-leaders__title">{{ page.leaders_title }}</h2>
        <p class="about-leaders__intro">{{ page.leaders_intro }}</p>
      </div>

      <div class="about-leaders__grid">
        <article
          v-for="leader in page.leaders || []"
          :key="leader.name"
          class="about-leaders__card"
        >
          <div class="about-leaders__photo-wrap">
            <img
              class="about-leaders__photo"
              :src="leader.image"
              :alt="leader.name"
              width="204"
              height="240"
              loading="lazy"
              decoding="async"
            />
          </div>
          <div class="about-leaders__copy">
            <h3 class="about-leaders__name">{{ leader.name }}</h3>
            <p class="about-leaders__role">{{ leader.role }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="about-principles" aria-label="Core principles">
      <div class="about-principles__head">
        <h2 class="about-principles__title">{{ page.principles_title }}</h2>
        <p class="about-principles__intro">{{ page.principles_intro }}</p>
      </div>

      <div class="about-principles__body">
        <div class="about-principles__list">
          <div
            v-for="(item, index) in page.principles || []"
            :key="item.number"
            class="about-principles__item"
            :class="{ 'about-principles__item--open': openPrinciple === index }"
          >
            <button
              type="button"
              class="about-principles__trigger"
              :aria-expanded="openPrinciple === index"
              @click="togglePrinciple(index)"
            >
              <span class="about-principles__num">[{{ item.number }}]</span>
              <span class="about-principles__label">{{ item.title }}</span>
              <span class="about-principles__icon" aria-hidden="true">
                {{ openPrinciple === index ? "−" : "+" }}
              </span>
            </button>
            <div v-show="openPrinciple === index" class="about-principles__answer">
              <p>{{ item.body }}</p>
            </div>
          </div>
        </div>

        <figure class="about-principles__photo">
          <img
            src="/images/figma-about/principles-photo@2x.png"
            alt="Urbanrupee team at work"
            width="508"
            height="422"
            loading="lazy"
            decoding="async"
          />
        </figure>
      </div>
    </section>

  </main>
</template>

<style scoped>
.about-page {
  --about-ink: #252b37;
  --about-muted: #535862;
  --about-teal: #097495;
  --about-font: "Manrope", "DM Sans", system-ui, sans-serif;
  font-family: var(--about-font);
  background: #ffffff;
  color: var(--about-ink);
  margin-top: -129px;
  overflow-x: clip;
  max-width: 100%;
}

.about-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  overflow: hidden;
}

.about-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
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
  min-width: 100%;
  height: 100%;
  min-height: 100%;
  transform: translateX(-50%);
  object-fit: cover;
  object-position: center top;
}

.about-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: var(--ur-page-max, 1440px);
  margin: 0 auto;
  min-height: 100vh;
  padding: 148px var(--ur-gutter) 40px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 611px) minmax(340px, 1fr);
  align-items: stretch;
  gap: clamp(32px, 4vw, 56px);
}

.about-hero__copy {
  position: relative;
  z-index: 1;
  width: 611px;
  max-width: 100%;
  margin: 0;
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  min-height: 100%;
  gap: 24px;
}

.about-hero__title {
  margin: 0;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -1.26px;
}

.about-hero__intros {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.about-hero__intro {
  margin: 0;
  font-size: 14px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  font-weight: 400;
  line-height: 22px;
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
  background: #097495;
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

.about-hero__visual {
  position: relative;
  z-index: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding-top: 30px;
}

.about-hero__graphic {
  width: min(100%, 360px);
  margin-bottom: 28px;
}

.about-hero__panel {
  width: min(100%, 420px);
}

.about-trust {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 80px 100px;
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
  font-weight: 700;
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

.about-purpose {
  max-width: 1081px;
  margin: 0 auto;
  padding: 0 24px 120px;
}

.about-purpose__head {
  max-width: 671px;
  margin: 0 auto 56px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.about-purpose__title {
  margin: 0;
  font-size: var(--ur-heading-md, 40px);
  font-weight: 700;
  line-height: 1.4;
}

.about-purpose__intro {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-purpose__grid {
  display: grid;
  grid-template-columns: 315px 347px 315px;
  gap: 52px;
  align-items: center;
  justify-content: center;
}

.about-purpose__col {
  display: flex;
  flex-direction: column;
  gap: 39px;
}

.about-purpose__card {
  background: #ffffff;
  border-radius: 14.141px;
  padding: 20px;
  /* Figma 722:7669 — default soft shadow */
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.25s ease;
}

.about-purpose__card:hover {
  /* Figma 722:7640 — elevated 4-layer hover shadow */
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

.about-purpose__icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  margin-bottom: 16px;
  border-radius: 6.642px;
  background: rgba(9, 116, 149, 0.1);
}

.about-purpose__icon-wrap img {
  width: 24px;
  height: 24px;
}

.about-purpose__card-title {
  margin: 0 0 7px;
  font-size: 16px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.48px;
}

.about-purpose__card-body {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: var(--about-muted);
}

.about-purpose__photo {
  margin: 0;
}

.about-purpose__photo img {
  display: block;
  width: 347px;
  height: 424px;
  border-radius: 16px;
  object-fit: cover;
}

.about-leaders {
  max-width: 1081px;
  margin: 0 auto;
  padding: 0 24px 120px;
}

.about-leaders__head {
  width: 363px;
  max-width: 100%;
  margin: 0 auto 56px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.about-leaders__title {
  margin: 0;
  width: 100%;
  font-size: var(--ur-heading-md, 40px);
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: -1.2px;
  color: var(--about-ink);
}

.about-leaders__intro {
  margin: 0;
  width: 100%;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-leaders__grid {
  display: flex;
  justify-content: center;
  gap: 62px;
  flex-wrap: wrap;
}

.about-leaders__card {
  width: 204px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 31px;
  text-align: center;
}

.about-leaders__photo-wrap {
  width: 204px;
  height: 240px;
  overflow: hidden;
  border-radius: 3000px;
  background: #d4d4d8;
}

.about-leaders__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-leaders__copy {
  width: 203px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
}

.about-leaders__name {
  margin: 0;
  width: 100%;
  font-size: 20px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.6px;
  color: var(--about-ink);
}

.about-leaders__role {
  margin: 0;
  width: 100%;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: var(--about-muted);
}

.about-principles {
  max-width: 1198px;
  margin: 0 auto;
  padding: 0 24px 120px;
}

.about-principles__head {
  display: grid;
  grid-template-columns: 608px 508px;
  gap: 82px;
  align-items: center;
  margin-bottom: 56px;
}

.about-principles__title {
  margin: 0;
  font-size: var(--ur-heading-md, 40px);
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: -1.2px;
}

.about-principles__intro {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-principles__body {
  display: grid;
  grid-template-columns: 627px 508px;
  gap: 63px;
  align-items: start;
}

.about-principles__item {
  border-bottom: 2px solid #f0f9f3;
}

.about-principles__trigger {
  display: grid;
  grid-template-columns: auto 1fr 30px;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 24px 0;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  color: var(--about-ink);
}

.about-principles__num,
.about-principles__label {
  font-size: 24px;
  font-weight: 700;
  line-height: 28px;
}

.about-principles__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 24px;
  background: var(--about-teal);
  color: #ffffff;
  font-size: 18px;
  line-height: 1;
}

.about-principles__item--open .about-principles__icon {
  background: transparent;
  color: var(--about-ink);
  font-size: 24px;
}

.about-principles__answer {
  padding: 0 46px 24px 0;
}

.about-principles__answer p {
  margin: 0;
  max-width: 584px;
  font-size: 16px;
  line-height: 22px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-principles__photo {
  margin: 0;
}

.about-principles__photo img {
  display: block;
  width: 508px;
  height: 422px;
  border-radius: 16px;
  object-fit: cover;
}

.about-testimonials {
  max-width: none;
  margin: 0;
  padding: 0 0 120px;
  text-align: center;
  overflow: hidden;
}

.about-testimonials__title {
  max-width: 1240px;
  margin: 0 auto 56px;
  padding: 0 24px;
  font-size: 40px;
  font-weight: 600;
  line-height: 56px;
  letter-spacing: -1.2px;
}

.about-testimonials__track-wrap {
  overflow: hidden;
  width: 100%;
}

.about-testimonials__track {
  --card-w: 612px;
  --gap: 24px;
  --active: 0;
  display: flex;
  gap: var(--gap);
  align-items: flex-start;
  width: max-content;
  min-height: 276px;
  position: relative;
  left: 50%;
  transform: translateX(
    calc(-1 * (var(--active) * (var(--card-w) + var(--gap)) + var(--card-w) / 2))
  );
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

.about-testimonials__track--snap {
  transition: none;
}

.about-testimonials__card {
  flex: 0 0 var(--card-w);
  width: var(--card-w);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 24px;
  min-height: 252px;
  padding: 32px;
  border-radius: 16px;
  background: #f8fafc;
  opacity: 0.4;
  transform: translateY(24px);
  transition:
    opacity 0.35s ease,
    transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
  cursor: pointer;
}

.about-testimonials__card--active {
  opacity: 1;
  transform: translateY(0);
  cursor: default;
}

.about-testimonials__card--inactive {
  opacity: 0.4;
}

.about-testimonials__quote {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: -0.48px;
  color: #020617;
}

.about-testimonials__author {
  display: flex;
  align-items: center;
  justify-content: center;
}

.about-testimonials__meta {
  margin: 0;
  font-size: 18px;
  line-height: 26px;
  letter-spacing: -0.54px;
  color: #020617;
}

.about-testimonials__meta strong {
  font-weight: 700;
}

.about-testimonials__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 36px;
}

.about-testimonials__dot {
  width: 12px;
  height: 12px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #cbd5e1;
  cursor: pointer;
}

.about-testimonials__dot--active {
  background: var(--about-teal);
}

.about-audiences {
  max-width: 1328px;
  margin: 0 auto;
  padding: 0 24px 180px;
}

.about-audiences__panel {
  padding: 70px 44px;
  border-radius: 24px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.about-audiences__title {
  margin: 0 auto 56px;
  max-width: 517px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.2px;
  color: #ffffff;
}

.about-audiences__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 17px;
}

.about-audiences__card {
  min-height: 212px;
  padding: 16px 20px;
  border-radius: 18px;
  border: 1px solid rgba(200, 200, 200, 0.19);
  background: rgba(255, 255, 255, 0.06);
  transform: translateY(0) scale(1);
  transition:
    transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
    background 0.25s ease,
    border-color 0.25s ease,
    box-shadow 0.25s ease;
  cursor: default;
}

.about-audiences__card:hover {
  transform: translateY(-8px) scale(1.03);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
}

@media (prefers-reduced-motion: reduce) {
  .about-purpose__card,
  .about-audiences__card {
    transition: none;
  }

  .about-audiences__card:hover {
    transform: none;
  }
}

.about-audiences__num {
  display: block;
  margin-bottom: 20px;
  font-size: 68px;
  font-weight: 700;
  line-height: 72px;
  letter-spacing: -2.059px;
  background: linear-gradient(180deg, #636363 0%, #ffffff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.about-audiences__copy h3 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  letter-spacing: -0.66px;
  color: #ffffff;
}

.about-audiences__copy p {
  margin: 0;
  font-size: 14px;
  line-height: 19px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.about-faq {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 180px;
  box-sizing: border-box;
}

.about-faq__inner {
  display: grid;
  grid-template-columns: 501px 627px;
  gap: 94px;
  width: 1240px;
  max-width: 100%;
  margin: 0 auto;
  align-items: start;
}

.about-faq__intro {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 118px;
}

.about-faq__title {
  margin: 0;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
}

.about-faq__body {
  margin: 0;
  max-width: 510px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--about-muted);
}

.about-faq__item {
  border-bottom: 1px solid #f0f9f3;
}

.about-faq__trigger {
  display: grid;
  grid-template-columns: 36px 1fr 24px;
  align-items: center;
  gap: 16px;
  width: 100%;
  min-height: 76px;
  padding: 24px;
  box-sizing: border-box;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
}

.about-faq__num,
.about-faq__question {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
}

.about-faq__icon {
  font-size: 22px;
  line-height: 1;
  text-align: center;
}

.about-faq__answer {
  padding: 0 24px 24px 76px;
}

.about-faq__answer p {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: var(--about-muted);
}

.about-cta {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 94px;
  box-sizing: border-box;
}

.about-cta__panel {
  position: relative;
  width: 1240px;
  max-width: 100%;
  height: 331px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.about-cta__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-cta__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  height: 100%;
  padding: 52px 24px;
  text-align: center;
}

.about-cta__title {
  margin: 0;
  max-width: 728px;
  font-size: 40px;
  font-weight: 500;
  line-height: 52px;
  letter-spacing: 1.6px;
  color: #ffffff;
}

.about-cta__body {
  margin: 0;
  max-width: 728px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.about-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: #ffffff;
  color: var(--about-teal);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
}

.about-cta__btn img {
  width: 18px;
  height: 18px;
}

@media (max-width: 1200px) {
  .about-hero__inner {
    min-height: auto;
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .about-hero__copy {
    width: 100%;
    max-width: 640px;
    margin: 0 auto;
    text-align: center;
    align-items: center;
  }

  .about-hero__visual {
    padding-top: 0;
  }

  .about-principles__head,
  .about-principles__body {
    grid-template-columns: 1fr;
  }

  .about-principles__head {
    text-align: center;
    justify-items: center;
  }

  .about-principles__photo {
    order: -1;
  }

  .about-principles__photo img,
  .about-purpose__photo img {
    width: 100%;
    height: auto;
  }

  .about-audiences__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .about-faq__inner {
    grid-template-columns: 1fr;
  }

  .about-faq__intro {
    padding-top: 0;
  }
}

@media (max-width: 1100px) {
  .about-page {
    margin-top: -82px;
  }

  .about-purpose__grid {
    grid-template-columns: 1fr;
    max-width: 420px;
    margin: 0 auto;
  }

  .about-purpose__photo {
    order: -1;
  }

  .about-leaders__grid {
    gap: 32px;
  }
}


@media (max-width: 1200px) {
  .about-page {
    margin-top: -82px;
  }

  .about-hero__inner {
    padding: 120px var(--ur-gutter) 40px;
    gap: 40px;
  }

  .about-hero__copy {
    gap: 24px;
    max-width: min(var(--ur-stack-max), 100%);
    margin-inline: auto;
    text-align: center;
    align-items: center;
  }

  .about-hero__title {
    font-size: var(--ur-heading-stack, 28px);
    line-height: 1.25;
    letter-spacing: -1.08px;
  }

  .about-purpose__title,
  .about-leaders__title,
  .about-principles__title,
  .about-testimonials__title,
  .about-audiences__title,
  .about-faq__title,
  .about-cta__title {
    font-size: var(--ur-heading-stack, 28px);
    line-height: 1.2;
  }

  .about-hero__intros {
    gap: 0;
  }

  .about-hero__intro {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0;
  }

  .about-hero__cta {
    height: 40px;
    min-width: 142px;
    margin-top: 16px;
    margin-bottom: 8px;
    padding: 10px 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }

  .about-hero__visual {
    width: 100%;
    max-width: 354px;
    margin: 0 auto;
    gap: 24px;
    overflow: visible;
  }

  .about-hero__graphic {
    width: min(100%, 320px);
    margin-bottom: 36px;
  }

  .about-hero__panel {
    width: min(100%, 338px);
  }

  .about-trust {
    padding: 0 16px 48px;
  }

  .about-purpose,
  .about-leaders,
  .about-principles {
    padding-left: 16px;
    padding-right: 16px;
    padding-bottom: 72px;
  }

  .about-purpose__head,
  .about-leaders__head,
  .about-principles__head {
    margin-bottom: 28px;
    gap: 12px;
  }

  .about-purpose__grid,
  .about-principles__body {
    gap: 20px;
  }

  .about-purpose__col {
    gap: 20px;
  }

  .about-purpose__card {
    padding: 16px;
  }

  .about-principles__trigger {
    grid-template-columns: auto 1fr 24px;
    gap: 12px;
    padding: 18px 0;
  }

  .about-principles__num,
  .about-principles__label {
    font-size: 18px;
    line-height: 24px;
  }

  .about-principles__icon {
    width: 24px;
    height: 24px;
    font-size: 16px;
  }

  .about-principles__answer {
    padding: 0 0 18px;
  }

  .about-leaders__card,
  .about-leaders__photo-wrap {
    width: min(204px, 56vw);
  }

  .about-leaders__photo-wrap {
    height: auto;
    aspect-ratio: 204 / 240;
  }

  .about-leaders__copy {
    width: 100%;
  }

  .about-leaders__grid {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .about-page {
    margin-top: -88px;
  }

  .about-hero__copy {
    max-width: 354px;
  }
}
</style>
