<script setup>
import { computed, ref } from "vue";
import { useProductsScrollPin } from "@/composables/useProductsScrollPin";

const props = defineProps({
  section: { type: Object, required: true },
});

const items = computed(() => props.section.items || []);
const itemCount = computed(() => items.value.length);
const pinRef = ref(null);

const { activeIndex, slideStyle, reducedMotion } = useProductsScrollPin(
  pinRef,
  itemCount,
);

function mediaStyle(index) {
  return slideStyle(index, itemCount.value || 3);
}

function staticImage(item) {
  if (item?.image?.includes("2147225785")) {
    return "/images/figma-home/Frame%202147225785-content.svg";
  }
  return item.image;
}

function staticFigureClass(item) {
  return {
    "home-products__figure--white-label-mobile": item?.image?.includes("2147225785"),
  };
}
</script>

<template>
  <section class="home-products" aria-label="Payment products">
    <div class="home-products__intro">
      <h2>{{ section.title }}</h2>
      <p>{{ section.body }}</p>
    </div>

    <!-- Desktop: pinned media left + scrolling copy right -->
    <div
      v-if="!reducedMotion"
      ref="pinRef"
      class="home-products__pin"
      :style="{ '--step-count': itemCount }"
    >
      <div class="home-products__media-rail" aria-hidden="true">
        <div class="home-products__media-stage">
          <div
            v-for="(item, index) in items"
            :key="`${item.title}-media`"
            class="home-products__media-slide"
            :class="{ 'is-active': activeIndex === index }"
            :style="mediaStyle(index)"
          >
            <img
              :src="item.image"
              alt=""
              class="home-products__figure"
              width="661"
              height="526"
              :loading="index === 0 ? 'eager' : 'lazy'"
              decoding="async"
            />
            <span
              v-for="bubble in item.bubbles || []"
              :key="bubble.label"
              class="home-products__bubble"
              :style="{ left: `${bubble.x}%`, top: `${bubble.y}%` }"
            >
              {{ bubble.label }}
            </span>
          </div>
        </div>
      </div>

      <div class="home-products__copy-rail">
        <article
          v-for="(item, index) in items"
          :key="item.title"
          class="home-products__copy-step"
          :class="{ 'is-active': activeIndex === index }"
          :aria-current="activeIndex === index ? 'true' : undefined"
        >
          <div class="home-products__copy-inner">
            <span v-if="item.eyebrow" class="home-products__eyebrow">
              {{ item.eyebrow }}
            </span>
            <h3>{{ item.title }}</h3>
            <p class="home-products__lead">{{ item.body }}</p>
          </div>
        </article>
      </div>
    </div>

    <!-- Mobile / reduced motion: static stacked rows -->
    <div class="home-products__static">
      <article
        v-for="item in items"
        :key="`${item.title}-static`"
        class="home-products__static-row"
      >
        <div class="home-products__stage home-products__stage--static">
          <img
            :src="staticImage(item)"
            :alt="item.title"
            class="home-products__figure"
            :class="staticFigureClass(item)"
            width="661"
            height="526"
            loading="lazy"
            decoding="async"
          />
          <span
            v-for="bubble in item.bubbles || []"
            :key="bubble.label"
            class="home-products__bubble"
            :style="{ left: `${bubble.x}%`, top: `${bubble.y}%` }"
          >
            {{ bubble.label }}
          </span>
        </div>
        <div class="home-products__copy">
          <span v-if="item.eyebrow" class="home-products__eyebrow">
            {{ item.eyebrow }}
          </span>
          <h3>{{ item.title }}</h3>
          <p class="home-products__lead">{{ item.body }}</p>
          <ul v-if="item.points?.length">
            <li v-for="point in item.points" :key="point.title">
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

/* Pinned media left, scrolling copy right */
.home-products__pin {
  width: 100%;
  max-width: 1248px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: start;
  gap: 0 24px;
}

.home-products__copy-rail {
  display: flex;
  flex-direction: column;
}

.home-products__copy-step {
  /* Taller than one viewport so each product holds longer before the next slide */
  min-height: calc((100vh - var(--products-sticky-top)) * 1.6);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 48px 8px 48px 16px;
  box-sizing: border-box;
}

.home-products__copy-inner {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
  max-width: 90%;
}

.home-products__eyebrow {
  display: block;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 17px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: linear-gradient(90deg, #097495 0%, #18d4f5 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.home-products__copy-step h3,
.home-products__copy h3 {
  margin: 0;
  font-size: clamp(36px, 4vw, 48px);
  font-weight: 600;
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: #080808;
}

.home-products__copy-step .home-products__lead,
.home-products__copy .home-products__lead {
  margin: 0;
  max-width: 90%;
  font-size: 20px;
  font-weight: 400;
  line-height: 30px;
  letter-spacing: 0;
  color: #39393d;
}

.home-products__media-rail {
  position: sticky;
  top: var(--products-sticky-top);
  height: calc(100vh - var(--products-sticky-top));
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 16px;
  box-sizing: border-box;
}

.home-products__media-stage {
  position: relative;
  width: 100%;
  max-width: 661px;
  aspect-ratio: 661 / 526;
  height: auto;
  max-height: min(75vh, 640px);
  margin-inline: auto;
  border-radius: 22px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.home-products__media-slide {
  position: absolute;
  inset: 0;
  display: block;
  box-sizing: border-box;
  will-change: transform, opacity;
  transition:
    transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
    opacity 220ms ease-out;
  pointer-events: none;
}

.home-products__figure {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0;
}

/* Figma 89:2110 / 89:2108 — rgba(9,116,149,0.2) glass pills */
.home-products__bubble {
  position: absolute;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 25px;
  border-radius: 29px;
  background: rgba(9, 116, 149, 0.2);
  color: #ffffff;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  font-size: clamp(12px, 1.4vw, 16px);
  font-weight: 600;
  line-height: 20px;
  letter-spacing: -0.48px;
  text-align: center;
  white-space: nowrap;
  pointer-events: none;
  box-sizing: border-box;
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
  gap: 28px;
}

.home-products__stage--static {
  position: relative;
  width: 100%;
  max-width: 661px;
  margin: 0 auto;
  aspect-ratio: 661 / 526;
  border-radius: 22px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  box-sizing: border-box;
}

.home-products__stage--static .home-products__figure {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.home-products__copy {
  width: 100%;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.home-products__copy ul {
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 20px;
}

.home-products__copy li {
  display: grid;
  gap: 6px;
}

.home-products__copy strong {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px;
  color: #252b37;
}

.home-products__copy span {
  font-size: 14px;
  line-height: 22px;
  color: #535862;
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
    font-size: 32px;
  }

  .home-products__copy .home-products__lead {
    font-size: 18px;
    line-height: 28px;
  }
}

@media (max-width: 480px) {
  .home-products {
    padding: 0 16px 80px;
    gap: 40px;
  }

  .home-products__intro {
    gap: 14px;
  }

  .home-products__intro h2 {
    font-size: 28px;
    line-height: 1.2;
  }

  .home-products__intro p {
    font-size: 14px;
    line-height: 22px;
  }

  .home-products__static {
    gap: 40px;
  }

  .home-products__static-row {
    gap: 20px;
  }

  .home-products__stage--static {
    max-width: 100%;
    aspect-ratio: auto;
    min-height: 0;
    padding: 12px;
    border-radius: 16px;
  }

  .home-products__stage--static .home-products__figure {
    height: auto;
    object-fit: contain;
  }

  .home-products__stage--static .home-products__figure--white-label-mobile {
    width: 82%;
    margin: 0 auto;
  }

  .home-products__copy {
    gap: 14px;
  }

  .home-products__copy h3 {
    font-size: 28px;
    line-height: 1.15;
  }

  .home-products__copy .home-products__lead {
    max-width: 100%;
    font-size: 16px;
    line-height: 24px;
  }

  .home-products__bubble {
    max-width: calc(100% - 20px);
    padding: 8px 14px;
    font-size: 11px;
    line-height: 16px;
    white-space: normal;
  }

  .home-products__cta {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .home-products__pin {
    display: none;
  }

  .home-products__static {
    display: flex;
  }
}
</style>
