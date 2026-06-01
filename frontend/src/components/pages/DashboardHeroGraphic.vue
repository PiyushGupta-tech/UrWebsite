<script setup>
import DashboardPreview from "../DashboardPreview.vue";

defineProps({
  dashboard: { type: Object, required: true },
  ready: { type: Boolean, default: false },
  themeBreathe: { type: Boolean, default: false },
  logoPlaceholder: { type: Boolean, default: false },
});
</script>

<template>
  <div
    class="dash-hero"
    :class="{ 'dash-hero--ready': ready }"
  >
    <DashboardPreview
      :dashboard="dashboard"
      :tilted="false"
      :theme-breathe="themeBreathe"
      :logo-placeholder="logoPlaceholder"
    />
  </div>
</template>

<style scoped>
.dash-hero {
  width: 100%;
  max-width: 526px;
  margin-inline: auto;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.55s ease,
    transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.dash-hero--ready {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .dash-hero,
  .dash-hero--ready {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
