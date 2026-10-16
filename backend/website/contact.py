"""Contact form and chat lead email delivery.

Both forms use send_contact_email so the support inbox receives every lead the
same way: from noreply@urbanrupee.com to CONTACT_EMAIL_TO (and CONTACT_EMAIL_CC).
"""

from django.conf import settings
from django.core.mail import EmailMessage


def _recipients():
    to = [settings.CONTACT_EMAIL_TO]
    cc = [addr for addr in getattr(settings, "CONTACT_EMAIL_CC", ()) if addr and addr not in to]
    return to, cc


def send_contact_email(*, name, email, phone, subject, message):
    """Send a visitor enquiry to the support / sales inbox."""
    to, cc = _recipients()
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
        to=to,
        cc=cc,
        reply_to=[email],
    )
    msg.send(fail_silently=False)


def send_chat_lead_email(*, conversation, transcript):
    """Email chat "Talk to our team" details through the same path as Contact Us."""
    if conversation.lead_kind == conversation.LEAD_KIND_HANDOFF:
        subject = f"Talk to our team: {conversation.lead_name}"
    else:
        subject = f"Chat lead: {conversation.lead_name}"

    lines = [
        f"Started on page: {conversation.page_path or '-'}",
        f"Chat ID: {conversation.public_id}",
        "",
        "Visitor message:",
        conversation.lead_note or "(No message)",
        "",
        "Conversation:",
    ]
    if transcript:
        for message in transcript:
            speaker = "Visitor" if message.role == message.ROLE_USER else "Assistant"
            lines.append(f"{speaker}: {message.content}")
    else:
        lines.append("(The visitor had not sent any chat messages.)")

    send_contact_email(
        name=conversation.lead_name,
        email=conversation.lead_email,
        phone=conversation.lead_phone,
        subject=subject,
        message="\n".join(lines),
    )
