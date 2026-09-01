"""Tests for map city merchant enrichment."""

from django.test import TestCase

from website.map_city_merchants import enrich_map_cities_with_merchants


class MapCityMerchantTests(TestCase):
    def test_enriches_from_top_providers(self):
        summary = {
            "map_cities_today": [
                {
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "txn_count": 12,
                    "amount_with_fees": 95716.6,
                },
            ],
            "top_providers_today": [
                {
                    "name": "Dream nexus Tech",
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "txn_count": 12,
                    "amount_with_fees": 95716.6,
                },
            ],
            "latest_transactions": [],
        }

        enrich_map_cities_with_merchants(summary)
        self.assertEqual(summary["map_cities_today"][0]["merchant_name"], "Dream nexus Tech")

    def test_enriches_from_latest_transactions_when_not_top_provider(self):
        summary = {
            "map_cities_today": [
                {
                    "city": "Bengluru Urban",
                    "state": "Karnataka",
                    "txn_count": 5,
                    "amount_with_fees": 99066.08,
                },
            ],
            "top_providers_today": [],
            "latest_transactions": [
                {
                    "merchant": {
                        "name": "AAIJI WALLET FINTECH PVT LTD",
                        "location": {"city": "Bengluru Urban", "state": "Karnataka"},
                    },
                },
                {
                    "merchant": {
                        "name": "AAIJI WALLET FINTECH PVT LTD",
                        "location": {"city": "Bengluru Urban", "state": "Karnataka"},
                    },
                },
            ],
        }

        enrich_map_cities_with_merchants(summary)
        self.assertEqual(
            summary["map_cities_today"][0]["merchant_name"],
            "AAIJI WALLET FINTECH PVT LTD",
        )

    def test_matches_by_txn_stats(self):
        summary = {
            "map_cities_today": [
                {
                    "city": "Noida",
                    "state": "Uttar Pradesh",
                    "txn_count": 1,
                    "amount_with_fees": 7933.98,
                },
            ],
            "top_providers_today": [
                {
                    "name": "Classypay",
                    "city": "Noida",
                    "state": "Uttar Pradesh",
                    "txn_count": 1,
                    "amount_with_fees": 7933.98,
                },
            ],
            "latest_transactions": [],
        }

        enrich_map_cities_with_merchants(summary)
        self.assertEqual(summary["map_cities_today"][0]["merchant_name"], "Classypay")
