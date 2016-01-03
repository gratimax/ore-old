from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import ore.core.urls
import ore.accounts.urls
import ore.projects.urls
import ore.versions.urls
import ore.teams.urls
import ore.discourse_sso.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DISCOURSE_SSO_ENABLED:
    urlpatterns += [
        url(r'', include(ore.discourse_sso.urls)),
    ]

urlpatterns += [
    url(r'', include(ore.accounts.urls)),
    url(r'', include(ore.core.urls)),
    url(r'', include(ore.projects.urls)),

    url(r'', include(ore.versions.urls)),
    url(r'', include(ore.teams.urls))
]
