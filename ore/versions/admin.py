from django.contrib import admin
from ore.versions.models import File, Version
from reversion.admin import VersionAdmin


class VersionAdmin(VersionAdmin):
    pass
admin.site.register(Version, VersionAdmin)


class FileAdmin(VersionAdmin):
    pass
admin.site.register(File, FileAdmin)
