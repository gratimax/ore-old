from ore.core.models import Organization
from django.contrib import admin
import reversion


class OrganizationAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
