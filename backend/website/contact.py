"""Contact form email delivery."""

from django.conf import settings
from django.core.mail import EmailMessage


def send_contact_email(*, name, email, phone, subject, message):
    recipient = settings.CONTACT_EMAIL_TO
    mail_subject = f"[Urbanrupee Contact] {subject}"
    body = (
        "New message from the website contact form\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Subject: {subject}\n\n"
        "Message:\n"
        f"{message}\n"
    )

    msg = EmailMessage(
        subject=mail_subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[email],
    )
    msg.send(fail_silently=False)
