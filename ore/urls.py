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
import ore.organizations.urls

from django.views.generic import RedirectView
from ore.core.regexs import EXTENDED_URL_REGEX

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DISCOURSE_SSO_ENABLED:
    urlpatterns += [
        url(r'', include(ore.discourse_sso.urls)),
    ]

urlpatterns += [
    url(r'', include(ore.accounts.urls)),
    url(r'', include(ore.organizations.urls)),
    url(r'^users/(?P<namespace>' + EXTENDED_URL_REGEX + ')/$',
        RedirectView.as_view(pattern_name='core-namespace', permanent=False),
        name='users-root'
        ),
    url(r'^organizations/(?P<namespace>' + EXTENDED_URL_REGEX + ')/$',
        RedirectView.as_view(pattern_name='core-namespace', permanent=False),
        name='organizations-root'
        ),
    url(r'', include(ore.projects.urls)),
    url(r'', include(ore.versions.urls)),
    url(r'', include(ore.teams.urls)),
    url(r'', include(ore.core.urls)),

]
