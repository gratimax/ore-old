from django.conf.urls import patterns, url, include
from repo import views


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^explore/$', views.ExploreView.as_view(), name='repo-explore'),
    url(r'^projects/new/$', views.ProjectsNewView.as_view(), name='repo-projects-new'),

    url(r'^(?P<namespace>[\w.@+-]+)/$', views.NamespaceDetailView.as_view(), name='repo-namespace'),

    url(r'^(?P<namespace>[\w.@+-]+)/(?P<project>[\w.@+-]+)/', include(patterns('',
        url(r'^$', views.ProjectsDetailView.as_view(), name='repo-projects-detail'),
        url(r'^manage/$', views.ProjectsDetailView.as_view(), name='repo-projects-manage'),
        url(r'^flag/$', views.ProjectsDetailView.as_view(), name='repo-projects-flag'),
        url(r'^describe/$', views.ProjectsDetailView.as_view(), name='repo-projects-describe'),
        url(r'^rename/$', views.ProjectsDetailView.as_view(), name='repo-projects-rename'),
        url(r'^delete/$', views.ProjectsDetailView.as_view(), name='repo-projects-delete'),
    ))),

)
