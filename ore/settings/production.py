import dj_database_url
from .base import *

DEBUG = TEMPLATE_DEBUG = False

SECRET_KEY = from_env('SECRET_KEY')

db_url = os.environ.get('DB_URL', os.environ.get('DATABASE_URL'))

if db_url:

    DATABASES = {
        'default': dj_database_url.parse(db_url)
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': from_env('DB_NAME', 'repo'),
            'USER': from_env('DB_USER'),
            'PASSWORD': from_env('DB_PASSWORD'),
            'PORT': int(from_env('WEBDB_PORT_5432_TCP_PORT'), from_env('DB_PORT', 5432)),
            'HOST': from_env('WEBDB_PORT_5432_TCP_ADDR', from_env('DB_HOST')),
            'ATOMIC_REQUESTS': True,
        }
    }
