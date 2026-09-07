<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  title: { type: String, default: "" },
  body: { type: String, default: "" },
  label: { type: String, default: "" },
  to: { type: String, default: "" },
  href: { type: String, default: "" },
  variant: { type: String, default: "about" },
  ariaLabel: { type: String, default: "Call to action" },
  backgroundSrc: { type: String, default: "/images/figma-contact/cta-banner-bg.png" },
  iconSrc: { type: String, default: "" },
  paddingTop: { type: String, default: "0" },
  paddingBottom: { type: String, default: "94px" },
});

const usesLink = computed(() => !!props.to && !props.href);
</script>

<template>
  <section
    class="marketing-banner-cta"
    :class="`marketing-banner-cta--${variant}`"
    :aria-label="ariaLabel"
    :style="{ '--cta-pad-top': paddingTop, '--cta-pad-bottom': paddingBottom }"
  >
    <div class="marketing-banner-cta__panel">
      <img
        class="marketing-banner-cta__bg"
        :src="backgroundSrc"
        alt=""
        width="1240"
        height="331"
        loading="lazy"
        decoding="async"
      />
      <div class="marketing-banner-cta__content">
        <h2 class="marketing-banner-cta__title">{{ title }}</h2>
        <p class="marketing-banner-cta__body">{{ body }}</p>

        <RouterLink v-if="usesLink" :to="to" class="marketing-banner-cta__btn">
          {{ label }}
          <img
            v-if="iconSrc"
            :src="iconSrc"
            alt=""
            width="18"
            height="18"
            decoding="async"
          />
          <span v-else aria-hidden="true">›</span>
        </RouterLink>

        <a v-else :href="href" class="marketing-banner-cta__btn">
          {{ label }}
          <img
            v-if="iconSrc"
            :src="iconSrc"
            alt=""
            width="18"
            height="18"
            decoding="async"
          />
          <span v-else aria-hidden="true">›</span>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marketing-banner-cta {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: var(--cta-pad-top, 0) 100px var(--cta-pad-bottom, 94px);
  box-sizing: border-box;
  background: #ffffff;
}

.marketing-banner-cta__panel {
  position: relative;
  width: 1240px;
  max-width: 100%;
  height: 331px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.marketing-banner-cta__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.marketing-banner-cta__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  height: 100%;
  padding: 40px 24px;
  box-sizing: border-box;
  text-align: center;
}

.marketing-banner-cta__title {
  margin: 0;
  max-width: 728px;
  font-size: 40px;
  font-weight: 500;
  line-height: 52px;
  letter-spacing: 1.6px;
  color: #ffffff;
}

.marketing-banner-cta__body {
  margin: 0;
  max-width: 728px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.marketing-banner-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 52px;
  padding: 0 16px;
  border-radius: 8px;
  background: #ffffff;
  color: #097495;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: -0.32px;
  line-height: 21.856px;
  text-decoration: none;
}

.marketing-banner-cta__btn img {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.marketing-banner-cta__btn span {
  font-size: 18px;
  line-height: 1;
}

.marketing-banner-cta__btn:hover {
  opacity: 0.92;
}

@media (max-width: 1280px) {
  .marketing-banner-cta {
    padding-left: 40px;
    padding-right: 40px;
  }
}

@media (max-width: 900px) {
  .marketing-banner-cta {
    padding-left: 24px;
    padding-right: 24px;
    padding-bottom: 48px;
  }

  .marketing-banner-cta__panel {
    height: auto;
    min-height: 280px;
  }

  .marketing-banner-cta__title {
    font-size: 28px;
    line-height: 1.3;
    letter-spacing: 0.5px;
  }
}

@media (max-width: 480px) {
  .marketing-banner-cta {
    padding-left: 16px;
    padding-right: 16px;
    padding-bottom: 36px;
  }

  .marketing-banner-cta__panel {
    min-height: 244px;
    border-radius: 14px;
  }

  .marketing-banner-cta__content {
    gap: 12px;
    padding: 24px 16px;
  }

  .marketing-banner-cta__title {
    font-size: 24px;
    line-height: 1.25;
    letter-spacing: 0.2px;
  }

  .marketing-banner-cta__body {
    font-size: 13px;
    line-height: 20px;
  }

  .marketing-banner-cta__btn {
    width: 100%;
    min-height: 48px;
    font-size: 15px;
  }
}
</style>
