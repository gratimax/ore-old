from ore.accounts.models import OreUser
from django.contrib import admin
from reversion.admin import VersionAdmin


class OreUserAdmin(VersionAdmin):
    pass

admin.site.register(OreUser, OreUserAdmin)
