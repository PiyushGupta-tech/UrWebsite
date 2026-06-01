from django.urls import path

from .views import (
    ChatAPIView,
    ContactSubmitAPIView,
    HomepageAPIView,
    PageDetailAPIView,
    SiteAPIView,
)

urlpatterns = [
    path("site/", SiteAPIView.as_view(), name="site"),
    path("homepage/", HomepageAPIView.as_view(), name="homepage"),
    path("chat/", ChatAPIView.as_view(), name="chat"),
    path("contact/", ContactSubmitAPIView.as_view(), name="contact-submit"),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view(), name="page-detail"),
]
