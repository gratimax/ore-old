from .base import *

DEBUG = TEMPLATE_DEBUG = False

SECRET_KEY = from_env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgres_psycopg2',
        'NAME': from_env('DB_NAME', 'repo'),
        'USER': from_env('DB_USER'),
        'PASSWORD': from_env('DB_PASSWORD'),
        'PORT': int(from_env('DB_PORT_5432_TCP_PORT')),
        'HOST': from_env('DB_PORT_5432_TCP_ADDR'),
    }
}
