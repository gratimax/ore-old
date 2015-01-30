from django.conf.urls import patterns, url
from ore.accounts import views

urlpatterns = patterns(
    '',
    url(r'^login/$', views.loginview, name='accounts-login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='accounts-logout'),
    url(r'^new/$', views.RegisterView.as_view(), name='accounts-register'),
)
