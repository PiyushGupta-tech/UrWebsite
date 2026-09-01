<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const props = defineProps({
  section: { type: Object, required: true },
});

const openFaq = ref(0);
const testimonials = computed(() => props.section.testimonials || []);

function middleIndex(realIndex, total = testimonials.value.length) {
  return total + realIndex;
}

function initialTestimonialIndex() {
  const total = (props.section.testimonials || []).length;
  if (total < 2) return 0;
  return middleIndex(Math.min(1, total - 1), total);
}

const activeTestimonial = ref(initialTestimonialIndex());
const skipTestimonialTransition = ref(false);
let testimonialTimer = null;

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
  if (loopIndex === activeTestimonial.value) return "home-close__tcard--active";
  return "home-close__tcard--inactive";
}

onMounted(startTestimonialAutoplay);
onUnmounted(stopTestimonialAutoplay);
</script>

<template>
  <div class="home-close">
    <section class="home-close__testimonials" aria-label="Customer testimonials">
      <h2 class="home-close__ttitle">{{ section.testimonials_title }}</h2>

      <div class="home-close__track-wrap">
        <div
          class="home-close__track"
          :class="{ 'home-close__track--snap': skipTestimonialTransition }"
          :style="testimonialTrackStyle"
          @transitionend="onTestimonialTrackTransitionEnd"
        >
          <article
            v-for="(item, index) in loopedTestimonials"
            :key="`${item.name}-${index}`"
            class="home-close__tcard"
            :class="testimonialClass(index)"
            @click="setTestimonial(index % testimonials.length)"
          >
            <blockquote class="home-close__quote">{{ item.quote }}</blockquote>
            <footer class="home-close__author">
              <img
                class="home-close__avatar"
                :src="item.avatar"
                alt=""
                width="44"
                height="44"
                loading="lazy"
                decoding="async"
              />
              <p class="home-close__meta">
                <strong>{{ item.name }}</strong>, <span>{{ item.role }}</span>
              </p>
            </footer>
          </article>
        </div>
      </div>

      <div class="home-close__dots" role="tablist" aria-label="Testimonial slides">
        <button
          v-for="(_, index) in testimonials"
          :key="index"
          type="button"
          class="home-close__dot"
          :class="{ 'home-close__dot--active': realTestimonialIndex === index }"
          :aria-selected="realTestimonialIndex === index"
          :aria-label="`Show testimonial ${index + 1}`"
          @click="setTestimonial(index)"
        />
      </div>
    </section>

    <section class="home-close__audiences" aria-label="Industries we serve">
      <div class="home-close__audiences-panel">
        <h2>{{ section.audiences_title }}</h2>
        <div class="home-close__audiences-grid">
          <article
            v-for="item in section.audiences || []"
            :key="item.number"
            class="home-close__audience"
          >
            <span aria-hidden="true">{{ item.number }}</span>
            <div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="home-close__faq" aria-label="Frequently asked questions">
      <div class="home-close__faq-inner">
        <div class="home-close__faq-intro">
          <h2>{{ section.faq_title }}</h2>
          <p>{{ section.faq_intro }}</p>
        </div>

        <div class="home-close__faq-list">
          <div
            v-for="(item, index) in section.faq_items || []"
            :key="item.number"
            class="home-close__faq-item"
          >
            <button
              type="button"
              class="home-close__faq-trigger"
              :aria-expanded="openFaq === index"
              @click="toggleFaq(index)"
            >
              <span class="home-close__faq-num">{{ item.number }}</span>
              <span class="home-close__faq-q">{{ item.question }}</span>
              <span class="home-close__faq-icon" aria-hidden="true">
                {{ openFaq === index ? "−" : "+" }}
              </span>
            </button>
            <div v-show="openFaq === index" class="home-close__faq-answer">
              <p>{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="home-close__cta" aria-label="Call to action">
      <div class="home-close__cta-panel">
        <img
          class="home-close__cta-bg"
          src="/images/figma-contact/cta-banner-bg.png"
          alt=""
          width="1240"
          height="331"
          loading="lazy"
          decoding="async"
        />
        <div class="home-close__cta-content">
          <h2>{{ section.cta_title }}</h2>
          <p>{{ section.cta_body }}</p>
          <RouterLink to="/contact" class="home-close__cta-btn">
            {{ section.cta_label }}
            <img
              src="/images/figma-contact/nav-arrow-teal.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-close {
  --ink: #252b37;
  --muted: #535862;
  --teal: #097495;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: var(--ink);
}

.home-close__testimonials {
  padding: 0 0 100px;
  overflow: hidden;
}

.home-close__ttitle {
  margin: 0 auto 64px;
  max-width: 788px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 48px;
  color: var(--ink);
}

.home-close__track-wrap {
  overflow: hidden;
  width: 100%;
}

.home-close__track {
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

.home-close__track--snap {
  transition: none;
}

.home-close__tcard {
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

.home-close__tcard--active {
  opacity: 1;
  transform: translateY(0);
  cursor: default;
}

.home-close__tcard--inactive {
  opacity: 0.4;
}

.home-close__quote {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: -0.48px;
  color: #020617;
}

.home-close__author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.home-close__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.home-close__meta {
  margin: 0;
  font-size: 18px;
  line-height: 26px;
  letter-spacing: -0.54px;
  color: #020617;
}

.home-close__meta span {
  color: #64748b;
}

.home-close__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 36px;
}

.home-close__dot {
  width: 12px;
  height: 12px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #cbd5e1;
  cursor: pointer;
}

.home-close__dot--active {
  background: var(--teal);
}

.home-close__audiences {
  max-width: 1328px;
  margin: 0 auto;
  padding: 0 24px 100px;
}

.home-close__audiences-panel {
  padding: 70px 44px;
  border-radius: 24px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.home-close__audiences-panel h2 {
  margin: 0 auto 56px;
  max-width: 517px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.2px;
  color: #ffffff;
}

.home-close__audiences-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 17px;
}

.home-close__audience {
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
}

.home-close__audience:hover {
  transform: translateY(-8px) scale(1.03);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
}

.home-close__audience > span {
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

.home-close__audience h3 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  letter-spacing: -0.66px;
  color: #ffffff;
}

.home-close__audience p {
  margin: 0;
  font-size: 14px;
  line-height: 19px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.home-close__faq {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 100px;
  box-sizing: border-box;
}

.home-close__faq-inner {
  display: grid;
  grid-template-columns: 501px 627px;
  gap: 94px;
  width: 1240px;
  max-width: 100%;
  margin: 0 auto;
  align-items: start;
}

.home-close__faq-intro {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 118px;
}

.home-close__faq-intro h2 {
  margin: 0;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
}

.home-close__faq-intro p {
  margin: 0;
  max-width: 510px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--muted);
}

.home-close__faq-item {
  border-bottom: 1px solid #f0f9f3;
}

.home-close__faq-trigger {
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

.home-close__faq-num,
.home-close__faq-q {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
  color: var(--ink);
}

.home-close__faq-icon {
  font-size: 22px;
  line-height: 1;
  text-align: center;
  color: var(--ink);
}

.home-close__faq-answer {
  padding: 0 24px 24px 76px;
}

.home-close__faq-answer p {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: var(--muted);
}

.home-close__cta {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 94px;
  box-sizing: border-box;
}

.home-close__cta-panel {
  position: relative;
  width: 1240px;
  max-width: 100%;
  height: 331px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.home-close__cta-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.home-close__cta-content {
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

.home-close__cta-content h2 {
  margin: 0;
  max-width: 728px;
  font-size: 40px;
  font-weight: 500;
  line-height: 52px;
  letter-spacing: 1.6px;
  color: #ffffff;
}

.home-close__cta-content p {
  margin: 0;
  max-width: 728px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.home-close__cta-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: #ffffff;
  color: var(--teal);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
}

.home-close__cta-btn img {
  width: 18px;
  height: 18px;
}

@media (prefers-reduced-motion: reduce) {
  .home-close__audience {
    transition: none;
  }

  .home-close__audience:hover {
    transform: none;
  }
}

@media (max-width: 1200px) {
  .home-close__audiences-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .home-close__faq-inner {
    grid-template-columns: 1fr;
  }

  .home-close__faq-intro {
    padding-top: 0;
  }

  .home-close__faq,
  .home-close__cta {
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (max-width: 768px) {
  .home-close__ttitle,
  .home-close__audiences-panel h2,
  .home-close__faq-intro h2,
  .home-close__cta-content h2 {
    font-size: 32px;
    line-height: 1.2;
  }

  .home-close__audiences-grid {
    grid-template-columns: 1fr;
  }

  .home-close__track {
    --card-w: min(612px, calc(100vw - 48px));
  }

  .home-close__cta-panel {
    height: auto;
    min-height: 280px;
  }
}
</style>
