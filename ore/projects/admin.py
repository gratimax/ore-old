from django.contrib import admin
from ore.projects.models import Project, Page
from reversion.admin import VersionAdmin
from ore.versions.models import File


class ProjectAdmin(VersionAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class PageAdmin(VersionAdmin):
    pass

admin.site.register(Page, PageAdmin)
