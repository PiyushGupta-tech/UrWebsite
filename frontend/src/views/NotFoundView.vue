<script setup>
import { onBeforeUnmount, onMounted } from "vue";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

const TITLE = "Page not found | Urbanrupee";
/* Defaults from index.html: on a direct 404 visit the server has already swapped them out,
   so restoring the "previous" values would leak noindex onto the next page. */
const DEFAULT_TITLE = "Urbanrupee | Payment Orchestration & Infrastructure India";
const DEFAULT_ROBOTS = "index, follow, max-image-preview:large, max-snippet:-1";

const links = [
  { label: "All products", to: "/products" },
  { label: "Payment Orchestration", to: "/products/orchestration" },
  { label: "Collections", to: "/services/collections" },
  { label: "Payouts", to: "/services/payouts" },
  { label: "FAQ", to: "/faq" },
  { label: "Contact", to: "/contact" },
];

function setRobots(content) {
  let meta = document.querySelector('meta[name="robots"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.setAttribute("name", "robots");
    document.head.appendChild(meta);
  }
  meta.setAttribute("content", content);
}

onMounted(() => {
  document.title = TITLE;
  setRobots("noindex, follow");
});

onBeforeUnmount(() => {
  // The next page sets its own title once its data loads; until then show the site default.
  if (document.title === TITLE) document.title = DEFAULT_TITLE;
  setRobots(DEFAULT_ROBOTS);
});
</script>

<template>
  <main class="not-found" aria-labelledby="not-found-title">
    <div class="not-found__bg" aria-hidden="true">
      <img src="/images/herobg.svg" alt="" width="1440" height="600" decoding="async" />
    </div>

    <div class="not-found__inner">
      <p class="not-found__code">404</p>
      <h1 id="not-found-title" class="not-found__title">We couldn't find that page</h1>
      <p class="not-found__body">
        The link may be broken or the page may have moved. Try one of these instead.
      </p>

      <div class="not-found__actions">
        <RouterLink to="/" class="not-found__btn not-found__btn--primary">Back to home</RouterLink>
        <RouterLink to="/contact" class="not-found__btn not-found__btn--ghost">
          Talk to an Expert
        </RouterLink>
      </div>

      <nav class="not-found__links" aria-label="Popular pages">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="not-found__link">
          {{ link.label }}
        </RouterLink>
      </nav>
    </div>
  </main>
</template>

<style scoped>
.not-found {
  --nf-nav-offset: 129px;
  --nf-ink: #252b37;
  --nf-muted: #535861;
  position: relative;
  margin-top: calc(-1 * var(--nf-nav-offset));
  padding-top: var(--nf-nav-offset);
  overflow: hidden;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: var(--nf-ink);
  background: #ffffff;
}

.not-found__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.not-found__bg img {
  position: absolute;
  top: 0;
  left: 50%;
  width: 100%;
  min-width: 1440px;
  height: auto;
  transform: translateX(-50%);
  -webkit-mask-image: linear-gradient(to bottom, #000 55%, transparent);
  mask-image: linear-gradient(to bottom, #000 55%, transparent);
}

.not-found__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 120px var(--ur-gutter, 24px) 140px;
  box-sizing: content-box;
  text-align: center;
}

.not-found__code {
  margin: 0;
  font-size: 96px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -2px;
  color: #097495;
}

.not-found__title {
  margin: 0;
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -1.26px;
}

.not-found__body {
  margin: 0;
  max-width: 460px;
  font-size: 16px;
  line-height: 24px;
  color: var(--nf-muted);
}

.not-found__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.not-found__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 155px;
  height: 52px;
  padding: 0 20px;
  box-sizing: border-box;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: opacity 0.15s ease;
}

.not-found__btn:hover {
  opacity: 0.92;
}

.not-found__btn--primary {
  background: #097495;
  color: #ffffff;
}

.not-found__btn--ghost {
  border: 1px solid #d5d7da;
  background: #ffffff;
  color: var(--nf-ink);
}

.not-found__btn:focus-visible,
.not-found__link:focus-visible {
  outline: 2px solid #097495;
  outline-offset: 2px;
}

.not-found__links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 20px;
  margin-top: 24px;
}

.not-found__link {
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  color: #097495;
  text-decoration: none;
}

.not-found__link:hover {
  text-decoration: underline;
}

@media (max-width: 1280px) {
  .not-found {
    --nf-nav-offset: 113px;
  }
}

@media (max-width: 1200px) {
  .not-found {
    --nf-nav-offset: 82px;
  }
}

@media (max-width: 700px) {
  .not-found {
    --nf-nav-offset: 88px;
  }
}

@media (max-width: 767px) {
  .not-found__inner {
    padding: 72px 16px 96px;
  }

  .not-found__code {
    font-size: 72px;
  }

  .not-found__title {
    font-size: 28px;
    line-height: 36px;
    letter-spacing: -0.84px;
  }

  .not-found__body {
    font-size: 14px;
    line-height: 20px;
  }

  .not-found__actions {
    flex-direction: column;
    align-self: stretch;
  }

  .not-found__btn {
    width: 100%;
    height: 48px;
  }
}
</style>
