<script setup>
defineProps({
  ready: { type: Boolean, default: false },
  alt: { type: String, default: "Distribute funds across recipients" },
});
</script>

<template>
  <div
    class="po-hero-graphic"
    :class="{ 'po-hero-graphic--ready': ready }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="po-hero-graphic__art"
      data-po-part="distribute"
      src="/images/figma-payouts/hero/distribute-hero.svg"
      alt=""
      width="804"
      height="510"
      decoding="async"
    />
  </div>
</template>

<style scoped>
/* Cropped content frame 804×510 — no empty SVG padding */
.po-hero-graphic {
  position: relative;
  width: 100%;
  max-width: 100%;
  max-height: calc(100svh - var(--page-nav-offset, 129px) - 32px);
  aspect-ratio: 804 / 510;
  margin: 0;
  padding: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.7s ease,
    transform 0.7s ease;
}

.po-hero-graphic--ready {
  opacity: 1;
  transform: translateY(0);
}

.po-hero-graphic__art {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  /* Fill the box edge-to-edge — no letterboxing */
  object-fit: fill;
  pointer-events: none;
  user-select: none;
}
</style>
