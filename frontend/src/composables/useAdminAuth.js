import { ref } from "vue";
import { adminLogin, adminLogout, fetchAdminMe } from "@/api/client";

export function useAdminAuth() {
  const authenticated = ref(false);
  const loading = ref(true);

  async function refresh() {
    loading.value = true;
    try {
      const data = await fetchAdminMe();
      authenticated.value = Boolean(data.authenticated);
      return authenticated.value;
    } catch {
      authenticated.value = false;
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function login(username, password) {
    await adminLogin(username, password);
    authenticated.value = true;
  }

  async function logout() {
    try {
      await adminLogout();
    } finally {
      authenticated.value = false;
    }
  }

  return { authenticated, loading, refresh, login, logout };
}
