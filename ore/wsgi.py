"""
WSGI config for ore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ore.settings.production")

from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()

# Only use whitenoise as a static files server if configured to
if settings.USE_WHITENOISE:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
