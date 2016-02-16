from django.apps import AppConfig
import subprocess

class CoreConfig(AppConfig):
    name = 'ore.core'

    def ready(self):
        from actstream import registry
        from ore.core.models import Organization
        registry.register(Organization)
        subprocess.run(["node", "ore/markdown"])
