"""Tests for admin dashboard auth and payout proxy."""

from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient


@override_settings(
    ADMIN_DASHBOARD_USERNAME="admin",
    ADMIN_DASHBOARD_PASSWORD="secret-pass",
    INTERNAL_DASHBOARD_API_KEY="test-internal-key",
    PAYOUT_DASHBOARD_API_URL="https://payout.example.test/api/internal/payout-dashboard",
    PAYOUT_DASHBOARD_LATEST_LIMIT=25,
)
class AdminDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

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

    @patch("website.admin_views.requests.get")
    def test_proxy_returns_summary(self, mock_get):
        mock_get.return_value = MagicMock(
            ok=True,
            status_code=200,
            json=lambda: {
                "ok": True,
                "generated_at": "2026-06-24T10:00:00+00:00",
                "summary": {"today_success_with_fees": 100.0},
            },
        )

        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )

        response = self.client.get("/api/admin/payout-dashboard/")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["summary"]["today_success_with_fees"], 100.0)
        mock_get.assert_called_once()

    @patch("website.admin_views.requests.get")
    def test_proxy_handles_upstream_401(self, mock_get):
        mock_get.return_value = MagicMock(ok=False, status_code=401)

        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )

        response = self.client.get("/api/admin/payout-dashboard/")
        self.assertEqual(response.status_code, 502)

    @override_settings(INTERNAL_DASHBOARD_API_KEY="")
    def test_proxy_handles_missing_key(self):
        self.client.post(
            "/api/admin/login/",
            {"username": "admin", "password": "secret-pass"},
            format="json",
            **self._csrf_headers(),
        )
        response = self.client.get("/api/admin/payout-dashboard/")
        self.assertEqual(response.status_code, 503)
