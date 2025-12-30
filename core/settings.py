import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env for development (if present). This allows DEBUG and other
# settings to be provided from a .env file without requiring explicit export.
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=BASE_DIR / '.env')
except Exception:
    # If python-dotenv isn't installed or .env doesn't exist, silently continue
    pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY
# Load secret from env, but fall back to existing insecure one for local/dev convenience.
# Make sure to set SECRET_KEY in your Render/production environment.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-%_g38d_$48+stbb3^#$47!z8%j)8cz#o)=70np1a_y7$5zcq(="
)

# DEBUG should be False in production. Control with environment variable.
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: comma-separated list
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")).split(",") if os.environ.get("ALLOWED_HOSTS") or os.environ.get("RENDER_EXTERNAL_HOSTNAME") else []

ALLOWED_HOSTS = '*' 
# Application definition



CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://grandstor.uz",
    "https://grandstor.uz"
]




INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parda.apps.PardaConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Database — local sqlite only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Local dev: use default staticfiles storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files (uploaded images etc.) — local development defaults
MEDIA_URL = os.environ.get('MEDIA_URL', '/curtains/')
MEDIA_ROOT = Path(os.environ.get('MEDIA_ROOT', str(BASE_DIR / 'curtains')))






CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Store task results in Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Serialization settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Timezone settings
CELERY_TIMEZONE = 'Asia/Tashkent'
CELERY_ENABLE_UTC = False

# Optional: Task result expiration time (in seconds)
CELERY_RESULT_EXPIRES = 3600

# Optional: Task time limit (15 minutes max per task)
CELERY_TASK_TIME_LIMIT = 900


# ============================================
# TELEGRAM CONFIGURATION
# ============================================

# Get bot token from @BotFather on Telegram


# For single group:



TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ============================================
# LOGGING (Optional but recommended)
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'celery.log',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'parda': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}













# Ensure MEDIA_ROOT is inside the project and writable. If a relative path was
# provided, resolve it against BASE_DIR. If the resolved path is outside of
# BASE_DIR, fall back to BASE_DIR/'curtains'. Create the directory if missing
# and attempt to make it writable.
try:
    import warnings

    _media_root = Path(MEDIA_ROOT)
    if not _media_root.is_absolute():
        _media_root = (BASE_DIR / _media_root).resolve()

    # If resolved MEDIA_ROOT is not inside BASE_DIR, fallback
    base_resolved = BASE_DIR.resolve()
    if _media_root != base_resolved and base_resolved not in list(_media_root.parents):
        warnings.warn(
            f"MEDIA_ROOT '{_media_root}' is outside project BASE_DIR; using BASE_DIR/'curtains' instead."
        )
        _media_root = (BASE_DIR / 'curtains').resolve()

    # Create directory and ensure writable
    _media_root.mkdir(parents=True, exist_ok=True)
    try:
        if not os.access(str(_media_root), os.W_OK):
            _media_root.chmod(0o755)
    except Exception:
        warnings.warn(f"Could not set permissions on MEDIA_ROOT '{_media_root}'.")

    MEDIA_ROOT = _media_root
except Exception as exc:
    import warnings

    warnings.warn(f"Error configuring MEDIA_ROOT: {exc}. Falling back to BASE_DIR/'curtains'.")
    MEDIA_ROOT = (BASE_DIR / 'curtains')
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security defaults (toggleable via env vars)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('1', 'true', 'yes')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() in ('1', 'true', 'yes')
    CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True').lower() in ('1', 'true', 'yes')
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '3600'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ('1', 'true', 'yes')
    SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True').lower() in ('1', 'true', 'yes')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')




