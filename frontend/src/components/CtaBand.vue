<script setup>
defineProps({
  site: { type: Object, required: true },
  hero: { type: Object, required: true },
});
</script>

<template>
  <section id="get-started" class="cta section">
    <div class="container cta__inner card">
      <h2 class="cta__title">Send payments that get settled faster</h2>
      <p class="cta__lead">
        {{ site.footer_blurb }} Start with {{ site.name }} today.
      </p>
      <RouterLink :to="site.get_started_url" class="btn btn--primary">
        {{ hero.cta_primary }}
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.cta__inner {
  text-align: center;
  padding: 56px 32px;
  background: linear-gradient(
    135deg,
    var(--bg-surface) 0%,
    var(--accent-blue-tint) 100%
  );
}

.cta__title {
  font-size: clamp(28px, 4vw, 36px);
  margin: 0 0 12px;
  letter-spacing: -0.02em;
}

.cta__lead {
  margin: 0 0 28px;
  color: var(--text-secondary);
  max-width: 480px;
  margin-inline: auto;
}
</style>
