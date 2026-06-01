<script setup>
import CheckoutCard from "../CheckoutCard.vue";

defineProps({
  checkout: { type: Object, required: true },
  ready: { type: Boolean, default: false },
});

defineEmits(["method-change"]);
</script>

<template>
  <div
    class="checkout-hero"
    :class="{ 'checkout-hero--ready': ready }"
  >
    <CheckoutCard
      :checkout="checkout"
      :auto-rotate="true"
      @method-change="$emit('method-change', $event)"
    />
  </div>
</template>

<style scoped>
.checkout-hero {
  width: 100%;
  max-width: 400px;
  margin-inline: auto;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.55s ease,
    transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.checkout-hero--ready {
  opacity: 1;
  transform: translateY(0);
}

.checkout-hero :deep(.checkout) {
  width: 100%;
}

@media (prefers-reduced-motion: reduce) {
  .checkout-hero,
  .checkout-hero--ready {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
