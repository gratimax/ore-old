from .base import *

DEBUG = TEMPLATE_DEBUG = False

SECRET_KEY = from_env('SECRET_KEY')

COMPRESS_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': from_env('DB_NAME', 'repo'),
        'USER': from_env('DB_USER'),
        'PASSWORD': from_env('DB_PASSWORD'),
        'PORT': int(from_env('POSTGRES_PORT_5432_TCP_PORT', from_env('DB_PORT', 5432))),
        'HOST': from_env('POSTGRES_PORT_5432_TCP_ADDR', os.environ.get('DB_HOST')),
        'ATOMIC_REQUESTS': True,
    }
}
