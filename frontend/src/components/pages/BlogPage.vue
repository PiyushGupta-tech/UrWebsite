<script setup>
import PageHero from "./PageHero.vue";

defineProps({
  page: { type: Object, required: true },
});
</script>

<template>
  <main>
    <PageHero :title="page.title" :intro="page.intro" />

    <section class="section">
      <div class="container blog-grid">
        <article
          v-for="post in page.posts"
          :key="post.slug"
          class="card blog-card"
        >
          <span class="blog-card__category">{{ post.category }}</span>
          <time class="blog-card__date">{{ post.date }}</time>
          <h2 class="blog-card__title">{{ post.title }}</h2>
          <span class="blog-card__link">Read more →</span>
        </article>
      </div>
    </section>
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

.blog-card:hover {
  border-color: var(--accent-blue);
  transform: translateY(-2px);
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
