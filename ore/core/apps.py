from django.apps import AppConfig
import subprocess

class CoreConfig(AppConfig):
    name = 'ore.core'

    def ready(self):
        from actstream import registry
        from ore.core.models import Organization
        registry.register(Organization)
        subprocess.Popen(["node", "ore/markdown"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
