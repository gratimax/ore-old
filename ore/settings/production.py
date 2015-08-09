from .base import *

DEBUG = TEMPLATE_DEBUG = False

SECRET_KEY = from_env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': from_env('DB_NAME'),
        'USER': from_env('DB_USER'),
        'PASSWORD': from_env('DB_PASSWORD'),
        'PORT': int(from_env(('POSTGRES_PORT_5432_TCP_PORT', 'DB_PORT'), 5432)),
        'HOST': from_env(('POSTGRES_PORT_5432_TCP_ADDR', 'DB_HOST')),
        'ATOMIC_REQUESTS': True,
    }
}
