"""Session-based admin dashboard auth and cached payout API."""

from __future__ import annotations

import secrets
import time

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
