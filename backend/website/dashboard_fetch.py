"""Shared helpers for dashboard upstream fetch limits."""

from __future__ import annotations

from django.conf import settings


def upstream_latest_limit(configured_limit: int) -> int:
    """Never fetch fewer txns than needed to resolve map merchant names."""
    floor = getattr(settings, "DASHBOARD_MAP_MERCHANT_TXN_LIMIT", 100)
    return max(int(configured_limit or 0), int(floor or 0))
