from django.contrib import admin
from . import models
import reversion


class RepoUserAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.RepoUser, RepoUserAdmin)


class OrganizationAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.Organization, OrganizationAdmin)


class ProjectAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.Project, ProjectAdmin)


class VersionAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.Version, VersionAdmin)


class FileAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.File, FileAdmin)


class OrganizationTeamAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.OrganizationTeam, OrganizationTeamAdmin)


class ProjectTeamAdmin(reversion.VersionAdmin):
    pass
admin.site.register(models.ProjectTeam, ProjectTeamAdmin)
