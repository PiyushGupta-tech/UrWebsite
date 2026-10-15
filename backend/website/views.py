import logging
import re
import uuid

from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import chatbot
from .homepage import homepage_payload
from .models import ChatConversation
from .page_api import page_detail_payload, site_payload
from .seo_audit import run_seo_audit
from .contact import send_chat_lead_email, send_contact_email

logger = logging.getLogger(__name__)

PHONE_RE = re.compile(r"^[6-9][0-9]{9}$")
NAME_RE = re.compile(r"^[A-Za-z ]+$")
PAGE_PATH_RE = re.compile(r"^/[\w\-./]{0,199}$")


def validate_person_fields(*, name, email, phone):
    """Shared name/email/phone rules for the contact form and chat lead form."""
    errors = {}

    if len(name) < 2 or len(name) > 50 or not NAME_RE.fullmatch(name):
        errors["name"] = "Full Name can contain only letters and spaces, and must be 2 to 50 characters."

    if len(email) > 254 or email.count("@") != 1:
        errors["email"] = "Email Address must contain exactly one @ and be at most 254 characters."
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Enter a valid email address."

    if not PHONE_RE.fullmatch(phone):
        errors["phone"] = "Phone Number must be 10 digits and start with 6, 7, 8, or 9."

    return errors


def _request_data(request):
    return request.data if isinstance(request.data, dict) else {}


def _clean_page_path(value) -> str:
    path = str(value or "").strip()
    return path if PAGE_PATH_RE.fullmatch(path) else ""


def _find_conversation(raw_id):
    try:
        public_id = uuid.UUID(str(raw_id))
    except (TypeError, ValueError):
        return None
    return ChatConversation.objects.filter(public_id=public_id).first()


class SiteAPIView(APIView):
    """Shared site metadata and navigation."""

    def get(self, request):
        return Response(site_payload())


class HomepageAPIView(APIView):
    """Aggregated homepage content for the Vue SPA."""

    def get(self, request):
        return Response(homepage_payload())


class ContactSubmitAPIView(APIView):
    """Accept contact form submissions and email the support inbox."""

    REQUIRED_FIELDS = ("name", "email", "phone", "subject", "message")

    def _validate_payload(self, payload):
        errors = validate_person_fields(
            name=payload["name"],
            email=payload["email"],
            phone=payload["phone"],
        )

        subject = payload["subject"]
        if len(subject) < 3 or len(subject) > 120:
            errors["subject"] = "Subject must be 3 to 120 characters."

        message = payload["message"]
        if len(message) < 10 or len(message) > 500:
            errors["message"] = "Message must be 10 to 500 characters."

        return errors

    def post(self, request):
        payload = {field: str(request.data.get(field, "")).strip() for field in self.REQUIRED_FIELDS}
        missing = [field for field, value in payload.items() if not value]
        if missing:
            return Response(
                {"detail": f"Missing required fields: {', '.join(missing)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_payload(payload)
        if errors:
            return Response(
                {"detail": "Please correct the highlighted fields.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_contact_email(**payload)
        except Exception:
            return Response(
                {"detail": "We could not send your message. Please try again or email us directly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"ok": True, "message": "Thank you! We'll get back to you shortly."})


class ChatAPIView(APIView):
    """Site assistant — streams an AI reply as server-sent events and keeps chat history."""

    def perform_content_negotiation(self, request, force=False):
        # Browsers send Accept: text/event-stream; JSON error responses must still render.
        return super().perform_content_negotiation(request, force=True)

    def post(self, request):
        data = _request_data(request)
        message = str(data.get("message", "")).strip()
        if not message:
            return Response(
                {"detail": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(message) > chatbot.MAX_MESSAGE_LENGTH:
            return Response(
                {"detail": f"Message must be {chatbot.MAX_MESSAGE_LENGTH} characters or fewer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = _find_conversation(data.get("conversation_id"))
        if conversation and conversation.user_message_count >= settings.CHAT_MAX_USER_MESSAGES:
            return Response(
                {
                    "detail": "This chat has reached its length limit. Please start a new chat.",
                    "code": "conversation_limit",
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        if not chatbot.allow_chat_message(request):
            response = Response(
                {"detail": "You're sending messages very fast. Please wait a minute and try again."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
            response["Retry-After"] = str(settings.CHAT_RATE_WINDOW_SECONDS)
            return response
        use_ai = chatbot.ai_enabled() and chatbot.allow_ai_reply(request)

        if conversation is None:
            conversation = ChatConversation.objects.create(
                page_path=_clean_page_path(data.get("page_path")),
            )

        clean_message = chatbot.redact(message)
        chatbot.record_user_message(conversation, clean_message)

        response = StreamingHttpResponse(
            chatbot.stream_reply(
                conversation,
                clean_message,
                chatbot.clean_language(data.get("language")),
                use_ai=use_ai,
            ),
            content_type="text/event-stream; charset=utf-8",
        )
        response["Cache-Control"] = "no-cache"
        # Stops nginx buffering so text reaches the browser as it is generated.
        response["X-Accel-Buffering"] = "no"
        return response


class ChatLeadAPIView(APIView):
    """Save a chat visitor's contact details and email them to the sales inbox."""

    def post(self, request):
        data = _request_data(request)
        payload = {field: str(data.get(field, "")).strip() for field in ("name", "email", "phone")}
        missing = [field for field, value in payload.items() if not value]
        if missing:
            return Response(
                {"detail": f"Missing required fields: {', '.join(missing)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = validate_person_fields(**payload)
        note = str(data.get("note", "")).strip()
        if len(note) > 500:
            errors["note"] = "Message must be 500 characters or fewer."
        kind = str(data.get("kind", ChatConversation.LEAD_KIND_LEAD))
        if kind not in (ChatConversation.LEAD_KIND_LEAD, ChatConversation.LEAD_KIND_HANDOFF):
            errors["kind"] = "Unknown request type."
        if errors:
            return Response(
                {"detail": "Please correct the highlighted fields.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not chatbot.allow_lead_submission(request):
            return Response(
                {"detail": "Too many requests. Please try again later or use the contact page."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        conversation = _find_conversation(data.get("conversation_id"))
        if conversation is None:
            conversation = ChatConversation(page_path=_clean_page_path(data.get("page_path")))
        conversation.lead_kind = kind
        conversation.lead_name = payload["name"]
        conversation.lead_email = payload["email"]
        conversation.lead_phone = payload["phone"]
        conversation.lead_note = chatbot.redact(note)[:500]
        conversation.lead_submitted_at = timezone.now()
        conversation.save()

        transcript = list(conversation.messages.order_by("-created_at", "-id")[:60])[::-1]
        try:
            send_chat_lead_email(conversation=conversation, transcript=transcript)
        except Exception:
            # Details are already saved and visible on the admin chats page.
            logger.exception("Chat lead email failed for conversation %s", conversation.public_id)

        first_name = payload["name"].split()[0]
        return Response(
            {
                "ok": True,
                "conversation_id": str(conversation.public_id),
                "message": f"Thanks, {first_name}! Our team will reach out to you shortly.",
            }
        )


class PageDetailAPIView(APIView):
    """Single inner page by slug."""

    def get(self, request, slug):
        payload = page_detail_payload(slug)
        if not payload:
            return Response({"detail": "Page not found."}, status=404)
        return Response(payload)


class SeoAuditAPIView(APIView):
    """Phase 7 — SEO audit report for CI or pre-deploy checks."""

    def get(self, request):
        return Response(run_seo_audit())
