from .production import *

# We don't care too much about hosts in staging
ALLOWED_HOSTS = [
    '*'
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
