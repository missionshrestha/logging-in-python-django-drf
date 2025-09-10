from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # keep near the bottom to capture almost everything
    "scoped_logging.middleware.ScopedRequestLoggingMiddleware",
]

ROOT_URLCONF = "core.urls"
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "api.exceptions.traced_exception_handler",

    # (Optional) custom exception handler later
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "trace_ctx": {"()": "scoped_logging.context.TraceContextFilter"},
    },
    "formatters": {
        "console_fmt": {
            "format": "%(asctime)s.%(msecs)03d | %(levelname)s | %(trace_id)s | %(scope_type)s "
                      "| %(name)s:%(funcName)s:%(lineno)d — %(message)s",
            "datefmt": "%H:%M:%S",
        },
        # Optional JSON:
        # "json": {
        #   "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        #   "fmt": "%(asctime)s %(levelname)s %(trace_id)s %(scope_type)s %(name)s %(funcName)s %(lineno)d %(message)s",
        # }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "filters": ["trace_ctx"],
            "formatter": "console_fmt",
        },
        # per-scope file handlers are attached dynamically
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
