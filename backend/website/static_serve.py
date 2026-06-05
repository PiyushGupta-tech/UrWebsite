"""Serve frontend/dist assets with long-lived cache headers."""

from __future__ import annotations

from django.views.static import serve as django_serve


def cached_serve(request, path, document_root=None, show_indexes=False):
    response = django_serve(
        request,
        path,
        document_root=document_root,
        show_indexes=show_indexes,
    )
    if response.status_code == 200:
        response["Cache-Control"] = "public, max-age=31536000, immutable"
    return response
