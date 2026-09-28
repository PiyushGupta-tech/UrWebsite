"""Tests for page-specific closing FAQs."""

from django.test import SimpleTestCase
from rest_framework.test import APIClient

from website import content, page_content
from website.page_faqs import PAGE_FAQS, closing_for_slug, page_faq_items
from website.page_seo import page_context_for_slug
from website.seo_schema import structured_data_graph

ROUTES = set(page_content.SLUG_TO_ROUTE.values())


class PageFaqDataTests(SimpleTestCase):
    def test_every_entry_is_a_real_page(self):
        for slug in PAGE_FAQS:
            self.assertIn(slug, page_content.PAGES, slug)

    def test_every_routed_page_except_faq_has_questions(self):
        for slug in page_content.SLUG_TO_ROUTE:
            if slug == "faq":
                continue
            self.assertIn(slug, PAGE_FAQS, slug)

    def test_items_are_complete_and_unique(self):
        for slug, entry in PAGE_FAQS.items():
            self.assertTrue(entry["intro"].strip(), slug)
            self.assertGreaterEqual(len(entry["items"]), 4, slug)
            questions = [item["question"] for item in entry["items"]]
            self.assertEqual(len(questions), len(set(questions)), slug)
            for item in entry["items"]:
                self.assertTrue(item["question"].strip().endswith("?"), item["question"])
                self.assertTrue(item["answer"].strip(), item["question"])

    def test_links_point_to_routed_pages(self):
        for slug, entry in PAGE_FAQS.items():
            for item in entry["items"]:
                for link in item.get("links", []):
                    self.assertIn(link["href"], ROUTES, f"{slug}: {link['href']}")
                    self.assertTrue(link["label"].strip())

    def test_links_never_point_back_to_same_page(self):
        for slug, entry in PAGE_FAQS.items():
            own_route = page_content.SLUG_TO_ROUTE.get(slug)
            for item in entry["items"]:
                for link in item.get("links", []):
                    self.assertNotEqual(link["href"], own_route, slug)


class ClosingForSlugTests(SimpleTestCase):
    def test_page_with_faqs_gets_numbered_page_items(self):
        closing = closing_for_slug("reconciliation")
        items = closing["faq_items"]
        self.assertEqual(
            [item["question"] for item in items],
            [item["question"] for item in PAGE_FAQS["reconciliation"]["items"]],
        )
        self.assertEqual([item["number"] for item in items], ["01", "02", "03", "04", "05"])
        self.assertEqual(closing["faq_intro"], PAGE_FAQS["reconciliation"]["intro"])

    def test_rest_of_closing_is_shared(self):
        closing = closing_for_slug("payouts")
        for key in ("faq_title", "testimonials", "audiences", "cta_title", "cta_label"):
            self.assertEqual(closing[key], content.HOME_CLOSING[key], key)

    def test_unknown_or_missing_slug_falls_back_to_generic(self):
        self.assertIs(closing_for_slug("does-not-exist"), content.HOME_CLOSING)
        self.assertIs(closing_for_slug(None), content.HOME_CLOSING)
        self.assertIs(closing_for_slug("faq"), content.HOME_CLOSING)

    def test_shared_data_is_not_mutated(self):
        before = [dict(item) for item in content.HOME_CLOSING["faq_items"]]
        source = [dict(item) for item in PAGE_FAQS["collections"]["items"]]
        closing_for_slug("collections")
        page_faq_items("collections")
        self.assertEqual(content.HOME_CLOSING["faq_items"], before)
        self.assertEqual(PAGE_FAQS["collections"]["items"], source)
        self.assertNotIn("number", PAGE_FAQS["collections"]["items"][0])


class PageApiClosingTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_page_api_returns_page_specific_faqs(self):
        response = self.client.get("/api/pages/hyper-checkout/")
        self.assertEqual(response.status_code, 200)
        closing = response.json()["common_closing"]
        self.assertEqual(
            closing["faq_items"][1]["question"],
            PAGE_FAQS["hyper-checkout"]["items"][1]["question"],
        )

    def test_homepage_keeps_generic_faqs(self):
        response = self.client.get("/api/homepage/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["closing"]["faq_items"], content.HOME_CLOSING["faq_items"]
        )


class PageFaqSchemaTests(SimpleTestCase):
    def _graph(self, slug):
        page = page_content.PAGES[slug]
        ctx = page_context_for_slug(slug, page)
        return structured_data_graph(slug, page, ctx["seo"]), ctx["seo"]

    def test_inner_page_schema_matches_visible_faqs(self):
        graph, seo = self._graph("payouts")
        faq_nodes = [node for node in graph if node["@type"] == "FAQPage"]
        self.assertEqual(len(faq_nodes), 1)
        node = faq_nodes[0]
        self.assertEqual(node["@id"], f"{seo['canonical']}#faq")
        self.assertEqual(
            [q["name"] for q in node["mainEntity"]],
            [item["question"] for item in PAGE_FAQS["payouts"]["items"]],
        )

    def test_faq_page_has_no_duplicate_schema(self):
        graph, _ = self._graph("faq")
        self.assertFalse([node for node in graph if node["@type"] == "FAQPage"])
