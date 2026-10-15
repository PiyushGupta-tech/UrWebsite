<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import BrandLogo from "@/components/BrandLogo.vue";
import { fetchAdminChat, fetchAdminChats } from "@/api/client";
import { useAdminAuth } from "@/composables/useAdminAuth";

const FILTERS = [
  { id: "all", label: "All chats" },
  { id: "leads", label: "Leads" },
  { id: "handoff", label: "Asked for a human" },
];

const router = useRouter();
const { logout } = useAdminAuth();

const filter = ref("all");
const page = ref(1);
const list = ref({ results: [], page: 1, pages: 1, total: 0 });
const listLoading = ref(true);
const listError = ref("");

const selected = ref(null);
const detailLoading = ref(false);
const detailError = ref("");

function formatDateTime(iso) {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

function handleError(err, target) {
  if (err.status === 401) {
    router.replace({ name: "admin-login" });
    return;
  }
  target.value = err.message || "Could not load chats.";
}

async function loadList() {
  listLoading.value = true;
  listError.value = "";
  try {
    list.value = await fetchAdminChats({ filter: filter.value, page: page.value });
    page.value = list.value.page;
  } catch (err) {
    handleError(err, listError);
  } finally {
    listLoading.value = false;
  }
}

async function openChat(id) {
  detailLoading.value = true;
  detailError.value = "";
  try {
    selected.value = await fetchAdminChat(id);
  } catch (err) {
    selected.value = null;
    handleError(err, detailError);
  } finally {
    detailLoading.value = false;
  }
}

function setFilter(id) {
  if (filter.value === id) return;
  filter.value = id;
  page.value = 1;
  selected.value = null;
  loadList();
}

function goToPage(next) {
  page.value = next;
  loadList();
}

async function onLogout() {
  await logout();
  router.push({ name: "admin-login" });
}

onMounted(loadList);
</script>

<template>
  <div class="chats-shell admin-theme">
    <header class="chats-topbar">
      <BrandLogo variant="on-dark" alt="Urbanrupee" priority />
      <h1 class="chats-topbar__title">Website chats</h1>
      <div class="chats-topbar__actions">
        <RouterLink :to="{ name: 'admin-dashboard' }" class="chats-btn">Dashboard</RouterLink>
        <button type="button" class="chats-btn" @click="onLogout">Logout</button>
      </div>
    </header>

    <main class="chats-main">
      <section class="admin-card chats-list" aria-label="Chat list">
        <div class="chats-filters" role="tablist">
          <button
            v-for="f in FILTERS"
            :key="f.id"
            type="button"
            role="tab"
            class="chats-filter"
            :class="{ 'chats-filter--active': filter === f.id }"
            :aria-selected="filter === f.id"
            @click="setFilter(f.id)"
          >
            {{ f.label }}
          </button>
        </div>

        <p v-if="listError" class="chats-error" role="alert">{{ listError }}</p>
        <p v-else-if="listLoading" class="chats-muted">Loading…</p>
        <p v-else-if="!list.results.length" class="chats-muted">No chats yet.</p>

        <ul v-else class="chats-rows">
          <li v-for="row in list.results" :key="row.id">
            <button
              type="button"
              class="chats-row"
              :class="{ 'chats-row--active': selected?.id === row.id }"
              @click="openChat(row.id)"
            >
              <span class="chats-row__top">
                <span class="chats-row__time">{{ formatDateTime(row.updated_at) }}</span>
                <span v-if="row.lead" class="chats-tag" :class="`chats-tag--${row.lead.kind}`">
                  {{ row.lead.kind === "handoff" ? "Human" : "Lead" }}
                </span>
              </span>
              <span class="chats-row__preview">
                {{ row.lead ? `${row.lead.name}: ` : "" }}{{ row.first_message || "(no messages)" }}
              </span>
              <span class="chats-row__meta">
                {{ row.message_count }} message{{ row.message_count === 1 ? "" : "s" }}
                <template v-if="row.page_path"> · {{ row.page_path }}</template>
              </span>
            </button>
          </li>
        </ul>

        <nav v-if="list.pages > 1" class="chats-pager" aria-label="Pages">
          <button type="button" class="chats-btn" :disabled="page <= 1" @click="goToPage(page - 1)">
            Previous
          </button>
          <span class="chats-muted">Page {{ page }} of {{ list.pages }} · {{ list.total }} chats</span>
          <button
            type="button"
            class="chats-btn"
            :disabled="page >= list.pages"
            @click="goToPage(page + 1)"
          >
            Next
          </button>
        </nav>
      </section>

      <section class="admin-card chats-detail" aria-label="Conversation">
        <p v-if="detailError" class="chats-error" role="alert">{{ detailError }}</p>
        <p v-else-if="detailLoading" class="chats-muted">Loading…</p>
        <p v-else-if="!selected" class="chats-muted">Select a chat to read the conversation.</p>
        <template v-else>
          <div class="chats-detail__head">
            <p class="chats-muted">
              Started {{ formatDateTime(selected.started_at) }}
              <template v-if="selected.page_path"> on {{ selected.page_path }}</template>
            </p>
            <dl v-if="selected.lead" class="chats-lead">
              <div>
                <dt>{{ selected.lead.kind === "handoff" ? "Asked for a human" : "Lead" }}</dt>
                <dd>{{ selected.lead.name }}</dd>
              </div>
              <div>
                <dt>Email</dt>
                <dd><a :href="`mailto:${selected.lead.email}`">{{ selected.lead.email }}</a></dd>
              </div>
              <div>
                <dt>Phone</dt>
                <dd><a :href="`tel:+91${selected.lead.phone}`">{{ selected.lead.phone }}</a></dd>
              </div>
              <div v-if="selected.lead.note" class="chats-lead__note">
                <dt>Note</dt>
                <dd>{{ selected.lead.note }}</dd>
              </div>
            </dl>
          </div>

          <ol class="chats-transcript">
            <li
              v-for="(m, i) in selected.messages"
              :key="i"
              class="chats-msg"
              :class="`chats-msg--${m.role}`"
            >
              <span class="chats-msg__who">
                {{ m.role === "user" ? "Visitor" : m.ai_generated ? "Assistant (AI)" : "Assistant (FAQ match)" }}
                · {{ formatDateTime(m.created_at) }}
              </span>
              <p class="chats-msg__text">{{ m.content }}</p>
            </li>
          </ol>
          <p v-if="!selected.messages.length" class="chats-muted">
            The visitor shared their details without chatting.
          </p>
        </template>
      </section>
    </main>
  </div>
</template>

<style scoped>
.chats-shell {
  min-height: 100vh;
  min-height: 100dvh;
  background: #000;
  color: var(--ur-text);
  display: flex;
  flex-direction: column;
}

.chats-topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
  background: var(--btn-primary-gradient);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.chats-topbar__title {
  flex: 1;
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}

.chats-topbar__actions {
  display: flex;
  gap: 8px;
}

.chats-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: var(--ur-text);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.chats-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
}

.chats-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.chats-main {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(280px, 380px) minmax(0, 1fr);
  gap: 12px;
  padding: 12px 16px 16px;
  min-height: 0;
}

.chats-list,
.chats-detail {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
  max-height: calc(100dvh - 90px);
  overflow: auto;
}

.chats-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chats-filter {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--ur-card-border);
  background: var(--ur-surface-raised);
  color: var(--ur-muted);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.chats-filter--active {
  color: var(--ur-text);
  border-color: var(--ur-accent);
}

.chats-rows {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chats-row {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--ur-card-border);
  background: var(--ur-surface-raised);
  color: var(--ur-text);
  text-align: left;
  cursor: pointer;
}

.chats-row--active,
.chats-row:hover {
  border-color: var(--ur-accent);
}

.chats-row__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.chats-row__time,
.chats-row__meta,
.chats-muted {
  margin: 0;
  font-size: 12px;
  color: var(--ur-muted);
}

.chats-row__preview {
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chats-tag {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}

.chats-tag--lead {
  background: rgba(34, 197, 94, 0.15);
  color: var(--ur-success);
}

.chats-tag--handoff {
  background: rgba(234, 179, 8, 0.15);
  color: var(--ur-warning);
}

.chats-pager {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: auto;
}

.chats-error {
  margin: 0;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(255, 51, 102, 0.12);
  color: var(--ur-danger);
  font-size: 13px;
}

.chats-detail__head {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--ur-card-border);
}

.chats-lead {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 8px 16px;
  margin: 0;
}

.chats-lead dt {
  font-size: 11px;
  color: var(--ur-muted);
}

.chats-lead dd {
  margin: 2px 0 0;
  font-size: 14px;
  overflow-wrap: anywhere;
}

.chats-lead a {
  color: var(--ur-text);
}

.chats-lead__note {
  grid-column: 1 / -1;
}

.chats-transcript {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chats-msg {
  max-width: 85%;
  padding: 10px 12px;
  border-radius: 12px;
  background: var(--ur-surface-raised);
  border: 1px solid var(--ur-card-border);
}

.chats-msg--user {
  align-self: flex-end;
  background: #0c2a3a;
}

.chats-msg__who {
  display: block;
  margin-bottom: 4px;
  font-size: 11px;
  color: var(--ur-muted);
}

.chats-msg__text {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

@media (max-width: 900px) {
  .chats-main {
    grid-template-columns: 1fr;
  }

  .chats-list,
  .chats-detail {
    max-height: none;
  }
}
</style>
