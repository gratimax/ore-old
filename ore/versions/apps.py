from django.apps import AppConfig

class VersionsConfig(AppConfig):
    name = 'ore.versions'

    def ready(self):
        from actstream import registry
        from ore.versions.models import Version
        registry.register(Version)
