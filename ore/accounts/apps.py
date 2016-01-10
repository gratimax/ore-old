from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'ore.accounts'

    def ready(self):
        from actstream import registry
        from ore.accounts.models import OreUser

        registry.register(OreUser)
