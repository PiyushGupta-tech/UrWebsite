import uuid

from django.db import models


class ChatConversation(models.Model):
    LEAD_KIND_LEAD = "lead"
    LEAD_KIND_HANDOFF = "handoff"
    LEAD_KIND_CHOICES = [
        (LEAD_KIND_LEAD, "Lead"),
        (LEAD_KIND_HANDOFF, "Human handoff"),
    ]

    # Public, unguessable id handed to the browser; the integer pk never leaves the server.
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    page_path = models.CharField(max_length=200, blank=True)
    user_message_count = models.PositiveIntegerField(default=0)

    lead_kind = models.CharField(max_length=10, choices=LEAD_KIND_CHOICES, blank=True)
    lead_name = models.CharField(max_length=50, blank=True)
    lead_email = models.EmailField(max_length=254, blank=True)
    lead_phone = models.CharField(max_length=10, blank=True)
    lead_note = models.CharField(max_length=500, blank=True)
    lead_submitted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Chat {self.public_id}"


class ContactInquiry(models.Model):
    """Website Contact Us form submission — kept even if email delivery fails."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=500)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Contact {self.name} <{self.email}>"


class ChatMessage(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "Visitor"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    # True when the reply came from the AI model rather than the keyword fallback.
    ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:40]}"
