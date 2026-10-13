"""Tests for serving pre-compressed frontend assets."""

import gzip
import tempfile
from pathlib import Path

from django.core.exceptions import SuspiciousFileOperation
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase

from website.static_serve import accepted_encodings, cached_serve


class AcceptedEncodingsTests(SimpleTestCase):
    def test_parses_tokens_and_quality(self):
        self.assertEqual(accepted_encodings("gzip, deflate, br"), {"gzip", "deflate", "br"})
        self.assertEqual(accepted_encodings("br;q=0, gzip;q=0.5"), {"gzip"})
        self.assertEqual(accepted_encodings("br;q=abc"), set())
        self.assertEqual(accepted_encodings(""), set())


class CachedServeTests(SimpleTestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.body = b"console.log('hello');" * 50
        (self.root / "app.js").write_bytes(self.body)
        (self.root / "app.js.gz").write_bytes(gzip.compress(self.body))
        (self.root / "app.js.br").write_bytes(b"fake-brotli")
        (self.root / "plain.js").write_bytes(self.body)
        (self.root / "logo.png").write_bytes(b"\x89PNG")
        (self.root / "logo.png.gz").write_bytes(b"never-served")
        self.factory = RequestFactory()

    def tearDown(self):
        self._tmp.cleanup()

    def _get(self, path, accept=None, immutable=True, **extra):
        headers = {"HTTP_ACCEPT_ENCODING": accept} if accept is not None else {}
        request = self.factory.get(f"/assets/{path}", **headers, **extra)
        response = cached_serve(request, path, document_root=str(self.root), immutable=immutable)
        body = b"".join(response.streaming_content) if response.status_code == 200 else b""
        return response, body

    def test_prefers_brotli(self):
        response, body = self._get("app.js", "gzip, br")
        self.assertEqual(response["Content-Encoding"], "br")
        self.assertEqual(body, b"fake-brotli")
        self.assertIn("javascript", response["Content-Type"])
        self.assertEqual(response["Vary"], "Accept-Encoding")
        self.assertEqual(response["Cache-Control"], "public, max-age=31536000, immutable")

    def test_public_files_are_not_cached_forever(self):
        response, _ = self._get("logo.png", immutable=False)
        self.assertEqual(response["Cache-Control"], "public, max-age=3600")
        self.assertTrue(response.has_header("Last-Modified"))

    def test_unchanged_public_file_revalidates_with_304(self):
        first, _ = self._get("logo.png", immutable=False)
        response, _ = self._get(
            "logo.png", immutable=False, HTTP_IF_MODIFIED_SINCE=first["Last-Modified"]
        )
        self.assertEqual(response.status_code, 304)
        self.assertEqual(response["Cache-Control"], "public, max-age=3600")

    def test_falls_back_to_gzip(self):
        response, body = self._get("app.js", "gzip")
        self.assertEqual(response["Content-Encoding"], "gzip")
        self.assertEqual(gzip.decompress(body), self.body)

    def test_identity_without_accept_encoding(self):
        response, body = self._get("app.js")
        self.assertFalse(response.has_header("Content-Encoding"))
        self.assertEqual(body, self.body)
        self.assertEqual(response["Vary"], "Accept-Encoding")

    def test_missing_sibling_serves_original(self):
        response, body = self._get("plain.js", "br, gzip")
        self.assertFalse(response.has_header("Content-Encoding"))
        self.assertEqual(body, self.body)

    def test_binary_files_are_never_swapped(self):
        response, body = self._get("logo.png", "gzip")
        self.assertFalse(response.has_header("Content-Encoding"))
        self.assertEqual(body, b"\x89PNG")
        self.assertFalse(response.has_header("Vary"))

    def test_traversal_is_rejected(self):
        # Django's static serve raises this; the request handler turns it into a 400.
        with self.assertRaises(SuspiciousFileOperation):
            self._get("../../etc/passwd", "gzip")

    def test_missing_file_is_404(self):
        with self.assertRaises(Http404):
            self._get("nope.js", "gzip")
