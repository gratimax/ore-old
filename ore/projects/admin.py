from django.contrib import admin
from ore.projects.models import Project
import reversion
from ore.versions.models import File


class ProjectAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

class FileAdmin(reversion.VersionAdmin):
    pass
admin.site.register(File, FileAdmin)
