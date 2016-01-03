from ore.core.regexs import EXTENDED_URL_REGEX
from django.conf.urls import url, include

from .views import OrganizationSettingsView

urlpatterns = [
    url(r'^organizations/(?P<organization_slug>' + EXTENDED_URL_REGEX + ')/settings/', include([
        url(r'^$', OrganizationSettingsView.as_view(),
            name='organizations-settings'),
    ])),
]
