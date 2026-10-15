"""Tests for per-page head metadata and its server-side injection."""

import re
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase

from website import content, page_content
from website.page_seo import resolve_page_seo
from website.seo_audit import DESCRIPTION_MAX, DESCRIPTION_MIN, KEYWORDS_MAX, TITLE_MAX
from website.seo_schema import structured_data_graph
from website.spa_views import inject_seo

INDEX_SOURCE = (Path(settings.BASE_DIR).parent / "frontend" / "index.html").read_text(encoding="utf-8")


def _all_seo():
    rows = [("home", content.HOME_SEO)]
    rows += [
        (slug, resolve_page_seo(slug, page_content.PAGES[slug]))
        for slug in page_content.SLUG_TO_ROUTE
    ]
    return rows


def _meta(html, attr, key):
    match = re.search(rf'<meta\s+{attr}="{re.escape(key)}"\s+content="([^"]*)"', html)
    return match.group(1) if match else None


class PageMetaRulesTests(SimpleTestCase):
    def test_lengths_within_search_limits(self):
        for slug, seo in _all_seo():
            self.assertLessEqual(len(seo["title"]), TITLE_MAX, slug)
            self.assertGreaterEqual(len(seo["description"]), DESCRIPTION_MIN, slug)
            self.assertLessEqual(len(seo["description"]), DESCRIPTION_MAX, slug)

    def test_titles_and_descriptions_are_unique(self):
        rows = _all_seo()
        titles = [seo["title"] for _, seo in rows]
        descriptions = [seo["description"] for _, seo in rows]
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_keywords_are_short_and_unique(self):
        for slug, seo in _all_seo():
            keywords = [k.strip().lower() for k in seo.get("keywords", "").split(",") if k.strip()]
            self.assertLessEqual(len(keywords), KEYWORDS_MAX, slug)
            self.assertEqual(len(keywords), len(set(keywords)), slug)

    def test_every_title_names_the_brand(self):
        for slug, seo in _all_seo():
            self.assertIn("Urbanrupee", seo["title"], slug)


class InjectSeoTests(SimpleTestCase):
    def test_replaces_head_tags_in_real_template(self):
        seo = resolve_page_seo("reconciliation", page_content.PAGES["reconciliation"])
        html = inject_seo(INDEX_SOURCE, seo)

        self.assertIn("<title>Payment Reconciliation Software India | Urbanrupee</title>", html)
        for attr, key, expected in (
            ("name", "description", seo["description"]),
            ("property", "og:description", seo["description"]),
            ("name", "twitter:description", seo["description"]),
            ("property", "og:title", seo["title"]),
            ("name", "twitter:title", seo["title"]),
            ("name", "keywords", seo["keywords"]),
            ("property", "og:url", seo["canonical"]),
        ):
            self.assertEqual(_meta(html, attr, key), expected, key)
        self.assertIn(f'<link rel="canonical" href="{seo["canonical"]}"', html)
        self.assertEqual(html.count('name="description"'), 1)
        self.assertEqual(html.count('name="keywords"'), 1)

    def test_page_without_keywords_drops_default_home_keywords(self):
        seo = resolve_page_seo("privacy-policy", page_content.PAGES["privacy-policy"])
        html = inject_seo(INDEX_SOURCE, seo)
        self.assertIsNone(_meta(html, "name", "keywords"))
        self.assertIn("<title>Privacy Policy | Urbanrupee</title>", html)

    def test_special_characters_are_escaped(self):
        seo = {
            "title": 'A & B "quoted" <x> \\1',
            "description": 'Desc & "more" <b>',
            "keywords": "a & b",
            "canonical": "https://urbanrupee.com/x",
        }
        html = inject_seo(INDEX_SOURCE, seo)
        self.assertIn("<title>A &amp; B &quot;quoted&quot; &lt;x&gt; \\1</title>", html)
        self.assertEqual(_meta(html, "name", "description"), "Desc &amp; &quot;more&quot; &lt;b&gt;")
        self.assertEqual(_meta(html, "name", "keywords"), "a &amp; b")

    def test_share_image_survives_injection(self):
        seo = resolve_page_seo("payouts", page_content.PAGES["payouts"])
        html = inject_seo(INDEX_SOURCE, seo)
        image = _meta(html, "property", "og:image")
        self.assertTrue(image.startswith("https://") and image.endswith(".jpg"))
        self.assertTrue((Path(settings.BASE_DIR).parent / "frontend" / "public" / image.split("/", 3)[3]).is_file())
        self.assertEqual(_meta(html, "name", "twitter:image"), image)
        self.assertEqual(_meta(html, "name", "twitter:card"), "summary_large_image")

    def test_template_defaults_match_home_seo(self):
        self.assertIn(f"<title>{content.HOME_SEO['title'].replace('&', '&amp;')}</title>", INDEX_SOURCE)
        self.assertEqual(_meta(INDEX_SOURCE, "name", "description"), content.HOME_SEO["description"])
        self.assertEqual(_meta(INDEX_SOURCE, "name", "keywords"), content.HOME_SEO["keywords"])


class SpaIndexRobotsTests(SimpleTestCase):
    def _get(self, path):
        with patch("website.spa_views._index_template", return_value=INDEX_SOURCE):
            return self.client.get(path).content.decode()

    def test_admin_pages_are_noindex(self):
        for path in ("/admin", "/admin/dashboard", "/admin/chats"):
            html = self._get(path)
            self.assertEqual(_meta(html, "name", "robots"), "noindex, nofollow", path)

    def test_public_pages_stay_indexable(self):
        html = self._get("/services/payouts")
        self.assertTrue(_meta(html, "name", "robots").startswith("index, follow"))
        self.assertIn("<title>Payout Platform India | Bulk &amp; Instant Payouts | Urbanrupee</title>", html)


class SpaNotFoundTests(SimpleTestCase):
    def _get(self, path):
        with patch("website.spa_views._index_template", return_value=INDEX_SOURCE):
            return self.client.get(path)

    def test_unknown_path_is_a_real_404(self):
        response = self._get("/this-page-does-not-exist")
        html = response.content.decode()
        self.assertEqual(response.status_code, 404)
        self.assertIn("<title>Page not found | Urbanrupee</title>", html)
        self.assertEqual(_meta(html, "name", "robots"), "noindex, follow")
        self.assertNotIn('rel="canonical"', html)
        self.assertIsNone(_meta(html, "property", "og:url"))
        self.assertIsNone(_meta(html, "name", "keywords"))
        self.assertNotIn("application/ld+json", html)
        self.assertIn('<div id="app">', html)

    def test_known_paths_stay_200(self):
        for path in ("/", "/about", "/about/", "/services/payouts", "/services/payment", "/admin", "/thank-you"):
            self.assertEqual(self._get(path).status_code, 200, path)

    def test_thank_you_is_noindex(self):
        response = self._get("/thank-you")
        html = response.content.decode()
        self.assertIn("<title>Thank you | Urbanrupee</title>", html)
        self.assertEqual(_meta(html, "name", "robots"), "noindex, follow")
        self.assertNotIn('rel="canonical"', html)
        self.assertIn('id="site-bootstrap"', html)

    def test_page_bootstrap_matches_the_route(self):
        html = self._get("/contact").content.decode()
        self.assertIn('id="site-bootstrap"', html)
        self.assertIn('id="page-bootstrap"', html)
        self.assertIn('"slug": "contact"', html)

    def test_homepage_bootstraps_site_and_page_data(self):
        html = self._get("/").content.decode()
        self.assertIn('id="site-bootstrap"', html)
        self.assertIn('id="homepage-bootstrap"', html)
        self.assertNotIn('id="page-bootstrap"', html)

    def test_sitemap_skips_redirect_aliases(self):
        from website.seo_discovery import sitemap_urls

        locs = [entry["loc"] for entry in sitemap_urls()]
        self.assertEqual(len(locs), len(set(locs)))
        self.assertTrue(any(loc.endswith("/services/collections") for loc in locs))
        self.assertFalse(any(loc.endswith("/services/payment") for loc in locs))

    def test_favicon_is_an_icon(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 200)
        self.assertIn("icon", response["Content-Type"])
        response = self.client.get("/site.webmanifest")
        self.assertEqual(response.status_code, 200)
        self.assertIn("manifest", response["Content-Type"])

    def test_unknown_admin_path_is_404_and_noindex(self):
        response = self._get("/admin/nope")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(_meta(response.content.decode(), "name", "robots"), "noindex, nofollow")

    def test_mixed_case_known_path_redirects_to_lowercase(self):
        response = self._get("/About?ref=x")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/about?ref=x")

    def test_mixed_case_unknown_path_is_404(self):
        self.assertEqual(self._get("/Nope").status_code, 404)

    def test_not_found_view_defaults_match_index_html(self):
        source = (
            Path(settings.BASE_DIR).parent / "frontend" / "src" / "views" / "NotFoundView.vue"
        ).read_text(encoding="utf-8")
        robots = _meta(INDEX_SOURCE, "name", "robots")
        self.assertIn(f'const DEFAULT_ROBOTS = "{robots}";', source)
        self.assertIn(f'const DEFAULT_TITLE = "{content.HOME_SEO["title"]}";', source)

    def test_retired_spa_routes_redirect_server_side(self):
        for old, new in (
            ("/products/collections", "/services/collections"),
            ("/services/aml", "/services/risk-fraud-management"),
            ("/products/payout", "/services/payouts"),
        ):
            response = self.client.get(old)
            self.assertEqual(response.status_code, 301, old)
            self.assertEqual(response["Location"], new, old)


class AnalyticsIdInjectionTests(SimpleTestCase):
    def _get(self, path):
        with patch("website.spa_views._index_template", return_value=INDEX_SOURCE):
            return self.client.get(path).content.decode()

    def test_no_id_means_no_analytics(self):
        with self.settings(GA_MEASUREMENT_ID=""):
            self.assertIsNone(_meta(self._get("/"), "name", "ga-measurement-id"))

    def test_valid_id_is_exposed_on_public_pages(self):
        with self.settings(GA_MEASUREMENT_ID="G-ABC123XYZ9"):
            for path in ("/", "/contact", "/missing-page"):
                self.assertEqual(_meta(self._get(path), "name", "ga-measurement-id"), "G-ABC123XYZ9", path)

    def test_admin_pages_never_get_analytics(self):
        with self.settings(GA_MEASUREMENT_ID="G-ABC123XYZ9"):
            self.assertIsNone(_meta(self._get("/admin"), "name", "ga-measurement-id"))

    def test_malformed_id_is_ignored(self):
        for bad in ("UA-12345-1", 'G-ABC"><script>', "G-", "abc"):
            with self.settings(GA_MEASUREMENT_ID=bad):
                html = self._get("/")
                self.assertIsNone(_meta(html, "name", "ga-measurement-id"), bad)
                self.assertNotIn("<script>alert", html)


class ServiceSchemaTests(SimpleTestCase):
    def _graph(self, slug):
        page = page_content.PAGES[slug]
        seo = resolve_page_seo(slug, page)
        return structured_data_graph(slug, page, seo)

    def test_service_pages_get_service_node(self):
        for slug in ("collections", "reconciliation", "payment-orchestration", "unified-dashboard"):
            graph = self._graph(slug)
            services = [n for n in graph if n["@type"] == "Service"]
            self.assertEqual(len(services), 1, slug)
            self.assertTrue(services[0]["serviceType"], slug)
            webpage = next(n for n in graph if n["@type"] == "WebPage")
            self.assertEqual(webpage["mainEntity"]["@id"], services[0]["@id"], slug)

    def test_non_service_pages_have_no_service_node(self):
        for slug in ("faq", "privacy-policy", "contact", "about"):
            graph = self._graph(slug)
            self.assertFalse([n for n in graph if n["@type"] == "Service"], slug)
            webpage = next(n for n in graph if n["@type"] == "WebPage")
            self.assertNotIn("mainEntity", webpage, slug)
