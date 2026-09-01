"""Tests for admin dashboard auth and payout proxy."""

from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from website.payin_dashboard import CACHE_KEY as PAYIN_CACHE_KEY
from website.payout_dashboard import CACHE_KEY

TEST_CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "admin-dashboard-tests",
    }
}


@override_settings(
    ADMIN_DASHBOARD_USERNAME="admin",
    ADMIN_DASHBOARD_PASSWORD="secret-pass",
    INTERNAL_DASHBOARD_API_KEY="test-internal-key",
    PAYOUT_DASHBOARD_API_URL="https://payout.example.test/api/internal/payout-dashboard",
    PAYOUT_DASHBOARD_LATEST_LIMIT=25,
    CACHES=TEST_CACHES,
)
class AdminDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        cache.clear()

    def _csrf_headers(self):
        response = self.client.get("/api/admin/me/")
        token = self.client.cookies["csrftoken"].value
        return {"HTTP_X_CSRFTOKEN": token}

    def test_me_unauthenticated(self):
        response = self.client.get("/api/admin/me/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["authenticated"])

    def test_login_failure(self):
        response = self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "wrong"},
            format="json",
            **self._csrf_headers(),
        )
        self.assertEqual(response.status_code, 401)

    def test_login_success(self):
        response = self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["authenticated"])

        me = self.client.get("/api/admin/me/")
        self.assertTrue(me.json()["authenticated"])

    def test_proxy_requires_auth(self):
        response = self.client.get("/api/admin/payout-dashboard/")
        self.assertEqual(response.status_code, 401)

    def test_proxy_returns_cached_summary(self):
        cache.set(
            CACHE_KEY,
            {
                "ok": True,
                "generated_at": "2026-06-24T10:00:00+00:00",
                "summary": {"today_success_with_fees": 100.0},
            },
            timeout=30,
        )

        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )

        with patch("website.payout_dashboard.requests.get") as mock_get:
            response = self.client.get("/api/admin/payout-dashboard/")
            mock_get.assert_not_called()

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["summary"]["today_success_with_fees"], 100.0)

    def test_proxy_returns_503_when_cache_empty(self):
        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )

        response = self.client.get("/api/admin/payout-dashboard/")
        self.assertEqual(response.status_code, 503)

    def test_payin_proxy_requires_auth(self):
        response = self.client.get("/api/admin/payin-dashboard/")
        self.assertEqual(response.status_code, 401)

    def test_payin_proxy_returns_cached_summary(self):
        cache.set(
            PAYIN_CACHE_KEY,
            {
                "ok": True,
                "generated_at": "2026-06-24T10:00:00+00:00",
                "summary": {"today_success_amount": 250.0},
            },
            timeout=30,
        )

        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )

        with patch("website.payin_dashboard.requests.get") as mock_get:
            response = self.client.get("/api/admin/payin-dashboard/")
            mock_get.assert_not_called()

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["summary"]["today_success_amount"], 250.0)

    @override_settings(INTERNAL_DASHBOARD_API_KEY="")
    def test_refresh_reports_missing_key(self):
        from website.payout_dashboard import refresh_payout_dashboard_snapshot

        ok, detail = refresh_payout_dashboard_snapshot()
        self.assertFalse(ok)
        self.assertIn("not configured", detail.lower())
