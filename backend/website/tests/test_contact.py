"""Tests for contact form submission and email delivery."""

import importlib
import os
from unittest.mock import patch

from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from rest_framework.test import APIClient

from config import email_config

VALID = {
    "name": "Asha Rao",
    "email": "asha@example.com",
    "phone": "9876543210",
    "subject": "Payouts demo",
    "message": "Please share pricing for bulk payouts.",
}


def _load_settings(**env):
    """Re-import settings with a controlled environment."""
    import config.settings as settings_module

    with patch.dict(os.environ, env, clear=False):
        for key in ("EMAIL_HOST_PASSWORD", "CONTACT_EMAIL_TO", "EMAIL_HOST"):
            if key not in env:
                os.environ.pop(key, None)
        with patch("dotenv.load_dotenv"):
            return importlib.reload(settings_module)


class EmailConfigTests(SimpleTestCase):
    def tearDown(self):
        _load_settings()

    def test_recipient_comes_from_config_file_not_env(self):
        loaded = _load_settings(CONTACT_EMAIL_TO="it.support@urbanrupee.com")
        self.assertEqual(email_config.CONTACT_EMAIL_TO, "rajeev@urbanrupee.com")
        self.assertEqual(loaded.CONTACT_EMAIL_TO, "rajeev@urbanrupee.com")
        self.assertEqual(loaded.EMAIL_HOST, "smtp.gmail.com")

    def test_smtp_enabled_only_with_app_password(self):
        self.assertEqual(
            _load_settings().EMAIL_BACKEND,
            "django.core.mail.backends.console.EmailBackend",
        )
        self.assertEqual(
            _load_settings(EMAIL_HOST_PASSWORD="app-pass").EMAIL_BACKEND,
            "django.core.mail.backends.smtp.EmailBackend",
        )


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    ALLOWED_HOSTS=["localhost"],
)
class ContactSubmitTests(TestCase):
    def setUp(self):
        self.client = APIClient(HTTP_HOST="localhost")

    @override_settings(CONTACT_EMAIL_TO="rajeev@urbanrupee.com")
    def test_valid_submission_emails_recipient_with_reply_to(self):
        response = self.client.post("/api/contact/", VALID, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.to, ["rajeev@urbanrupee.com"])
        self.assertEqual(sent.reply_to, ["asha@example.com"])
        self.assertEqual(sent.subject, "[Urbanrupee Contact] Payouts demo")
        self.assertIn("Phone: 9876543210", sent.body)
        self.assertIn("Please share pricing for bulk payouts.", sent.body)

    def test_missing_field_rejected_without_email(self):
        response = self.client.post("/api/contact/", {**VALID, "phone": ""}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.json()["detail"])
        self.assertEqual(len(mail.outbox), 0)

    def test_send_failure_returns_503(self):
        with patch("website.views.send_contact_email", side_effect=OSError("smtp down")):
            response = self.client.post("/api/contact/", VALID, format="json")

        self.assertEqual(response.status_code, 503)
