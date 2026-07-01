from django.urls import path

from .admin_views import (
    AdminLoginAPIView,
    AdminLogoutAPIView,
    AdminMeAPIView,
    AdminPayoutDashboardAPIView,
)
from .views import (
    ChatAPIView,
    ContactSubmitAPIView,
    HomepageAPIView,
    PageDetailAPIView,
    SeoAuditAPIView,
    SiteAPIView,
)

urlpatterns = [
    path("site/", SiteAPIView.as_view(), name="site"),
    path("homepage/", HomepageAPIView.as_view(), name="homepage"),
    path("chat/", ChatAPIView.as_view(), name="chat"),
    path("contact/", ContactSubmitAPIView.as_view(), name="contact-submit"),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view(), name="page-detail"),
    path("seo/", SeoAuditAPIView.as_view(), name="seo-audit"),
    path("admin/me/", AdminMeAPIView.as_view(), name="admin-me"),
    path("admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("admin/logout/", AdminLogoutAPIView.as_view(), name="admin-logout"),
    path(
        "admin/payout-dashboard/",
        AdminPayoutDashboardAPIView.as_view(),
        name="admin-payout-dashboard",
    ),
]
