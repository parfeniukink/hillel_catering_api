from datetime import timedelta
from os import getenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv(
    "SECRET_KEY",
    default="django-insecure-c3v3c$$su#@4k@rc494q!)jy#h!jps@-#2ji)(-=v9l^h9g%ft",
)
DEBUG: bool = (
    True if getenv("DEBUG", "false").lower() in ("true", "1", "on", "yes") else False
)
ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3-rd party
    "rest_framework",
    "rest_framework_simplejwt",
    # custom
    "food",
    "delivery",
    "users",
    "shared",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DATABASE_NAME", "catering"),
        "USER": getenv("DATABASE_USER", "postgres"),
        "PASSWORD": getenv("DATABASE_PASSWORD", "postgres"),
        "HOST": getenv("DATABASE_HOST", "database"),
        "PORT": getenv("DATABASE_PORT", 5432),
        # "ATOMIC_REQUESTS": False,
    }
}


CACHE_CONNECTION_STRING = getenv("CACHE_URL", "redis://cache:6379/0")

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSIOtN_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

# client -> password + login
# server -> access token + refresh token
# client -> token -> request
# server -> validated token -> user by identifier -> process request -> response
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


AUTH_USER_MODEL = "users.User"


# MAILING SECTION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailing"
EMAIL_PORT = 1025
EMAIL_HOST_USER = "mailpit"
EMAIL_HOST_PASSWORD = "mailpit"


# CELERY SECTION
# settings ref: https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = getenv("BROKER_URL", default="redis://broker:6379/0")
CELERY_ACCEPT_CONTENT = ["pickle", "application/json", "application/x-python-serialize"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_EVENT_SERIALIZER = "pickle"


# PROVIDERS SECTION
# MELANGE_BASE_URL
# BUENO_BASE_URL
# UKLON_BASE_URL
