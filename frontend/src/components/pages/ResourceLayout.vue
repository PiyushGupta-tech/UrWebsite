<script setup>
defineProps({
  title: { type: String, required: true },
  intro: { type: String, default: "" },
});
</script>

<template>
  <main class="resource-page">
    <div class="resource-page__bg" aria-hidden="true">
      <img src="/images/herobg.svg" alt="" width="1440" height="600" decoding="async" />
    </div>

    <header class="resource-hero">
      <h1 class="resource-hero__title">{{ title }}</h1>
      <p v-if="intro" class="resource-hero__intro">{{ intro }}</p>
    </header>

    <div class="resource-page__body">
      <slot />
    </div>
  </main>
</template>

<style scoped>
/* Shared look for FAQ, Blog, Privacy Policy and Terms (matches Contact / About). */
.resource-page {
  --rs-ink: #252b37;
  --rs-muted: #535862;
  --rs-subtle: #8b919a;
  --rs-teal: #097495;
  --rs-teal-tint: rgba(9, 116, 149, 0.08);
  --rs-line: #eceef2;
  --rs-radius: 16px;
  --rs-shadow: 0 12px 40px rgba(37, 43, 55, 0.08);
  --rs-font: "Manrope", "DM Sans", system-ui, sans-serif;
  position: relative;
  font-family: var(--rs-font);
  color: var(--rs-ink);
  /* Run the hero background up under the floating nav, like Contact. */
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
}

.resource-page__bg {
  position: absolute;
  inset: 0 0 auto;
  height: 640px;
  overflow: hidden;
  pointer-events: none;
  -webkit-mask-image: linear-gradient(to bottom, #000 55%, transparent);
  mask-image: linear-gradient(to bottom, #000 55%, transparent);
}

.resource-page__bg img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.resource-hero {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: calc(var(--page-nav-offset, 129px) + 60px) var(--ur-gutter) 0;
  text-align: center;
}

.resource-hero__title {
  margin: 0;
  max-width: 760px;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.03em;
  color: var(--rs-ink);
}

.resource-hero__intro {
  margin: 0;
  max-width: 680px;
  font-size: var(--ur-lead, 16px);
  line-height: 1.65;
  color: var(--rs-muted);
}

.resource-page__body {
  position: relative;
  z-index: 1;
  width: min(100% - 2 * var(--ur-gutter), 1240px);
  margin: 56px auto 0;
}

@media (max-width: 700px) {
  .resource-hero {
    padding-top: calc(var(--page-nav-offset, 88px) + 36px);
  }

  .resource-page__body {
    margin-top: 36px;
  }
}
</style>
