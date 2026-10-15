"""Tests for the AI chat assistant, chat leads, and admin chat review."""

import json
import time
from datetime import timedelta
from datetime import timezone as dt_timezone
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

import openai
from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.db import connection
from django.test import SimpleTestCase, TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from website import chatbot
from website.models import ChatConversation, ChatMessage

TEST_CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "chatbot-tests",
    }
}

LEAD = {"name": "Asha Rao", "email": "asha@example.com", "phone": "9876543210"}


def parse_events(response):
    body = b"".join(response.streaming_content).decode()
    events = []
    for block in body.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


def reply_text(events):
    return "".join(data["text"] for name, data in events if name == "delta")


def fake_chunks(*pieces):
    return [
        SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=p, refusal=None))])
        for p in pieces
    ]


class MarkerFilterTests(SimpleTestCase):
    def test_marker_split_across_chunks_is_removed(self):
        f = chatbot.MarkerFilter()
        out = f.feed("Happy to help! [[LE") + f.feed("AD]]") + f.flush()
        self.assertEqual(out, "Happy to help! ")
        self.assertTrue(f.found)

    def test_text_resembling_marker_start_is_released(self):
        f = chatbot.MarkerFilter()
        out = f.feed("Use [[brackets") + f.feed(" freely") + f.flush()
        self.assertEqual(out, "Use [[brackets freely")
        self.assertFalse(f.found)


class RedactTests(SimpleTestCase):
    def test_card_and_account_numbers_removed(self):
        self.assertEqual(
            chatbot.redact("my card 4111 1111 1111 1111 failed"),
            f"my card {chatbot.REDACTED_NUMBER} failed",
        )
        self.assertEqual(chatbot.redact("acct 123456789012"), f"acct {chatbot.REDACTED_NUMBER}")

    def test_phone_numbers_and_amounts_kept(self):
        text = "call 9876543210 about a 50000 payout"
        self.assertEqual(chatbot.redact(text), text)


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.db.DatabaseCache", "LOCATION": "django_cache"}}
)
class RateLimitWindowTests(TestCase):
    def setUp(self):
        cache.clear()

    def hit_at(self, now, limit=1):
        with patch.object(chatbot, "time", SimpleNamespace(time=lambda: now)):
            return chatbot.allow_hit("test:rate", limit, 60)

    def test_blocked_visitor_is_freed_when_the_window_ends(self):
        self.assertTrue(self.hit_at(100))
        self.assertFalse(self.hit_at(110))
        self.assertFalse(self.hit_at(119))
        self.assertTrue(self.hit_at(120))

    def test_database_cache_keeps_the_window_expiry_after_incr(self):
        self.assertTrue(chatbot.allow_hit("test:hourly", 5, 3600))
        self.assertTrue(chatbot.allow_hit("test:hourly", 5, 3600))
        window = int(time.time() // 3600)
        with connection.cursor() as cursor:
            cursor.execute("SELECT expires FROM django_cache WHERE cache_key LIKE %s", [f"%test:hourly:{window}"])
            (expires,) = cursor.fetchone()
        if timezone.is_naive(expires):
            expires = timezone.make_aware(expires, dt_timezone.utc)
        remaining = (expires - timezone.now()).total_seconds()
        expected = (window + 1) * 3600 - time.time()
        self.assertAlmostEqual(remaining, expected, delta=5)


class KnowledgePromptTests(SimpleTestCase):
    def test_prompt_contains_site_facts_without_media_paths(self):
        prompt = chatbot.SYSTEM_PROMPT
        self.assertIn("it.support@urbanrupee.com", prompt)
        self.assertIn("Is Urbanrupee a payment gateway?", prompt)
        self.assertIn("(page /services/payouts)", prompt)
        self.assertNotIn(".svg", prompt)
        self.assertNotIn("/images/", prompt)


@override_settings(CACHES=TEST_CACHES, GEMINI_API_KEY="", OPENAI_API_KEY="", ALLOWED_HOSTS=["localhost"])
class ChatEndpointTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(HTTP_HOST="localhost")

    def post(self, message, **extra):
        return self.client.post("/api/chat/", {"message": message, **extra}, format="json")

    def test_keyword_fallback_streams_and_saves_both_messages(self):
        response = self.post("Is Urbanrupee a payment gateway?", page_path="/about")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream; charset=utf-8")
        self.assertEqual(response["X-Accel-Buffering"], "no")
        events = parse_events(response)
        self.assertEqual([name for name, _ in events], ["meta", "delta", "done"])
        self.assertIn("not a payment gateway", reply_text(events))

        conversation = ChatConversation.objects.get(public_id=events[0][1]["conversation_id"])
        self.assertEqual(conversation.page_path, "/about")
        self.assertEqual(conversation.user_message_count, 1)
        roles = list(conversation.messages.values_list("role", "ai_generated"))
        self.assertEqual(roles, [("user", False), ("assistant", False)])

    def test_browser_event_stream_accept_header(self):
        response = self.client.post(
            "/api/chat/",
            {"message": "What is Urbanrupee?"},
            format="json",
            HTTP_ACCEPT="text/event-stream",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parse_events(response)[-1][0], "done")

        error = self.client.post(
            "/api/chat/", {"message": ""}, format="json", HTTP_ACCEPT="text/event-stream"
        )
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.json()["detail"], "Message is required.")

    def test_validation_errors(self):
        self.assertEqual(self.post("   ").status_code, 400)
        self.assertEqual(self.post("x" * 501).status_code, 400)
        self.assertEqual(ChatConversation.objects.count(), 0)

    def test_invalid_page_path_is_dropped(self):
        events = parse_events(self.post("hello", page_path="javascript:alert(1)"))
        conversation = ChatConversation.objects.get(public_id=events[0][1]["conversation_id"])
        self.assertEqual(conversation.page_path, "")

    def test_card_number_is_redacted_before_saving(self):
        parse_events(self.post("charged twice on 4111-1111-1111-1111"))
        stored = ChatMessage.objects.get(role="user").content
        self.assertNotIn("4111", stored)
        self.assertIn(chatbot.REDACTED_NUMBER, stored)

    def test_unknown_conversation_id_starts_new_chat(self):
        events = parse_events(self.post("hello", conversation_id="not-a-uuid"))
        self.assertTrue(ChatConversation.objects.filter(public_id=events[0][1]["conversation_id"]).exists())

    @override_settings(CHAT_RATE_LIMIT=2)
    def test_rate_limit_per_ip(self):
        self.assertEqual(self.post("one").status_code, 200)
        self.assertEqual(self.post("two").status_code, 200)
        response = self.post("three")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response["Retry-After"], "60")
        self.assertIn("wait a minute", response.json()["detail"])

    @override_settings(CHAT_MAX_USER_MESSAGES=3)
    def test_conversation_length_limit(self):
        conversation = ChatConversation.objects.create(user_message_count=3)
        response = self.post("more", conversation_id=str(conversation.public_id))
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["code"], "conversation_limit")


@override_settings(
    CACHES=TEST_CACHES,
    GEMINI_API_KEY="",
    OPENAI_API_KEY="sk-test",
    OPENAI_MODEL="gpt-test",
    OPENAI_REASONING_EFFORT="low",
    ALLOWED_HOSTS=["localhost"],
)
class ChatAITests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(HTTP_HOST="localhost")

    def post(self, message, **extra):
        return self.client.post("/api/chat/", {"message": message, **extra}, format="json")

    def test_streams_ai_reply_and_strips_lead_marker(self):
        with patch.object(chatbot, "_openai_stream", return_value=iter(["Sure, ", "our team can help.\n[[LE", "AD]]"])):
            events = parse_events(self.post("I want a demo"))

        self.assertNotIn("[[", reply_text(events))
        self.assertEqual(events[-1], ("done", {"sources": events[-1][1]["sources"], "offer_lead": True}))
        assistant = ChatMessage.objects.get(role="assistant")
        self.assertEqual(assistant.content, "Sure, our team can help.")
        self.assertTrue(assistant.ai_generated)

    def test_lead_not_offered_again_after_submission(self):
        conversation = ChatConversation.objects.create(lead_submitted_at=timezone.now())
        with patch.object(chatbot, "_openai_stream", return_value=iter(["Okay [[LEAD]]"])):
            events = parse_events(self.post("pricing?", conversation_id=str(conversation.public_id)))
        self.assertFalse(events[-1][1]["offer_lead"])

    def test_follow_up_sends_history_and_settings_to_openai(self):
        captured = {}

        def create(**params):
            captured.update(params)
            return fake_chunks("Second answer")

        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        with patch.object(chatbot, "_openai_client", return_value=fake_client):
            first = parse_events(self.post("What is payment orchestration?"))
            conversation_id = first[0][1]["conversation_id"]
            second = parse_events(self.post("How long does it take?", conversation_id=conversation_id))

        self.assertEqual(second[0][1]["conversation_id"], conversation_id)
        self.assertEqual(captured["model"], "gpt-test")
        self.assertEqual(captured["reasoning_effort"], "low")
        self.assertTrue(captured["stream"])
        messages = captured["messages"]
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(
            [(m["role"], m["content"]) for m in messages[1:]],
            [
                ("user", "What is payment orchestration?"),
                ("assistant", "Second answer"),
                ("user", "How long does it take?"),
            ],
        )
        self.assertEqual(ChatConversation.objects.get().user_message_count, 2)

    def test_chosen_language_is_sent_after_system_prompt(self):
        calls = []

        def create(**params):
            calls.append(params["messages"])
            return fake_chunks("नमस्ते")

        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        with patch.object(chatbot, "_openai_client", return_value=fake_client):
            parse_events(self.post("What is UPI?", language=" HI "))
            parse_events(self.post("What is UPI?", language="xx"))
            parse_events(self.post("What is UPI?"))

        hindi, unknown, missing = calls
        self.assertEqual(hindi[0]["content"], chatbot.SYSTEM_PROMPT)
        self.assertEqual(hindi[1]["role"], "system")
        self.assertIn("Hindi, written in Devanagari script", hindi[1]["content"])
        self.assertEqual(hindi[2], {"role": "user", "content": "What is UPI?"})
        for messages in (unknown, missing):
            self.assertEqual([m["role"] for m in messages], ["system", "user"])

    def test_ai_failure_before_any_text_falls_back_to_keywords(self):
        with patch.object(chatbot, "_openai_stream", side_effect=RuntimeError("api down")):
            events = parse_events(self.post("Is Urbanrupee a payment gateway?"))

        self.assertIn("not a payment gateway", reply_text(events))
        self.assertFalse(ChatMessage.objects.get(role="assistant").ai_generated)

    def test_ai_failure_mid_reply_keeps_partial_text(self):
        def broken():
            yield "Partial answer"
            raise RuntimeError("connection reset")

        with patch.object(chatbot, "_openai_stream", return_value=broken()):
            events = parse_events(self.post("Tell me about payouts"))

        text = reply_text(events)
        self.assertTrue(text.startswith("Partial answer"))
        self.assertIn(chatbot.INTERRUPTED_NOTE, text)
        self.assertEqual(events[-1][0], "done")

    @override_settings(CHAT_DAILY_AI_LIMIT=1)
    def test_daily_ai_budget_falls_back_to_keywords(self):
        with patch.object(chatbot, "_openai_stream", return_value=iter(["AI answer"])) as stream:
            parse_events(self.post("first"))
            events = parse_events(self.post("Is Urbanrupee a payment gateway?"))
        self.assertEqual(stream.call_count, 1)
        self.assertIn("not a payment gateway", reply_text(events))

    @override_settings(CHAT_AI_RATE_LIMIT=1)
    def test_per_ip_ai_allowance_falls_back_to_keywords_without_blocking(self):
        with patch.object(chatbot, "_openai_stream", return_value=iter(["AI answer"])) as stream:
            parse_events(self.post("first"))
            response = self.post("Is Urbanrupee a payment gateway?")
            events = parse_events(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(stream.call_count, 1)
        self.assertIn("not a payment gateway", reply_text(events))

    @override_settings(CHAT_AI_RATE_LIMIT=1)
    def test_per_ip_ai_allowance_is_per_ip(self):
        def post_from(ip, message):
            return self.client.post("/api/chat/", {"message": message}, format="json", REMOTE_ADDR=ip)

        with patch.object(chatbot, "_openai_stream", side_effect=lambda *a: iter(["AI answer"])) as stream:
            parse_events(post_from("10.0.0.1", "first"))
            events = parse_events(post_from("10.0.0.2", "second"))
        self.assertEqual(stream.call_count, 2)
        self.assertEqual(reply_text(events), "AI answer")

    def test_reasoning_effort_omitted_when_blank(self):
        captured = {}

        def create(**params):
            captured.update(params)
            return fake_chunks("ok")

        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        with override_settings(OPENAI_REASONING_EFFORT=""), patch.object(
            chatbot, "_openai_client", return_value=fake_client
        ):
            parse_events(self.post("hi"))
        self.assertNotIn("reasoning_effort", captured)

    def test_openai_sends_its_cache_and_safety_fields(self):
        captured = {}

        def create(**params):
            captured.update(params)
            return fake_chunks("ok")

        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        with patch.object(chatbot, "_openai_client", return_value=fake_client) as make_client:
            parse_events(self.post("hi"))
        self.assertEqual(make_client.call_args.args[0].name, "openai")
        self.assertEqual(captured["prompt_cache_key"], "urbanrupee-site-chat")
        self.assertEqual(len(captured["safety_identifier"]), 32)


def status_error(cls, status_code):
    error = cls.__new__(cls)
    Exception.__init__(error, "model error")
    error.status_code = status_code
    return error


@override_settings(
    CACHES=TEST_CACHES,
    GEMINI_API_KEY="gem-test",
    GEMINI_MODEL="gemini-main",
    GEMINI_FALLBACK_MODELS=["gemini-backup", "gemini-main"],
    GEMINI_REASONING_EFFORT="low",
    OPENAI_API_KEY="sk-test",
    ALLOWED_HOSTS=["localhost"],
)
class ChatGeminiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(HTTP_HOST="localhost")

    def post(self, message):
        return self.client.post("/api/chat/", {"message": message}, format="json")

    def run_with(self, create):
        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        with patch.object(chatbot, "_openai_client", return_value=fake_client) as make_client:
            events = parse_events(self.post("What is MDR?"))
        return events, make_client

    def test_gemini_preferred_and_openai_only_fields_omitted(self):
        calls = []

        def create(**params):
            calls.append(params)
            return fake_chunks("MDR is the merchant discount rate.")

        events, make_client = self.run_with(create)

        provider = make_client.call_args.args[0]
        self.assertEqual(provider.name, "gemini")
        self.assertIn("generativelanguage.googleapis.com", provider.base_url)
        self.assertEqual(provider.models, ("gemini-main", "gemini-backup"))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["model"], "gemini-main")
        self.assertEqual(calls[0]["reasoning_effort"], "low")
        self.assertNotIn("prompt_cache_key", calls[0])
        self.assertNotIn("safety_identifier", calls[0])
        self.assertEqual(reply_text(events), "MDR is the merchant discount rate.")
        self.assertTrue(ChatMessage.objects.get(role="assistant").ai_generated)

    def test_overloaded_model_falls_back_to_next(self):
        models = []

        def create(**params):
            models.append(params["model"])
            if params["model"] == "gemini-main":
                raise status_error(openai.InternalServerError, 503)
            return fake_chunks("Backup answer")

        events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main", "gemini-backup"])
        self.assertEqual(reply_text(events), "Backup answer")

    def test_bad_request_does_not_try_other_models(self):
        models = []

        def create(**params):
            models.append(params["model"])
            raise status_error(openai.BadRequestError, 400)

        events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main"])
        self.assertFalse(ChatMessage.objects.get(role="assistant").ai_generated)
        self.assertTrue(reply_text(events))

    def test_overloaded_models_tried_twice_then_keyword_answer(self):
        models = []

        def create(**params):
            models.append(params["model"])
            raise status_error(openai.InternalServerError, 503)

        events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main", "gemini-backup", "gemini-main", "gemini-backup"])
        self.assertTrue(reply_text(events))
        self.assertFalse(ChatMessage.objects.get(role="assistant").ai_generated)

    def test_rate_limited_model_skipped_by_later_chats(self):
        models = []

        def create(**params):
            models.append(params["model"])
            if params["model"] == "gemini-main":
                raise status_error(openai.RateLimitError, 429)
            return fake_chunks("From backup")

        first, _ = self.run_with(create)
        second, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main", "gemini-backup", "gemini-backup"])
        self.assertEqual(reply_text(first), "From backup")
        self.assertEqual(reply_text(second), "From backup")

    def test_all_models_cooling_down_uses_keyword_answer_without_calls(self):
        models = []

        def create(**params):
            models.append(params["model"])
            raise status_error(openai.RateLimitError, 429)

        self.run_with(create)
        self.assertEqual(models, ["gemini-main", "gemini-backup"])

        events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main", "gemini-backup"])
        self.assertTrue(reply_text(events))
        self.assertFalse(ChatMessage.objects.filter(ai_generated=True).exists())

    def test_retired_model_is_not_retried(self):
        models = []

        def create(**params):
            models.append(params["model"])
            if params["model"] == "gemini-main":
                raise status_error(openai.NotFoundError, 404)
            if models.count("gemini-backup") == 1:
                raise status_error(openai.InternalServerError, 503)
            return fake_chunks("Second try")

        events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main", "gemini-backup", "gemini-backup"])
        self.assertEqual(reply_text(events), "Second try")

    def test_no_new_attempt_after_retry_budget(self):
        models = []

        def create(**params):
            models.append(params["model"])
            raise status_error(openai.InternalServerError, 503)

        with patch.object(chatbot, "_MODEL_RETRY_BUDGET_SECONDS", -1):
            events, _ = self.run_with(create)

        self.assertEqual(models, ["gemini-main"])
        self.assertFalse(ChatMessage.objects.get(role="assistant").ai_generated)

    @override_settings(GEMINI_API_KEY="", OPENAI_MODEL="gpt-test")
    def test_openai_retries_its_single_model_once(self):
        models = []

        def create(**params):
            models.append(params["model"])
            if len(models) == 1:
                raise status_error(openai.InternalServerError, 503)
            return fake_chunks("Recovered")

        events, make_client = self.run_with(create)

        self.assertEqual(make_client.call_args.args[0].name, "openai")
        self.assertEqual(models, ["gpt-test", "gpt-test"])
        self.assertEqual(reply_text(events), "Recovered")


@override_settings(
    CACHES=TEST_CACHES,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL_TO="sales@example.com",
    ALLOWED_HOSTS=["localhost"],
)
class ChatLeadTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(HTTP_HOST="localhost")
        self.conversation = ChatConversation.objects.create(page_path="/products/orchestration")
        ChatMessage.objects.create(conversation=self.conversation, role="user", content="Need pricing")
        ChatMessage.objects.create(conversation=self.conversation, role="assistant", content="Happy to help")

    def post(self, **data):
        return self.client.post("/api/chat/lead/", data, format="json")

    def test_lead_saved_and_emailed_with_transcript(self):
        response = self.post(**LEAD, note="Call after 5pm", conversation_id=str(self.conversation.public_id))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Asha", response.json()["message"])
        self.conversation.refresh_from_db()
        self.assertEqual(self.conversation.lead_kind, "lead")
        self.assertEqual(self.conversation.lead_phone, "9876543210")
        self.assertIsNotNone(self.conversation.lead_submitted_at)

        sent = mail.outbox[0]
        self.assertEqual(sent.to, ["sales@example.com"])
        self.assertEqual(sent.reply_to, ["asha@example.com"])
        self.assertEqual(sent.subject, "[Urbanrupee Chat] New lead: Asha Rao")
        self.assertIn("Visitor: Need pricing", sent.body)
        self.assertIn("Assistant: Happy to help", sent.body)
        self.assertIn("Call after 5pm", sent.body)
        self.assertIn("/products/orchestration", sent.body)

    def test_handoff_without_chat_creates_conversation(self):
        response = self.post(**LEAD, kind="handoff", page_path="/contact")

        self.assertEqual(response.status_code, 200)
        conversation = ChatConversation.objects.get(public_id=response.json()["conversation_id"])
        self.assertEqual(conversation.lead_kind, "handoff")
        self.assertEqual(conversation.page_path, "/contact")
        self.assertTrue(mail.outbox[0].subject.startswith("[Urbanrupee Chat] Visitor asked for a human"))
        self.assertIn("had not sent any chat messages", mail.outbox[0].body)

    def test_invalid_fields_rejected(self):
        response = self.post(name="A1", email="bad", phone="12345", kind="other", note="x" * 501)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["errors"]), {"name", "email", "phone", "kind", "note"})
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_fields_rejected(self):
        response = self.post(name="Asha Rao")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["detail"])

    def test_email_failure_still_saves_lead(self):
        with patch("website.views.send_chat_lead_email", side_effect=OSError("smtp down")):
            response = self.post(**LEAD, conversation_id=str(self.conversation.public_id))
        self.assertEqual(response.status_code, 200)
        self.conversation.refresh_from_db()
        self.assertEqual(self.conversation.lead_email, "asha@example.com")

    @override_settings(CHAT_LEAD_RATE_LIMIT=1)
    def test_lead_rate_limit(self):
        self.assertEqual(self.post(**LEAD).status_code, 200)
        self.assertEqual(self.post(**LEAD).status_code, 429)


@override_settings(
    CACHES=TEST_CACHES,
    ADMIN_DASHBOARD_USERNAME="admin",
    ADMIN_DASHBOARD_PASSWORD="secret-pass",
)
class AdminChatTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.lead = ChatConversation.objects.create(
            user_message_count=1,
            lead_kind="handoff",
            lead_name="Asha Rao",
            lead_email="asha@example.com",
            lead_phone="9876543210",
            lead_submitted_at=timezone.now(),
        )
        ChatMessage.objects.create(conversation=self.lead, role="user", content="Talk to sales")
        self.plain = ChatConversation.objects.create(user_message_count=1)
        ChatMessage.objects.create(conversation=self.plain, role="user", content="What is UPI?")
        ChatConversation.objects.create()  # opened but never used; hidden from the list

    def login(self):
        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
        )

    def test_requires_admin_session(self):
        self.assertEqual(self.client.get("/api/admin/chats/").status_code, 401)
        self.assertEqual(
            self.client.get(f"/api/admin/chats/{self.lead.public_id}/").status_code,
            401,
        )

    def test_list_and_filters(self):
        self.login()
        data = self.client.get("/api/admin/chats/").json()
        self.assertEqual(data["total"], 2)
        previews = {row["first_message"] for row in data["results"]}
        self.assertEqual(previews, {"Talk to sales", "What is UPI?"})

        leads = self.client.get("/api/admin/chats/?filter=leads").json()
        self.assertEqual([row["id"] for row in leads["results"]], [str(self.lead.public_id)])
        self.assertEqual(leads["results"][0]["lead"]["phone"], "9876543210")

        bad = self.client.get("/api/admin/chats/?filter=nope&page=abc").json()
        self.assertEqual((bad["filter"], bad["page"]), ("all", 1))

    def test_detail(self):
        self.login()
        data = self.client.get(f"/api/admin/chats/{self.plain.public_id}/").json()
        self.assertEqual(data["messages"][0]["content"], "What is UPI?")
        self.assertIsNone(data["lead"])

        missing = self.client.get("/api/admin/chats/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(missing.status_code, 404)


class PurgeChatLogsTests(TestCase):
    def test_deletes_only_old_chats(self):
        old = ChatConversation.objects.create()
        ChatMessage.objects.create(conversation=old, role="user", content="old")
        ChatConversation.objects.filter(pk=old.pk).update(updated_at=timezone.now() - timedelta(days=91))
        recent = ChatConversation.objects.create()

        call_command("purge_chat_logs", stdout=StringIO())

        self.assertFalse(ChatConversation.objects.filter(pk=old.pk).exists())
        self.assertFalse(ChatMessage.objects.filter(content="old").exists())
        self.assertTrue(ChatConversation.objects.filter(pk=recent.pk).exists())
