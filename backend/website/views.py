import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import content
from . import page_content
from .homepage import homepage_payload
from .page_seo import page_context_for_slug
from .seo_audit import run_seo_audit
from .seo_schema import structured_data_graph
from .contact import send_contact_email
from .knowledge import answer_query


class SiteAPIView(APIView):
    """Shared site metadata and navigation."""

    def get(self, request):
        return Response({"site": content.SITE, "nav": content.NAV, "footer": content.FOOTER})


class HomepageAPIView(APIView):
    """Aggregated homepage content for the Vue SPA."""

    def get(self, request):
        return Response(homepage_payload())


class ContactSubmitAPIView(APIView):
    """Accept contact form submissions and email the support inbox."""

    REQUIRED_FIELDS = ("name", "email", "phone", "subject", "message")
    PHONE_RE = re.compile(r"^[6-9][0-9]{9}$")
    NAME_RE = re.compile(r"^[A-Za-z ]+$")

    def _validate_payload(self, payload):
        errors = {}

        name = payload["name"]
        if len(name) < 2 or len(name) > 50 or not self.NAME_RE.fullmatch(name):
            errors["name"] = "Full Name can contain only alphabets and spaces, and must be 2 to 50 characters."

        email = payload["email"]
        if len(email) > 254 or email.count("@") != 1:
            errors["email"] = "Email Address must contain exactly one @ and be at most 254 characters."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors["email"] = "Enter a valid email address."

        phone = payload["phone"]
        if not self.PHONE_RE.fullmatch(phone):
            errors["phone"] = "Phone Number must be 10 digits and start with 6, 7, 8, or 9."

        subject = payload["subject"]
        if len(subject) < 3 or len(subject) > 120:
            errors["subject"] = "Subject must be 3 to 120 characters."

        message = payload["message"]
        if len(message) < 10 or len(message) > 500:
            errors["message"] = "Message must be 10 to 500 characters."

        return errors

    def post(self, request):
        payload = {field: str(request.data.get(field, "")).strip() for field in self.REQUIRED_FIELDS}
        missing = [field for field, value in payload.items() if not value]
        if missing:
            return Response(
                {"detail": f"Missing required fields: {', '.join(missing)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_payload(payload)
        if errors:
            return Response(
                {"detail": "Please correct the highlighted fields.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_contact_email(**payload)
        except Exception:
            return Response(
                {"detail": "We could not send your message. Please try again or email us directly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"ok": True, "message": "Thank you — we'll get back to you shortly."})


class ChatAPIView(APIView):
    """Phase 1 site bot — keyword search over marketing content (no LLM)."""

    def post(self, request):
        message = str(request.data.get("message", "")).strip()
        if not message:
            return Response(
                {"detail": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(answer_query(message))


class PageDetailAPIView(APIView):
    """Single inner page by slug."""

    def get(self, request, slug):
        page = page_content.PAGES.get(slug)
        if not page:
            return Response({"detail": "Page not found."}, status=404)
        ctx = page_context_for_slug(slug, page)
        return Response(
            {
                "slug": slug,
                "route": page_content.SLUG_TO_ROUTE.get(slug),
                **ctx,
                "structured_data": structured_data_graph(slug, page, ctx["seo"]),
                "page": page,
                "site": content.SITE,
                "nav": content.NAV,
                "footer": content.FOOTER,
                "common_closing": content.HOME_CLOSING,
                "checkout_demo": content.CHECKOUT_DEMO,
                "dashboard_preview": content.DASHBOARD_PREVIEW,
            }
        )


class SeoAuditAPIView(APIView):
    """Phase 7 — SEO audit report for CI or pre-deploy checks."""

    def get(self, request):
        return Response(run_seo_audit())
