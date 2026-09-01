<script setup>
import { computed, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

defineProps({
  nav: { type: Object, required: true },
  site: { type: Object, required: true },
});

const route = useRoute();
const openMenu = ref(null);
const mobileOpen = ref(false);

const ctaTo = computed(() =>
  route.path === "/contact" ? { path: "/contact", hash: "#contact-form" } : "/contact",
);

function closeMenus() {
  openMenu.value = null;
  mobileOpen.value = false;
}

function openDropdown(key) {
  openMenu.value = key;
}

function toggleDropdown(key) {
  openMenu.value = openMenu.value === key ? null : key;
}

function toggleMobile() {
  mobileOpen.value = !mobileOpen.value;
  if (!mobileOpen.value) openMenu.value = null;
}
</script>

<template>
  <!-- Figma Frame 2147225433 — 1146×89 @ (147, 40); logo → links → CTA gaps 175px -->
  <header class="nav">
    <div class="nav__shell">
      <div class="nav__bar">
        <RouterLink to="/" class="nav__logo" :aria-label="site.name" @click="closeMenus">
          <img
            class="nav__logo-img"
            src="/logos/urbanrupee-nav.svg"
            alt=""
            width="200"
            height="38"
            decoding="async"
            fetchpriority="high"
          />
        </RouterLink>

        <nav class="nav__links" :class="{ 'nav__links--open': mobileOpen }" aria-label="Primary">
          <RouterLink
            v-for="link in nav.links"
            :key="link.href"
            :to="link.href"
            class="nav__link"
            @click="closeMenus"
          >
            {{ link.label }}
          </RouterLink>

          <div
            class="nav__dropdown"
            @mouseenter="openDropdown('solutions')"
            @mouseleave="closeMenus"
          >
            <button
              type="button"
              class="nav__link nav__link--btn"
              :class="{ 'nav__link--open': openMenu === 'solutions' }"
              :aria-expanded="openMenu === 'solutions'"
              @click="toggleDropdown('solutions')"
            >
              Solutions
              <img
                class="nav__chevron"
                src="/images/figma-contact/nav-chevron.svg"
                alt=""
                width="24"
                height="24"
                decoding="async"
              />
            </button>
            <div v-show="openMenu === 'solutions'" class="nav__panel">
              <div class="nav__panel-inner">
                <p class="nav__panel-label">Services</p>
                <RouterLink
                  v-for="item in nav.services"
                  :key="item.href"
                  :to="item.href"
                  @click="closeMenus"
                >
                  {{ item.label }}
                </RouterLink>
                <p class="nav__panel-label">Products</p>
                <RouterLink
                  v-for="item in nav.products"
                  :key="item.href"
                  :to="item.href"
                  @click="closeMenus"
                >
                  {{ item.label }}
                </RouterLink>
                <p class="nav__panel-label">Resources</p>
                <RouterLink
                  v-for="item in nav.resources"
                  :key="item.href"
                  :to="item.href"
                  @click="closeMenus"
                >
                  {{ item.label }}
                </RouterLink>
              </div>
            </div>
          </div>

          <RouterLink
            :to="nav.contact_href"
            class="nav__link nav__link--contact"
            @click="closeMenus"
          >
            Contact Us
          </RouterLink>
        </nav>

        <div class="nav__actions">
          <RouterLink :to="ctaTo" class="nav__cta" @click="closeMenus">
            Talk to Expert
            <img
              class="nav__cta-arrow"
              src="/images/figma-contact/nav-arrow.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
          <button
            type="button"
            class="nav__menu-btn"
            :aria-expanded="mobileOpen"
            aria-label="Toggle menu"
            @click="toggleMobile"
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </div>
    </div>
  </header>
  <div class="nav-spacer" aria-hidden="true" />
</template>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: transparent;
  pointer-events: none;
}

.nav-spacer {
  height: 129px; /* 40 + 89 */
  flex-shrink: 0;
}

.nav__shell {
  pointer-events: none;
  max-width: 1440px;
  margin: 0 auto;
  padding: 40px 147px 0;
  box-sizing: border-box;
}

.nav__bar {
  pointer-events: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  width: 100%;
  max-width: 1146px;
  height: 89px;
  margin: 0 auto;
  padding: 16px 26px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(9, 116, 149, 0.18);
  border-radius: 8.428px;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 8px 24px rgba(9, 116, 149, 0.06);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.nav__logo {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  text-decoration: none;
}

.nav__logo-img {
  display: block;
  width: 200px;
  height: auto;
  max-height: 38px;
  object-fit: contain;
  object-position: left center;
}

.nav__links {
  display: none;
  align-items: center;
  gap: 35px;
  flex: 0 0 auto;
}

.nav__link {
  padding: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: #052201;
  background: transparent;
  border-radius: 0;
  text-shadow: none;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.15s ease;
}

.nav__link:hover,
.nav__link.router-link-exact-active,
.nav__link--btn.nav__link--open {
  color: #097495;
  background: transparent;
  text-shadow: none;
}

.nav__link.router-link-exact-active {
  font-weight: 600;
}

.nav__link--contact {
  color: #052201;
}

.nav__link--contact.router-link-active,
.nav__link--contact.router-link-exact-active {
  color: #097495;
  font-weight: 600;
}

.nav__link--btn {
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0;
  cursor: pointer;
  font: inherit;
  color: #052201;
  background: transparent;
  padding: 0;
}

.nav__link--btn:hover {
  background: transparent;
}

.nav__chevron {
  display: block;
  width: 24px;
  height: 24px;
  transform: rotate(180deg);
  flex-shrink: 0;
}

.nav__dropdown {
  position: relative;
}

.nav__panel {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding-top: 12px;
  min-width: 260px;
  z-index: 20;
}

.nav__panel-inner {
  padding: 8px;
  background: #ffffff;
  border: 1px solid rgba(9, 116, 149, 0.12);
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
  display: flex;
  flex-direction: column;
  max-height: min(70vh, 480px);
  overflow: auto;
}

.nav__panel-label {
  margin: 8px 12px 4px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #097495;
}

.nav__panel-label:first-child {
  margin-top: 4px;
}

.nav__panel-inner a {
  padding: 10px 12px;
  font-size: 14px;
  border-radius: 8px;
  color: #252b37;
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}

.nav__panel-inner a:hover {
  background: rgba(9, 116, 149, 0.08);
  color: #097495;
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.nav__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  width: 155px;
  height: 52px;
  padding: 0 16px;
  box-sizing: border-box;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  line-height: normal;
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}

.nav__cta:hover {
  opacity: 0.92;
  color: #ffffff;
}

.nav__cta-arrow {
  display: block;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav__menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  padding: 0;
  border: none;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.nav__menu-btn span {
  display: block;
  width: 18px;
  height: 2px;
  background: #097495;
  border-radius: 1px;
}

@media (min-width: 1100px) {
  .nav__links {
    display: flex;
  }
}

@media (max-width: 1280px) {
  .nav__shell {
    padding: 24px 40px 0;
  }

  .nav-spacer {
    height: 113px;
  }

  .nav__logo-img {
    width: 180px;
  }

  .nav__links {
    gap: 28px;
  }
}

@media (max-width: 1099px) {
  .nav__shell {
    padding: 16px 16px 0;
  }

  .nav-spacer {
    height: 92px;
  }

  .nav__bar {
    gap: 16px;
    height: auto;
    min-height: 64px;
    padding: 12px 16px;
    position: relative;
  }

  .nav__logo {
    width: auto;
  }

  .nav__logo-img {
    width: 160px;
    max-height: 32px;
  }

  .nav__links {
    display: none;
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    width: auto;
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(9, 116, 149, 0.18);
    border-radius: 8.428px;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(12px);
  }

  .nav__links--open {
    display: flex;
  }

  .nav__actions {
    margin-left: auto;
  }

  .nav__link,
  .nav__link--btn {
    padding: 12px;
    border-radius: 8px;
  }

  .nav__panel {
    position: static;
    transform: none;
    padding-top: 4px;
    min-width: 0;
  }

  .nav__cta {
    width: auto;
    height: 44px;
    font-size: 14px;
    padding: 0 12px;
  }

  .nav__menu-btn {
    display: inline-flex;
  }
}
</style>
