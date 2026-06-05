from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import content
from . import page_content
from .contact import send_contact_email
from .knowledge import answer_query


class SiteAPIView(APIView):
    """Shared site metadata and navigation."""

    def get(self, request):
        return Response({"site": content.SITE, "nav": content.NAV, "footer": content.FOOTER})


class HomepageAPIView(APIView):
    """Aggregated homepage content for the Vue SPA."""

    def get(self, request):
        return Response(
            {
                "site": content.SITE,
                "nav": content.NAV,
                "seo": content.HOME_SEO,
                "hero": content.HERO,
                "payment_solution": content.PAYMENT_SOLUTION,
                "banking_partners": content.BANKING_PARTNERS,
                "merchant_partners": content.MERCHANT_PARTNERS,
                "features": content.FEATURES,
                "stats": content.STATS,
                "why_choose": content.WHY_CHOOSE,
                "testimonials": content.TESTIMONIALS,
                "faqs": content.FAQS,
                "footer": content.FOOTER,
                "checkout_demo": content.CHECKOUT_DEMO,
                "problem_trio": content.PROBLEM_TRIO,
                "value_prop": content.VALUE_PROP,
                "personas": content.PERSONAS,
                "product_catalogue": content.PRODUCT_CATALOGUE,
                "dashboard_preview": content.DASHBOARD_PREVIEW,
            }
        )


class ContactSubmitAPIView(APIView):
    """Accept contact form submissions and email the support inbox."""

    REQUIRED_FIELDS = ("name", "email", "phone", "subject", "message")

    def post(self, request):
        payload = {field: str(request.data.get(field, "")).strip() for field in self.REQUIRED_FIELDS}
        missing = [field for field, value in payload.items() if not value]
        if missing:
            return Response(
                {"detail": f"Missing required fields: {', '.join(missing)}."},
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
        return Response(
            {
                "slug": slug,
                "route": page_content.SLUG_TO_ROUTE.get(slug),
                "page": page,
                "site": content.SITE,
                "nav": content.NAV,
                "footer": content.FOOTER,
                "checkout_demo": content.CHECKOUT_DEMO,
                "dashboard_preview": content.DASHBOARD_PREVIEW,
            }
        )
