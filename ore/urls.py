from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import repo.urls
import accounts.urls


urlpatterns = patterns(
    '',
    url(r'^accounts/', include(accounts.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(repo.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
