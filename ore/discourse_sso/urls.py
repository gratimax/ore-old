from django.conf.urls import url, include
from .views import SSOBeginView, SSOReturnView

urlpatterns = [
    url(r'^sso/', include([
                          url(r'^$', SSOBeginView.as_view(), name='sso-begin'),
                          url(r'^return/$', SSOReturnView.as_view(),
                              name='sso-return'),
                          ])),
]
