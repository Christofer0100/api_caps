from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

import dj_database_url

# -----------------------------------------------------
# PATHS
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------
# SECURITY
# -----------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# Detectar si estamos en Render
RENDER = os.environ.get("RENDER")

if RENDER:
    DEBUG = False
    ALLOWED_HOSTS = [
        os.environ.get("RENDER_EXTERNAL_HOSTNAME"),
        "localhost"
    ]
else:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# -----------------------------------------------------
# APPS
# -----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'app',
]


# -----------------------------------------------------
# REST FRAMEWORK
# -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}


# -----------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True


# -----------------------------------------------------
# URLS / WSGI
# -----------------------------------------------------
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -----------------------------------------------------
# BASE DE DATOS (Render + Local)
# -----------------------------------------------------
if RENDER:
    # BASE DE DATOS EN RENDER (usa DATABASE_URL automáticamente)
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }

else:
    # BASE DE DATOS LOCAL (PostgreSQL con search_path capstone_wsp)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("PG_NAME", "postgres"),
            "USER": os.getenv("PG_USER", "postgres"),
            "PASSWORD": os.getenv("PG_PASS", ""),
            "HOST": os.getenv("PG_HOST", "127.0.0.1"),
            "PORT": os.getenv("PG_PORT", "5432"),
            "OPTIONS": {
                "options": "-c search_path=capstone_wsp"
            },
        }
    }


# -----------------------------------------------------
# AUTH PASSWORD VALIDATORS
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------------------
# TIMEZONE
# -----------------------------------------------------
LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True  # Django convertirá a UTC internamente pero usará la zona correcta


# -----------------------------------------------------
# STATIC FILES
# -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -----------------------------------------------------
# DEFAULT PK
# -----------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------------
# CUSTOM CONFIG
# -----------------------------------------------------
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN", "whatsapp333")
