from django.conf.urls import patterns, url
from repo import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^explore/$', views.HomeView.as_view(), name='repo-explore'),
    url(r'^projects/new/$', views.ProjectsNewView.as_view(), name='repo-projects-new'),

    url(r'^(?P<namespace>[\w.@+-]+)/$', views.NamespaceDetailView.as_view(), name='repo-namespace'),
    url(r'^(?P<namespace>[\w.@+-]+)/(?P<project>[\w.@+-]+)/$', views.ProjectsDetailView.as_view(), name='repo-projects-detail')
)
