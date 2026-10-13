"""Serve frontend/dist files: hashed build assets cached for good, public files briefly."""

from __future__ import annotations

import mimetypes
import posixpath
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.utils._os import safe_join
from django.views.static import serve as django_serve

PUBLIC_DIR = Path(settings.BASE_DIR).parent / "frontend" / "public"
ROOT_PUBLIC_FILES = frozenset({
    "favicon.ico",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "icon-192.png",
    "icon-512.png",
    "site.webmanifest",
})

# Sibling files written by frontend/scripts/compress-dist.mjs, best first.
PRECOMPRESSED = (("br", ".br"), ("gzip", ".gz"))
COMPRESSIBLE_EXTENSIONS = frozenset(
    {".js", ".css", ".svg", ".json", ".webmanifest", ".xml", ".txt", ".map"}
)

# Only Vite's content-hashed build output may be cached forever. Files copied from
# frontend/public keep their names when edited, so browsers must recheck them.
IMMUTABLE_CACHE = "public, max-age=31536000, immutable"
PUBLIC_FILE_CACHE = "public, max-age=3600"


def accepted_encodings(header: str) -> set[str]:
    """Codings the client accepts (q > 0) from an Accept-Encoding header."""
    accepted = set()
    for part in (header or "").split(","):
        token, _, params = part.strip().partition(";")
        token = token.strip().lower()
        if not token:
            continue
        q = 1.0
        for param in params.split(";"):
            key, _, value = param.strip().partition("=")
            if key.strip().lower() == "q":
                try:
                    q = float(value)
                except ValueError:
                    q = 0.0
        if q > 0:
            accepted.add(token)
    return accepted


def _precompressed_variant(request, path: str, document_root) -> tuple[str, str] | None:
    """Return (sibling path, coding) for a pre-compressed copy the client can take."""
    if posixpath.splitext(path)[1].lower() not in COMPRESSIBLE_EXTENSIONS:
        return None
    accepted = accepted_encodings(request.META.get("HTTP_ACCEPT_ENCODING", ""))
    for coding, suffix in PRECOMPRESSED:
        if coding not in accepted:
            continue
        candidate = f"{path}{suffix}"
        try:
            full = Path(safe_join(document_root, posixpath.normpath(candidate).lstrip("/")))
        except Exception:
            return None
        if full.is_file():
            return candidate, coding
    return None


def cached_serve(request, path, document_root=None, show_indexes=False, immutable=False):
    variant = _precompressed_variant(request, path, document_root) if document_root else None
    response = django_serve(
        request,
        variant[0] if variant else path,
        document_root=document_root,
        show_indexes=show_indexes,
    )
    if variant and response.status_code == 200:
        content_type, _ = mimetypes.guess_type(path)
        if content_type:
            response["Content-Type"] = content_type
        response["Content-Encoding"] = variant[1]
    if posixpath.splitext(path)[1].lower() in COMPRESSIBLE_EXTENSIONS:
        response["Vary"] = "Accept-Encoding"
    if response.status_code in (200, 304):
        response["Cache-Control"] = IMMUTABLE_CACHE if immutable else PUBLIC_FILE_CACHE
    return response


def public_root_file(request, filename):
    """Favicon set and web manifest, served from frontend/public at the site root."""
    if filename not in ROOT_PUBLIC_FILES:
        raise Http404
    response = cached_serve(request, filename, document_root=str(PUBLIC_DIR))
    if response.status_code == 200:
        if filename.endswith(".webmanifest"):
            response["Content-Type"] = "application/manifest+json"
        response["Cache-Control"] = "public, max-age=86400"
    return response
