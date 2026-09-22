<script setup>
defineProps({
  ready: { type: Boolean, default: false },
  alt: { type: String, default: "Urbanrupee withdrawals platform diagram" },
});

/** Discrete parts for later animation — Figma 385:7109 */
const PARTS = [
  {
    id: "customers",
    src: "/images/figma-payouts/platform/customers.png",
    label: "Your customers",
  },
  {
    id: "center",
    src: "/images/figma-payouts/platform/center.png",
    label: "Withdrawals platform",
  },
  {
    id: "beneficiaries",
    src: "/images/figma-payouts/platform/beneficiaries.png",
    label: "Your beneficiaries",
  },
  {
    id: "methods",
    src: "/images/figma-payouts/platform/methods.png",
    label: "Payment methods",
  },
];
</script>

<template>
  <div
    class="po-platform"
    :class="{ 'po-platform--ready': ready }"
    role="img"
    :aria-label="alt"
  >
    <!-- Full composite for exact Figma layout; parts kept for animation hooks -->
    <img
      class="po-platform__full"
      data-po-part="diagram"
      src="/images/figma-payouts/platform/diagram-graphic.png"
      alt=""
      width="1291"
      height="813"
      decoding="async"
    />
    <div class="po-platform__parts" aria-hidden="true">
      <img
        v-for="part in PARTS"
        :key="part.id"
        class="po-platform__part"
        :class="`po-platform__part--${part.id}`"
        :data-po-part="part.id"
        :src="part.src"
        :alt="part.label"
        decoding="async"
      />
    </div>
  </div>
</template>

<style scoped>
.po-platform {
  /* Figma diagram group 385:7673 — 1291×813 (heading excluded) */
  --po-platform-w: 1291;
  --po-platform-h: 813;
  /* Fill the band under the navbar with 10px pad top + bottom */
  --po-platform-max-h: calc(100svh - var(--page-nav-offset, 129px) - 20px);
  position: relative;
  width: min(
    1291px,
    100%,
    calc(var(--po-platform-max-h) * var(--po-platform-w) / var(--po-platform-h))
  );
  margin-inline: auto;
  flex-shrink: 1;
  min-width: 0;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.8s ease,
    transform 0.8s ease;
}

.po-platform--ready {
  opacity: 1;
  transform: translateY(0);
}

.po-platform__full {
  display: block;
  width: 100%;
  height: auto;
  pointer-events: none;
  user-select: none;
}

/* Hidden composition layers — available for future part-based motion */
.po-platform__parts {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
}

.po-platform__part {
  position: absolute;
  display: block;
  max-width: none;
}
</style>
