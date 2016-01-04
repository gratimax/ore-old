from django.contrib import admin
from ore.projects.models import Project, Page, Channel
from reversion.admin import VersionAdmin
from ore.versions.models import File


class ProjectAdmin(VersionAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class ChannelAdmin(VersionAdmin):
    pass


admin.site.register(Channel, ChannelAdmin)


class PageAdmin(VersionAdmin):
    pass

admin.site.register(Page, PageAdmin)
