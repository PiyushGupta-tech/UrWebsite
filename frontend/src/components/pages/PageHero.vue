<script setup>
defineProps({
  title: { type: String, required: true },
  intro: { type: String, default: "" },
  split: { type: Boolean, default: false },
  ready: { type: Boolean, default: true },
  /** "left" puts graphic before copy; "right" (default) puts copy first */
  graphicPosition: {
    type: String,
    default: "right",
    validator: (v) => v === "left" || v === "right",
  },
});
</script>

<template>
  <section
    class="page-hero section--tight"
    :class="{
      'page-hero--split': split,
      'page-hero--ready': ready,
      'page-hero--graphic-left': split && graphicPosition === 'left',
    }"
  >
    <div v-if="split" class="page-hero__glow" aria-hidden="true" />
    <div class="container" :class="split ? 'page-hero__layout' : 'page-hero__inner'">
      <div v-if="$slots.graphic && graphicPosition === 'left'" class="page-hero__graphic">
        <slot name="graphic" />
      </div>

      <div class="page-hero__copy">
        <h1 class="page-hero__title">{{ title }}</h1>
        <p v-if="intro" class="page-hero__intro">{{ intro }}</p>
        <div v-if="$slots['copy-extra']" class="page-hero__extra">
          <slot name="copy-extra" />
        </div>
        <div v-if="split" class="page-hero__rule" aria-hidden="true" />
      </div>

      <div v-if="$slots.graphic && graphicPosition === 'right'" class="page-hero__graphic">
        <slot name="graphic" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.page-hero {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
}

.page-hero--split {
  position: relative;
  overflow: visible;
}

.page-hero__glow {
  position: absolute;
  top: 30%;
  width: min(420px, 45vw);
  height: 240px;
  border-radius: 24px;
  background: linear-gradient(
    135deg,
    rgba(6, 182, 212, 0.08) 0%,
    rgba(26, 54, 93, 0.06) 50%,
    transparent 100%
  );
  pointer-events: none;
  animation: page-hero-glow 5s ease-in-out infinite;
}

.page-hero--graphic-left .page-hero__glow {
  left: 5%;
  right: auto;
}

.page-hero:not(.page-hero--graphic-left) .page-hero__glow {
  right: 5%;
  left: auto;
}

@keyframes page-hero-glow {
  0%,
  100% {
    opacity: 0.7;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-8px);
  }
}

.page-hero__inner {
  max-width: 720px;
}

.page-hero__layout {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 28px;
  align-items: start;
}

@media (min-width: 900px) {
  .page-hero__layout {
    grid-template-columns: 1.05fr 0.95fr;
    gap: 36px;
    min-height: 0;
  }

  .page-hero--graphic-left .page-hero__layout {
    grid-template-columns: 0.95fr 1.05fr;
  }
}

.page-hero__copy {
  max-width: 520px;
  align-self: start;
}

.page-hero--graphic-left .page-hero__copy {
  justify-self: end;
}

.page-hero__graphic {
  justify-self: center;
  align-self: start;
  width: 100%;
  max-width: 400px;
}

@media (min-width: 900px) {
  .page-hero__graphic {
    max-width: 520px;
  }

  .page-hero:not(.page-hero--graphic-left) .page-hero__graphic {
    justify-self: end;
  }

  .page-hero--graphic-left .page-hero__graphic {
    justify-self: start;
  }
}

.page-hero__title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin: 0 0 16px;
}

.page-hero--split .page-hero__title,
.page-hero--split .page-hero__intro {
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.55s ease,
    transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

.page-hero--split.page-hero--ready .page-hero__title,
.page-hero--split.page-hero--ready .page-hero__intro {
  opacity: 1;
  transform: translateY(0);
}

.page-hero__intro {
  margin: 0;
  font-size: 18px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.page-hero__extra {
  margin-top: 20px;
}

.page-hero--split .page-hero__extra {
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 0.5s ease 0.08s,
    transform 0.5s cubic-bezier(0.22, 1, 0.36, 1) 0.08s;
}

.page-hero--split.page-hero--ready .page-hero__extra {
  opacity: 1;
  transform: translateY(0);
}

.page-hero__rule {
  margin-top: 24px;
  height: 3px;
  width: 0;
  background: linear-gradient(90deg, #1a365d, #06b6d4);
  border-radius: 2px;
  transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.2s;
}

.page-hero--split.page-hero--ready .page-hero__rule {
  width: 100px;
}

@media (prefers-reduced-motion: reduce) {
  .page-hero__glow {
    animation: none;
  }

  .page-hero--split .page-hero__title,
  .page-hero--split .page-hero__intro,
  .page-hero--split .page-hero__extra {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .page-hero--split.page-hero--ready .page-hero__rule {
    width: 100px;
    transition: none;
  }
}
</style>
