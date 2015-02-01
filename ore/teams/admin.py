from django.contrib import admin
import reversion
from ore.teams.models import OrganizationTeam, ProjectTeam


class OrganizationTeamAdmin(reversion.VersionAdmin):
    pass
admin.site.register(OrganizationTeam, OrganizationTeamAdmin)


class ProjectTeamAdmin(reversion.VersionAdmin):
    pass
admin.site.register(ProjectTeam, ProjectTeamAdmin)
