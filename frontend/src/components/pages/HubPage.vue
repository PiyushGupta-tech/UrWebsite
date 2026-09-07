<script setup>
import PageHero from "./PageHero.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
</script>

<template>
  <main class="hub-page">
    <PageHero :title="page.title" :intro="page.intro" />

    <section
      v-for="section in page.sections"
      :key="section.heading"
      class="section"
      :class="{ 'section--alt': section.alt }"
    >
      <div class="container">
        <h2 class="section-title hub__heading">{{ section.heading }}</h2>
        <div class="hub__grid">
          <RouterLink
            v-for="item in section.items"
            :key="item.href"
            :to="item.href"
            class="hub__card card"
          >
            <h3 class="hub__card-title">{{ item.title }}</h3>
            <p class="hub__card-body">{{ item.body }}</p>
            <span class="hub__card-link">Learn more →</span>
          </RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.hub-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.hub__heading {
  margin-bottom: 28px;
  text-align: center;
}

.hub__grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.hub__card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 24px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  text-align: center;
}

.hub__card:hover {
  border-color: var(--accent-blue);
  box-shadow: 0 4px 16px rgba(0, 152, 242, 0.12);
}

.hub__card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.25;
}

.hub__card-body {
  margin: 0;
  flex: 1;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.55;
}

.hub__card-link {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-blue);
  justify-content: center;
}

</style>
