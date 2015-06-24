from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from ore.accounts import views

urlpatterns = patterns(
    '',
    url(r'^accounts/', include(patterns('',
                                        url(r'^login/$', views.loginview,
                                            name='accounts-login'),
                                        url(r'^logout/$', views.LogoutView.as_view(),
                                            name='accounts-logout'),
                                        url(r'^new/$', views.RegisterView.as_view(),
                                            name='accounts-register'),
                                        ))),
    url(r'^settings/', include(patterns('',
                                        url(r'^$', RedirectView.as_view(
                                            pattern_name='settings-profile'), name='settings-root'),
                                        url(r'^profile/$', views.ProfileSettings.as_view(),
                                            name='settings-profile'),
                                        ))),
)
