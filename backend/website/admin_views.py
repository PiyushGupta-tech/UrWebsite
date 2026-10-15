"""Session-based admin dashboard auth, cached payout API, and saved chat review."""

from __future__ import annotations

import secrets
import time

from django.conf import settings
from django.db.models import OuterRef, Q, Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from website.models import ChatConversation, ChatMessage
from website.payin_dashboard import get_cached_snapshot as get_payin_cached_snapshot
from website.payout_dashboard import get_cached_snapshot

ADMIN_SESSION_KEY = "admin_dashboard_auth"
LOGIN_ATTEMPTS: dict[str, list[float]] = {}
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _is_authenticated(request) -> bool:
    return bool(request.session.get(ADMIN_SESSION_KEY))


def _credentials_configured() -> bool:
    return bool(settings.ADMIN_DASHBOARD_USERNAME and settings.ADMIN_DASHBOARD_PASSWORD)


def _throttle_login(request) -> bool:
    """Return True if login attempt is allowed."""
    ip = _client_ip(request)
    now = time.time()
    attempts = [t for t in LOGIN_ATTEMPTS.get(ip, []) if now - t < LOGIN_WINDOW_SECONDS]
    LOGIN_ATTEMPTS[ip] = attempts
    return len(attempts) < MAX_LOGIN_ATTEMPTS


def _record_failed_login(request) -> None:
    ip = _client_ip(request)
    LOGIN_ATTEMPTS.setdefault(ip, []).append(time.time())


def _valid_credentials(username: str, password: str) -> bool:
    if not _credentials_configured():
        return False
    user_ok = secrets.compare_digest(username, settings.ADMIN_DASHBOARD_USERNAME)
    pass_ok = secrets.compare_digest(password, settings.ADMIN_DASHBOARD_PASSWORD)
    return user_ok and pass_ok


class AdminMeAPIView(APIView):
    """Return whether the browser session is authenticated for admin."""

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"authenticated": _is_authenticated(request)})


class AdminLoginAPIView(APIView):
    """Validate env credentials and create a session."""

    @method_decorator(csrf_protect)
    def post(self, request):
        if not _credentials_configured():
            return Response(
                {"detail": "Admin login is not configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not _throttle_login(request):
            return Response(
                {"detail": "Too many login attempts. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        username = str(request.data.get("username", "")).strip()
        password = str(request.data.get("password", ""))

        if not _valid_credentials(username, password):
            _record_failed_login(request)
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.session[ADMIN_SESSION_KEY] = True
        request.session.set_expiry(60 * 60 * 12)
        return Response({"ok": True, "authenticated": True})


class AdminLogoutAPIView(APIView):
    """Destroy admin session."""

    @method_decorator(csrf_protect)
    def post(self, request):
        request.session.pop(ADMIN_SESSION_KEY, None)
        return Response({"ok": True, "authenticated": False})


class AdminPayoutDashboardAPIView(APIView):
    """Serve cached payout dashboard snapshot (refreshed by background worker)."""

    def get(self, request):
        if not _is_authenticated(request):
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data, code, detail = get_cached_snapshot()
        if data is None:
            return Response({"detail": detail}, status=code)
        return Response(data)


CHAT_PAGE_SIZE = 25
CHAT_FILTERS = ("all", "leads", "handoff")


def _chat_summary(conversation) -> dict:
    lead = None
    if conversation.lead_submitted_at:
        lead = {
            "kind": conversation.lead_kind,
            "name": conversation.lead_name,
            "email": conversation.lead_email,
            "phone": conversation.lead_phone,
            "note": conversation.lead_note,
            "submitted_at": conversation.lead_submitted_at.isoformat(),
        }
    return {
        "id": str(conversation.public_id),
        "started_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "page_path": conversation.page_path,
        "message_count": conversation.user_message_count,
        "lead": lead,
    }


class AdminChatListAPIView(APIView):
    """Paginated list of saved website chats, newest activity first."""

    def get(self, request):
        if not _is_authenticated(request):
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        chat_filter = request.query_params.get("filter", "all")
        if chat_filter not in CHAT_FILTERS:
            chat_filter = "all"
        try:
            page = max(1, int(request.query_params.get("page", "1")))
        except ValueError:
            page = 1

        first_user_message = (
            ChatMessage.objects.filter(conversation=OuterRef("pk"), role=ChatMessage.ROLE_USER)
            .order_by("created_at", "id")
            .values("content")[:1]
        )
        conversations = ChatConversation.objects.filter(
            Q(user_message_count__gt=0) | Q(lead_submitted_at__isnull=False)
        )
        if chat_filter == "leads":
            conversations = conversations.filter(lead_submitted_at__isnull=False)
        elif chat_filter == "handoff":
            conversations = conversations.filter(lead_kind=ChatConversation.LEAD_KIND_HANDOFF)

        total = conversations.count()
        pages = max(1, -(-total // CHAT_PAGE_SIZE))
        page = min(page, pages)
        start = (page - 1) * CHAT_PAGE_SIZE
        rows = conversations.annotate(first_message=Subquery(first_user_message)).order_by(
            "-updated_at"
        )[start : start + CHAT_PAGE_SIZE]

        results = []
        for conversation in rows:
            summary = _chat_summary(conversation)
            summary["first_message"] = (conversation.first_message or "")[:160]
            results.append(summary)

        return Response(
            {
                "results": results,
                "page": page,
                "pages": pages,
                "total": total,
                "filter": chat_filter,
            }
        )


class AdminChatDetailAPIView(APIView):
    """Full transcript of one saved chat."""

    def get(self, request, chat_id):
        if not _is_authenticated(request):
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        conversation = ChatConversation.objects.filter(public_id=chat_id).first()
        if conversation is None:
            return Response({"detail": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        payload = _chat_summary(conversation)
        payload["messages"] = [
            {
                "role": message.role,
                "content": message.content,
                "sources": message.sources,
                "ai_generated": message.ai_generated,
                "created_at": message.created_at.isoformat(),
            }
            for message in conversation.messages.all()
        ]
        return Response(payload)


class AdminPayinDashboardAPIView(APIView):
    """Serve cached payin dashboard snapshot (refreshed by background worker)."""

    def get(self, request):
        if not _is_authenticated(request):
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data, code, detail = get_payin_cached_snapshot()
        if data is None:
            return Response({"detail": detail}, status=code)
        return Response(data)
