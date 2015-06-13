from .production import *

# We don't care too much about hosts in staging
ALLOWED_HOSTS = [
    '*'
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

RAVEN_CONFIG = {
    'dsn': from_env('SENTRY_DSN', 'http://b7c76c65c6424ddf885765dafcf2173a:4f9dbb0bfd15467a94679e12abfdab48@sentry:9000/2'),
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
