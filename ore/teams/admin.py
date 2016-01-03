from django.contrib import admin
from reversion.admin import VersionAdmin
from ore.teams.models import OrganizationTeam, ProjectTeam


class OrganizationTeamAdmin(VersionAdmin):
    pass
admin.site.register(OrganizationTeam, OrganizationTeamAdmin)


class ProjectTeamAdmin(VersionAdmin):
    pass
admin.site.register(ProjectTeam, ProjectTeamAdmin)
