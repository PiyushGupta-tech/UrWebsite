from pathlib import Path

from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from website.legacy_redirects import LEGACY_GONE_PATHS, LEGACY_REDIRECTS, LegacyGoneView
from website.seo_discovery import RobotsTxtView, SitemapXmlView
from website.static_serve import ROOT_PUBLIC_FILES, cached_serve, public_root_file
from website.spa_views import SpaIndexView

urlpatterns = [
    path("api/", include("website.urls")),
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path("sitemap.xml", SitemapXmlView.as_view(), name="sitemap-xml"),
]

for _root_file in sorted(ROOT_PUBLIC_FILES):
    urlpatterns.append(
        path(
            _root_file,
            public_root_file,
            {"filename": _root_file},
            name=f"public-{_root_file.replace('.', '-')}",
        )
    )

for _legacy, _target in LEGACY_REDIRECTS.items():
    urlpatterns.append(
        path(
            f"{_legacy}/",
            RedirectView.as_view(url=_target, permanent=True),
            name=f"legacy-{_legacy.replace('/', '-')}-slash",
        )
    )
    urlpatterns.append(
        path(
            _legacy,
            RedirectView.as_view(url=_target, permanent=True),
            name=f"legacy-{_legacy.replace('/', '-')}",
        )
    )

for _gone in LEGACY_GONE_PATHS:
    urlpatterns.append(path(_gone, LegacyGoneView.as_view(), name=f"legacy-gone-{_gone}"))

frontend_dist = Path(settings.BASE_DIR).parent / "frontend" / "dist"
if (frontend_dist / "index.html").exists():
    public_static_dirs = ("assets", "logos", "images", "maps", "videos", "downloads")
    for folder in public_static_dirs:
        document_root = frontend_dist / folder
        if document_root.is_dir():
            urlpatterns.append(
                re_path(
                    rf"^{folder}/(?P<path>.*)$",
                    cached_serve,
                    {"document_root": document_root, "immutable": folder == "assets"},
                )
            )
    urlpatterns.append(
        re_path(
            r"^(?!api/|static/|assets/|logos/|images/|maps/|videos/|downloads/|robots\.txt|sitemap\.xml).*$",
            SpaIndexView.as_view(),
            name="spa",
        )
    )
