from .production import *
import raven

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': from_env('SENTRY_DSN')
}
