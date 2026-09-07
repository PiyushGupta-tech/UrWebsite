<script setup>
import PageHero from "./PageHero.vue";
import MarketingFaqAccordion from "@/components/marketing/MarketingFaqAccordion.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
</script>

<template>
  <main>
    <PageHero :title="page.title" :intro="page.intro" />

    <section class="section">
      <div class="container">
        <MarketingFaqAccordion
          :items="page.items || []"
          variant="simple"
          :numbered="false"
          aria-label="Frequently asked questions"
        />
      </div>
    </section>

    <section v-if="page.product_links?.items?.length" class="section section--alt">
      <div class="container faq-products">
        <h2>{{ page.product_links.title }}</h2>
        <p v-if="page.product_links.intro" class="faq-products__intro">
          {{ page.product_links.intro }}
        </p>
        <ul class="faq-products__list">
          <li v-for="link in page.product_links.items" :key="link.href">
            <RouterLink :to="link.href">{{ link.label }}</RouterLink>
          </li>
        </ul>
      </div>
    </section>
  </main>
</template>

<style scoped>
.section--alt {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.faq-products {
  max-width: 720px;
}

.faq-products h2 {
  margin: 0 0 8px;
  font-size: 22px;
}

.faq-products__intro {
  margin: 0 0 16px;
  color: var(--text-secondary);
}

.faq-products__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.faq-products__list a {
  font-weight: 600;
  color: var(--accent-blue);
}

</style>
