from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'ore.projects'

    def ready(self):
        from actstream import registry
        from ore.projects.models import Project

        registry.register(Project)
