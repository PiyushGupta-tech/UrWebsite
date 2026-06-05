<script setup>
import DashboardPreview from "./DashboardPreview.vue";

defineProps({
  hero: { type: Object, required: true },
  dashboard: { type: Object, required: true },
  site: { type: Object, default: null },
});
</script>

<template>
  <section class="hero section">
    <div class="container hero__grid">
      <div class="hero__copy">
        <p class="hero__proof">{{ hero.social_proof }}</p>
        <h1 class="hero__title">{{ hero.headline }}</h1>
        <p class="hero__lead">{{ hero.subheadline }}</p>

        <div class="hero__chips">
          <div v-for="chip in hero.fee_chips" :key="chip.label" class="chip">
            <span class="chip__label">{{ chip.label }}</span>
            <span class="chip__value">{{ chip.value }}</span>
          </div>
        </div>

        <div v-if="site?.sign_in_url" class="hero__actions">
          <a
            :href="site.sign_in_url"
            class="btn btn--primary"
            target="_blank"
            rel="noopener noreferrer"
          >{{ hero.cta_secondary }}</a>
        </div>

        <ul class="hero__badges">
          <li v-for="badge in hero.badges" :key="badge">{{ badge }}</li>
        </ul>
      </div>

      <div class="hero__visual">
        <DashboardPreview :dashboard="dashboard" :tilted="true" />
        <div class="hero__glow" aria-hidden="true" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding-top: 48px;
  overflow: hidden;
}

.hero__grid {
  display: grid;
  gap: 48px;
  align-items: center;
}

.hero__proof {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 16px;
}

.hero__title {
  font-size: clamp(36px, 5vw, 56px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.08;
  margin: 0 0 20px;
}

.hero__lead {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 520px;
  margin: 0 0 28px;
}

.hero__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 28px;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 32px;
}

.hero__badges {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero__badges li {
  font-size: 11px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: var(--radius-pill);
  background: rgba(6, 182, 212, 0.12);
  color: #0e7490;
}

.hero__visual {
  position: relative;
  display: flex;
  justify-content: center;
  padding: 8px 0;
  min-height: 420px;
}

.hero__glow {
  position: absolute;
  inset: 10% 0;
  background: radial-gradient(
    ellipse at 70% 50%,
    rgba(6, 182, 212, 0.2),
    transparent 65%
  );
  z-index: -1;
  pointer-events: none;
}

@media (min-width: 900px) {
  .hero__grid {
    grid-template-columns: 1fr 1fr;
  }

  .hero__visual {
    justify-content: flex-end;
  }
}
</style>
