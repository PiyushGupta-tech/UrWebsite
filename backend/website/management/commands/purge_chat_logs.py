"""Delete saved website chats past the retention period (run: python manage.py purge_chat_logs)."""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from website.models import ChatConversation


class Command(BaseCommand):
    help = "Delete website chats whose last activity is older than CHAT_LOG_RETENTION_DAYS."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=settings.CHAT_LOG_RETENTION_DAYS,
            help="Override the retention period in days.",
        )

    def handle(self, *_args, **options):
        days = options["days"]
        if days < 1:
            self.stderr.write(self.style.ERROR("--days must be at least 1."))
            return
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _ = ChatConversation.objects.filter(updated_at__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} chat records older than {days} days."))
