import tornado
import os
from tornado.options import define, options

# Root path for the application
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Parse command-line options

define('port', default=3000, help='run on this port', type=int)
#define('debug', default=False, help='debug mode')

tornado.options.parse_command_line()

# Default settings

settings = {}

# Template directory
TEMPLATE_ROOT = os.path.join(APP_ROOT, "templates/")
settings['template_path'] = TEMPLATE_ROOT

# Staticfiles directory
STATIC_ROOT = os.path.join(APP_ROOT, "static/")
settings['static_path'] = STATIC_ROOT

# Cross-site request forgery detection
settings['xsrf_cookies'] = True

# Turn debug off by default
settings['debug'] = False

# Environments
# options: PRODUCTION, STAGING, DEVELOPMENT

ENVIRONMENT = os.environ.get('APP_ENV', 'DEVELOPMENT')

# TODO setup logging
print 'env: %s' % ENVIRONMENT

if ENVIRONMENT == 'PRODUCTION':
    import settings_production
elif ENVIRONMENT == 'STAGING':
    import settings_staging
elif ENVIRONMENT == 'DEVELOPMENT':
    import settings_development