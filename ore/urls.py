from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

import ore.accounts.urls
import ore.repo.urls


urlpatterns = patterns(
    '',
    url(r'^accounts/', include(ore.accounts.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(ore.repo.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
