from django.contrib import admin
from ore.projects.models import Project, Page
import reversion
from ore.versions.models import File


class ProjectAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class PageAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Page, PageAdmin)
