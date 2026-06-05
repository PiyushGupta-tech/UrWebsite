"""Phase 7 — print SEO audit report (run: python manage.py seo_report)."""

from django.core.management.base import BaseCommand

from website.seo_audit import run_seo_audit


class Command(BaseCommand):
    help = "Audit per-page SEO metadata, canonicals, and sitemap coverage."

    def handle(self, *_args, **_options):
        report = run_seo_audit()
        status = "OK" if report["ok"] else "ISSUES FOUND"
        self.stdout.write(
            f"SEO audit — {status}\n"
            f"  Site: {report['site_base_url']}\n"
            f"  Pages checked: {report['pages_checked']}\n"
            f"  Sitemap URLs: {report['sitemap_urls']}\n"
            f"  Related-link slugs: {report['related_link_slugs']}\n"
            f"  GSC verification configured: {report['gsc_configured']}\n"
            f"  Errors: {report['error_count']}  Warnings: {report['warning_count']}\n"
        )

        for issue in report["issues"]:
            prefix = "ERROR" if issue["level"] == "error" else "WARN"
            self.stdout.write(f"  [{prefix}] {issue['slug']}: {issue['message']}")

        if report["ok"]:
            self.stdout.write(self.style.SUCCESS("All critical SEO checks passed."))
        else:
            self.stdout.write(self.style.ERROR("Fix errors above before deploy."))
