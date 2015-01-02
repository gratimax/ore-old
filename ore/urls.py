from django.conf.urls import patterns, include, url
from django.contrib import admin
import repo.urls

urlpatterns = patterns(
    '',
    url(r'^$', include(repo.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
