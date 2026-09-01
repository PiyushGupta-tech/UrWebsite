"""Refresh the cached payin dashboard snapshot from the merchant API."""

from django.conf import settings
from django.core.management.base import BaseCommand

from website.payin_dashboard import refresh_payin_dashboard_snapshot, run_refresh_loop


class Command(BaseCommand):
    help = (
        "Fetch payin dashboard data into Django cache. "
        "Use --loop for a background worker (every PAYIN_DASHBOARD_REFRESH_INTERVAL seconds)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--loop",
            action="store_true",
            help="Run continuously (for systemd/supervisor worker).",
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=None,
            help="Seconds between refreshes when --loop is set (default: settings).",
        )

    def handle(self, *args, **options):
        if options["loop"]:
            interval = options["interval"] or settings.PAYIN_DASHBOARD_REFRESH_INTERVAL
            self.stdout.write(
                self.style.NOTICE(
                    f"Payin dashboard refresh loop started (every {interval}s). Ctrl+C to stop."
                )
            )
            try:
                run_refresh_loop(interval=interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Refresh loop stopped."))
            return

        ok, detail = refresh_payin_dashboard_snapshot()
        if ok:
            self.stdout.write(self.style.SUCCESS("Payin dashboard snapshot refreshed."))
            return

        self.stderr.write(self.style.ERROR(detail))
        raise SystemExit(1)
