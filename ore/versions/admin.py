from django.contrib import admin
from ore.versions.models import File, Version
import reversion


class VersionAdmin(reversion.VersionAdmin):
    pass
admin.site.register(Version, VersionAdmin)

class FileAdmin(reversion.VersionAdmin):
    pass
admin.site.register(File, FileAdmin)
