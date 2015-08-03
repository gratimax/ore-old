from django.conf.urls import patterns, url, include
from .views import SSOBeginView, SSOReturnView

urlpatterns = patterns(
    '',
    url(r'^sso/', include(patterns('',
                          url(r'^$', SSOBeginView.as_view(), name='sso-begin'),
                          url(r'^return/$', SSOReturnView.as_view(),
                              name='sso-return'),
                          ))),
)
