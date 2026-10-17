<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { streamChat } from "@/api/client";
import { CHAT_LANGUAGES, DEFAULT_CHAT_LANGUAGE, findChatLanguage } from "@/constants/chatLanguages";
import { LOGO_PATHS } from "@/constants/logos";

const STORAGE_KEY = "ur-chat-v1";
const LANGUAGE_KEY = "ur-chat-lang";
const MAX_STORED_MESSAGES = 40;
// Mirrors the server-side redaction of 12–19 digit card/account numbers. No lookbehind:
// older Safari cannot parse it and this module ships on every page.
const LONG_NUMBER_RE = /(^|\D)\d(?:[ -]?\d){11,18}(?!\d)/g;

function redactNumbers(text) {
  return text.replace(LONG_NUMBER_RE, (_match, before) => `${before}[number removed]`);
}

const MAX_FOLLOWUPS = 3;

function cleanSuggestions(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter((q) => typeof q === "string" && q.trim() && q.length <= 120)
    .map((q) => q.trim())
    .slice(0, MAX_FOLLOWUPS);
}

function loadLanguage() {
  try {
    return findChatLanguage(localStorage.getItem(LANGUAGE_KEY)).code;
  } catch {
    return DEFAULT_CHAT_LANGUAGE;
  }
}

const route = useRoute();
const router = useRouter();
const open = ref(false);
const input = ref("");
const loading = ref(false);
const listRef = ref(null);
const inputRef = ref(null);
let nextId = 1;
let controller = null;

const conversationId = ref("");
const limitReached = ref(false);
const messages = ref([]);

const language = ref(loadLanguage());
const currentLanguage = computed(() => findChatLanguage(language.value));
const langOpen = ref(false);
const langActive = ref(0);
const langPickerRef = ref(null);
const langButtonRef = ref(null);
const langOptionRefs = [];

function greeting() {
  return { id: nextId++, role: "bot", text: currentLanguage.value.greeting, sources: [] };
}

function restore() {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "null");
    if (saved && Array.isArray(saved.messages) && saved.messages.length) {
      conversationId.value = String(saved.conversationId || "");
      messages.value = saved.messages
        .filter((m) => (m.role === "user" || m.role === "bot") && typeof m.text === "string")
        .map((m) => ({
          id: nextId++,
          role: m.role,
          text: redactNumbers(m.text),
          sources: Array.isArray(m.sources) ? m.sources : [],
          suggestions: m.role === "bot" ? cleanSuggestions(m.suggestions) : [],
        }));
      persist();
      return;
    }
  } catch {
    /* storage unavailable or corrupt: start fresh */
  }
  messages.value = [greeting()];
}

function persist() {
  try {
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        conversationId: conversationId.value,
        messages: messages.value
          .filter((m) => !m.streaming && m.role !== "notice")
          .slice(-MAX_STORED_MESSAGES)
          .map(({ role, text, sources, suggestions }) => ({
            role,
            text: redactNumbers(text),
            sources,
            ...(suggestions?.length ? { suggestions } : {}),
          })),
      }),
    );
  } catch {
    /* storage full or blocked: chat still works for this page view */
  }
}

restore();

const hasUserMessages = computed(() => messages.value.some((m) => m.role === "user"));
// Follow-up chips only show under the latest reply, so older ones never pile up.
const latestBotId = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i -= 1) {
    if (messages.value[i].role === "bot") return messages.value[i].id;
  }
  return null;
});

function displayText(text) {
  return text.replace(/\*\*/g, "").replace(/^#{1,6}\s+/gm, "").trim();
}

// Typewriter reveal: the hidden backlog shrinks exponentially (time constant REVEAL_TAU_MS) but
// never slower than REVEAL_MIN_CPS, so the text keeps pace with the stream and long fallback
// answers still land in well under a second.
const REVEAL_TAU_MS = 90;
const REVEAL_MIN_CPS = 180;
const COMBINING_RE = /[\p{M}\u200c\u200d\ufe0f]/u;
const reduceMotion =
  typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
// Frames can be throttled in unfocused windows, so a short timer backs up each animation frame.
const REVEAL_BACKUP_MS = 50;
const revealing = ref(false);
let revealMsg = null;
let revealFrame = 0;
let revealTimer = 0;
let revealLast = 0;

function bubbleText(msg) {
  const full = msg.role === "bot" ? displayText(msg.text) : msg.text;
  return msg.revealing ? full.slice(0, msg.shown) : full;
}

// Never cut inside a surrogate pair or before a combining mark (Indic vowel signs, viramas).
function clusterEnd(text, index) {
  let end = Math.min(index, text.length);
  while (end < text.length) {
    const code = text.charCodeAt(end);
    if ((code >= 0xdc00 && code <= 0xdfff) || COMBINING_RE.test(text[end])) end += 1;
    else break;
  }
  return end;
}

function startReveal(msg) {
  finishReveal();
  if (reduceMotion) return;
  msg.shown = 0;
  msg.revealing = true;
  revealMsg = msg;
  revealing.value = true;
}

function cancelRevealTick() {
  if (revealFrame) cancelAnimationFrame(revealFrame);
  if (revealTimer) clearTimeout(revealTimer);
  revealFrame = 0;
  revealTimer = 0;
}

function scheduleRevealTick() {
  const run = () => {
    cancelRevealTick();
    pumpReveal(performance.now());
  };
  revealFrame = requestAnimationFrame(run);
  revealTimer = setTimeout(run, REVEAL_BACKUP_MS);
}

function finishReveal() {
  cancelRevealTick();
  revealLast = 0;
  if (revealMsg) {
    revealMsg.revealing = false;
    if (revealMsg.text.trim()) revealMsg.shine = true;
  }
  revealMsg = null;
  revealing.value = false;
}

function kickReveal() {
  if (revealMsg && !revealFrame) scheduleRevealTick();
}

function pumpReveal(now) {
  const msg = revealMsg;
  if (!msg) return;
  const full = displayText(msg.text);
  const dt = revealLast ? Math.min(now - revealLast, 100) : 16;
  const backlog = full.length - msg.shown;
  if (backlog > 0) {
    const step = Math.max((REVEAL_MIN_CPS * dt) / 1000, backlog * (1 - Math.exp(-dt / REVEAL_TAU_MS)));
    msg.shown = clusterEnd(full, msg.shown + Math.ceil(step));
    followScroll();
  }
  if (msg.shown < full.length) {
    revealLast = now;
    scheduleRevealTick();
  } else if (!msg.streaming) {
    finishReveal();
    scrollToBottom();
  } else {
    revealLast = 0;
  }
}

// Keep the newest text in view without pulling a visitor back down while they read history.
function followScroll() {
  const el = listRef.value;
  if (el && el.scrollHeight - el.scrollTop - el.clientHeight < 120) {
    nextTick(() => {
      el.scrollTop = el.scrollHeight;
    });
  }
}

function clearFresh(msg, e) {
  if (e.target === e.currentTarget) msg.fresh = false;
}

function clearShine(msg, e) {
  if (e.target === e.currentTarget) msg.shine = false;
}

function toggle() {
  open.value = !open.value;
  langOpen.value = false;
  if (open.value) {
    scrollToBottom();
    nextTick(() => inputRef.value?.focus());
  }
}

function closeOnNavigate(e) {
  // Modified clicks open a new tab, so the visitor is still on this page.
  if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  langOpen.value = false;
  open.value = false;
}

/** Close the chat and open Contact Us so the visitor fills the website form. */
function goToContact() {
  langOpen.value = false;
  open.value = false;
  if (route.path === "/contact") return;
  router.push({ name: "contact" }).catch(() => {
    window.location.assign("/contact");
  });
}

function focusLangOption(index) {
  const count = CHAT_LANGUAGES.length;
  langActive.value = (index + count) % count;
  langOptionRefs[langActive.value]?.focus();
}

function openLangMenu() {
  langOpen.value = true;
  nextTick(() =>
    focusLangOption(Math.max(0, CHAT_LANGUAGES.findIndex((l) => l.code === language.value))),
  );
}

function closeLangMenu({ restoreFocus = true } = {}) {
  if (!langOpen.value) return;
  langOpen.value = false;
  if (restoreFocus) langButtonRef.value?.focus();
}

function onLangMenuKeydown(e) {
  const keys = {
    ArrowDown: langActive.value + 2,
    ArrowUp: langActive.value - 2,
    ArrowRight: langActive.value + 1,
    ArrowLeft: langActive.value - 1,
    Home: 0,
    End: CHAT_LANGUAGES.length - 1,
  };
  if (e.key in keys) {
    e.preventDefault();
    focusLangOption(keys[e.key]);
  } else if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    selectLanguage(CHAT_LANGUAGES[langActive.value].code);
  } else if (e.key === "Escape") {
    e.preventDefault();
    e.stopPropagation();
    closeLangMenu();
  } else if (e.key === "Tab") {
    closeLangMenu({ restoreFocus: false });
  }
}

function onOutsidePointer(e) {
  if (!langPickerRef.value?.contains(e.target)) closeLangMenu({ restoreFocus: false });
}

watch(langOpen, (isOpen) => {
  if (isOpen) document.addEventListener("pointerdown", onOutsidePointer);
  else document.removeEventListener("pointerdown", onOutsidePointer);
});

function selectLanguage(code) {
  closeLangMenu();
  if (code === language.value) return;
  language.value = code;
  try {
    localStorage.setItem(LANGUAGE_KEY, code);
  } catch {
    /* preference only lasts for this page view */
  }

  const onlyGreeting = messages.value.length === 1 && messages.value[0].role === "bot";
  if (onlyGreeting) {
    messages.value = [greeting()];
  } else {
    const label = currentLanguage.value.code === "auto" ? "your language" : currentLanguage.value.label;
    const notice = { id: nextId++, role: "notice", text: `Replies will now be in ${label}`, sources: [] };
    const last = messages.value[messages.value.length - 1];
    if (last?.role === "notice") messages.value.splice(-1, 1, notice);
    else messages.value.push(notice);
  }
  persist();
  scrollToBottom();
}

async function scrollToBottom() {
  await nextTick();
  if (listRef.value) {
    listRef.value.scrollTop = listRef.value.scrollHeight;
  }
}

function newChat() {
  controller?.abort();
  controller = null;
  finishReveal();
  loading.value = false;
  conversationId.value = "";
  limitReached.value = false;
  messages.value = [greeting()];
  persist();
  nextTick(() => inputRef.value?.focus());
}

async function send(text) {
  const message = (text ?? input.value).trim();
  if (!message || loading.value || limitReached.value) return;

  messages.value.push({ id: nextId++, role: "user", text: message, sources: [], fresh: true });
  messages.value.push({ id: nextId++, role: "bot", text: "", sources: [], streaming: true, fresh: true });
  const reply = messages.value[messages.value.length - 1];
  startReveal(reply);
  input.value = "";
  loading.value = true;
  scrollToBottom();

  controller = new AbortController();
  const ownController = controller;
  try {
    await streamChat({
      message,
      conversationId: conversationId.value,
      pagePath: route.path,
      language: language.value === DEFAULT_CHAT_LANGUAGE ? "" : language.value,
      signal: ownController.signal,
      onEvent(name, data) {
        if (name === "meta" && data.conversation_id) {
          conversationId.value = data.conversation_id;
        } else if (name === "delta" && data.text) {
          reply.text += data.text;
          if (reply.revealing) kickReveal();
          else scrollToBottom();
        } else if (name === "done") {
          reply.sources = Array.isArray(data.sources) ? data.sources : [];
          reply.offerLead = Boolean(data.offer_lead);
          reply.suggestions = cleanSuggestions(data.suggestions);
        }
      },
    });
    if (!reply.text.trim()) {
      reply.text = "Sorry, I couldn't answer that. Please try again or contact our team.";
      reply.sources = [{ title: "Contact Us", href: "/contact" }];
    }
  } catch (err) {
    if (ownController.signal.aborted) return;
    if (err.code === "conversation_limit") limitReached.value = true;
    if (!reply.text.trim()) {
      reply.text =
        err.status === 429 || err.status === 400
          ? err.message
          : err.status
            ? "Something went wrong. Please try again or contact us on the website."
            : "Couldn't reach the assistant. Please try again or contact us on the website.";
      reply.sources = err.status === 429 ? [] : [{ title: "Contact Us", href: "/contact" }];
    }
  } finally {
    if (controller === ownController) {
      reply.streaming = false;
      loading.value = false;
      controller = null;
      persist();
      if (reply.revealing) kickReveal();
      else scrollToBottom();
    }
  }
}

function onKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
}

onBeforeUnmount(() => {
  controller?.abort();
  cancelRevealTick();
  document.removeEventListener("pointerdown", onOutsidePointer);
});
</script>

<template>
  <div class="chat-widget" :class="{ 'chat-widget--open': open }">
    <div v-if="open" class="chat-widget__panel" role="dialog" aria-label="Urbanrupee assistant">
      <header class="chat-widget__header">
        <span class="chat-widget__brand" aria-hidden="true">
          <img :src="LOGO_PATHS.chatAssistant" alt="" width="20" height="24" />
        </span>
        <div ref="langPickerRef" class="chat-widget__heading">
          <p class="chat-widget__title">Urbanrupee Assistant</p>
          <button
            ref="langButtonRef"
            type="button"
            class="chat-widget__lang-btn"
            aria-haspopup="listbox"
            :aria-expanded="langOpen"
            aria-controls="chat-widget-lang-menu"
            :aria-label="`Reply language: ${currentLanguage.english}. Change language`"
            @click="langOpen ? closeLangMenu() : openLangMenu()"
          >
            <svg class="chat-widget__lang-globe" viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="12" cy="12" r="9" />
              <path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z" />
            </svg>
            <span class="chat-widget__lang-current">{{ currentLanguage.label }}</span>
            <svg
              class="chat-widget__lang-chevron"
              :class="{ 'chat-widget__lang-chevron--open': langOpen }"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
          </button>

          <Transition name="chat-lang">
            <div v-if="langOpen" class="chat-widget__lang-menu" @keydown="onLangMenuKeydown">
              <p class="chat-widget__lang-heading">Reply language</p>
              <div
                id="chat-widget-lang-menu"
                class="chat-widget__lang-grid"
                role="listbox"
                aria-label="Reply language"
              >
                <button
                  v-for="(lang, i) in CHAT_LANGUAGES"
                  :key="lang.code"
                  :ref="(el) => (langOptionRefs[i] = el)"
                  type="button"
                  role="option"
                  class="chat-widget__lang-option"
                  :class="{ 'chat-widget__lang-option--active': lang.code === language }"
                  :aria-selected="lang.code === language"
                  :tabindex="i === langActive ? 0 : -1"
                  :lang="lang.code === 'auto' || lang.code === 'hinglish' ? 'en' : lang.code"
                  @click="selectLanguage(lang.code)"
                >
                  <span class="chat-widget__lang-native">{{ lang.label }}</span>
                  <span class="chat-widget__lang-english" lang="en">{{ lang.english }}</span>
                  <svg
                    v-if="lang.code === language"
                    class="chat-widget__lang-check"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M5 12.5l4.5 4.5L19 7.5" />
                  </svg>
                </button>
              </div>
            </div>
          </Transition>
        </div>
        <button
          v-if="hasUserMessages"
          type="button"
          class="chat-widget__icon-btn"
          aria-label="Start a new chat"
          title="New chat"
          @click="newChat"
        >
          ↺
        </button>
        <button type="button" class="chat-widget__icon-btn" aria-label="Close chat" @click="toggle">
          ×
        </button>
      </header>

      <div
        ref="listRef"
        class="chat-widget__messages"
        aria-live="polite"
        :aria-busy="loading || revealing ? 'true' : 'false'"
      >
        <template v-for="msg in messages" :key="msg.id">
          <p v-if="msg.role === 'notice'" class="chat-widget__lang-notice">{{ msg.text }}</p>
          <div
            v-else
            class="chat-widget__msg"
            :class="[`chat-widget__msg--${msg.role}`, { 'chat-widget__msg--fresh': msg.fresh }]"
            @animationend="clearFresh(msg, $event)"
          >
            <span
              v-if="msg.role === 'bot'"
              class="chat-widget__avatar"
              :class="{ 'chat-widget__avatar--live': msg.streaming || msg.revealing }"
              aria-hidden="true"
            >
              <img :src="LOGO_PATHS.chatAssistant" alt="" width="13" height="16" />
            </span>
            <div class="chat-widget__body">
              <p
                v-if="(msg.streaming || msg.revealing) && !bubbleText(msg)"
                class="chat-widget__bubble chat-widget__bubble--typing"
              >
                <span class="chat-widget__dot" />
                <span class="chat-widget__dot" />
                <span class="chat-widget__dot" />
                <span class="sr-only">Assistant is typing</span>
              </p>
              <p
                v-else
                class="chat-widget__bubble"
                :class="{ 'chat-widget__bubble--shine': msg.shine }"
                @animationend="clearShine(msg, $event)"
              >{{ bubbleText(msg) }}<span
                  v-if="msg.streaming || msg.revealing"
                  class="chat-widget__caret"
                  aria-hidden="true"
                /></p>
              <ul v-if="msg.sources?.length && !msg.streaming && !msg.revealing" class="chat-widget__sources">
                <li v-for="src in msg.sources" :key="src.href">
                  <RouterLink :to="src.href" @click="closeOnNavigate">{{ src.title }}</RouterLink>
                </li>
              </ul>
              <button
                v-if="msg.offerLead && !msg.revealing"
                type="button"
                class="chat-widget__cta"
                @click="goToContact"
              >
                Contact our team
              </button>
              <div
                v-if="msg.id === latestBotId && msg.suggestions?.length && !msg.streaming && !msg.revealing"
                class="chat-widget__followups"
                role="group"
                :aria-label="currentLanguage.tryAsking"
              >
                <span class="chat-widget__followups-label" aria-hidden="true">
                  <svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor">
                    <path d="M8 0l1.7 4.6L14.3 6l-4.6 1.7L8 12.3 6.3 7.7 1.7 6l4.6-1.4z" />
                  </svg>
                  {{ currentLanguage.tryAsking }}
                </span>
                <button
                  v-for="(q, i) in msg.suggestions"
                  :key="q"
                  type="button"
                  class="chat-widget__followup"
                  :style="{ '--i': i }"
                  :disabled="loading"
                  @click="send(q)"
                >
                  <span>{{ q }}</span>
                  <svg class="chat-widget__followup-arrow" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
                    <path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>

      <div v-if="!hasUserMessages" class="chat-widget__suggestions">
        <button
          v-for="(q, i) in currentLanguage.suggestions"
          :key="`${language}-${i}`"
          type="button"
          class="chat-widget__chip"
          @click="send(q)"
        >
          {{ q }}
        </button>
      </div>

      <div v-if="limitReached" class="chat-widget__limit">
        <span>This chat is full.</span>
        <button type="button" class="chat-widget__link-btn" @click="newChat">Start a new chat</button>
      </div>

      <form v-else class="chat-widget__form" @submit.prevent="send()">
        <input
          ref="inputRef"
          v-model="input"
          type="text"
          class="chat-widget__input"
          :placeholder="currentLanguage.placeholder"
          maxlength="500"
          autocomplete="off"
          aria-label="Your message"
          :disabled="loading"
          @keydown="onKeydown"
        />
        <button type="submit" class="chat-widget__send" :disabled="loading || !input.trim()">
          Send
        </button>
      </form>

      <footer class="chat-widget__footer">
        <button type="button" class="chat-widget__human-btn" @click="goToContact">
          <span class="chat-widget__human-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M4 14v-2a8 8 0 0116 0v2" />
              <rect x="3" y="14" width="4" height="6" rx="1.5" />
              <rect x="17" y="14" width="4" height="6" rx="1.5" />
            </svg>
          </span>
          <span class="chat-widget__human-text">Talk to a human</span>
          <svg class="chat-widget__human-arrow" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M9 6l6 6-6 6" />
          </svg>
        </button>
        <span class="chat-widget__notice">
          AI replies can be wrong. Chats are saved; never share card details or OTPs.
          <RouterLink to="/privacy-policy" @click="closeOnNavigate">Privacy</RouterLink>
        </span>
      </footer>
    </div>

    <button
      type="button"
      class="chat-widget__launcher"
      :class="{ 'chat-widget__launcher--open': open }"
      :aria-expanded="open"
      aria-label="Open chat assistant"
      @click="toggle"
    >
      <img
        v-if="!open"
        :src="LOGO_PATHS.chatAssistant"
        alt=""
        width="25"
        height="30"
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
  position: relative;
  width: min(380px, calc(100vw - 40px));
  height: min(560px, calc(100vh - 120px));
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
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 12px 12px 16px;
  background: var(--btn-primary-gradient);
  color: var(--btn-primary-text);
}

.chat-widget__brand {
  flex-shrink: 0;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.chat-widget__brand img,
.chat-widget__avatar img {
  display: block;
  object-fit: contain;
}

.chat-widget__brand img {
  width: 20px;
  height: 24px;
}

.chat-widget__avatar img {
  width: 13px;
  height: 16px;
}

.chat-widget__heading {
  flex: 1;
  min-width: 0;
}

.chat-widget__title {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.chat-widget__lang-btn {
  margin-top: 4px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: 100%;
  min-height: 30px;
  padding: 4px 10px 4px 8px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.16);
  color: inherit;
  font-size: 12px;
  font-weight: 600;
  font-family: inherit;
  backdrop-filter: blur(6px);
  transition:
    background 0.15s ease,
    border-color 0.15s ease;
}

.chat-widget__lang-btn:hover,
.chat-widget__lang-btn[aria-expanded="true"] {
  background: rgba(255, 255, 255, 0.28);
  border-color: rgba(255, 255, 255, 0.6);
}

.chat-widget__lang-btn:focus-visible,
.chat-widget__lang-option:focus-visible {
  outline: 2px solid #fff;
  outline-offset: 2px;
}

.chat-widget__lang-globe,
.chat-widget__lang-chevron,
.chat-widget__lang-check {
  flex-shrink: 0;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chat-widget__lang-globe {
  width: 14px;
  height: 14px;
}

.chat-widget__lang-current {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-widget__lang-chevron {
  width: 12px;
  height: 12px;
  transition: transform 0.2s ease;
}

.chat-widget__lang-chevron--open {
  transform: rotate(180deg);
}

.chat-widget__lang-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 12px;
  right: 12px;
  z-index: 5;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--bg-surface);
  color: var(--text-primary);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18);
  transform-origin: top left;
}

.chat-widget__lang-heading {
  margin: 0 0 8px 2px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.chat-widget__lang-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
  max-height: min(300px, calc(100vh - 260px));
  overflow-y: auto;
}

.chat-widget__lang-option {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1px;
  min-height: 48px;
  padding: 8px 28px 8px 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-surface);
  color: var(--text-primary);
  font-family: inherit;
  text-align: left;
  transition:
    border-color 0.15s ease,
    background 0.15s ease,
    transform 0.15s ease;
}

.chat-widget__lang-option:hover {
  border-color: #06b6d4;
  background: rgba(6, 182, 212, 0.06);
  transform: translateY(-1px);
}

.chat-widget__lang-option:focus-visible {
  outline-color: #06b6d4;
}

.chat-widget__lang-option--active {
  border-color: #06b6d4;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.14), rgba(37, 99, 235, 0.1));
}

.chat-widget__lang-native {
  font-size: 14px;
  font-weight: 700;
  line-height: 1.3;
}

.chat-widget__lang-english {
  font-size: 11px;
  line-height: 1.3;
  color: var(--text-muted);
}

.chat-widget__lang-check {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 16px;
  height: 16px;
  padding: 2px;
  border-radius: 50%;
  background: #06b6d4;
  color: #fff;
  stroke-width: 3;
}

.chat-lang-enter-active,
.chat-lang-leave-active {
  transition:
    opacity 0.16s ease,
    transform 0.16s ease;
}

.chat-lang-enter-from,
.chat-lang-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}

.chat-widget__lang-notice {
  align-self: center;
  margin: 0;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  background: var(--bg-muted);
  color: var(--text-secondary);
  font-size: 12px;
}

.chat-widget__icon-btn {
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

.chat-widget__icon-btn:hover {
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

.chat-widget__msg {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.chat-widget__msg--user {
  align-self: flex-end;
  max-width: 88%;
  transform-origin: bottom right;
}

.chat-widget__msg--bot {
  align-self: flex-start;
  max-width: 95%;
  transform-origin: bottom left;
}

.chat-widget__body {
  min-width: 0;
}

.chat-widget__msg--fresh {
  animation: chat-msg-in 0.32s cubic-bezier(0.22, 1.2, 0.36, 1) both;
}

@keyframes chat-msg-in {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.92);
    filter: blur(6px);
  }
  to {
    opacity: 1;
    transform: none;
    filter: none;
  }
}

.chat-widget__avatar {
  position: relative;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #fff;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-widget__bubble {
  margin: 0;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
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

.chat-widget__avatar--live::before {
  content: "";
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, #06b6d4, #2563eb, #8b5cf6, #06b6d4);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 2px), #000 calc(100% - 2px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 2px), #000 calc(100% - 2px));
  animation: chat-spin 0.8s linear infinite;
}

@keyframes chat-spin {
  to {
    transform: rotate(360deg);
  }
}

.chat-widget__bubble--typing {
  display: flex;
  gap: 5px;
  align-items: center;
  min-height: 41px;
}

.chat-widget__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: linear-gradient(135deg, #06b6d4, #2563eb);
  animation: chat-dot 0.9s infinite ease-in-out;
}

.chat-widget__dot:nth-child(2) {
  animation-delay: 0.12s;
}

.chat-widget__dot:nth-child(3) {
  animation-delay: 0.24s;
}

@keyframes chat-dot {
  0%,
  70%,
  100% {
    opacity: 0.35;
    transform: translateY(0) scale(0.85);
  }
  35% {
    opacity: 1;
    transform: translateY(-4px) scale(1);
  }
}

.chat-widget__caret {
  display: inline-block;
  width: 2px;
  height: 1.1em;
  margin-left: 2px;
  vertical-align: -0.18em;
  border-radius: 1px;
  background: linear-gradient(180deg, #06b6d4, #2563eb);
  box-shadow: 0 0 8px rgba(6, 182, 212, 0.8);
  animation: chat-caret 0.8s steps(1) infinite;
}

@keyframes chat-caret {
  50% {
    opacity: 0;
  }
}

.chat-widget__bubble--shine {
  position: relative;
  overflow: hidden;
}

.chat-widget__bubble--shine::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    105deg,
    transparent 30%,
    rgba(6, 182, 212, 0.18) 45%,
    rgba(255, 255, 255, 0.75) 50%,
    rgba(37, 99, 235, 0.14) 55%,
    transparent 70%
  );
  transform: translateX(-100%);
  animation: chat-shine 0.7s ease-out forwards;
  pointer-events: none;
}

@keyframes chat-shine {
  to {
    transform: translateX(100%);
  }
}

.chat-widget__sources,
.chat-widget__cta {
  animation: chat-fade-up 0.25s ease-out both;
}

.chat-widget__cta {
  animation-delay: 0.08s;
}

@keyframes chat-fade-up {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .chat-widget__panel,
  .chat-widget__dot,
  .chat-widget__msg--fresh,
  .chat-widget__avatar--live::before,
  .chat-widget__caret,
  .chat-widget__bubble--shine::after,
  .chat-widget__sources,
  .chat-widget__cta,
  .chat-widget__followups-label,
  .chat-widget__followup,
  .chat-widget__human-btn,
  .chat-widget__human-btn::after,
  .chat-widget__human-btn:hover .chat-widget__human-icon,
  .chat-widget__human-btn:focus-visible .chat-widget__human-icon {
    animation: none;
  }

  .chat-widget__human-btn::before,
  .chat-widget__human-arrow,
  .chat-widget__followup,
  .chat-widget__followup-arrow {
    transition: none;
  }

  .chat-widget__bubble--shine::after {
    display: none;
  }

  .chat-lang-enter-active,
  .chat-lang-leave-active,
  .chat-widget__lang-chevron,
  .chat-widget__lang-option {
    transition: none;
  }
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

.chat-widget__cta {
  margin-top: 8px;
  padding: 10px 14px;
  min-height: 44px;
  border: 1px solid var(--accent-blue);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--accent-blue);
  font-size: 13px;
  font-weight: 600;
}

.chat-widget__cta:hover {
  background: var(--accent-blue);
  color: #fff;
}

.chat-widget__followups {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  margin-top: 10px;
}

.chat-widget__followups-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--text-secondary);
  animation: chat-fade-up 0.25s ease-out both;
}

.chat-widget__followups-label svg {
  color: var(--accent-blue);
}

.chat-widget__followup {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 100%;
  min-height: 40px;
  padding: 9px 12px 9px 14px;
  border: 1px solid rgba(0, 152, 242, 0.3);
  border: 1px solid color-mix(in srgb, var(--accent-blue) 28%, var(--border));
  border-radius: var(--radius-pill);
  background: rgba(0, 152, 242, 0.06);
  background: color-mix(in srgb, var(--accent-blue) 6%, var(--bg-surface));
  color: var(--accent-blue);
  font-size: 13px;
  font-weight: 500;
  line-height: 1.3;
  text-align: left;
  cursor: pointer;
  animation: chat-fade-up 0.28s ease-out both;
  animation-delay: calc(80ms + var(--i, 0) * 70ms);
  transition:
    background 0.18s ease,
    border-color 0.18s ease,
    color 0.18s ease,
    transform 0.18s ease;
}

.chat-widget__followup-arrow {
  flex-shrink: 0;
  transition: transform 0.18s ease;
}

.chat-widget__followup:hover:not(:disabled),
.chat-widget__followup:focus-visible {
  border-color: var(--accent-blue);
  background: var(--accent-blue);
  color: #fff;
  transform: translateY(-1px);
}

.chat-widget__followup:hover:not(:disabled) .chat-widget__followup-arrow,
.chat-widget__followup:focus-visible .chat-widget__followup-arrow {
  transform: translateX(3px);
}

.chat-widget__followup:disabled {
  opacity: 0.55;
  cursor: default;
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
  padding: 12px 16px 8px;
  border-top: 1px solid var(--border);
}

.chat-widget__limit {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 12px 16px 8px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-secondary);
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

.chat-widget__footer {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 16px 12px;
  font-size: 11px;
  line-height: 1.4;
  color: var(--text-muted);
}

.chat-widget__link-btn {
  align-self: flex-start;
  padding: 4px 0;
  border: none;
  background: none;
  color: var(--accent-blue);
  font-size: 13px;
  font-weight: 600;
  text-decoration: underline;
}

.chat-widget__human-btn {
  position: relative;
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  margin-bottom: 6px;
  padding: 4px 12px 4px 4px;
  overflow: hidden;
  border: 1.5px solid transparent;
  border-radius: var(--radius-pill);
  background:
    linear-gradient(var(--bg-surface), var(--bg-surface)) padding-box,
    linear-gradient(120deg, #06b6d4, #2563eb, #8b5cf6, #06b6d4) border-box;
  background-size:
    100% 100%,
    250% 100%;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.12);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    color 0.2s ease;
  animation: chat-border-flow 4s linear infinite;
}

.chat-widget__human-btn::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  background: linear-gradient(120deg, #06b6d4, #2563eb);
  transform: translateX(-101%);
  transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.chat-widget__human-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 2;
  background: linear-gradient(105deg, transparent 35%, rgba(255, 255, 255, 0.85) 50%, transparent 65%);
  transform: translateX(-100%);
  animation: chat-human-shine 0.9s ease-out 0.9s forwards;
  pointer-events: none;
}

.chat-widget__human-btn > * {
  position: relative;
  z-index: 1;
}

.chat-widget__human-btn:hover,
.chat-widget__human-btn:focus-visible {
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 8px 22px rgba(37, 99, 235, 0.32);
}

.chat-widget__human-btn:hover::before,
.chat-widget__human-btn:focus-visible::before {
  transform: translateX(0);
}

.chat-widget__human-btn:focus-visible {
  outline: 2px solid #06b6d4;
  outline-offset: 2px;
}

.chat-widget__human-btn:active {
  transform: translateY(0) scale(0.98);
}

.chat-widget__human-icon {
  position: relative;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #06b6d4, #2563eb);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.45);
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.chat-widget__human-btn:hover .chat-widget__human-icon,
.chat-widget__human-btn:focus-visible .chat-widget__human-icon {
  background: rgba(255, 255, 255, 0.22);
  animation: chat-wiggle 0.5s ease;
}

.chat-widget__human-icon svg,
.chat-widget__human-arrow {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chat-widget__human-icon svg {
  width: 16px;
  height: 16px;
}

.chat-widget__human-arrow {
  width: 14px;
  height: 14px;
  stroke-width: 2.5;
  transition: transform 0.2s ease;
}

.chat-widget__human-btn:hover .chat-widget__human-arrow,
.chat-widget__human-btn:focus-visible .chat-widget__human-arrow {
  transform: translateX(3px);
}

@keyframes chat-border-flow {
  to {
    background-position:
      0 0,
      250% 0;
  }
}

@keyframes chat-human-shine {
  to {
    transform: translateX(100%);
  }
}

@keyframes chat-wiggle {
  25% {
    transform: rotate(-12deg);
  }
  50% {
    transform: rotate(10deg);
  }
  75% {
    transform: rotate(-5deg);
  }
}

.chat-widget__notice a {
  color: inherit;
  text-decoration: underline;
}

.chat-widget__launcher {
  width: 56px;
  height: 56px;
  border: 2px solid #06b6d4;
  border-radius: 50%;
  background: #fff;
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-widget__launcher--open {
  background: #06b6d4;
}

.chat-widget__launcher:hover {
  transform: scale(1.04);
}

.chat-widget__launcher-logo {
  width: 25px;
  height: 30px;
  object-fit: contain;
  display: block;
}

.chat-widget__launcher-icon {
  font-size: 22px;
  font-weight: 700;
  line-height: 1;
  color: #000;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 480px) {
  .chat-widget {
    right: 12px;
    bottom: calc(12px + var(--ur-sticky-cta, 0px));
  }
}
</style>
