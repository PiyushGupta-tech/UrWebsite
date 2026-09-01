<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { RouterLink } from "vue-router";
import PartnersMarquee from "@/components/PartnersMarquee.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const pillarIcons = {
  handshake: "/images/figma-about/icon-handshake.svg",
  performance: "/images/figma-about/icon-performance.svg",
  link: "/images/figma-about/icon-link.svg",
  growth: "/images/figma-about/icon-growth.svg",
};

const openPrinciple = ref(0);
const openFaq = ref(0);

const leftPillars = computed(() => (props.page.pillars || []).slice(0, 2));
const rightPillars = computed(() => (props.page.pillars || []).slice(2, 4));
const testimonials = computed(() => props.page.testimonials || []);

function middleIndex(realIndex, total = testimonials.value.length) {
  return total + realIndex;
}

function initialTestimonialIndex() {
  const total = (props.page.testimonials || []).length;
  if (total < 2) return 0;
  return middleIndex(Math.min(1, total - 1), total);
}

/**
 * Index into loopedTestimonials (3 copies). Live slides stay in the middle copy
 * so the first/last real cards always have neighbors on both sides.
 */
const activeTestimonial = ref(initialTestimonialIndex());
const skipTestimonialTransition = ref(false);
let testimonialTimer = null;

/** Three copies: [A][B][C]. We keep the active index in [B], then snap after wrapping into [C]. */
const loopedTestimonials = computed(() => {
  const items = testimonials.value;
  if (items.length < 2) return items;
  return [...items, ...items, ...items];
});

const realTestimonialIndex = computed(() => {
  const total = testimonials.value.length;
  if (total < 1) return 0;
  return ((activeTestimonial.value % total) + total) % total;
});

const testimonialTrackStyle = computed(() => ({
  "--active": String(activeTestimonial.value),
}));

function togglePrinciple(index) {
  openPrinciple.value = openPrinciple.value === index ? -1 : index;
}

function toggleFaq(index) {
  openFaq.value = openFaq.value === index ? -1 : index;
}

function snapTo(index) {
  skipTestimonialTransition.value = true;
  activeTestimonial.value = index;
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      skipTestimonialTransition.value = false;
    });
  });
}

/** After sliding into the third (or first) copy, jump back to the matching middle-copy card. */
function normalizeTestimonialIndex() {
  const total = testimonials.value.length;
  if (total < 2) return;
  const upper = total * 2;
  if (activeTestimonial.value >= upper) {
    snapTo(activeTestimonial.value - total);
  } else if (activeTestimonial.value < total) {
    snapTo(activeTestimonial.value + total);
  }
}

function advanceTestimonial() {
  const total = testimonials.value.length;
  if (total < 2) return;
  activeTestimonial.value += 1;
}

function onTestimonialTrackTransitionEnd(event) {
  if (event.propertyName !== "transform") return;
  normalizeTestimonialIndex();
}

function startTestimonialAutoplay() {
  stopTestimonialAutoplay();
  if (testimonials.value.length < 2) return;
  testimonialTimer = window.setInterval(advanceTestimonial, 5000);
}

function stopTestimonialAutoplay() {
  if (testimonialTimer != null) {
    window.clearInterval(testimonialTimer);
    testimonialTimer = null;
  }
}

/** Dot / card selection: always move forward through the loop. */
function setTestimonial(realIndex) {
  const total = testimonials.value.length;
  if (total < 1) return;

  const current = realTestimonialIndex.value;
  const inMiddle =
    activeTestimonial.value >= total && activeTestimonial.value < total * 2;

  if (realIndex === current && inMiddle) {
    startTestimonialAutoplay();
    return;
  }

  const moveForward = () => {
    if (realIndex > current) {
      activeTestimonial.value = middleIndex(realIndex);
    } else {
      // Slide forward into the third copy (e.g. last → first).
      activeTestimonial.value = total * 2 + realIndex;
    }
    startTestimonialAutoplay();
  };

  if (!inMiddle) {
    skipTestimonialTransition.value = true;
    activeTestimonial.value = middleIndex(current);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        skipTestimonialTransition.value = false;
        moveForward();
      });
    });
    return;
  }

  moveForward();
}

function testimonialClass(loopIndex) {
  if (loopIndex === activeTestimonial.value) return "about-testimonials__card--active";
  return "about-testimonials__card--inactive";
}

onMounted(startTestimonialAutoplay);
onUnmounted(stopTestimonialAutoplay);
</script>

<template>
  <main class="about-page">
    <section class="about-hero">
      <div class="about-hero__bg" aria-hidden="true">
        <img
          src="/images/figma-contact/hero-bg@2x.png"
          alt=""
          width="1440"
          height="628"
          decoding="async"
        />
      </div>

      <div class="about-hero__copy">
        <h1 class="about-hero__title">{{ page.title }}</h1>
        <p class="about-hero__intro">{{ page.intro }}</p>
        <RouterLink to="/contact" class="about-hero__cta">
          Talk to Expert
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

    <section class="about-testimonials" aria-label="Customer testimonials">
      <h2 class="about-testimonials__title">{{ page.testimonials_title }}</h2>

      <div class="about-testimonials__track-wrap">
        <div
          class="about-testimonials__track"
          :class="{ 'about-testimonials__track--snap': skipTestimonialTransition }"
          :style="testimonialTrackStyle"
          @transitionend="onTestimonialTrackTransitionEnd"
        >
          <article
            v-for="(item, index) in loopedTestimonials"
            :key="`${item.name}-${index}`"
            class="about-testimonials__card"
            :class="testimonialClass(index)"
            @click="setTestimonial(index % testimonials.length)"
          >
            <blockquote class="about-testimonials__quote">{{ item.quote }}</blockquote>
            <footer class="about-testimonials__author">
              <img
                class="about-testimonials__avatar"
                :src="item.avatar"
                alt=""
                width="44"
                height="44"
                loading="lazy"
                decoding="async"
              />
              <p class="about-testimonials__meta">
                <strong>{{ item.name }}</strong>, <span>{{ item.role }}</span>
              </p>
            </footer>
          </article>
        </div>
      </div>

      <div class="about-testimonials__dots" role="tablist" aria-label="Testimonial slides">
        <button
          v-for="(_, index) in testimonials"
          :key="index"
          type="button"
          class="about-testimonials__dot"
          :class="{ 'about-testimonials__dot--active': realTestimonialIndex === index }"
          :aria-selected="realTestimonialIndex === index"
          :aria-label="`Show testimonial ${index + 1}`"
          @click="setTestimonial(index)"
        />
      </div>
    </section>

    <section class="about-audiences" aria-label="Industries we serve">
      <div class="about-audiences__panel">
        <h2 class="about-audiences__title">{{ page.audiences_title }}</h2>
        <div class="about-audiences__grid">
          <article
            v-for="item in page.audiences || []"
            :key="item.number"
            class="about-audiences__card"
          >
            <span class="about-audiences__num" aria-hidden="true">{{ item.number }}</span>
            <div class="about-audiences__copy">
              <h3>{{ item.title }}</h3>
              <p>{{ item.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="about-faq" aria-label="Frequently asked questions">
      <div class="about-faq__inner">
        <div class="about-faq__intro">
          <h2 class="about-faq__title">{{ page.faq_title }}</h2>
          <p class="about-faq__body">{{ page.faq_intro }}</p>
        </div>

        <div class="about-faq__list">
          <div
            v-for="(item, index) in page.faq_items || []"
            :key="item.number"
            class="about-faq__item"
            :class="{ 'about-faq__item--open': openFaq === index }"
          >
            <button
              type="button"
              class="about-faq__trigger"
              :aria-expanded="openFaq === index"
              @click="toggleFaq(index)"
            >
              <span class="about-faq__num">{{ item.number }}</span>
              <span class="about-faq__question">{{ item.question }}</span>
              <span class="about-faq__icon" aria-hidden="true">{{ openFaq === index ? "−" : "+" }}</span>
            </button>
            <div v-show="openFaq === index" class="about-faq__answer">
              <p>{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="about-cta" aria-label="Call to action">
      <div class="about-cta__panel">
        <img
          class="about-cta__bg"
          src="/images/figma-contact/cta-banner-bg.png"
          alt=""
          width="1240"
          height="331"
          loading="lazy"
          decoding="async"
        />
        <div class="about-cta__content">
          <h2 class="about-cta__title">{{ page.cta_title }}</h2>
          <p class="about-cta__body">{{ page.cta_body }}</p>
          <RouterLink to="/contact" class="about-cta__btn">
            {{ page.cta_label }}
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
}

.about-hero {
  position: relative;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 200px 100px 48px;
  box-sizing: border-box;
  overflow: hidden;
}

.about-hero__bg {
  position: absolute;
  inset: 0 auto auto 50%;
  transform: translateX(-50%);
  width: 1440px;
  height: 560px;
  pointer-events: none;
  z-index: 0;
}

.about-hero__bg img {
  display: block;
  width: 1440px;
  height: 560px;
  object-fit: cover;
  object-position: center top;
}

.about-hero__copy {
  position: relative;
  z-index: 1;
  width: 611px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.about-hero__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.26px;
}

.about-hero__intro {
  margin: 0;
  font-size: 14px;
  line-height: normal;
  letter-spacing: 0.56px;
  color: #64748b;
}

.about-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 52px;
  padding: 15px 16px;
  border-radius: 8px;
  background: var(--about-teal);
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
}

.about-hero__cta:hover {
  background: #086681;
}

.about-hero__cta img {
  display: block;
  width: 18px;
  height: 18px;
  filter: brightness(0) invert(1);
}

.about-trust {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 80px 100px;
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
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
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
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
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
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
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
  gap: 16px;
}

.about-testimonials__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.about-testimonials__meta {
  margin: 0;
  font-size: 18px;
  line-height: 26px;
  letter-spacing: -0.54px;
  color: #020617;
}

.about-testimonials__meta span {
  color: #64748b;
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
  .about-principles__head,
  .about-principles__body {
    grid-template-columns: 1fr;
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
  .about-purpose__grid {
    grid-template-columns: 1fr;
    max-width: 420px;
    margin: 0 auto;
  }

  .about-purpose__photo {
    order: -1;
  }
}

@media (max-width: 768px) {
  .about-hero {
    min-height: auto;
    padding: 160px 24px 32px;
  }

  .about-hero__title {
    font-size: 32px;
    line-height: 1.2;
  }

  .about-trust {
    padding: 0 24px 64px;
  }

  .about-purpose__title,
  .about-principles__title,
  .about-testimonials__title,
  .about-audiences__title,
  .about-faq__title,
  .about-cta__title {
    font-size: 32px;
    line-height: 1.2;
  }

  .about-testimonials__track {
    --card-w: min(612px, calc(100vw - 48px));
  }

  .about-audiences__grid {
    display: flex;
    overflow-x: auto;
    gap: 17px;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 8px;
  }

  .about-audiences__card {
    flex: 0 0 min(280px, 78vw);
    scroll-snap-align: start;
  }

  .about-faq,
  .about-cta {
    padding-inline: 24px;
  }

  .about-cta__panel {
    height: auto;
    min-height: 331px;
  }
}
</style>
