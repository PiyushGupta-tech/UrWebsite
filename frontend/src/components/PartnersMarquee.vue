<script setup>
import { computed, onMounted, ref } from "vue";
import {
  getPartnerLogo,
  getPartnerLogoColor,
  PARTNER_LOGO_HEIGHT,
} from "@/constants/logos.js";

const props = defineProps({
  title: { type: String, default: "" },
  partners: { type: Array, required: true },
  variant: { type: String, default: "banks" },
  showTitle: { type: Boolean, default: true },
});

const imgFailed = ref({});
const colorImgFailed = ref({});
const scrollHovered = ref(false);

const scrollItems = computed(() => {
  const mapped = props.partners.map((name) => ({
    name,
    logo: getPartnerLogo(name, props.variant),
  }));
  return [...mapped, ...mapped];
});

function itemKey(name, index) {
  return `${name}-${index}`;
}

function markImgFailed(key) {
  imgFailed.value = { ...imgFailed.value, [key]: true };
}

function markColorImgFailed(key) {
  colorImgFailed.value = { ...colorImgFailed.value, [key]: true };
}

function showLogo(item, index) {
  const key = itemKey(item.name, index);
  return item.logo && !imgFailed.value[key];
}

function showColorLogo(item, index) {
  const key = itemKey(item.name, index);
  return showLogo(item, index) && !colorImgFailed.value[key];
}

function partnerLogoStyle(name) {
  const height = PARTNER_LOGO_HEIGHT[name];
  if (!height) return undefined;
  const style = { height: `${height}px` };
  if (name === "Jio Pay") style.width = `${height}px`;
  return style;
}

function isLargeLogo(name) {
  return Boolean(PARTNER_LOGO_HEIGHT[name]);
}

onMounted(() => {
  const seen = new Set();
  for (const item of scrollItems.value) {
    if (!item.logo || seen.has(item.logo)) continue;
    seen.add(item.logo);
    const colorSrc = getPartnerLogoColor(item.logo);
    if (colorSrc) {
      const img = new Image();
      img.src = colorSrc;
    }
  }
});
</script>

<template>
  <section class="partners section--tight" :class="`partners--${variant}`">
    <div class="container">
      <h2 v-if="showTitle && title" class="partners__title">{{ title }}</h2>
      <div class="partners__track" aria-hidden="true">
        <div
          class="partners__scroll"
          :class="{ 'partners__scroll--hovered': scrollHovered }"
          @mouseenter="scrollHovered = true"
          @mouseleave="scrollHovered = false"
        >
          <span
            v-for="(item, i) in scrollItems"
            :key="itemKey(item.name, i)"
            class="partners__pill"
            :class="{ 'partners__pill--logo-lg': isLargeLogo(item.name) }"
          >
            <span
              v-if="showLogo(item, i)"
              class="partners__logo-stack"
              :class="{ 'partners__logo-stack--lg': isLargeLogo(item.name) }"
            >
              <img
                class="partners__logo partners__logo--default"
                :class="{ 'partners__logo--lg': isLargeLogo(item.name) }"
                :style="partnerLogoStyle(item.name)"
                :src="item.logo"
                :alt="item.name"
                width="160"
                height="32"
                loading="lazy"
                decoding="async"
                @error="markImgFailed(itemKey(item.name, i))"
              />
              <img
                v-if="showColorLogo(item, i)"
                class="partners__logo partners__logo--color"
                :class="{ 'partners__logo--lg': isLargeLogo(item.name) }"
                :style="partnerLogoStyle(item.name)"
                :src="getPartnerLogoColor(item.logo)"
                alt=""
                aria-hidden="true"
                width="160"
                height="32"
                loading="lazy"
                decoding="async"
                @error="markColorImgFailed(itemKey(item.name, i))"
              />
            </span>
            <span v-else class="partners__label">{{ item.name }}</span>
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.partners {
  overflow: hidden;
  border-block: 1px solid var(--border);
}

.partners--banks {
  background: var(--bg-surface);
}

.partners--merchants {
  background: var(--bg-page);
}

.partners__title {
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin: 0 0 24px;
}

.partners__track {
  mask-image: linear-gradient(
    90deg,
    transparent,
    #000 12%,
    #000 88%,
    transparent
  );
}

.partners__scroll {
  display: flex;
  gap: 12px;
  width: max-content;
  animation: marquee 40s linear infinite;
}

.partners__pill {
  flex-shrink: 0;
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 183px;
  padding: 12px 20px;
  height: 47px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text-secondary);
  background: var(--bg-page);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
}

.partners--banks .partners__pill {
  background: var(--bg-page);
}

.partners__logo-stack {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  max-width: 100%;
}

.partners__logo {
  display: block;
  height: 23px;
  width: auto;
  max-width: 100%;
  object-fit: contain;
  transition: opacity 0.28s ease;
}

.partners__logo--color {
  position: absolute;
  inset: 0;
  margin: auto;
  opacity: 0;
  pointer-events: none;
}

.partners__scroll--hovered .partners__logo--default {
  opacity: 0;
}

.partners__scroll--hovered .partners__logo--color {
  opacity: 1;
}

.partners--merchants .partners__pill {
  padding-block: 6px;
}

.partners--merchants .partners__logo-stack {
  width: 100%;
}

.partners--merchants .partners__logo {
  height: 35px;
  max-width: 143px;
}

.partners__pill--logo-lg {
  padding-block: 0;
}

.partners__logo--lg {
  max-width: none;
  object-fit: contain;
}

.partners__label {
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}

@keyframes marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .partners__logo {
    transition: none;
  }
}

@media (max-width: 480px) {
  .partners__title {
    margin-bottom: 16px;
    font-size: 13px;
  }

  .partners__scroll {
    gap: 8px;
  }

  .partners__pill {
    width: 132px;
    height: 40px;
    padding: 8px 12px;
  }

  .partners__logo {
    height: 18px;
  }

  .partners--merchants .partners__logo {
    height: 28px;
    max-width: 118px;
  }
}
</style>
