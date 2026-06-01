<script setup>
import { useAboutEco } from "@/composables/useAboutEco.js";

const eco = useAboutEco();
const { lockedId } = eco;
</script>

<template>
  <p
    class="eco__panel-tip"
    :class="{ 'eco__panel-tip--ready': eco.ready }"
  >
    <template v-if="lockedId">
      Pinned — click again or tap Payments to resume
    </template>
    <template v-else>
      Hover or click a node · auto-cycles every few seconds
    </template>
  </p>
</template>

<style scoped>
.eco__panel-tip {
  margin: 0;
  width: 100%;
  max-width: 384px;
  text-align: center;
  font-size: 11px;
  color: #94a3b8;
  opacity: 0;
  transform: translateY(6px);
  transition:
    opacity 0.4s ease 0.35s,
    transform 0.4s cubic-bezier(0.22, 1, 0.36, 1) 0.35s;
}

.eco__panel-tip--ready {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .eco__panel-tip--ready {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
