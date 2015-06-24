from actstream import registry
from django.apps import AppConfig


class AccountsAppConfig(AppConfig):

    name = 'ore.accounts'

    def ready(self):
        registry.register(self.get_model('OreUser'))
