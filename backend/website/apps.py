import os
import sys
import threading

from django.apps import AppConfig
from django.conf import settings


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"
    _refresh_thread_started = False

    def ready(self) -> None:
        if not settings.PAYOUT_DASHBOARD_BACKGROUND_REFRESH:
            return
        if not settings.INTERNAL_DASHBOARD_API_KEY:
            return
        # Avoid duplicate threads under runserver autoreload.
        if os.environ.get("RUN_MAIN") != "true" and "runserver" in sys.argv:
            return
        if WebsiteConfig._refresh_thread_started:
            return

        from website.payout_dashboard import run_refresh_loop

        thread = threading.Thread(
            target=run_refresh_loop,
            name="payout-dashboard-refresh",
            daemon=True,
        )
        thread.start()
        WebsiteConfig._refresh_thread_started = True
