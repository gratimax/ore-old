from .production import *
import raven

MEDIA_URL = "/media/"
MEDIA_ROOT = '/app/media'

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': from_env('SENTRY_DSN'),
    'release': BUILD_STAMP,
}
