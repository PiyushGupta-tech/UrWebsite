"""Tests for payout dashboard cache refresh."""

from unittest.mock import MagicMock, patch

from django.core.cache import cache
from django.test import TestCase, override_settings

from website.payout_dashboard import (
    CACHE_KEY,
    META_KEY,
    fetch_upstream_snapshot,
    get_cached_snapshot,
    refresh_payout_dashboard_snapshot,
)

TEST_CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "payout-dashboard-tests",
    }
}


@override_settings(
    INTERNAL_DASHBOARD_API_KEY="test-internal-key",
    PAYOUT_DASHBOARD_API_URL="https://payout.example.test/api/internal/payout-dashboard",
    PAYOUT_DASHBOARD_LATEST_LIMIT=25,
    PAYOUT_DASHBOARD_CACHE_TTL=30,
    CACHES=TEST_CACHES,
)
class PayoutDashboardCacheTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch("website.payout_dashboard.requests.get")
    def test_fetch_upstream_success(self, mock_get):
        mock_get.return_value = MagicMock(
            ok=True,
            status_code=200,
            json=lambda: {
                "ok": True,
                "generated_at": "2026-06-24T10:00:00+00:00",
                "summary": {"today_success_with_fees": 100.0},
            },
        )

        data, code, detail = fetch_upstream_snapshot()
        self.assertEqual(code, 200)
        self.assertEqual(detail, "")
        self.assertEqual(data["summary"]["today_success_with_fees"], 100.0)

    @patch("website.payout_dashboard.requests.get")
    def test_refresh_stores_snapshot_in_cache(self, mock_get):
        mock_get.return_value = MagicMock(
            ok=True,
            status_code=200,
            json=lambda: {
                "ok": True,
                "generated_at": "2026-06-24T10:00:00+00:00",
                "summary": {"today_success_with_fees": 42.0},
            },
        )

        ok, detail = refresh_payout_dashboard_snapshot()
        self.assertTrue(ok)
        self.assertEqual(detail, "")

        cached, code, _ = get_cached_snapshot()
        self.assertEqual(code, 200)
        self.assertEqual(cached["summary"]["today_success_with_fees"], 42.0)
        self.assertIsNotNone(cache.get(META_KEY))

    def test_get_cached_snapshot_missing(self):
        data, code, detail = get_cached_snapshot()
        self.assertIsNone(data)
        self.assertEqual(code, 503)
        self.assertIn("not ready", detail.lower())

    @patch("website.payout_dashboard.requests.get")
    def test_refresh_failure_records_meta(self, mock_get):
        mock_get.return_value = MagicMock(ok=False, status_code=401)

        ok, detail = refresh_payout_dashboard_snapshot()
        self.assertFalse(ok)
        self.assertIn("credentials", detail.lower())

        data, code, _ = get_cached_snapshot()
        self.assertIsNone(data)
        self.assertEqual(code, 502)
