from .production import *

# We don't care too much about hosts in staging
ALLOWED_HOSTS = [
    '*'
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
