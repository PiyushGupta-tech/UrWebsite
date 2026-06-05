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

    <section class="section">
      <div class="container blog-grid">
        <template v-for="post in page.posts" :key="post.slug">
          <RouterLink
            v-if="post.href"
            :to="post.href"
            class="card blog-card blog-card--link"
          >
            <span class="blog-card__category">{{ post.category }}</span>
            <time class="blog-card__date">{{ post.date }}</time>
            <h2 class="blog-card__title">{{ post.title }}</h2>
            <span class="blog-card__link">Explore product →</span>
          </RouterLink>
          <article v-else class="card blog-card">
            <span class="blog-card__category">{{ post.category }}</span>
            <time class="blog-card__date">{{ post.date }}</time>
            <h2 class="blog-card__title">{{ post.title }}</h2>
            <span class="blog-card__link">Read more →</span>
          </article>
        </template>
      </div>
    </section>

    <RelatedLinks v-if="relatedLinks.length" :links="relatedLinks" />
  </main>
</template>

<style scoped>
.blog-grid {
  display: grid;
  gap: 20px;
}

@media (min-width: 640px) {
  .blog-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.blog-card {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color 0.15s, transform 0.15s;
}

.blog-card:hover,
.blog-card--link:hover {
  border-color: var(--accent-blue);
  transform: translateY(-2px);
}

.blog-card--link {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
}

.blog-card__category {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent-purple);
}

.blog-card__date {
  font-size: 13px;
  color: var(--text-muted);
}

.blog-card__title {
  margin: 0;
  font-size: 18px;
  line-height: 1.35;
  flex: 1;
}

.blog-card__link {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-blue);
}
</style>
