"""Attach merchant names to map_cities_today entries for admin map tooltips."""

from __future__ import annotations

from typing import Any

CITY_ALIASES = {
    "gurgaon": "gurugram",
    "bangalore": "bengaluru",
    "bengluru urban": "bengaluru",
    "bengaluru urban": "bengaluru",
    "fatehgarh saheb": "fatehgarh sahib",
    "new delhi": "delhi",
    "mumbai suburban": "mumbai",
    "greater noida": "greater noida",
    "noida": "noida",
}


def _normalize_city(value: str = "") -> str:
    city = " ".join(value.strip().lower().split())
    return CITY_ALIASES.get(city, city)


def _normalize_state(value: str = "") -> str:
    return " ".join(value.strip().lower().split())


def _provider_name(provider: dict[str, Any]) -> str:
    return (provider.get("name") or provider.get("userid") or "").strip()


def _merchant_from_transaction(tx: dict[str, Any]) -> tuple[str, str, str]:
    merchant = tx.get("merchant") or {}
    location = merchant.get("location") or {}
    name = (merchant.get("name") or tx.get("userid") or "").strip()
    city = (location.get("city") or merchant.get("city") or tx.get("city") or "").strip()
    state = (location.get("state") or merchant.get("state") or tx.get("state") or "").strip()
    return name, city, state


def _top_merchant_name(counts: dict[str, int]) -> str:
    if not counts:
        return ""
    return max(counts.items(), key=lambda item: item[1])[0]


def _entry_amount(entry: dict[str, Any]) -> float:
    return round(float(entry.get("amount_with_fees") or entry.get("amount") or 0), 2)


def _resolve_merchant_name(
    entry: dict[str, Any],
    provider_by_city_state: dict[tuple[str, str], str],
    provider_by_city: dict[str, str],
    provider_by_stats: dict[tuple[int, float], str],
    tx_by_city_state: dict[tuple[str, str], dict[str, int]],
    tx_by_city: dict[str, dict[str, int]],
) -> str:
    city = _normalize_city(entry.get("city") or "")
    state = _normalize_state(entry.get("state") or "")
    txn_count = int(entry.get("txn_count") or 0)
    amount = _entry_amount(entry)

    if not city:
        return ""

    return (
        provider_by_city_state.get((city, state), "")
        or provider_by_city.get(city, "")
        or provider_by_stats.get((txn_count, amount), "")
        or _top_merchant_name(tx_by_city_state.get((city, state), {}))
        or _top_merchant_name(tx_by_city.get(city, {}))
    )


def enrich_map_cities_with_merchants(summary: dict[str, Any] | None) -> dict[str, Any] | None:
    """Add merchant_name to each map_cities_today row when resolvable."""
    if not summary:
        return summary

    providers = summary.get("top_providers_today") or []
    transactions = summary.get("latest_transactions") or []

    provider_by_city_state: dict[tuple[str, str], str] = {}
    provider_by_city: dict[str, str] = {}
    provider_by_stats: dict[tuple[int, float], str] = {}
    tx_by_city_state: dict[tuple[str, str], dict[str, int]] = {}
    tx_by_city: dict[str, dict[str, int]] = {}

    for provider in providers:
        name = _provider_name(provider)
        if not name:
            continue

        location = provider.get("location") or {}
        city = _normalize_city(location.get("city") or provider.get("city") or "")
        state = _normalize_state(location.get("state") or provider.get("state") or "")
        if city:
            provider_by_city_state.setdefault((city, state), name)
            provider_by_city.setdefault(city, name)

        txn_count = int(provider.get("txn_count") or 0)
        amount = round(float(provider.get("amount_with_fees") or provider.get("amount") or 0), 2)
        provider_by_stats.setdefault((txn_count, amount), name)

    for tx in transactions:
        name, city_raw, state_raw = _merchant_from_transaction(tx)
        if not name or not city_raw:
            continue

        city = _normalize_city(city_raw)
        state = _normalize_state(state_raw)
        tx_by_city_state.setdefault((city, state), {})
        tx_by_city_state[(city, state)][name] = tx_by_city_state[(city, state)].get(name, 0) + 1
        tx_by_city.setdefault(city, {})
        tx_by_city[city][name] = tx_by_city[city].get(name, 0) + 1

    for entry in summary.get("map_cities_today") or []:
        if entry.get("merchant_name"):
            continue
        merchant_name = _resolve_merchant_name(
            entry,
            provider_by_city_state,
            provider_by_city,
            provider_by_stats,
            tx_by_city_state,
            tx_by_city,
        )
        if merchant_name:
            entry["merchant_name"] = merchant_name

    return summary
