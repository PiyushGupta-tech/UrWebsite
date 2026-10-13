<script setup>
import { onBeforeUnmount, onMounted } from "vue";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

const TITLE = "Thank you | Urbanrupee";
const DEFAULT_TITLE = "Urbanrupee | Payment Orchestration & Infrastructure India";
const DEFAULT_ROBOTS = "index, follow, max-image-preview:large, max-snippet:-1";

function setRobots(content) {
  let meta = document.querySelector('meta[name="robots"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.setAttribute("name", "robots");
    document.head.appendChild(meta);
  }
  meta.setAttribute("content", content);
}

onMounted(() => {
  document.title = TITLE;
  setRobots("noindex, follow");
});

onBeforeUnmount(() => {
  if (document.title === TITLE) document.title = DEFAULT_TITLE;
  setRobots(DEFAULT_ROBOTS);
});
</script>

<template>
  <main class="thanks" aria-labelledby="thanks-title">
    <div class="thanks__bg" aria-hidden="true">
      <img src="/images/herobg.svg" alt="" width="1440" height="600" decoding="async" />
    </div>
    <div class="thanks__inner">
      <p class="thanks__mark" aria-hidden="true">✓</p>
      <h1 id="thanks-title" class="thanks__title">Thank you</h1>
      <p class="thanks__body">
        We have received your message and will get back to you shortly.
      </p>
      <div class="thanks__actions">
        <RouterLink to="/" class="thanks__btn thanks__btn--primary">Back to home</RouterLink>
        <RouterLink to="/products" class="thanks__btn thanks__btn--ghost">Explore products</RouterLink>
      </div>
    </div>
  </main>
</template>

<style scoped>
.thanks {
  --ty-nav-offset: 129px;
  position: relative;
  margin-top: calc(-1 * var(--ty-nav-offset));
  padding-top: var(--ty-nav-offset);
  overflow: hidden;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
  background: #ffffff;
}

.thanks__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.thanks__bg img {
  position: absolute;
  top: 0;
  left: 50%;
  width: 100%;
  min-width: 1440px;
  height: auto;
  transform: translateX(-50%);
  -webkit-mask-image: linear-gradient(to bottom, #000 55%, transparent);
  mask-image: linear-gradient(to bottom, #000 55%, transparent);
}

.thanks__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  max-width: 560px;
  margin: 0 auto;
  padding: 120px var(--ur-gutter, 24px) 160px;
  box-sizing: content-box;
  text-align: center;
}

.thanks__mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin: 0;
  border-radius: 50%;
  background: #097495;
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
}

.thanks__title {
  margin: 0;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -1.26px;
}

.thanks__body {
  margin: 0;
  max-width: 420px;
  font-size: 16px;
  line-height: 24px;
  color: #535861;
}

.thanks__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.thanks__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 155px;
  height: 52px;
  padding: 0 20px;
  box-sizing: border-box;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
}

.thanks__btn--primary {
  background: #097495;
  color: #ffffff;
}

.thanks__btn--ghost {
  border: 1px solid #d5d7da;
  background: #ffffff;
  color: #252b37;
}

.thanks__btn:focus-visible {
  outline: 2px solid #097495;
  outline-offset: 2px;
}

@media (max-width: 1280px) {
  .thanks {
    --ty-nav-offset: 113px;
  }
}

@media (max-width: 1200px) {
  .thanks {
    --ty-nav-offset: 82px;
  }
}

@media (max-width: 700px) {
  .thanks {
    --ty-nav-offset: 88px;
  }
}

@media (max-width: 767px) {
  .thanks__inner {
    padding: 72px 16px 120px;
  }

  .thanks__title {
    font-size: 28px;
    line-height: 36px;
    letter-spacing: -0.84px;
  }

  .thanks__body {
    font-size: 14px;
    line-height: 20px;
  }

  .thanks__actions {
    flex-direction: column;
    align-self: stretch;
  }

  .thanks__btn {
    width: 100%;
    height: 48px;
  }
}
</style>
