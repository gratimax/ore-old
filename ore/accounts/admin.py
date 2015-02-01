from ore.accounts.models import OreUser
from django.contrib import admin
import reversion


class OreUserAdmin(reversion.VersionAdmin):
    pass

admin.site.register(OreUser, OreUserAdmin)
