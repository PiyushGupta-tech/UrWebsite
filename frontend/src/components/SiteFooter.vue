<script setup>
import { computed } from "vue";
import { SOCIAL_LINKS } from "@/constants/socialLinks.js";

const props = defineProps({
  footer: { type: Object, required: true },
  site: { type: Object, required: true },
});

const copyrightText = computed(() => {
  const currentYear = new Date().getFullYear();
  const base = String(props.site?.copyright || "").trim();
  if (!base) {
    return `Copyright © ${currentYear} Urbanrupee. All rights reserved.`;
  }
  if (/\b20\d{2}\b/.test(base)) {
    return base.replace(/\b20\d{2}\b/, String(currentYear));
  }
  return `Copyright © ${currentYear} ${base.replace(/^Copyright\s*©?\s*/i, "").trim()}`;
});
</script>

<template>
  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__top">
        <div class="footer__brand">
          <img
            class="footer__logo-img"
            src="/images/figma-footer-logo.png"
            :alt="site.name"
            width="799"
            height="156"
            loading="lazy"
            decoding="async"
          />
          <p>{{ site.footer_blurb }}</p>
          <img
            class="footer__certs"
            src="/images/figma-footer-certs.png"
            alt="PCI DSS compliant and ISO certified"
            width="141"
            height="42"
            loading="lazy"
            decoding="async"
          />
        </div>

        <div class="footer__cols">
          <div class="footer__col">
            <h3 class="footer__col-title">Company</h3>
            <RouterLink v-for="link in footer.company" :key="link.href" :to="link.href">
              {{ link.label }}
            </RouterLink>
          </div>

          <div class="footer__col">
            <h3 class="footer__col-title">Services</h3>
            <RouterLink v-for="link in footer.services" :key="link.href" :to="link.href">
              {{ link.label }}
            </RouterLink>
          </div>

          <div class="footer__col">
            <h3 class="footer__col-title">Products</h3>
            <RouterLink v-for="link in footer.products" :key="link.href" :to="link.href">
              {{ link.label }}
            </RouterLink>
          </div>

          <div class="footer__col footer__col--social">
            <h3 class="footer__col-title">Find us on</h3>
            <div class="footer__social" aria-label="Social media">
              <a
                v-for="item in SOCIAL_LINKS"
                :key="item.id"
                class="footer__social-link"
                :href="item.href"
                target="_blank"
                rel="noopener noreferrer"
                :aria-label="item.label"
              >
                <svg
                  v-if="item.id === 'linkedin'"
                  viewBox="0 0 24 24"
                  preserveAspectRatio="xMidYMid meet"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
                  />
                </svg>
                <svg
                  v-else-if="item.id === 'youtube'"
                  viewBox="0 0 24 24"
                  preserveAspectRatio="xMidYMid meet"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
                  />
                </svg>
                <svg
                  v-else-if="item.id === 'facebook'"
                  viewBox="0 0 24 24"
                  preserveAspectRatio="xMidYMid meet"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
                  />
                </svg>
                <svg
                  v-else-if="item.id === 'instagram'"
                  viewBox="0 0 24 24"
                  preserveAspectRatio="xMidYMid meet"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"
                  />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="footer__divider" />

      <div class="footer__bottom">
        <p>{{ copyrightText }}</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #18181a;
  color: #ffffff;
  padding: 42px 0;
}

.footer__inner {
  display: flex;
  flex-direction: column;
  gap: 27px;
}

.footer__top {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.footer__logo-img {
  display: block;
  margin-bottom: 16px;
  width: 186px;
  max-width: 100%;
  height: auto;
}

.footer__brand p {
  margin: 0 0 20px;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0.04em;
  color: rgba(255, 255, 255, 0.92);
  max-width: 358px;
}

.footer__certs {
  display: block;
  height: 42px;
  width: auto;
  object-fit: contain;
}

.footer__cols {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: auto auto;
  grid-auto-flow: column;
  gap: 28px 24px;
  align-content: start;
}

.footer__col {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  min-width: 0;
}

.footer__col-title {
  margin: 0 0 7px;
  font-size: 16px;
  font-weight: 600;
  line-height: 20px;
  color: #ffffff;
  text-transform: none;
  letter-spacing: 0;
}

.footer__cols a {
  display: block;
  font-size: 12px;
  line-height: 20px;
  color: rgba(255, 255, 255, 0.8);
  transition: color 0.15s;
  text-decoration: none;
}

.footer__cols a:hover {
  color: #ffffff;
}

.footer__col--social {
  gap: 12px;
}

.footer__social {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.footer__social-link {
  position: relative;
  display: inline-block;
  box-sizing: border-box;
  width: 32px;
  height: 32px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.88);
  background: transparent;
  transition:
    color 0.15s,
    background 0.15s,
    border-color 0.15s,
    box-shadow 0.15s;
}

.footer__social-link:hover {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.42);
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.16);
}

.footer__social-link svg {
  position: absolute;
  top: 50%;
  left: 50%;
  display: block;
  width: 14px;
  height: 14px;
  transform: translate(-50%, -50%);
}

.footer__divider {
  width: 100%;
  height: 1px;
  background: rgba(14, 162, 199, 0.12);
}

.footer__bottom {
  font-size: 14px;
  line-height: 20px;
  color: rgba(255, 255, 255, 0.72);
}

.footer__bottom p {
  margin: 0;
}

@media (min-width: 960px) {
  .footer__top {
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
    gap: 32px;
  }

  .footer__cols {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: none;
    grid-auto-flow: row;
    gap: 24px;
    min-width: 560px;
  }

  .footer__social {
    flex-wrap: nowrap;
  }
}
</style>
