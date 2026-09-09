<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const props = defineProps({
  title: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  variant: { type: String, default: "about" },
  ariaLabel: { type: String, default: "Customer testimonials" },
  autoplayMs: { type: Number, default: 5000 },
});

function middleIndex(realIndex, total = props.items.length) {
  return total + realIndex;
}

function initialTestimonialIndex() {
  const total = props.items.length;
  if (total < 2) return 0;
  return middleIndex(Math.min(1, total - 1), total);
}

const activeTestimonial = ref(initialTestimonialIndex());
const skipTransition = ref(false);
let testimonialTimer = null;

const loopedTestimonials = computed(() => {
  if (props.items.length < 2) return props.items;
  return [...props.items, ...props.items, ...props.items];
});

const realTestimonialIndex = computed(() => {
  const total = props.items.length;
  if (total < 1) return 0;
  return ((activeTestimonial.value % total) + total) % total;
});

const testimonialTrackStyle = computed(() => ({
  "--active": String(activeTestimonial.value),
}));

function snapTo(index) {
  skipTransition.value = true;
  activeTestimonial.value = index;
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      skipTransition.value = false;
    });
  });
}

function normalizeTestimonialIndex() {
  const total = props.items.length;
  if (total < 2) return;
  const upper = total * 2;
  if (activeTestimonial.value >= upper) {
    snapTo(activeTestimonial.value - total);
  } else if (activeTestimonial.value < total) {
    snapTo(activeTestimonial.value + total);
  }
}

function advanceTestimonial() {
  if (props.items.length < 2) return;
  activeTestimonial.value += 1;
}

function onTestimonialTrackTransitionEnd(event) {
  if (event.propertyName !== "transform") return;
  normalizeTestimonialIndex();
}

function startTestimonialAutoplay() {
  stopTestimonialAutoplay();
  if (props.items.length < 2) return;
  testimonialTimer = window.setInterval(advanceTestimonial, props.autoplayMs);
}

function stopTestimonialAutoplay() {
  if (testimonialTimer != null) {
    window.clearInterval(testimonialTimer);
    testimonialTimer = null;
  }
}

function setTestimonial(realIndex) {
  const total = props.items.length;
  if (total < 1) return;

  const current = realTestimonialIndex.value;
  const inMiddle = activeTestimonial.value >= total && activeTestimonial.value < total * 2;

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
    skipTransition.value = true;
    activeTestimonial.value = middleIndex(current);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        skipTransition.value = false;
        moveForward();
      });
    });
    return;
  }

  moveForward();
}

function testimonialClass(loopIndex) {
  if (loopIndex === activeTestimonial.value) return "marketing-testimonials__card--active";
  return "marketing-testimonials__card--inactive";
}

onMounted(startTestimonialAutoplay);
onUnmounted(stopTestimonialAutoplay);
</script>

<template>
  <section
    class="marketing-testimonials"
    :class="`marketing-testimonials--${variant}`"
    :aria-label="ariaLabel"
  >
    <h2 v-if="title" class="marketing-testimonials__title">{{ title }}</h2>

    <div class="marketing-testimonials__track-wrap">
      <div
        class="marketing-testimonials__track"
        :class="{ 'marketing-testimonials__track--snap': skipTransition }"
        :style="testimonialTrackStyle"
        @transitionend="onTestimonialTrackTransitionEnd"
      >
        <article
          v-for="(item, index) in loopedTestimonials"
          :key="`${item.company || item.name || index}-${index}`"
          class="marketing-testimonials__card"
          :class="testimonialClass(index)"
          @click="setTestimonial(index % items.length)"
        >
          <blockquote class="marketing-testimonials__quote">{{ item.quote }}</blockquote>
          <footer class="marketing-testimonials__author">
            <template v-if="item.company">
              <p class="marketing-testimonials__meta">
                <strong>{{ item.company }}</strong>
              </p>
            </template>
            <template v-else>
              <img
                v-if="item.avatar"
                class="marketing-testimonials__avatar"
                :src="item.avatar"
                alt=""
                width="44"
                height="44"
                loading="lazy"
                decoding="async"
              />
              <p class="marketing-testimonials__meta">
                <strong>{{ item.name }}</strong><span v-if="item.role">, {{ item.role }}</span>
              </p>
            </template>
          </footer>
        </article>
      </div>
    </div>

    <div
      v-if="items.length > 1"
      class="marketing-testimonials__dots"
      role="tablist"
      aria-label="Testimonial slides"
    >
      <button
        v-for="(_, index) in items"
        :key="index"
        type="button"
        class="marketing-testimonials__dot"
        :class="{ 'marketing-testimonials__dot--active': realTestimonialIndex === index }"
        :aria-selected="realTestimonialIndex === index"
        :aria-label="`Show testimonial ${index + 1}`"
        @click="setTestimonial(index)"
      />
    </div>
  </section>
</template>

<style scoped>
.marketing-testimonials {
  overflow: hidden;
}

.marketing-testimonials--about {
  margin: 0;
  padding: 80px 0 120px;
  text-align: center;
}

.marketing-testimonials--home {
  padding: 80px 0 100px;
}

.marketing-testimonials__title {
  text-align: center;
  color: #252b37;
}

.marketing-testimonials--about .marketing-testimonials__title {
  max-width: 1240px;
  margin: 0 auto 56px;
  padding: 0 24px;
  font-size: 40px;
  font-weight: 600;
  line-height: 56px;
  letter-spacing: -1.2px;
}

.marketing-testimonials--home .marketing-testimonials__title {
  margin: 0 auto 24px;
  max-width: 788px;
  padding: 0 24px;
  font-size: 40px;
  font-weight: 700;
  line-height: 48px;
}

.marketing-testimonials__track-wrap {
  overflow: hidden;
  width: 100%;
}

.marketing-testimonials__track {
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

.marketing-testimonials__track--snap {
  transition: none;
}

.marketing-testimonials__card {
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

.marketing-testimonials__card--active {
  opacity: 1;
  transform: translateY(0);
  cursor: default;
}

.marketing-testimonials__card--inactive {
  opacity: 0.4;
}

.marketing-testimonials__quote {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: -0.48px;
  color: #020617;
}

.marketing-testimonials__author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.marketing-testimonials__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.marketing-testimonials__meta {
  margin: 0;
  font-size: 18px;
  line-height: 26px;
  letter-spacing: -0.54px;
  color: #020617;
}

.marketing-testimonials__meta span {
  color: #64748b;
}

.marketing-testimonials__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 36px;
}

.marketing-testimonials__dot {
  width: 12px;
  height: 12px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #cbd5e1;
  cursor: pointer;
}

.marketing-testimonials__dot--active {
  background: #097495;
}

@media (max-width: 900px) {
  .marketing-testimonials--about,
  .marketing-testimonials--home {
    padding-top: 48px;
    padding-bottom: 72px;
  }

  .marketing-testimonials--about .marketing-testimonials__title,
  .marketing-testimonials--home .marketing-testimonials__title {
    padding: 0 clamp(16px, 4vw, 24px);
    font-size: var(--ur-heading-sm, 28px) !important;
    line-height: 1.2 !important;
  }

  .marketing-testimonials__track {
    --card-w: min(612px, calc(100vw - 48px));
    --gap: 16px;
  }

  .marketing-testimonials__card {
    gap: 18px;
    min-height: 220px;
    padding: 24px 20px;
  }

  .marketing-testimonials__quote {
    font-size: 15px;
    line-height: 22px;
  }

  .marketing-testimonials__author {
    gap: 12px;
  }

  .marketing-testimonials__meta {
    font-size: 16px;
    line-height: 22px;
  }
}

@media (max-width: 480px) {
  .marketing-testimonials__track {
    --card-w: calc(100vw - 32px);
  }
}
</style>
