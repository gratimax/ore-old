import os
from settings import settings

# Grab this from the environment as to not expose production secret key
settings['cookie_secret'] = os.environ.get('SECRET_KEY')