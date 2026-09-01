<script setup>
import { computed, ref } from "vue";
import { useProductsScrollPin } from "@/composables/useProductsScrollPin";

const props = defineProps({
  section: { type: Object, required: true },
});

const items = computed(() => props.section.items || []);

const pinRef = ref(null);
const { activeIndex, reducedMotion, slideStyle, copyStyle } = useProductsScrollPin(
  pinRef,
  computed(() => items.value.length),
);

function visualClass(image = "") {
  if (image.includes("5785")) return "home-products__visual--5785";
  if (image.includes("5787")) return "home-products__visual--5787";
  if (image.includes("1171275326")) return "home-products__visual--orchestration";
  return "";
}

function slideImage(image = "") {
  if (image.includes("5785")) {
    return "/images/figma-home/Frame%202147225785-content.svg";
  }
  if (image.includes("5787")) {
    return "/images/figma-home/Frame%202147225787-content.svg";
  }
  if (image.includes("1171275326")) {
    return "/images/figma-home/Group%201171275326-content.svg";
  }
  return image;
}
</script>

<template>
  <section class="home-products" aria-label="Payment products">
    <div class="home-products__intro">
      <h2>{{ section.title }}</h2>
      <p>{{ section.body }}</p>
    </div>

    <!-- Desktop: Juspay-style pin — visuals left (sticky), copy right (scroll steps) -->
    <div ref="pinRef" class="home-products__pin">
      <div class="home-products__pin-visual" aria-hidden="false">
        <div class="home-products__pin-stage">
          <div class="home-products__card" aria-hidden="true">
            <img
              src="/images/figma-home/products-card-bg.svg"
              alt=""
              width="661"
              height="526"
              decoding="async"
            />
          </div>
          <div class="home-products__viewport">
            <div class="home-products__slides">
              <div
                v-for="(item, index) in items"
                :key="item.title"
                class="home-products__slide"
                :class="{ 'home-products__slide--active': activeIndex === index }"
                :style="slideStyle(index, items.length)"
              >
                <div
                  class="home-products__visual home-products__visual--pin"
                  :class="visualClass(item.image)"
                >
                  <img
                    :src="slideImage(item.image)"
                    :alt="item.title"
                    width="661"
                    height="526"
                    :loading="index === 0 ? 'eager' : 'lazy'"
                    decoding="async"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="home-products__pin-copy">
        <article
          v-for="(item, index) in items"
          :key="item.title"
          class="home-products__copy-step"
          :class="{ 'home-products__copy-step--active': activeIndex === index }"
          :style="copyStyle(index, items.length)"
          :aria-current="activeIndex === index ? 'step' : undefined"
        >
          <div class="home-products__copy">
            <h3>{{ item.title }}</h3>
            <p class="home-products__lead">{{ item.body }}</p>
            <ul>
              <li v-for="point in item.points || []" :key="point.title">
                <strong>{{ point.title }}</strong>
                <span>{{ point.body }}</span>
              </li>
            </ul>
          </div>
        </article>
      </div>
    </div>

    <!-- Mobile / reduced motion: static stacked rows -->
    <div
      class="home-products__static"
      :class="{ 'home-products__static--visible': reducedMotion }"
    >
      <article
        v-for="item in items"
        :key="`${item.title}-static`"
        class="home-products__static-row"
      >
        <div class="home-products__visual" :class="visualClass(item.image)">
          <img
            :src="item.image"
            :alt="item.title"
            width="661"
            height="526"
            loading="lazy"
            decoding="async"
          />
        </div>
        <div class="home-products__copy">
          <h3>{{ item.title }}</h3>
          <p class="home-products__lead">{{ item.body }}</p>
          <ul>
            <li v-for="point in item.points || []" :key="point.title">
              <strong>{{ point.title }}</strong>
              <span>{{ point.body }}</span>
            </li>
          </ul>
        </div>
      </article>
    </div>

    <RouterLink to="/contact" class="home-products__cta">
      <span>{{ section.cta }}</span>
      <img
        src="/images/figma-contact/nav-arrow.svg"
        alt=""
        width="18"
        height="18"
        decoding="async"
      />
    </RouterLink>
  </section>
</template>

<style scoped>
.home-products {
  --products-card-width: 661px;
  --products-card-height: 526px;
  --products-sticky-top: 120px;
  max-width: 1296px;
  margin: 0 auto;
  padding: 0 24px 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-products__intro {
  max-width: 698px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.home-products__intro h2 {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.home-products__intro p {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* Pin section: copy steps set scroll height; visual stays sticky */
.home-products__pin {
  width: 100%;
  max-width: 1248px;
  display: grid;
  grid-template-columns: minmax(0, var(--products-card-width)) minmax(0, 1fr);
  gap: 72px;
  align-items: start;
}

.home-products__pin-visual {
  position: sticky;
  top: var(--products-sticky-top);
  height: calc(100vh - var(--products-sticky-top) - 40px);
  min-height: var(--products-card-height);
  display: flex;
  align-items: center;
  justify-content: center;
}

.home-products__pin-stage {
  position: relative;
  width: var(--products-card-width);
  height: var(--products-card-height);
  flex-shrink: 0;
}

.home-products__card {
  position: absolute;
  inset: 0;
  border-radius: 22.109px;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.home-products__viewport {
  position: absolute;
  inset: 0;
  border-radius: 22.109px;
  overflow: hidden;
  z-index: 1;
  isolation: isolate;
}

.home-products__card img {
  display: block;
  width: 100%;
  height: 100%;
}

.home-products__slides {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.home-products__slide {
  position: absolute;
  inset: 0;
  will-change: transform;
  transition: none;
}

.home-products__visual {
  width: var(--products-card-width);
  height: var(--products-card-height);
  position: relative;
  overflow: visible;
}

.home-products__visual--pin {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.home-products__visual img {
  position: absolute;
  display: block;
  max-width: none;
}

.home-products__visual--5785 img {
  width: calc(689 / 661.415 * 100%);
  height: 100%;
  left: calc(-14 / 661.415 * 100%);
  top: 0;
}

.home-products__visual--5787 img {
  width: calc(733 / 661.415 * 100%);
  height: calc(549 / 526 * 100%);
  left: calc(-26 / 661.415 * 100%);
  top: calc(-23 / 526 * 100%);
}

.home-products__visual--orchestration img {
  width: calc(702 / 661 * 100%);
  height: calc(558 / 529 * 100%);
  left: calc(-21.001 / 661 * 100%);
  top: calc(-19 / 529 * 100%);
}

.home-products__pin-copy {
  display: flex;
  flex-direction: column;
}

.home-products__copy-step {
  min-height: calc(100vh - var(--products-sticky-top));
  display: flex;
  align-items: center;
  padding: 24px 0;
  will-change: opacity, transform;
}

.home-products__copy {
  width: 100%;
  max-width: 515px;
}

.home-products__copy h3 {
  margin: 0 0 12px;
  font-size: 28px;
  font-weight: 700;
  line-height: 32px;
  color: #252b37;
}

.home-products__lead {
  margin: 0 0 48px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: #535862;
}

.home-products__copy ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 24px;
}

.home-products__copy li {
  display: grid;
  gap: 8px;
}

.home-products__copy strong {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px;
  color: #252b37;
}

.home-products__copy span {
  font-size: 14px;
  line-height: 24px;
  letter-spacing: 0.28px;
  color: #535862;
}

.home-products__static {
  display: none;
  width: 100%;
  max-width: 1248px;
  flex-direction: column;
  gap: 68px;
}

.home-products__static-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
}

.home-products__cta {
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
  text-decoration: none;
  box-sizing: border-box;
}

.home-products__cta:hover {
  filter: brightness(1.05);
}

@media (max-width: 1100px) {
  .home-products__pin {
    display: none;
  }

  .home-products__static {
    display: flex;
  }
}

@media (max-width: 768px) {
  .home-products__intro h2 {
    font-size: 32px;
    line-height: 42px;
  }

  .home-products__copy h3 {
    font-size: 24px;
  }

  .home-products__lead {
    margin-bottom: 32px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .home-products__pin {
    display: none;
  }

  .home-products__static,
  .home-products__static--visible {
    display: flex;
  }
}
</style>
