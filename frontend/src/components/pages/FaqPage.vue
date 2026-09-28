<script setup>
import ResourceLayout from "./ResourceLayout.vue";
import MarketingFaqAccordion from "@/components/marketing/MarketingFaqAccordion.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
</script>

<template>
  <ResourceLayout :title="page.title" :intro="page.intro">
    <div
      class="faq-layout"
      :class="{ 'faq-layout--with-aside': page.product_links?.items?.length }"
    >
      <MarketingFaqAccordion
        :items="page.items || []"
        variant="simple"
        :numbered="false"
        aria-label="Frequently asked questions"
      />

      <aside v-if="page.product_links?.items?.length" class="faq-products">
        <h2 class="faq-products__title">{{ page.product_links.title }}</h2>
        <p v-if="page.product_links.intro" class="faq-products__intro">
          {{ page.product_links.intro }}
        </p>
        <ul class="faq-products__list">
          <li v-for="link in page.product_links.items" :key="link.href">
            <RouterLink :to="link.href" class="faq-products__link">
              <span>{{ link.label }}</span>
              <img
                src="/images/figma-contact/nav-arrow-teal.svg"
                alt=""
                width="18"
                height="18"
                decoding="async"
              />
            </RouterLink>
          </li>
        </ul>
      </aside>
    </div>
  </ResourceLayout>
</template>

<style scoped>
.faq-layout {
  display: grid;
  gap: 24px;
  align-items: start;
}

@media (min-width: 1024px) {
  .faq-layout--with-aside {
    grid-template-columns: minmax(0, 1fr) 360px;
  }

  .faq-products {
    position: sticky;
    top: 120px;
  }
}

.faq-products {
  padding: 28px;
  background: #ffffff;
  border: 1px solid var(--rs-line);
  border-radius: var(--rs-radius);
  box-shadow: var(--rs-shadow);
}

.faq-products__title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--rs-ink);
}

.faq-products__intro {
  margin: 8px 0 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--rs-muted);
}

.faq-products__list {
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}

.faq-products__list li + li {
  border-top: 1px solid var(--rs-line);
}

.faq-products__link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--rs-ink);
  text-decoration: none;
  transition: color 0.15s ease;
}

.faq-products__link img {
  flex-shrink: 0;
  transition: transform 0.15s ease;
}

.faq-products__link:hover,
.faq-products__link:focus-visible {
  color: var(--rs-teal);
}

.faq-products__link:hover img,
.faq-products__link:focus-visible img {
  transform: translateX(3px);
}

@media (prefers-reduced-motion: reduce) {
  .faq-products__link img {
    transition: none;
  }
}
</style>
