<script setup>
defineProps({
  features: { type: Object, required: true },
});
</script>

<template>
  <section class="features section">
    <div class="container">
      <p class="eyebrow">{{ features.eyebrow }}</p>
      <h2 class="section-title">{{ features.title }}</h2>
      <div class="features__grid">
        <article
          v-for="(item, index) in features.items"
          :key="item.title"
          class="features__card card"
        >
          <span class="features__index">0{{ index + 1 }}</span>
          <h3>{{ item.title }}</h3>
          <p>{{ item.body }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.features__grid {
  display: grid;
  gap: 20px;
  margin-top: 40px;
}

.features__card {
  padding: 32px;
}

.features__index {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent-purple);
  margin-bottom: 16px;
}

.features__card h3 {
  margin: 0 0 12px;
  font-size: 20px;
}

.features__card p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
}

@media (min-width: 768px) {
  .features__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
