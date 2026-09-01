"""Tests for dashboard upstream fetch limits."""

from django.test import SimpleTestCase, override_settings

from website.dashboard_fetch import upstream_latest_limit


class DashboardFetchLimitTests(SimpleTestCase):
    @override_settings(DASHBOARD_MAP_MERCHANT_TXN_LIMIT=100)
    def test_upstream_limit_never_below_map_floor(self):
        self.assertEqual(upstream_latest_limit(1), 100)
        self.assertEqual(upstream_latest_limit(25), 100)
        self.assertEqual(upstream_latest_limit(100), 100)
        self.assertEqual(upstream_latest_limit(250), 250)
