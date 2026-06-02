from pathlib import Path

from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path("api/", include("website.urls")),
]

frontend_dist = Path(settings.BASE_DIR).parent / "frontend" / "dist"
if (frontend_dist / "index.html").exists():
    public_static_dirs = ("assets", "logos", "images", "maps", "videos")
    for folder in public_static_dirs:
        document_root = frontend_dist / folder
        if document_root.is_dir():
            urlpatterns.append(
                re_path(
                    rf"^{folder}/(?P<path>.*)$",
                    serve,
                    {"document_root": document_root},
                )
            )
    urlpatterns.append(
        re_path(
            r"^(?!api/|static/|assets/|logos/|images/|maps/|videos/).*$",
            TemplateView.as_view(template_name="index.html"),
            name="spa",
        )
    )
