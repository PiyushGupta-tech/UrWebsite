<script setup>
import PageHero from "./PageHero.vue";
import RelatedLinks from "@/components/RelatedLinks.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
</script>

<template>
  <main>
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

    <section v-if="page.cta" class="section section--tight">
      <div class="container hub__cta">
        <RouterLink :to="page.cta.href" class="btn btn--primary">{{ page.cta.label }}</RouterLink>
      </div>
    </section>

    <RelatedLinks v-if="relatedLinks.length" :links="relatedLinks" />
  </main>
</template>

<style scoped>
.hub__heading {
  margin-bottom: 28px;
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
}

.hub__cta {
  display: flex;
  justify-content: center;
}
</style>
