<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import BrandLogo from "./BrandLogo.vue";

defineProps({
  nav: { type: Object, required: true },
  site: { type: Object, required: true },
});

const openMenu = ref(null);

function closeMenus() {
  openMenu.value = null;
}

function openDropdown(key) {
  openMenu.value = key;
}

function toggleDropdown(key) {
  openMenu.value = openMenu.value === key ? null : key;
}
</script>

<template>
  <header class="nav">
    <div class="container nav__inner">
      <RouterLink to="/" class="nav__logo" @click="closeMenus">
        <BrandLogo variant="on-dark" :alt="site.name" />
      </RouterLink>

      <nav class="nav__links">
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
          @mouseenter="openDropdown('services')"
          @mouseleave="closeMenus"
        >
          <button
            type="button"
            class="nav__link nav__link--btn"
            :class="{ 'nav__link--open': openMenu === 'services' }"
            :aria-expanded="openMenu === 'services'"
            @click="toggleDropdown('services')"
          >
            Services
            <span class="nav__chevron">▾</span>
          </button>
          <div v-show="openMenu === 'services'" class="nav__panel">
            <div class="nav__panel-inner">
              <RouterLink
                v-for="item in nav.services"
                :key="item.href"
                :to="item.href"
                @click="closeMenus"
              >
                {{ item.label }}
              </RouterLink>
            </div>
          </div>
        </div>

        <div
          class="nav__dropdown"
          @mouseenter="openDropdown('products')"
          @mouseleave="closeMenus"
        >
          <button
            type="button"
            class="nav__link nav__link--btn"
            :class="{ 'nav__link--open': openMenu === 'products' }"
            :aria-expanded="openMenu === 'products'"
            @click="toggleDropdown('products')"
          >
            Products
            <span class="nav__chevron">▾</span>
          </button>
          <div v-show="openMenu === 'products'" class="nav__panel">
            <div class="nav__panel-inner">
              <RouterLink
                v-for="item in nav.products"
                :key="item.href"
                :to="item.href"
                @click="closeMenus"
              >
                {{ item.label }}
              </RouterLink>
            </div>
          </div>
        </div>

        <div
          class="nav__dropdown"
          @mouseenter="openDropdown('resources')"
          @mouseleave="closeMenus"
        >
          <button
            type="button"
            class="nav__link nav__link--btn"
            :class="{ 'nav__link--open': openMenu === 'resources' }"
            :aria-expanded="openMenu === 'resources'"
            @click="toggleDropdown('resources')"
          >
            Resources
            <span class="nav__chevron">▾</span>
          </button>
          <div v-show="openMenu === 'resources'" class="nav__panel">
            <div class="nav__panel-inner">
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

        <RouterLink :to="nav.contact_href" class="nav__link" @click="closeMenus">
          Contact
        </RouterLink>
      </nav>

      <div class="nav__actions">
        <a
          :href="site.sign_in_url"
          class="nav__sign-in nav__sign-in--solo"
          target="_blank"
          rel="noopener noreferrer"
        >
          Sign In
        </a>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--btn-primary-gradient);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.nav__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  min-height: 64px;
}

.nav__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 18px;
  color: #fff;
}

.nav__logo-mark {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 10px;
  font-size: 13px;
  letter-spacing: -0.02em;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.nav__links {
  display: none;
  align-items: center;
  gap: 4px;
}

.nav__link {
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.88);
  border-radius: 8px;
  background: transparent;
  transition: color 0.2s ease, text-shadow 0.2s ease;
}

.nav__link:hover,
.nav__link.router-link-exact-active,
.nav__link--btn.nav__link--open {
  color: #fff;
  background: transparent;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.95),
    0 0 16px rgba(6, 182, 212, 0.8),
    0 0 28px rgba(6, 182, 212, 0.45);
}

.nav__link--btn {
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.88);
  background: transparent;
}

.nav__link--btn:hover {
  background: transparent;
}

.nav__chevron {
  font-size: 10px;
  opacity: 0.75;
}

.nav__dropdown {
  position: relative;
}

/* Bridge hover gap between trigger and panel */
.nav__panel {
  position: absolute;
  top: 100%;
  left: 0;
  padding-top: 6px;
  min-width: 240px;
  z-index: 20;
}

.nav__panel-inner {
  padding: 8px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
}

.nav__panel-inner a {
  padding: 10px 12px;
  font-size: 14px;
  border-radius: 8px;
  color: var(--text-secondary);
  transition: background 0.15s, color 0.15s;
}

.nav__panel-inner a:hover {
  background: var(--bg-page);
  color: var(--text-primary);
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav__sign-in {
  display: none;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(255, 255, 255, 0.45);
  background: transparent;
  transition: text-shadow 0.2s ease, border-color 0.2s ease;
}

.nav__sign-in--solo {
  display: inline;
}

.nav__sign-in:hover {
  color: #fff;
  background: transparent;
  border-color: rgba(255, 255, 255, 0.7);
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.95),
    0 0 16px rgba(6, 182, 212, 0.8);
}

@media (min-width: 900px) {
  .nav__links {
    display: flex;
  }
}
</style>
