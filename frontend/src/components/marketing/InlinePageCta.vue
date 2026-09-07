<script setup>
import { RouterLink } from "vue-router";

defineProps({
  title: { type: String, default: "" },
  body: { type: String, default: "" },
  to: { type: String, default: "" },
  buttonLabel: { type: String, default: "" },
});
</script>

<template>
  <section class="section cta-inline">
    <div class="container card cta-inline__inner">
      <h2>{{ title }}</h2>
      <p>{{ body }}</p>
      <RouterLink :to="to" class="btn btn--primary">{{ buttonLabel }}</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.cta-inline__inner {
  text-align: center;
  padding: 48px 32px;
}

.cta-inline__inner h2 {
  margin: 0 0 8px;
}

.cta-inline__inner p {
  color: var(--text-secondary);
  margin: 0 0 24px;
}
</style>
