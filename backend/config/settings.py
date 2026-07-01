import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-change-in-production",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,urbanrupee.com,www.urbanrupee.com",
    ).split(",")
    if host.strip()
]

SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "https://urbanrupee.com").rstrip("/")
GSC_SITE_VERIFICATION = os.environ.get("GSC_SITE_VERIFICATION", "").strip()

# Admin payout micro-dashboard (session auth + server-side payout proxy)
ADMIN_DASHBOARD_USERNAME = os.environ.get("ADMIN_DASHBOARD_USERNAME", "").strip()
ADMIN_DASHBOARD_PASSWORD = os.environ.get("ADMIN_DASHBOARD_PASSWORD", "").strip()
PAYOUT_DASHBOARD_API_URL = os.environ.get(
    "PAYOUT_DASHBOARD_API_URL",
    "https://payout.urbanrupee.in/api/internal/payout-dashboard",
).strip()
INTERNAL_DASHBOARD_API_KEY = os.environ.get("INTERNAL_DASHBOARD_API_KEY", "").strip()
PAYOUT_DASHBOARD_LATEST_LIMIT = int(os.environ.get("PAYOUT_DASHBOARD_LATEST_LIMIT", "1"))
PAYOUT_DASHBOARD_HTTP_TIMEOUT = int(os.environ.get("PAYOUT_DASHBOARD_HTTP_TIMEOUT", "10"))
PAYOUT_DASHBOARD_REFRESH_INTERVAL = int(os.environ.get("PAYOUT_DASHBOARD_REFRESH_INTERVAL", "10"))
PAYOUT_DASHBOARD_CACHE_TTL = int(os.environ.get("PAYOUT_DASHBOARD_CACHE_TTL", "30"))
# Dev only: background refresh thread when running manage.py runserver
PAYOUT_DASHBOARD_BACKGROUND_REFRESH = os.environ.get(
    "PAYOUT_DASHBOARD_BACKGROUND_REFRESH", "false"
).lower() in ("1", "true", "yes")

_redis_url = os.environ.get("REDIS_URL", "").strip()
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_url,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "django_cache",
        }
    }

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = not DEBUG

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "website.apps.WebsiteConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# SPA assets and index.html are served from FRONTEND_DIST via config.urls — do not
# collect them into staticfiles or WhiteNoise will serve a stale index.html at /.
STATICFILES_DIRS = []

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Avoid WhiteNoise serving backend/staticfiles/index.html instead of frontend/dist.
WHITENOISE_INDEX_FILE = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIST] if FRONTEND_DIST.exists() else [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
        },
    },
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://urbanrupee.com",
    "https://www.urbanrupee.com",
]

CONTACT_EMAIL_TO = os.environ.get("CONTACT_EMAIL_TO", "it.support@urbanrupee.com")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@urbanrupee.com")

if os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
    EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "false").lower() in ("1", "true", "yes")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}
