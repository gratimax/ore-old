from ore.core.regexs import EXTENDED_URL_REGEX
from django.conf.urls import url, include

from .views import OrganizationSettingsView, OrganizationDeleteView, OrganizationRenameView, OrganizationCreateView

urlpatterns = [
    url(r'^organizations/new/$', OrganizationCreateView.as_view(),
            name='organizations-new'),
    url(r'^organizations/(?P<namespace>' + EXTENDED_URL_REGEX + ')/', include([
        url(r'^settings/$', OrganizationSettingsView.as_view(),
            name='organizations-settings'),
        url(r'^delete/$', OrganizationDeleteView.as_view(),
            name='organizations-delete'),
        url(r'^rename/$', OrganizationRenameView.as_view(),
            name='organizations-rename'),
    ])),
]
