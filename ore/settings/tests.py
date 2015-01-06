try:
    from .local import *
except ImportError:
    from .development import *


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'notmigrations'


# Migrations slow down tests quite substantially, so, at least locally, don't run with migrations
MIGRATION_MODULES = DisableMigrations()