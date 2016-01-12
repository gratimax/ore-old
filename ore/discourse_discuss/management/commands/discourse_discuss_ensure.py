from django.core.management.base import BaseCommand, CommandError
from ore.projects.models import Project
from ore.discourse_discuss.models import DiscourseProjectThread


class Command(BaseCommand):
    help = 'Ensures all projects have threads and that the thread content matches the main page content'

    def add_arguments(self, parser):
        parser.add_argument('project_id', nargs='*', type=int)

    def handle(self, *args, **options):
        total_count = 0
        updated_count = 0
        project_ids = options.get('project_id', None)
        if not project_ids:
            project_ids = Project.objects.all().values_list('id', flat=True)
        for project_id in project_ids:
            try:
                project = Project.objects.get(pk=project_id)
                updated = DiscourseProjectThread.objects.update_or_create_for_project(project)

                total_count += 1
                if updated:
                    self.stdout.write("Updated {}".format(project))
                    updated_count += 1
                else:
                    self.stdout.write("Left alone {}".format(project))
            except Project.DoesNotExist:
                raise CommandError(
                    "Project '{}' does not exist!".format(project_id))
        self.stdout.write(self.style.SUCCESS("Updated {} of {} inspected".format(updated_count, total_count)))
