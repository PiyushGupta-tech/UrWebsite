"""Fetch payin dashboard snapshots from the merchant API and cache them server-side."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from website.dashboard_fetch import upstream_latest_limit
from website.map_city_merchants import enrich_map_cities_with_merchants

logger = logging.getLogger(__name__)

CACHE_KEY = "payin_dashboard:snapshot"
META_KEY = "payin_dashboard:meta"


def fetch_upstream_snapshot() -> tuple[dict[str, Any] | None, int, str]:
    """Call the merchant payin internal API (server-side token only)."""
    token = settings.PAYIN_DASHBOARD_API_TOKEN
    if not token:
        return None, 503, "Payin dashboard is not configured."

    params = {"latest_limit": upstream_latest_limit(settings.PAYIN_DASHBOARD_LATEST_LIMIT)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        upstream = requests.get(
            settings.PAYIN_DASHBOARD_API_URL,
            params=params,
            headers=headers,
            timeout=settings.PAYIN_DASHBOARD_HTTP_TIMEOUT,
        )
    except requests.RequestException:
        logger.exception("Payin dashboard upstream request failed")
        return None, 502, "Could not reach payin dashboard."

    if upstream.status_code == 401:
        return None, 502, "Payin dashboard rejected credentials."
    if upstream.status_code == 403:
        return None, 502, "Payin dashboard blocked this server IP."
    if upstream.status_code == 503:
        return None, 503, "Payin dashboard is unavailable."
    if not upstream.ok:
        return None, 502, "Payin dashboard returned an error."

    try:
        payload = upstream.json()
    except ValueError:
        return None, 502, "Payin dashboard returned invalid JSON."

    if not payload.get("ok"):
        return None, 502, "Payin dashboard returned an error."

    summary = payload.get("summary") or {}
    enrich_map_cities_with_merchants(summary)

    return {
        "ok": True,
        "generated_at": payload.get("generated_at"),
        "summary": summary,
    }, 200, ""


def refresh_payin_dashboard_snapshot() -> tuple[bool, str]:
    """Fetch upstream and store the latest snapshot in Django cache."""
    data, code, detail = fetch_upstream_snapshot()
    ttl = settings.PAYIN_DASHBOARD_CACHE_TTL

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
        logger.warning("Payin dashboard refresh failed: %s", detail)
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
        summary = data.get("summary")
        if summary:
            enrich_map_cities_with_merchants(summary)
        return data, 200, ""

    meta = cache.get(META_KEY) or {}
    detail = meta.get("detail") or "Payin dashboard snapshot is not ready yet."
    code = int(meta.get("code") or 503)
    return None, code, detail


def run_refresh_loop(interval: int | None = None) -> None:
    """Poll upstream forever — intended for a dedicated worker process."""
    sleep_seconds = interval or settings.PAYIN_DASHBOARD_REFRESH_INTERVAL
    while True:
        refresh_payin_dashboard_snapshot()
        time.sleep(sleep_seconds)
