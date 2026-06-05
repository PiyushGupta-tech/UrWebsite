<script setup>
import { ref } from "vue";
import PageHero from "./PageHero.vue";
import RelatedLinks from "@/components/RelatedLinks.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const openIndex = ref(0);

function toggle(index) {
  openIndex.value = openIndex.value === index ? -1 : index;
}
</script>

<template>
  <main>
    <PageHero :title="page.title" :intro="page.intro" />

    <section class="section">
      <div class="container faq-page">
        <div
          v-for="(item, index) in page.items"
          :key="item.question"
          class="faq-page__item card"
          :class="{ 'faq-page__item--open': openIndex === index }"
        >
          <button
            type="button"
            class="faq-page__question"
            :aria-expanded="openIndex === index"
            @click="toggle(index)"
          >
            {{ item.question }}
            <span class="faq-page__icon">{{ openIndex === index ? "−" : "+" }}</span>
          </button>
          <div v-show="openIndex === index" class="faq-page__answer">
            <p>{{ item.answer }}</p>
            <ul v-if="item.links?.length" class="faq-page__links">
              <li v-for="link in item.links" :key="link.href">
                <RouterLink :to="link.href">{{ link.label }}</RouterLink>
              </li>
            </ul>
          </div>
        </div>
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

    <RelatedLinks
      v-if="relatedLinks.length"
      :links="relatedLinks"
      title="You may also need"
    />

    <section v-if="page.cta" class="section cta-inline">
      <div class="container card cta-inline__inner">
        <h2>{{ page.cta.title }}</h2>
        <p>{{ page.cta.body }}</p>
        <RouterLink :to="page.cta.href" class="btn btn--primary">{{ page.cta.button }}</RouterLink>
      </div>
    </section>
  </main>
</template>

<style scoped>
.faq-page {
  max-width: 720px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.faq-page__item {
  padding: 0;
  overflow: hidden;
}

.faq-page__question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px;
  border: none;
  background: none;
  text-align: left;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.faq-page__icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-page);
  color: var(--text-muted);
}

.faq-page__answer {
  padding: 0 24px 20px;
}

.faq-page__answer p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.65;
}

.faq-page__links {
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
}

.faq-page__links a {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-blue);
}

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

.faq-page__item--open {
  border-color: var(--accent-blue);
}

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
