import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "@/layouts/AppLayout.vue";
import { fetchAdminMe } from "@/api/client";
import { disableScrollRestore } from "@/utils/scrollRestoration.js";

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
        path: "services/collections",
        name: "collections",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "collections" },
      },
      {
        path: "services/payouts",
        name: "payouts",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "payouts" },
      },
      {
        path: "services/financial-operations",
        name: "financial-operations",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "financial-operations" },
      },
      {
        path: "services/risk-fraud-management",
        name: "risk-fraud-management",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "risk-fraud-management" },
      },
      {
        path: "services/reconciliation",
        name: "reconciliation",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "reconciliation" },
      },
      {
        path: "services/payment",
        redirect: { name: "collections" },
      },
      {
        path: "products/collections",
        redirect: { name: "collections" },
      },
      {
        path: "services/aml",
        redirect: { name: "risk-fraud-management" },
      },
      {
        path: "products/payout",
        redirect: { name: "payouts" },
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
        path: "products/unified-dashboard",
        name: "unified-dashboard",
        component: () => import("@/views/PageView.vue"),
        meta: { slug: "unified-dashboard" },
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
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return { el: to.hash, top: 96 };
    }
    // Full page load / refresh — don't force top; manual restore runs after content paints.
    if (!from.matched.length) {
      return false;
    }
    // In-app link navigation — start at top.
    disableScrollRestore();
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
