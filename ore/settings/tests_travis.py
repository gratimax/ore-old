from .tests import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ore',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT': 5432,
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
    }
}