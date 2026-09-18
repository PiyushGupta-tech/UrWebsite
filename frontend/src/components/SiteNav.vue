<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

defineProps({
  nav: { type: Object, required: true },
  site: { type: Object, required: true },
});

const route = useRoute();
const openMenu = ref(null);
const mobileOpen = ref(false);
/** 0 at page top → 1 after scrolling one viewport */
const compact = ref(0);
/** Mobile only: hide chrome while scrolling down */
const navHidden = ref(false);

const ctaTo = computed(() =>
  route.path === "/contact" ? { path: "/contact", hash: "#contact-form" } : "/contact",
);

const navStyle = computed(() => ({
  "--nav-compact": String(compact.value),
}));

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
  else navHidden.value = false;
}

let raf = 0;
let reduceMotion = false;
let lastScrollY = 0;
/** Phone only — tablet keeps the Figma full bar */
const MOBILE_NAV_MAX = 700;
const SCROLL_DELTA = 6;
const TOP_REVEAL = 16;

function isMobileNav() {
  return window.innerWidth <= MOBILE_NAV_MAX;
}

function updateNavChrome() {
  raf = 0;
  const y = Math.max(window.scrollY, 0);

  if (!isMobileNav()) {
    navHidden.value = false;
    if (reduceMotion) {
      compact.value = 0;
    } else {
      const vh = Math.max(window.innerHeight, 1);
      compact.value = Math.min(Math.max(y / vh, 0), 1);
    }
    lastScrollY = y;
    return;
  }

  compact.value = 0;

  if (reduceMotion || mobileOpen.value) {
    navHidden.value = false;
    lastScrollY = y;
    return;
  }

  const delta = y - lastScrollY;
  if (y <= TOP_REVEAL) {
    navHidden.value = false;
  } else if (delta > SCROLL_DELTA) {
    navHidden.value = true;
  } else if (delta < -SCROLL_DELTA) {
    navHidden.value = false;
  }

  lastScrollY = y;
}

function onScrollOrResize() {
  if (raf) return;
  raf = requestAnimationFrame(updateNavChrome);
}

onMounted(() => {
  reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  lastScrollY = Math.max(window.scrollY, 0);
  updateNavChrome();
  window.addEventListener("scroll", onScrollOrResize, { passive: true });
  window.addEventListener("resize", onScrollOrResize, { passive: true });
});

onUnmounted(() => {
  window.removeEventListener("scroll", onScrollOrResize);
  window.removeEventListener("resize", onScrollOrResize);
  if (raf) cancelAnimationFrame(raf);
});
</script>

<template>
  <!-- Figma Frame 2147225433 — 1146×89 @ (147, 40); logo → links → CTA gaps 175px -->
  <header
    class="nav"
    :class="{
      'nav--compact': compact >= 0.5,
      'nav--hidden': navHidden,
    }"
    :style="navStyle"
  >
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
            <div
              v-show="openMenu === 'solutions'"
              class="nav__panel nav__panel--solutions"
            >
              <div class="nav__panel-inner nav__panel-inner--mega">
                <div class="nav__mega-col">
                  <p class="nav__panel-label">Products</p>
                  <div class="nav__mega-list">
                    <RouterLink
                      v-for="item in nav.products"
                      :key="item.href"
                      :to="item.href"
                      class="nav__mega-item"
                      @click="closeMenus"
                    >
                      <span>{{ item.label }}</span>
                      <img
                        class="nav__mega-arrow"
                        src="/images/figma-nav/item-arrow.svg"
                        alt=""
                        width="12"
                        height="12"
                        decoding="async"
                      />
                    </RouterLink>
                  </div>
                </div>
                <div class="nav__mega-col nav__mega-col--services">
                  <p class="nav__panel-label">Services</p>
                  <div class="nav__mega-list">
                    <RouterLink
                      v-for="item in nav.services"
                      :key="item.href"
                      :to="item.href"
                      class="nav__mega-item"
                      @click="closeMenus"
                    >
                      <span>{{ item.label }}</span>
                      <img
                        class="nav__mega-arrow"
                        src="/images/figma-nav/item-arrow.svg"
                        alt=""
                        width="12"
                        height="12"
                        decoding="async"
                      />
                    </RouterLink>
                  </div>
                </div>
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
              <img
                class="nav__chevron"
                src="/images/figma-contact/nav-chevron.svg"
                alt=""
                width="24"
                height="24"
                decoding="async"
              />
            </button>
            <div
              v-show="openMenu === 'resources'"
              class="nav__panel nav__panel--resources"
            >
              <div class="nav__panel-inner nav__panel-inner--list">
                <div class="nav__mega-list">
                  <RouterLink
                    v-for="item in nav.resources"
                    :key="item.href"
                    :to="item.href"
                    class="nav__mega-item"
                    @click="closeMenus"
                  >
                    <span>{{ item.label }}</span>
                    <img
                      class="nav__mega-arrow"
                      src="/images/figma-nav/item-arrow.svg"
                      alt=""
                      width="12"
                      height="12"
                      decoding="async"
                    />
                  </RouterLink>
                </div>
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
            <span class="nav__cta-label">Talk to an Expert</span>
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
  --nav-compact: 0;
  --nav-pad-top: 40px;
  --nav-shrink: calc(1 - (var(--nav-compact) * 0.3));
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
  padding: calc(var(--nav-pad-top) * var(--nav-shrink)) 147px 0;
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
  transform: scale(var(--nav-shrink));
  transform-origin: top center;
  will-change: transform;
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
  font-weight: 700;
  line-height: normal;
  color: #052201;
  background: transparent;
  border-radius: 0;
  text-decoration: none;
  white-space: nowrap;
  transition:
    color 0.15s ease,
    font-weight 0.2s ease;
}

.nav--compact .nav__link,
.nav--compact .nav__link--btn {
  font-weight: 700;
}

.nav__link.router-link-exact-active,
.nav__link--contact.router-link-active,
.nav__link--contact.router-link-exact-active,
.nav--compact .nav__link.router-link-exact-active,
.nav--compact .nav__link--contact.router-link-active,
.nav--compact .nav__link--contact.router-link-exact-active {
  font-weight: 800;
}

.nav__link:hover,
.nav__link.router-link-exact-active,
.nav__link--btn.nav__link--open {
  color: #097495;
  background: transparent;
  text-shadow: none;
}

.nav__link--contact {
  color: #052201;
}

.nav__link--contact.router-link-active,
.nav__link--contact.router-link-exact-active {
  color: #097495;
}

.nav__link--btn {
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0;
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  font-weight: 700;
  line-height: inherit;
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
  z-index: 20;
}

.nav__panel--solutions {
  left: 50%;
  min-width: 582px;
}

.nav__panel--resources {
  min-width: 240px;
}

.nav__panel-inner {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
  overflow: hidden;
}

/* Figma 466:32322 / 466:32350 — 582×221, pad 16, Products | Services */
.nav__panel-inner--mega {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 582px;
  max-width: min(582px, calc(100vw - 32px));
  padding: 16px;
  box-sizing: border-box;
}

.nav__panel-inner--list {
  padding: 16px;
  min-width: 220px;
}

.nav__mega-col {
  width: 243px;
  flex-shrink: 0;
}

.nav__mega-col--services {
  width: 258px;
}

.nav__panel-label {
  margin: 0 0 8px;
  padding: 0 8px 0 10px;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 12px;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0;
  text-transform: none;
  color: #535862;
}

.nav__mega-col--services .nav__panel-label {
  padding-left: 8px;
}

.nav__mega-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
  width: 100%;
}

.nav__mega-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
  max-width: 100%;
  padding: 6px 8px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 0.5px solid transparent;
  font-family: Manrope, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  color: #252b37;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.nav__mega-item span {
  min-width: 0;
}

.nav__mega-arrow {
  display: none;
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  transform: rotate(90deg);
}

.nav__mega-item:hover,
.nav__mega-item:focus-visible,
.nav__mega-item.router-link-active {
  background: #097495;
  border-color: rgba(213, 215, 218, 0.2);
  color: #ffffff;
}

.nav__mega-item:hover .nav__mega-arrow,
.nav__mega-item:focus-visible .nav__mega-arrow,
.nav__mega-item.router-link-active .nav__mega-arrow {
  display: block;
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
  width: auto;
  min-width: 155px;
  height: 52px;
  padding: 0 16px;
  box-sizing: border-box;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  line-height: 1;
  text-align: center;
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}

.nav__cta:hover {
  opacity: 0.92;
  color: #ffffff;
}

.nav__cta-label {
  display: inline-flex;
  align-items: center;
  line-height: 1;
}

.nav__cta-arrow {
  display: block;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  align-self: center;
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

/* Desktop + tablet: inline links (Figma iPad keeps full bar) */
@media (min-width: 701px) {
  .nav__links {
    display: flex;
  }
}

@media (max-width: 1280px) and (min-width: 1201px) {
  .nav {
    --nav-pad-top: 24px;
  }

  .nav__shell {
    padding-left: 40px;
    padding-right: 40px;
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

/* Tablet: Figma 208:6003 — 752×58 bar, full links, no hamburger */
@media (min-width: 701px) and (max-width: 1200px) {
  .nav {
    --nav-pad-top: 24px;
    --nav-shrink: 1;
  }

  .nav__shell {
    padding-left: max(40px, calc((100% - 752px) / 2));
    padding-right: max(40px, calc((100% - 752px) / 2));
  }

  .nav-spacer {
    height: 82px;
  }

  .nav__bar {
    max-width: min(752px, 100%);
    height: 58px;
    padding: 10.5px 17px;
    justify-content: space-between;
    gap: clamp(24px, 6vw, 114px);
    border-radius: 5.531px;
    /* Keep ≥1px teal stroke — Figma's 0.46px white vanishes when scaled down */
    border: 1px solid rgba(9, 116, 149, 0.18);
    box-shadow: none;
    transform: none;
    will-change: auto;
  }

  .nav__logo-img {
    width: 132px;
    max-height: 25px;
  }

  .nav__links {
    gap: 23px;
    flex: 0 0 auto;
    justify-content: center;
  }

  .nav__link,
  .nav__link--btn {
    font-size: 10.5px;
  }

  .nav__chevron {
    width: 16px;
    height: 16px;
  }

  .nav__cta {
    width: auto;
    min-width: 101px;
    height: 34px;
    padding: 0 10px;
    gap: 2.6px;
    border-radius: 5.25px;
    font-size: 10.5px;
    letter-spacing: -0.21px;
  }

  .nav__cta-arrow {
    width: 12px;
    height: 12px;
  }

  .nav__menu-btn {
    display: none;
  }
}

/* Phone: hamburger + hide-on-scroll */
@media (max-width: 700px) {
  .nav {
    --nav-pad-top: 16px;
    transition: transform 0.42s cubic-bezier(0.22, 1, 0.36, 1);
    will-change: transform;
  }

  .nav--hidden {
    transform: translate3d(0, calc(-100% - 12px), 0);
  }

  .nav__shell {
    padding-left: 16px;
    padding-right: 16px;
  }

  .nav-spacer {
    height: 88px;
  }

  .nav__bar {
    gap: 16px;
    height: auto;
    min-height: 64px;
    padding: 12px 16px;
    position: relative;
    transform: none;
    will-change: auto;
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
    font-size: 16px;
  }

  .nav__panel {
    position: static;
    transform: none;
    padding-top: 4px;
    min-width: 0;
  }

  .nav__panel--solutions {
    min-width: 0;
  }

  .nav__panel-inner--mega {
    width: 100%;
    max-width: none;
    flex-direction: column;
    gap: 16px;
  }

  .nav__mega-col,
  .nav__mega-col--services {
    width: 100%;
  }

  .nav__mega-item {
    width: 100%;
    white-space: normal;
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

@media (prefers-reduced-motion: reduce) {
  .nav {
    transition: none;
  }
}

@media (max-width: 480px) {
  .nav__shell {
    padding-left: 12px;
    padding-right: 12px;
  }

  .nav__bar {
    gap: 10px;
    padding: 10px 12px;
  }

  .nav__logo-img {
    width: 136px;
    max-height: 28px;
  }

  .nav__actions {
    gap: 8px;
  }

  .nav__cta {
    display: none;
  }

  .nav__menu-btn {
    width: 36px;
    height: 36px;
  }

  .nav__links {
    padding: 10px;
  }

  .nav__mega-item {
    font-size: 13px;
    padding: 8px;
  }
}
</style>
