from .base import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'repo',
        'USER': 'admin',
        'PASSWORD': 'password',
        'PORT': 5432,
        'HOST': 'localhost',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
