<script setup>
defineProps({
  catalogue: { type: Object, required: true },
});
</script>

<template>
  <section class="catalogue section">
    <div class="container">
      <p class="eyebrow">{{ catalogue.eyebrow }}</p>
      <h2 class="section-title">{{ catalogue.title }}</h2>
      <p class="catalogue__intro">{{ catalogue.intro }}</p>

      <div class="catalogue__grid">
        <RouterLink
          v-for="item in catalogue.items"
          :key="item.title"
          :to="item.href"
          class="catalogue__card card"
        >
          <h3>{{ item.title }}</h3>
          <p class="catalogue__body">{{ item.body }}</p>
          <ul class="catalogue__highlights">
            <li v-for="h in item.highlights" :key="h">{{ h }}</li>
          </ul>
          <span class="catalogue__link">Learn more →</span>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.catalogue {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.catalogue__intro {
  max-width: 720px;
  margin: 0 0 40px;
  font-size: 18px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.catalogue__grid {
  display: grid;
  gap: 20px;
}

.catalogue__card {
  padding: 28px;
  display: flex;
  flex-direction: column;
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.catalogue__card:hover {
  border-color: #06b6d4;
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(26, 54, 93, 0.12);
}

.catalogue__card h3 {
  margin: 0 0 10px;
  font-size: 18px;
  letter-spacing: -0.02em;
}

.catalogue__body {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  flex: 1;
}

.catalogue__highlights {
  margin: 0 0 16px;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.catalogue__highlights li {
  font-size: 11px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: var(--radius-pill);
  background: rgba(6, 182, 212, 0.12);
  color: #0e7490;
}

.catalogue__link {
  font-size: 14px;
  font-weight: 600;
  background: var(--btn-primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

@media (min-width: 640px) {
  .catalogue__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1000px) {
  .catalogue__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
