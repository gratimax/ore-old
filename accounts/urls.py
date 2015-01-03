from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns(
    '',
    url(r'^login/$', views.loginview),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^new/$', views.RegisterView.as_view()),
)
