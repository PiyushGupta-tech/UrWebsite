<script setup>
defineProps({
  links: { type: Array, default: () => [] },
  title: { type: String, default: "Related solutions" },
});
</script>

<template>
  <section v-if="links.length" class="section related-links">
    <div class="container">
      <h2 class="related-links__title">{{ title }}</h2>
      <div class="related-links__grid">
        <RouterLink
          v-for="link in links"
          :key="link.href"
          :to="link.href"
          class="card related-links__card"
        >
          <h3>{{ link.label }}</h3>
          <p v-if="link.description">{{ link.description }}</p>
          <span class="related-links__cta">Learn more →</span>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.related-links {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.related-links__title {
  margin: 0 0 20px;
  font-size: clamp(22px, 3vw, 28px);
  letter-spacing: -0.02em;
}

.related-links__grid {
  display: grid;
  gap: 16px;
}

@media (min-width: 640px) {
  .related-links__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.related-links__card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color 0.15s, transform 0.15s;
}

.related-links__card:hover {
  border-color: var(--accent-blue);
  transform: translateY(-2px);
}

.related-links__card h3 {
  margin: 0;
  font-size: 16px;
}

.related-links__card p {
  margin: 0;
  flex: 1;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.55;
}

.related-links__cta {
  font-size: 14px;
  font-weight: 600;
  background: var(--btn-primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
</style>
