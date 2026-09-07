import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "@/layouts/AppLayout.vue";
import { fetchAdminMe } from "@/api/client";

const routes = [
  {
    path: "/admin",
    name: "admin-login",
    component: () => import("@/views/admin/AdminLoginView.vue"),
    meta: { adminGuest: true },
  },
  {
    path: "/admin/dashboard",
    name: "admin-dashboard",
    component: () => import("@/views/admin/AdminDashboardView.vue"),
    meta: { requiresAdmin: true },
  },
  {
    path: "/",
    component: AppLayout,
    children: [
      {
        path: "",
        name: "home",
        component: () => import("@/views/HomeView.vue"),
      },
      {
        path: "about",
        name: "about",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "about" },
      },
      {
        path: "services/payment",
        name: "payment-services",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "payment-services" },
      },
      {
        path: "services/aml",
        name: "aml-detector",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "aml-detector" },
      },
      {
        path: "services/reconciliation",
        name: "automatic-reconciliation",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "automatic-reconciliation" },
      },
      {
        path: "products",
        name: "products",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "products-index" },
      },
      {
        path: "resources",
        name: "resources",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "resources-index" },
      },
      {
        path: "products/white-label",
        name: "white-label",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "white-label-platform" },
      },
      {
        path: "products/custom-checkout",
        name: "custom-checkout",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "custom-checkout" },
      },
      {
        path: "products/hyper-checkout",
        name: "hyper-checkout",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "hyper-checkout" },
      },
      {
        path: "products/orchestration",
        name: "orchestration",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "payment-orchestration" },
      },
      {
        path: "products/upi-switch",
        name: "upi-switch",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "upi-switch" },
      },
      {
        path: "products/affordability",
        name: "affordability",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "affordability" },
      },
      {
        path: "products/payout",
        name: "payout-portal",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "payout-portal" },
      },
      {
        path: "products/wallet",
        name: "close-route-wallet",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "close-route-wallet" },
      },
      {
        path: "faq",
        name: "faq",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "faq" },
      },
      {
        path: "blog",
        name: "blog",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "blog" },
      },
      {
        path: "privacy-policy",
        name: "privacy-policy",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "privacy-policy" },
      },
      {
        path: "terms-and-conditions",
        name: "terms-and-conditions",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "terms-and-conditions" },
      },
      {
        path: "contact",
        name: "contact",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "contact" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

async function isAdminAuthenticated() {
  try {
    const data = await fetchAdminMe();
    return Boolean(data.authenticated);
  } catch {
    return false;
  }
}

router.beforeEach(async (to) => {
  if (!to.meta.requiresAdmin && !to.meta.adminGuest) return true;

  const authed = await isAdminAuthenticated();
  if (to.meta.requiresAdmin && !authed) {
    return { name: "admin-login" };
  }
  if (to.meta.adminGuest && authed) {
    return { name: "admin-dashboard" };
  }
  return true;
});

export default router;
