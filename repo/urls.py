from django.conf.urls import patterns, url
from repo import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^explore/$', views.index, name='repo-explore'),
    url(r'^(?P<namespace>[a-zA-Z0-9_]+)/$', views.index, name='repo-namespace'),
)
