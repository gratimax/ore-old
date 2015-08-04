from .base import *

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

DEBUG = TEMPLATE_DEBUG = True

COMPRESS_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'repo',
        'USER': 'admin',
        'PASSWORD': 'password',
        'PORT': 5432,
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
