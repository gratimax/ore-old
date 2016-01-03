from ore.core.models import Organization
from django.contrib import admin
from reversion.admin import VersionAdmin


class OrganizationAdmin(VersionAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
