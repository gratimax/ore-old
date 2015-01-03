from django.conf.urls import patterns, url, include
from repo import views


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^explore/$', views.ExploreView.as_view(), name='repo-explore'),
    url(r'^projects/new/$', views.ProjectsNewView.as_view(), name='repo-projects-new'),
    url(r'^test/$', views.FormTestView.as_view()),

    url(r'^(?P<namespace>[\w.@+-]+)/$', views.NamespaceDetailView.as_view(), name='repo-namespace'),

    url(r'^(?P<namespace>[\w.@+-]+)/(?P<project>[\w.@+-]+)/', include(patterns('',
        url(r'^$', views.ProjectsDetailView.as_view(), name='repo-projects-detail'),
        url(r'^manage/$', views.ProjectsManageView.as_view(), name='repo-projects-manage'),
        url(r'^flag/$', views.ProjectsDetailView.as_view(), name='repo-projects-flag'),
        url(r'^describe/$', views.ProjectsDetailView.as_view(), name='repo-projects-describe'),
        url(r'^rename/$', views.ProjectsDetailView.as_view(), name='repo-projects-rename'),
        url(r'^delete/$', views.ProjectsDetailView.as_view(), name='repo-projects-delete'),

        url(r'^upload/$', views.VersionsNewView.as_view(), name='repo-versions-new'),

        url(r'^(?P<version>[\w.@+-]+)/', include(patterns('',
            url(r'^$', views.VersionsDetailView.as_view(), name='repo-versions-detail'),
            url(r'^manage/$', views.VersionsDetailView.as_view(), name='repo-versions-manage'),
            url(r'^flag/$', views.VersionsDetailView.as_view(), name='repo-versions-flag'),
            url(r'^delete/$', views.VersionsDetailView.as_view(), name='repo-versions-delete'),

            url(r'^(?P<file>[\w.@+-]+)(?P<file_extension>\.[a-zA-Z0-9-]+)', views.FileDownloadView.as_view(), name='repo-files-download'),
        ))),
    ))),

)
