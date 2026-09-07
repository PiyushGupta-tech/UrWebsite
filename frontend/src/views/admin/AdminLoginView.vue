<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import BrandLogo from "@/components/BrandLogo.vue";
import { useAdminAuth } from "@/composables/useAdminAuth";

const router = useRouter();
const { authenticated, loading, refresh, login } = useAdminAuth();

const username = ref("");
const password = ref("");
const showPassword = ref(false);
const error = ref("");
const submitting = ref(false);

onMounted(async () => {
  await refresh();
  if (authenticated.value) {
    router.replace({ name: "admin-dashboard" });
  }
});

async function onSubmit() {
  error.value = "";
  submitting.value = true;
  try {
    await login(username.value.trim(), password.value);
    router.push({ name: "admin-dashboard" });
  } catch (err) {
    error.value = err.status === 401 ? "Invalid credentials." : err.message || "Login failed.";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="admin-login admin-theme">
    <form class="admin-login__card admin-card" @submit.prevent="onSubmit">
      <div class="admin-login__brand">
        <BrandLogo variant="on-dark" alt="Urbanrupee" priority class="admin-login__logo" />
        <div>
          <p class="admin-login__name">Urbanrupee</p>
          <p class="admin-login__subtitle">Admin Dashboard</p>
        </div>
      </div>

      <h1 class="admin-login__title">Sign in</h1>
      <p class="admin-login__hint">Internal read-only payout dashboard</p>

      <label class="admin-login__field">
        <span>Username</span>
        <input v-model="username" type="text" autocomplete="username" required />
      </label>

      <label class="admin-login__field">
        <span>Password</span>
        <div class="admin-login__password-wrap">
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            required
          />
          <button
            type="button"
            class="admin-login__toggle"
            :aria-label="showPassword ? 'Hide password' : 'Show password'"
            :aria-pressed="showPassword"
            @click="showPassword = !showPassword"
          >
            <svg
              v-if="showPassword"
              viewBox="0 0 24 24"
              width="18"
              height="18"
              aria-hidden="true"
            >
              <path
                fill="currentColor"
                d="M12 6.5c3.79 0 7.17 2.13 8.82 5.5-1.65 3.37-5.03 5.5-8.82 5.5S4.83 15.37 3.18 12C4.83 8.63 8.21 6.5 12 6.5m0-2C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5C20.27 7.61 17 4.5 12 4.5zm0 5a2.5 2.5 0 0 1 0 5 2.5 2.5 0 0 1 0-5z"
              />
            </svg>
            <svg
              v-else
              viewBox="0 0 24 24"
              width="18"
              height="18"
              aria-hidden="true"
            >
              <path
                fill="currentColor"
                d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78 3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"
              />
            </svg>
          </button>
        </div>
      </label>

      <p v-if="error" class="admin-login__error" role="alert">{{ error }}</p>

      <button type="submit" class="admin-login__submit" :disabled="submitting || loading">
        {{ submitting ? "Signing in…" : "Sign in" }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #000;
}

.admin-login__card {
  width: min(100%, 420px);
  padding: 28px;
}

.admin-login__brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.admin-login__logo {
  height: 28px;
  width: auto;
  flex-shrink: 0;
}

.admin-login__name {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--ur-text);
}

.admin-login__subtitle {
  margin: 0;
  font-size: 12px;
  color: var(--ur-accent);
}

.admin-login__title {
  margin: 0 0 6px;
  font-size: 24px;
  color: var(--ur-text);
}

.admin-login__hint {
  margin: 0 0 20px;
  font-size: 13px;
  color: var(--ur-muted);
}

.admin-login__field {
  display: grid;
  gap: 6px;
  margin-bottom: 14px;
  font-size: 12px;
  color: var(--ur-muted);
}

.admin-login__field input {
  width: 100%;
  padding: 11px 12px;
  border-radius: 10px;
  border: 1px solid var(--ur-card-border);
  background: #0f1a1c;
  color: var(--ur-text);
}

.admin-login__password-wrap {
  position: relative;
}

.admin-login__password-wrap input {
  padding-right: 42px;
}

.admin-login__toggle {
  position: absolute;
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--ur-muted);
  cursor: pointer;
}

.admin-login__toggle:hover {
  color: var(--ur-text);
  background: rgba(255, 255, 255, 0.08);
}

.admin-login__toggle:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.25);
  outline-offset: 2px;
}

.admin-login__field input:focus {
  outline: 2px solid rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
}

.admin-login__error {
  margin: 0 0 12px;
  font-size: 13px;
  color: var(--ur-danger);
}

.admin-login__submit {
  width: 100%;
  margin-top: 8px;
  padding: 12px 14px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #1a3a7a, #2563eb);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.admin-login__submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style>
