from .production import *

# We don't care too much about hosts in staging
ALLOWED_HOSTS = [
    '*'
]

USE_WHITENOISE = True
