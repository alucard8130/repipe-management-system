from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

#CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


