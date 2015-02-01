from django.contrib import admin
import reversion
from reversion.models import Version


class VersionAdmin(reversion.VersionAdmin):
    pass
admin.site.register(Version, VersionAdmin)
