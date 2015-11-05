from .production import *
import raven

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

with open('APP-VERSION') as f:
    app_version = f.readlines().strip()

RAVEN_CONFIG = {
    'dsn': from_env('SENTRY_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': app_version,
}
