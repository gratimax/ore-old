from .base import *

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = True
TEMPLATES[0]['OPTIONS']['string_if_invalid'] = 'INVALID_TEMPLATE_VARIABLE'

# COMPRESS_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': from_env('POSTGRES_ENV_POSTGRES_USER', 'repo'),
        'USER': from_env('POSTGRES_ENV_POSTGRES_USER', 'admin'),
        'PASSWORD': from_env('POSTGRES_ENV_POSTGRES_PASSWORD', 'password'),
        'PORT': int(from_env('POSTGRES_PORT_5432_TCP_PORT', 5432)),
        'HOST': from_env('POSTGRES_PORT_5432_TCP_ADDR', '127.0.0.1'),
        'ATOMIC_REQUESTS': True,
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
