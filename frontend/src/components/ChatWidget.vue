<script setup>
import { nextTick, ref } from "vue";
import { submitChat } from "@/api/client";
import { LOGO_PATHS } from "@/constants/logos";

const open = ref(false);
const input = ref("");
const loading = ref(false);
const messages = ref([
  {
    role: "bot",
    text: "Hi! Ask me about Urbanrupee: products, services, security, or how to get started.",
    sources: [],
  },
]);

const suggestions = [
  "What is Urbanrupee?",
  "Is Urbanrupee a payment gateway?",
  "What is payment orchestration?",
];

const panelRef = ref(null);
const listRef = ref(null);

function toggle() {
  open.value = !open.value;
}

async function scrollToBottom() {
  await nextTick();
  if (listRef.value) {
    listRef.value.scrollTop = listRef.value.scrollHeight;
  }
}

async function send(text) {
  const message = (text ?? input.value).trim();
  if (!message || loading.value) return;

  messages.value.push({ role: "user", text: message });
  input.value = "";
  loading.value = true;
  await scrollToBottom();

  try {
    const data = await submitChat(message);
    messages.value.push({
      role: "bot",
      text: data.reply,
      sources: data.sources || [],
    });
  } catch {
    messages.value.push({
      role: "bot",
      text: "Something went wrong. Please try again or contact us on the website.",
      sources: [{ title: "Contact Us", href: "/contact" }],
    });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
}

function onKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
}
</script>

<template>
  <div class="chat-widget" :class="{ 'chat-widget--open': open }">
    <div v-if="open" ref="panelRef" class="chat-widget__panel" role="dialog" aria-label="Urbanrupee assistant">
      <header class="chat-widget__header">
        <div>
          <p class="chat-widget__title">Urbanrupee Assistant</p>
        </div>
        <button type="button" class="chat-widget__close" aria-label="Close chat" @click="toggle">
          ×
        </button>
      </header>

      <div ref="listRef" class="chat-widget__messages">
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="chat-widget__msg"
          :class="`chat-widget__msg--${msg.role}`"
        >
          <p class="chat-widget__bubble">{{ msg.text }}</p>
          <ul v-if="msg.sources?.length" class="chat-widget__sources">
            <li v-for="(src, j) in msg.sources" :key="j">
              <RouterLink :to="src.href">{{ src.title }}</RouterLink>
            </li>
          </ul>
        </div>
        <p v-if="loading" class="chat-widget__typing">Thinking…</p>
      </div>

      <div v-if="messages.length === 1" class="chat-widget__suggestions">
        <button
          v-for="(q, i) in suggestions"
          :key="i"
          type="button"
          class="chat-widget__chip"
          @click="send(q)"
        >
          {{ q }}
        </button>
      </div>

      <form class="chat-widget__form" @submit.prevent="send()">
        <input
          v-model="input"
          type="text"
          class="chat-widget__input"
          placeholder="Ask a question…"
          maxlength="500"
          autocomplete="off"
          :disabled="loading"
          @keydown="onKeydown"
        />
        <button type="submit" class="chat-widget__send" :disabled="loading || !input.trim()">
          Send
        </button>
      </form>
    </div>

    <button
      type="button"
      class="chat-widget__launcher"
      :aria-expanded="open"
      aria-label="Open chat assistant"
      @click="toggle"
    >
      <img
        v-if="!open"
        :src="LOGO_PATHS.chatBot"
        alt=""
        width="29"
        height="29"
        class="chat-widget__launcher-logo"
      />
      <span v-else class="chat-widget__launcher-icon" aria-hidden="true">↓</span>
    </button>
  </div>
</template>

<style scoped>
.chat-widget {
  position: fixed;
  right: 20px;
  bottom: calc(20px + var(--ur-sticky-cta, 0px));
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
  font-family: var(--font);
}

.chat-widget__panel {
  width: min(380px, calc(100vw - 40px));
  height: min(520px, calc(100vh - 120px));
  display: flex;
  flex-direction: column;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  animation: chat-slide-up 0.2s ease-out;
}

@keyframes chat-slide-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-widget__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 16px 12px;
  background: var(--btn-primary-gradient);
  color: var(--btn-primary-text);
}

.chat-widget__title {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.chat-widget__close {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  min-width: 44px;
  min-height: 44px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  color: inherit;
  font-size: 22px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-widget__close:hover {
  background: rgba(255, 255, 255, 0.25);
}

.chat-widget__messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-widget__msg--user {
  align-self: flex-end;
  max-width: 88%;
}

.chat-widget__msg--bot {
  align-self: flex-start;
  max-width: 95%;
}

.chat-widget__bubble {
  margin: 0;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.5;
}

.chat-widget__msg--user .chat-widget__bubble {
  background: var(--accent-blue);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-widget__msg--bot .chat-widget__bubble {
  background: var(--bg-muted);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

.chat-widget__sources {
  margin: 6px 0 0;
  padding: 0;
  list-style: none;
  font-size: 12px;
}

.chat-widget__sources a {
  color: var(--accent-blue);
  text-decoration: underline;
}

.chat-widget__typing {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

.chat-widget__suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 16px 8px;
}

.chat-widget__chip {
  padding: 12px 14px;
  min-height: 44px;
  font-size: 13px;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--text-secondary);
}

.chat-widget__chip:hover {
  border-color: var(--accent-blue);
  color: var(--accent-blue);
}

.chat-widget__form {
  display: flex;
  gap: 8px;
  padding: 12px 16px 16px;
  border-top: 1px solid var(--border);
}

.chat-widget__input {
  flex: 1;
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
}

.chat-widget__input:focus {
  outline: none;
  border-color: var(--accent-blue);
}

.chat-widget__send {
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  background: var(--btn-primary-bg);
  color: var(--btn-primary-text);
  font-size: 14px;
  font-weight: 600;
}

.chat-widget__send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-widget__launcher {
  width: 56px;
  height: 56px;
  border: none;
  border-radius: 50%;
  background: #06b6d4;
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-widget__launcher:hover {
  transform: scale(1.04);
}

.chat-widget__launcher-logo {
  width: 29px;
  height: 29px;
  object-fit: contain;
  display: block;
}

.chat-widget__launcher-icon {
  font-size: 22px;
  font-weight: 700;
  line-height: 1;
  color: #000;
}

@media (max-width: 480px) {
  .chat-widget {
    right: 12px;
    bottom: calc(12px + var(--ur-sticky-cta, 0px));
  }
}
</style>
