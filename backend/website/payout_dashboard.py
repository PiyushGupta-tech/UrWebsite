"""Fetch payout dashboard snapshots from the portal API and cache them server-side."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

CACHE_KEY = "payout_dashboard:snapshot"
META_KEY = "payout_dashboard:meta"


def fetch_upstream_snapshot() -> tuple[dict[str, Any] | None, int, str]:
    """Call the payout portal internal API (server-side key only)."""
    api_key = settings.INTERNAL_DASHBOARD_API_KEY
    if not api_key:
        return None, 503, "Payout dashboard is not configured."

    params = {"latest_limit": settings.PAYOUT_DASHBOARD_LATEST_LIMIT}
    headers = {"X-Internal-Key": api_key, "Accept": "application/json"}

    try:
        upstream = requests.get(
            settings.PAYOUT_DASHBOARD_API_URL,
            params=params,
            headers=headers,
            timeout=settings.PAYOUT_DASHBOARD_HTTP_TIMEOUT,
        )
    except requests.RequestException:
        logger.exception("Payout dashboard upstream request failed")
        return None, 502, "Could not reach payout dashboard."

    if upstream.status_code == 401:
        return None, 502, "Payout dashboard rejected credentials."
    if upstream.status_code == 403:
        return None, 502, "Payout dashboard blocked this server IP."
    if upstream.status_code == 503:
        return None, 503, "Payout dashboard is unavailable."
    if not upstream.ok:
        return None, 502, "Payout dashboard returned an error."

    try:
        payload = upstream.json()
    except ValueError:
        return None, 502, "Payout dashboard returned invalid JSON."

    if not payload.get("ok"):
        return None, 502, "Payout dashboard returned an error."

    return {
        "ok": True,
        "generated_at": payload.get("generated_at"),
        "summary": payload.get("summary") or {},
    }, 200, ""


def refresh_payout_dashboard_snapshot() -> tuple[bool, str]:
    """Fetch upstream and store the latest snapshot in Django cache."""
    data, code, detail = fetch_upstream_snapshot()
    ttl = settings.PAYOUT_DASHBOARD_CACHE_TTL

    if data is None:
        cache.set(
            META_KEY,
            {
                "ok": False,
                "detail": detail,
                "code": code,
                "failed_at": timezone.now().isoformat(),
            },
            timeout=ttl,
        )
        logger.warning("Payout dashboard refresh failed: %s", detail)
        return False, detail

    cache.set(CACHE_KEY, data, timeout=ttl)
    cache.set(
        META_KEY,
        {
            "ok": True,
            "refreshed_at": timezone.now().isoformat(),
            "generated_at": data.get("generated_at"),
        },
        timeout=ttl,
    )
    return True, ""


def get_cached_snapshot() -> tuple[dict[str, Any] | None, int, str]:
    """Return the cached snapshot for admin API consumers."""
    data = cache.get(CACHE_KEY)
    if data is not None:
        return data, 200, ""

    meta = cache.get(META_KEY) or {}
    detail = meta.get("detail") or "Dashboard snapshot is not ready yet."
    code = int(meta.get("code") or 503)
    return None, code, detail


def run_refresh_loop(interval: int | None = None) -> None:
    """Poll upstream forever — intended for a dedicated worker process."""
    sleep_seconds = interval or settings.PAYOUT_DASHBOARD_REFRESH_INTERVAL
    while True:
        refresh_payout_dashboard_snapshot()
        time.sleep(sleep_seconds)
