<script setup>
import CheckoutCard from "./CheckoutCard.vue";

defineProps({
  valueProp: { type: Object, required: true },
  checkout: { type: Object, required: true },
});
</script>

<template>
  <section class="value section">
    <div class="container value__grid">
      <div>
        <h2 class="section-title">{{ valueProp.headline }}</h2>
        <p class="section-lead">{{ valueProp.subheadline }}</p>
        <ul class="value__list">
          <li v-for="bullet in valueProp.bullets" :key="bullet">
            {{ bullet }}
          </li>
        </ul>
        <RouterLink to="/contact" class="btn btn--primary">{{ valueProp.cta }}</RouterLink>
      </div>
      <CheckoutCard :checkout="checkout" />
    </div>
  </section>
</template>

<style scoped>
.value__grid {
  display: grid;
  gap: 48px;
  align-items: center;
}

.value__list {
  margin: 0 0 28px;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 12px;
}

.value__list li {
  padding-left: 24px;
  position: relative;
  color: var(--text-secondary);
  font-size: 15px;
}

.value__list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-blue);
}

@media (min-width: 900px) {
  .value__grid {
    grid-template-columns: 1.1fr 0.9fr;
  }
}
</style>
