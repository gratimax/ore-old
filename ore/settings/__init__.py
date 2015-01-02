# try to work out which environment we're in

import os

def importstar(module_name):
    import importlib
    module = importlib.import_module(module_name, __name__)
    module_dict = module.__dict__
    try:
        to_import = module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]
    globals().update({name: module_dict[name] for name in to_import})

environment = os.environ.get('ORE_ENVIRONMENT', 'development')
importstar('.' + environment)
