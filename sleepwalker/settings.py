"""
Django settings for sleepwalker project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import datetime
import secrets
import dotenv
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

dotenv.load_dotenv(os.path.join(PROJECT_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.token_hex(32)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG", 0))
TESTING = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework',
    'corsheaders',
    'sleepwalker.apps.authenticate',
    'sleepwalker.apps.core',
    'sleepwalker.apps.logs_sessions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

if DEBUG:
    INSTALLED_APPS.append('django.contrib.admin')
    INSTALLED_APPS.append('django.contrib.staticfiles')
    INSTALLED_APPS.append('django.contrib.messages')
    INSTALLED_APPS.append('drf_spectacular')

    MIDDLEWARE.append('django.contrib.auth.middleware.AuthenticationMiddleware')
    MIDDLEWARE.append('django.contrib.messages.middleware.MessageMiddleware')
    MIDDLEWARE.append('django.middleware.clickjacking.XFrameOptionsMiddleware')

    REDIS_HOST_NAME = "127.0.0.1"

    CELERY_BROKER_URL = "redis://127.0.0.1:6000/2"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6000/2"

else:
    REDIS_HOST_NAME = "redis"

    CELERY_BROKER_URL = "redis://redis:6000/2"
    CELERY_RESULT_BACKEND = "redis://redis:6000/2"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "auth-token",
    "api-key"
)

ROOT_URLCONF = 'sleepwalker.urls'

TEMPLATES = []

if DEBUG:
    TEMPLATES.append(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    )

WSGI_APPLICATION = 'sleepwalker.wsgi.application'

# DB Migrations
# https://docs.djangoproject.com/en/4.2/ref/settings/#migration-modules
MIGRATION_MODULES = {
    "authenticate": "database.migrations.authenticate",
    "core": "database.migrations.core",
    "logs_sessions": "database.migrations.logs_sessions"
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "dev": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sleepwalker",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": 5432
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sleepwalker",
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "postgresql",
        "PORT": 5432
    }
}

DATABASES["default"] = DATABASES["dev" if DEBUG else "production"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST_NAME}:6000/1",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
# https://docs.djangoproject.com/en/4.2/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": os.path.join(PROJECT_DIR, "logs", "log.log"),
        },
        "celery_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": os.path.join(PROJECT_DIR, "logs", "celery_log.log"),
        },
    },
    "loggers": {
        "main": {
            "level": "INFO",
            "handlers": ["file"],
        },
        "dev": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "celery_logger": {
            "handlers": ["celery_file"],
            "propagate": False,
            "level": "INFO",
        },
    },
}

LOGGER_NAME = "dev" if DEBUG else "main"
CELERY_LOGGER_NAME = "celery_logger"

AUTH_USER_MODEL = "authenticate.User"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": []
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

    SPECTACULAR_SETTINGS = {
        "TITLE": "Sleepwalker API",
        "DESCRIPTION": "",
        "VERSION": "1.0.0",
        "SERVERS": [
            {"url": "http://127.0.0.1:8000/", "description": "dev"}
        ],
        "SERVE_INCLUDE_SCHEMA": False,
        "DISABLE_ERRORS_AND_WARNINGS": True,
        "TAGS": ["auth", "user", "core", "logs_sessions", "body_sensors_logs", "environment_sensors_logs"],
        "SWAGGER_UI_SETTINGS": {
            "persistAuthorization": True,
        },
        "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@5.9.4"
    }

API_AUTH_TOKEN_LIFESPAN = datetime.timedelta(days=7)
