from pathlib import Path

from django.conf import settings
from django.urls import include, path, re_path
from website.seo_discovery import RobotsTxtView, SitemapXmlView
from website.static_serve import cached_serve
from website.spa_views import SpaIndexView

urlpatterns = [
    path("api/", include("website.urls")),
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path("sitemap.xml", SitemapXmlView.as_view(), name="sitemap-xml"),
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
                    cached_serve,
                    {"document_root": document_root},
                )
            )
    urlpatterns.append(
        re_path(
            r"^(?!api/|static/|assets/|logos/|images/|maps/|videos/|robots\.txt|sitemap\.xml).*$",
            SpaIndexView.as_view(),
            name="spa",
        )
    )
