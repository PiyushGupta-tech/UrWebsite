"""Contact form and chat lead email delivery."""

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


def send_chat_lead_email(*, conversation, transcript):
    """Email the sales inbox a chat lead or human-handoff request with the transcript."""
    if conversation.lead_kind == conversation.LEAD_KIND_HANDOFF:
        mail_subject = f"[Urbanrupee Chat] Visitor asked for a human: {conversation.lead_name}"
        intro = "A website chat visitor asked to talk to the team."
    else:
        mail_subject = f"[Urbanrupee Chat] New lead: {conversation.lead_name}"
        intro = "A website chat visitor shared their details."

    lines = [
        intro,
        "",
        f"Name: {conversation.lead_name}",
        f"Email: {conversation.lead_email}",
        f"Phone: {conversation.lead_phone}",
        f"Started on page: {conversation.page_path or '-'}",
        f"Chat ID: {conversation.public_id}",
    ]
    lines += ["", "Message:", conversation.lead_note or "(No message)", "", "Conversation:"]
    if transcript:
        for message in transcript:
            speaker = "Visitor" if message.role == message.ROLE_USER else "Assistant"
            lines.append(f"{speaker}: {message.content}")
    else:
        lines.append("(The visitor had not sent any chat messages.)")

    msg = EmailMessage(
        subject=mail_subject,
        body="\n".join(lines) + "\n",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL_TO],
        reply_to=[conversation.lead_email],
    )
    msg.send(fail_silently=False)
