<script setup>
defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="why section">
    <div class="container">
      <p class="eyebrow">{{ section.eyebrow }}</p>
      <h2 class="section-title">{{ section.title }}</h2>
      <div class="why__grid">
        <article
          v-for="item in section.items"
          :key="item.title"
          class="why__card"
        >
          <h3>{{ item.title }}</h3>
          <p>{{ item.body }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.why {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.why__grid {
  display: grid;
  gap: 32px;
  margin-top: 40px;
}

.why__card h3 {
  margin: 0 0 10px;
  font-size: 18px;
}

.why__card p {
  margin: 0;
  font-size: 15px;
  color: var(--text-secondary);
}

@media (min-width: 640px) {
  .why__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1000px) {
  .why__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
