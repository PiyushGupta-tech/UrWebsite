<script setup>
import { computed, nextTick, onBeforeUnmount, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { streamChat, submitChatLead } from "@/api/client";
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

// Same rules and messages as the contact form (validation/contactSchema.js), without
// pulling Joi into the bundle that every page loads.
function validateLead(fields) {
  const value = {
    name: fields.name.trim(),
    email: fields.email.trim(),
    phone: fields.phone.trim(),
    note: fields.note.trim(),
  };
  const errors = {};
  if (!value.name) errors.name = "Full Name is required.";
  else if (value.name.length < 2) errors.name = "Full Name must be at least 2 characters.";
  else if (value.name.length > 50) errors.name = "Full Name must be at most 50 characters.";
  else if (!/^[A-Za-z ]+$/.test(value.name)) errors.name = "Full Name can contain only letters and spaces.";

  if (!value.email) errors.email = "Email Address is required.";
  else if (value.email.length > 254) errors.email = "Email Address must be at most 254 characters.";
  else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(value.email)) errors.email = "Enter a valid email address.";

  if (!value.phone) errors.phone = "Phone Number is required.";
  else if (!/^[6-9][0-9]{9}$/.test(value.phone)) {
    errors.phone = "Phone Number must be 10 digits and start with 6, 7, 8, or 9.";
  }

  if (value.note.length > 500) errors.note = "Message must be 500 characters or fewer.";
  return { value, errors };
}

const route = useRoute();
const open = ref(false);
const input = ref("");
const loading = ref(false);
const listRef = ref(null);
const inputRef = ref(null);
let nextId = 1;
let controller = null;

const conversationId = ref("");
const leadSubmitted = ref(false);
const limitReached = ref(false);
const messages = ref([]);

const language = ref(loadLanguage());
const currentLanguage = computed(() => findChatLanguage(language.value));
const langOpen = ref(false);
const langActive = ref(0);
const langPickerRef = ref(null);
const langButtonRef = ref(null);
const langOptionRefs = [];

const lead = reactive({
  visible: false,
  kind: "lead",
  submitting: false,
  success: "",
  error: "",
  fields: { name: "", email: "", phone: "", note: "" },
  errors: {},
});

function greeting() {
  return { id: nextId++, role: "bot", text: currentLanguage.value.greeting, sources: [] };
}

function restore() {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "null");
    if (saved && Array.isArray(saved.messages) && saved.messages.length) {
      conversationId.value = String(saved.conversationId || "");
      leadSubmitted.value = Boolean(saved.leadSubmitted);
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
        leadSubmitted: leadSubmitted.value,
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
    nextTick(() => (lead.visible && !lead.success ? leadNameRef : inputRef).value?.focus());
  }
}

function closeOnNavigate(e) {
  // Modified clicks open a new tab, so the visitor is still on this page.
  if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  langOpen.value = false;
  open.value = false;
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
  leadSubmitted.value = false;
  limitReached.value = false;
  closeLeadForm();
  messages.value = [greeting()];
  persist();
  nextTick(() => inputRef.value?.focus());
}

async function send(text) {
  const message = (text ?? input.value).trim();
  if (!message || loading.value || limitReached.value) return;

  closeLeadForm();
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
          reply.offerLead = Boolean(data.offer_lead) && !leadSubmitted.value;
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
          : "Something went wrong. Please try again or contact us on the website.";
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

const LEAD_SUCCESS_MS = 2600;
const leadNameRef = ref(null);
const leadDoneRef = ref(null);
let leadTrigger = null;
let leadSuccessTimer = 0;

function openLeadForm(kind) {
  langOpen.value = false;
  // Safari does not focus buttons on click, leaving focus on <body>.
  leadTrigger = document.activeElement === document.body ? null : document.activeElement;
  lead.kind = kind;
  lead.error = "";
  lead.errors = {};
  lead.success = "";
  lead.visible = true;
  nextTick(() => leadNameRef.value?.focus({ preventScroll: true }));
}

function closeLeadForm() {
  clearTimeout(leadSuccessTimer);
  leadSuccessTimer = 0;
  const wasVisible = lead.visible;
  lead.visible = false;
  lead.error = "";
  lead.errors = {};
  lead.success = "";
  if (wasVisible) {
    nextTick(() => {
      const target = leadTrigger?.isConnected ? leadTrigger : inputRef.value;
      target?.focus({ preventScroll: true });
      leadTrigger = null;
    });
  }
}

function onLeadKeydown(e) {
  if (e.key === "Escape" && !lead.submitting) {
    e.stopPropagation();
    closeLeadForm();
  }
}

async function submitLead() {
  if (lead.submitting) return;
  lead.error = "";
  const { value, errors } = validateLead(lead.fields);
  lead.errors = errors;
  if (Object.keys(errors).length) return;

  lead.submitting = true;
  try {
    const data = await submitChatLead({
      ...value,
      kind: lead.kind,
      conversation_id: conversationId.value || undefined,
      page_path: route.path,
    });
    conversationId.value = data.conversation_id || conversationId.value;
    leadSubmitted.value = true;
    for (const m of messages.value) m.offerLead = false;
    messages.value.push({ id: nextId++, role: "bot", text: data.message, sources: [], fresh: true });
    lead.fields = { name: "", email: "", phone: "", note: "" };
    lead.success = data.message;
    persist();
    scrollToBottom();
    nextTick(() => leadDoneRef.value?.focus({ preventScroll: true }));
    leadSuccessTimer = setTimeout(closeLeadForm, LEAD_SUCCESS_MS);
  } catch (err) {
    if (err.conversationId) {
      conversationId.value = err.conversationId;
      persist();
    }
    lead.errors = err.fieldErrors || {};
    lead.error = err.message || "We could not send your details. Please try again.";
  } finally {
    lead.submitting = false;
  }
}

onBeforeUnmount(() => {
  controller?.abort();
  cancelRevealTick();
  clearTimeout(leadSuccessTimer);
  document.removeEventListener("pointerdown", onOutsidePointer);
});
</script>

<template>
  <div class="chat-widget" :class="{ 'chat-widget--open': open }">
    <div v-if="open" class="chat-widget__panel" role="dialog" aria-label="Urbanrupee assistant">
      <header class="chat-widget__header" :inert="lead.visible">
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
        :inert="lead.visible"
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
                v-if="msg.offerLead && !msg.revealing && !leadSubmitted && !lead.visible"
                type="button"
                class="chat-widget__cta"
                @click="openLeadForm('lead')"
              >
                Share my details with the team
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

      <div v-if="!hasUserMessages" class="chat-widget__suggestions" :inert="lead.visible">
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

      <div v-if="limitReached" class="chat-widget__limit" :inert="lead.visible">
        <span>This chat is full.</span>
        <button type="button" class="chat-widget__link-btn" @click="newChat">Start a new chat</button>
      </div>

      <form v-else class="chat-widget__form" :inert="lead.visible" @submit.prevent="send()">
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

      <footer class="chat-widget__footer" :inert="lead.visible">
        <button
          v-if="!leadSubmitted"
          type="button"
          class="chat-widget__human-btn"
          @click="openLeadForm('handoff')"
        >
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
        <span v-else class="chat-widget__footer-done">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
          Our team has your details
        </span>
        <span class="chat-widget__notice">
          AI replies can be wrong. Chats are saved; never share card details or OTPs.
          <RouterLink to="/privacy-policy" @click="closeOnNavigate">Privacy</RouterLink>
        </span>
      </footer>

      <Transition name="chat-sheet" :duration="{ enter: 420, leave: 240 }">
        <div
          v-if="lead.visible"
          class="chat-widget__sheet-backdrop"
          @click.self="lead.submitting || closeLeadForm()"
          @keydown="onLeadKeydown"
        >
          <div
            class="chat-widget__sheet"
            role="dialog"
            aria-modal="true"
            aria-labelledby="chat-widget-sheet-title"
          >
            <span class="chat-widget__sheet-grip" aria-hidden="true" />
            <button
              type="button"
              class="chat-widget__sheet-close"
              aria-label="Close form"
              :disabled="lead.submitting"
              @click="closeLeadForm"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" /></svg>
            </button>

            <div v-if="lead.success" class="chat-widget__sheet-success" role="status">
              <svg class="chat-widget__success-mark" viewBox="0 0 52 52" aria-hidden="true">
                <circle class="chat-widget__success-circle" cx="26" cy="26" r="23" />
                <path class="chat-widget__success-check" d="M15 27l7.5 7.5L37.5 19" />
              </svg>
              <span v-for="n in 8" :key="n" class="chat-widget__spark" :style="{ '--n': n }" aria-hidden="true" />
              <p id="chat-widget-sheet-title" class="chat-widget__sheet-title">Request sent</p>
              <p class="chat-widget__sheet-text">{{ lead.success }}</p>
              <button ref="leadDoneRef" type="button" class="chat-widget__sheet-submit" @click="closeLeadForm">
                Back to chat
              </button>
            </div>

            <form v-else class="chat-widget__sheet-form" novalidate @submit.prevent="submitLead">
              <div class="chat-widget__sheet-hero chat-widget__sheet-item" style="--i: 0">
                <span class="chat-widget__sheet-badge" aria-hidden="true">
                  <svg viewBox="0 0 24 24">
                    <path d="M4 14v-2a8 8 0 0116 0v2" />
                    <rect x="3" y="14" width="4" height="6" rx="1.5" />
                    <rect x="17" y="14" width="4" height="6" rx="1.5" />
                  </svg>
                </span>
                <div>
                  <p id="chat-widget-sheet-title" class="chat-widget__sheet-title">
                    {{ lead.kind === "handoff" ? "Talk to our team" : "Get in touch" }}
                  </p>
                  <p class="chat-widget__sheet-text">
                    Share your details and our sales team will contact you. This chat will be shared with them.
                  </p>
                </div>
              </div>

              <div class="chat-widget__sheet-item" style="--i: 1">
                <label class="chat-widget__float" :class="{ 'chat-widget__float--error': lead.errors.name }">
                  <svg class="chat-widget__float-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <circle cx="12" cy="8" r="4" />
                    <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
                  </svg>
                  <input
                    ref="leadNameRef"
                    v-model="lead.fields.name"
                    type="text"
                    autocomplete="name"
                    maxlength="50"
                    placeholder=" "
                    :aria-invalid="Boolean(lead.errors.name)"
                    :aria-describedby="lead.errors.name ? 'chat-lead-name-error' : undefined"
                  />
                  <span class="chat-widget__float-label">Full Name</span>
                </label>
                <small v-if="lead.errors.name" id="chat-lead-name-error" class="chat-widget__float-error">
                  {{ lead.errors.name }}
                </small>
              </div>

              <div class="chat-widget__sheet-item" style="--i: 2">
                <label class="chat-widget__float" :class="{ 'chat-widget__float--error': lead.errors.email }">
                  <svg class="chat-widget__float-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="5" width="18" height="14" rx="2" />
                    <path d="M3 7l9 6 9-6" />
                  </svg>
                  <input
                    v-model="lead.fields.email"
                    type="email"
                    autocomplete="email"
                    maxlength="254"
                    placeholder=" "
                    :aria-invalid="Boolean(lead.errors.email)"
                    :aria-describedby="lead.errors.email ? 'chat-lead-email-error' : undefined"
                  />
                  <span class="chat-widget__float-label">Email Address</span>
                </label>
                <small v-if="lead.errors.email" id="chat-lead-email-error" class="chat-widget__float-error">
                  {{ lead.errors.email }}
                </small>
              </div>

              <div class="chat-widget__sheet-item" style="--i: 3">
                <label class="chat-widget__float" :class="{ 'chat-widget__float--error': lead.errors.phone }">
                  <svg class="chat-widget__float-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"
                    />
                  </svg>
                  <input
                    v-model="lead.fields.phone"
                    type="tel"
                    inputmode="numeric"
                    autocomplete="tel-national"
                    maxlength="10"
                    placeholder=" "
                    :aria-invalid="Boolean(lead.errors.phone)"
                    :aria-describedby="lead.errors.phone ? 'chat-lead-phone-error' : undefined"
                  />
                  <span class="chat-widget__float-label">Phone Number</span>
                </label>
                <small v-if="lead.errors.phone" id="chat-lead-phone-error" class="chat-widget__float-error">
                  {{ lead.errors.phone }}
                </small>
              </div>

              <div class="chat-widget__sheet-item" style="--i: 4">
                <label
                  class="chat-widget__float chat-widget__float--area"
                  :class="{ 'chat-widget__float--error': lead.errors.note }"
                >
                  <svg class="chat-widget__float-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M4 5h16v11H8l-4 4z" />
                  </svg>
                  <textarea
                    v-model="lead.fields.note"
                    rows="2"
                    maxlength="500"
                    placeholder=" "
                    :aria-invalid="Boolean(lead.errors.note)"
                    :aria-describedby="lead.errors.note ? 'chat-lead-note-error' : undefined"
                  />
                  <span class="chat-widget__float-label">Message (optional)</span>
                </label>
                <small v-if="lead.errors.note" id="chat-lead-note-error" class="chat-widget__float-error">
                  {{ lead.errors.note }}
                </small>
              </div>

              <p v-if="lead.error" class="chat-widget__float-error chat-widget__sheet-alert" role="alert">
                {{ lead.error }}
              </p>

              <button
                type="submit"
                class="chat-widget__sheet-submit chat-widget__sheet-item"
                style="--i: 5"
                :disabled="lead.submitting"
              >
                <span v-if="lead.submitting" class="chat-widget__spinner" aria-hidden="true" />
                {{ lead.submitting ? "Sending…" : "Send details" }}
                <svg v-if="!lead.submitting" class="chat-widget__submit-arrow" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </Transition>
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
  .chat-widget__sheet-item,
  .chat-widget__sheet-badge::after,
  .chat-widget__float--error,
  .chat-widget__spark,
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

  .chat-widget__bubble--shine::after,
  .chat-widget__spark {
    display: none;
  }

  .chat-widget__success-circle,
  .chat-widget__success-check {
    animation: none;
    stroke-dashoffset: 0;
  }

  .chat-sheet-enter-active,
  .chat-sheet-leave-active,
  .chat-sheet-enter-active .chat-widget__sheet,
  .chat-sheet-leave-active .chat-widget__sheet {
    transition: none;
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

.chat-widget__sheet-backdrop {
  position: absolute;
  inset: 0;
  z-index: 10;
  display: flex;
  align-items: flex-end;
  background: rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(3px);
}

.chat-widget__sheet {
  position: relative;
  width: 100%;
  max-height: calc(100% - 48px);
  overflow-y: auto;
  padding: 10px 18px 18px;
  border-radius: 22px 22px 0 0;
  background:
    radial-gradient(120% 70% at 100% 0%, rgba(6, 182, 212, 0.14), transparent 60%),
    radial-gradient(90% 60% at 0% 0%, rgba(37, 99, 235, 0.1), transparent 55%),
    var(--bg-surface);
  box-shadow: 0 -18px 40px rgba(15, 23, 42, 0.22);
}

.chat-sheet-enter-active,
.chat-sheet-leave-active {
  transition: opacity 0.22s ease;
}

.chat-sheet-enter-active .chat-widget__sheet {
  transition: transform 0.42s cubic-bezier(0.2, 1.15, 0.32, 1);
}

.chat-sheet-leave-active .chat-widget__sheet {
  transition: transform 0.24s cubic-bezier(0.4, 0, 1, 1);
}

.chat-sheet-enter-from,
.chat-sheet-leave-to {
  opacity: 0;
}

.chat-sheet-enter-from .chat-widget__sheet,
.chat-sheet-leave-to .chat-widget__sheet {
  transform: translateY(100%);
}

.chat-widget__sheet-grip {
  display: block;
  width: 40px;
  height: 4px;
  margin: 0 auto 10px;
  border-radius: 2px;
  background: var(--border);
}

.chat-widget__sheet-close {
  position: absolute;
  top: 12px;
  right: 12px;
  /* The animated sheet items form their own layers and would otherwise cover the button. */
  z-index: 2;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: var(--bg-muted);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    transform 0.2s ease,
    background 0.2s ease;
}

.chat-widget__sheet-close:hover {
  transform: rotate(90deg);
  background: var(--border);
}

.chat-widget__sheet-close svg,
.chat-widget__sheet-badge svg,
.chat-widget__float-icon,
.chat-widget__submit-arrow {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chat-widget__sheet-close svg {
  width: 16px;
  height: 16px;
}

.chat-widget__sheet-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-widget__sheet-item {
  animation: chat-sheet-item 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(var(--i, 0) * 50ms + 120ms);
}

@keyframes chat-sheet-item {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.chat-widget__sheet-hero {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding-right: 36px;
}

.chat-widget__sheet-badge {
  position: relative;
  flex-shrink: 0;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: linear-gradient(135deg, #06b6d4, #2563eb);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
}

.chat-widget__sheet-badge::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 2px solid #06b6d4;
  animation: chat-ping 1.8s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes chat-ping {
  75%,
  100% {
    transform: scale(1.45);
    opacity: 0;
  }
}

.chat-widget__sheet-badge svg {
  width: 24px;
  height: 24px;
}

.chat-widget__sheet-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  line-height: 1.25;
  background: linear-gradient(90deg, #0e7490, #2563eb);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.chat-widget__sheet-text {
  margin: 4px 0 0;
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.chat-widget__float {
  position: relative;
  display: block;
}

.chat-widget__float input,
.chat-widget__float textarea {
  display: block;
  width: 100%;
  padding: 22px 12px 8px 42px;
  border: 1.5px solid var(--border);
  border-radius: 14px;
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 15px;
  font-family: inherit;
  resize: none;
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease;
}

.chat-widget__float input:focus,
.chat-widget__float textarea:focus {
  outline: none;
  border-color: #06b6d4;
  box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.16);
}

.chat-widget__float-icon {
  position: absolute;
  left: 13px;
  top: 17px;
  width: 18px;
  height: 18px;
  color: var(--text-muted);
  pointer-events: none;
  transition: color 0.18s ease;
}

.chat-widget__float:focus-within .chat-widget__float-icon {
  color: #06b6d4;
}

.chat-widget__float-label {
  position: absolute;
  left: 42px;
  top: 16px;
  font-size: 15px;
  color: var(--text-muted);
  pointer-events: none;
  transform-origin: left top;
  transition:
    transform 0.18s ease,
    color 0.18s ease;
}

.chat-widget__float input:focus + .chat-widget__float-label,
.chat-widget__float input:not(:placeholder-shown) + .chat-widget__float-label,
.chat-widget__float textarea:focus + .chat-widget__float-label,
.chat-widget__float textarea:not(:placeholder-shown) + .chat-widget__float-label {
  transform: translateY(-10px) scale(0.76);
  color: #0891b2;
  font-weight: 600;
}

.chat-widget__float--error input,
.chat-widget__float--error textarea {
  border-color: #dc2626;
}

.chat-widget__float--error {
  animation: chat-shake 0.32s ease;
}

@keyframes chat-shake {
  20%,
  60% {
    transform: translateX(-4px);
  }
  40%,
  80% {
    transform: translateX(4px);
  }
}

.chat-widget__float-error {
  display: block;
  margin: 4px 0 0 4px;
  color: #dc2626;
  font-size: 12px;
}

.chat-widget__sheet-alert {
  margin: 0;
}

.chat-widget__sheet-submit {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  min-height: 48px;
  padding: 12px 18px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #06b6d4, #2563eb);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  font-family: inherit;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.3);
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;
}

.chat-widget__sheet-submit::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(105deg, transparent 35%, rgba(255, 255, 255, 0.4) 50%, transparent 65%);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.chat-widget__sheet-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.38);
}

.chat-widget__sheet-submit:hover:not(:disabled)::before {
  transform: translateX(100%);
}

.chat-widget__sheet-submit:disabled {
  opacity: 0.75;
  cursor: progress;
}

.chat-widget__submit-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.18s ease;
}

.chat-widget__sheet-submit:hover .chat-widget__submit-arrow {
  transform: translateX(3px);
}

.chat-widget__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: chat-spin 0.7s linear infinite;
}

.chat-widget__sheet-success {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 18px 8px 4px;
  text-align: center;
}

.chat-widget__sheet-success .chat-widget__sheet-submit {
  margin-top: 14px;
}

.chat-widget__success-mark {
  width: 72px;
  height: 72px;
  margin-bottom: 8px;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chat-widget__success-circle {
  stroke: #06b6d4;
  stroke-width: 3;
  stroke-dasharray: 145;
  stroke-dashoffset: 145;
  animation: chat-draw 0.5s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.chat-widget__success-check {
  stroke: #2563eb;
  stroke-width: 4;
  stroke-dasharray: 40;
  stroke-dashoffset: 40;
  animation: chat-draw 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.45s forwards;
}

@keyframes chat-draw {
  to {
    stroke-dashoffset: 0;
  }
}

.chat-widget__spark {
  position: absolute;
  top: 54px;
  left: 50%;
  width: 6px;
  height: 6px;
  margin-left: -3px;
  border-radius: 50%;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  opacity: 0;
  transform: rotate(calc(var(--n) * 45deg)) translateY(0);
  animation: chat-spark 0.6s ease-out 0.55s forwards;
}

@keyframes chat-spark {
  0% {
    opacity: 1;
    transform: rotate(calc(var(--n) * 45deg)) translateY(-30px) scale(1);
  }
  100% {
    opacity: 0;
    transform: rotate(calc(var(--n) * 45deg)) translateY(-56px) scale(0.4);
  }
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
.chat-widget__human-arrow,
.chat-widget__footer-done svg {
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

.chat-widget__footer-done {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  padding: 6px 12px 6px 8px;
  border-radius: var(--radius-pill);
  background: rgba(16, 185, 129, 0.1);
  color: #047857;
  font-size: 12px;
  font-weight: 600;
}

.chat-widget__footer-done svg {
  width: 16px;
  height: 16px;
  padding: 2px;
  border-radius: 50%;
  background: #10b981;
  color: #fff;
  stroke-width: 3;
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
