# ~/.sentry/sentry.conf.py
import os

# for more information on DATABASES, see the Django configuration at:
# https://docs.djangoproject.com/en/1.6/ref/databases/
DATABASES = {
    'default': {
        # We suggest PostgreSQL for optimal performance
        'ENGINE': 'sentry.db.postgres',

        # Alternatively you can use MySQL
        #'ENGINE': 'django.db.backends.mysql',

        'NAME': os.environ.get('DB_NAME', 'sentry'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', os.environ.get('DB_HOST')),
        'PORT': int(os.environ.get('POSTGRES_PORT_5432_TCP_PORT', os.environ.get('DB_PORT', 5432))),
    }
}

SENTRY_ADMIN_EMAIL = 'web@spongepowered.org'

# No trailing slash!
SENTRY_URL_PREFIX = ''

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 1,  # the number of gunicorn workers
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},  # detect HTTPS mode from X-Forwarded-Proto header
}

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': 'redis',
            'port': 6379,
            'timeout': 3
        }
    }
}
