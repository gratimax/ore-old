from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import RedirectView
from ore.accounts import views
from ore.core.regexs import EXTENDED_URL_REGEX

accounts_urlpatterns = [
    url(r'^logout/$', views.LogoutView.as_view(),
        name='accounts-logout'),
]

if not settings.DISCOURSE_SSO_ENABLED:
    accounts_urlpatterns += [
        url(r'^login/$', views.loginview,
            name='accounts-login'),
        url(r'^new/$', views.RegisterView.as_view(),
            name='accounts-register'),
    ]
else:
    sso_redirect_view = RedirectView.as_view(
        pattern_name='sso-begin', query_string=True)
    accounts_urlpatterns += [
        url(r'^login/$', sso_redirect_view,
            name='accounts-login'),
        url(r'^new/$', sso_redirect_view,
            name='accounts-register'),
    ]


urlpatterns = [
    url(r'^accounts/', include(accounts_urlpatterns)),
    url(r'^users/(?P<namespace>' + EXTENDED_URL_REGEX + ')/settings/', include([
        url(r'^$', RedirectView.as_view(
            pattern_name='accounts-settings-profile', permanent=False),
            name='accounts-settings-root'),
        url(r'^profile/$', views.ProfileSettings.as_view(),
            name='accounts-settings-profile'),
    ])),
]
