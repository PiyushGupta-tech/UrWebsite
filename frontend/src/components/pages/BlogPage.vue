<script setup>
import ResourceLayout from "./ResourceLayout.vue";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});
</script>

<template>
  <ResourceLayout :title="page.title" :intro="page.intro">
    <div class="blog-grid">
      <component
        :is="post.href ? 'RouterLink' : 'article'"
        v-for="post in page.posts"
        :key="post.slug"
        :to="post.href || undefined"
        class="blog-card"
        :class="{ 'blog-card--link': post.href }"
      >
        <div class="blog-card__meta">
          <span class="blog-card__category">{{ post.category }}</span>
          <time class="blog-card__date">{{ post.date }}</time>
        </div>
        <h2 class="blog-card__title">{{ post.title }}</h2>
        <span class="blog-card__link">
          {{ post.href ? "Explore product" : "Read more" }}
          <img
            src="/images/figma-contact/nav-arrow-teal.svg"
            alt=""
            width="18"
            height="18"
            decoding="async"
          />
        </span>
      </component>
    </div>
  </ResourceLayout>
</template>

<style scoped>
.blog-grid {
  display: grid;
  gap: 24px;
}

@media (min-width: 700px) {
  .blog-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.blog-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 32px;
  background: #ffffff;
  border: 1px solid var(--rs-line);
  border-radius: var(--rs-radius);
  box-shadow: var(--rs-shadow);
  color: inherit;
  text-decoration: none;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.blog-card--link:hover,
.blog-card--link:focus-visible {
  transform: translateY(-4px);
  border-color: rgba(9, 116, 149, 0.28);
  box-shadow: 0 18px 48px rgba(37, 43, 55, 0.12);
}

.blog-card__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
}

.blog-card__category {
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--rs-teal-tint);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--rs-teal);
}

.blog-card__date {
  font-size: 13px;
  color: var(--rs-subtle);
}

.blog-card__title {
  flex: 1;
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: var(--rs-ink);
}

.blog-card__link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 15px;
  font-weight: 600;
  color: var(--rs-teal);
}

.blog-card__link img {
  transition: transform 0.2s ease;
}

.blog-card--link:hover .blog-card__link img,
.blog-card--link:focus-visible .blog-card__link img {
  transform: translateX(3px);
}

@media (max-width: 700px) {
  .blog-card {
    padding: 24px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .blog-card,
  .blog-card__link img {
    transition: none;
  }

  .blog-card--link:hover,
  .blog-card--link:focus-visible {
    transform: none;
  }
}
</style>
