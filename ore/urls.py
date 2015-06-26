import actstream.urls
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import ore.core.urls
import ore.accounts.urls
import ore.projects.urls
import ore.versions.urls
import ore.teams.urls
import ore.discourse_sso.urls

urlpatterns = patterns(
    '',

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^activity/', include(actstream.urls)),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DISCOURSE_SSO_ENABLED:
    urlpatterns += patterns('',
        url(r'', include(ore.discourse_sso.urls)),
    )

urlpatterns += patterns('',
    url(r'', include(ore.accounts.urls)),
    url(r'', include(ore.core.urls)),
    url(r'', include(ore.projects.urls)),

    # commented out for now because there are no urls in these files
    url(r'', include(ore.versions.urls)),
    url(r'', include(ore.teams.urls))
)
