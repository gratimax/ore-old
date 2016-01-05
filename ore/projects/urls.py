from ore.core.regexs import EXTENDED_URL_REGEX
from django.conf.urls import url, include
from ore.flags.views import ProjectsFlagView
from ore.projects.views import ProjectsNewView, ProjectsDetailView, ProjectsManageView, ProjectsDescribeView, \
    ProjectsRenameView, ProjectsDeleteView, PagesDetailView, ProjectsStarView, PagesUpdateView

urlpatterns = [
    url(r'^projects/new/$', ProjectsNewView.as_view(),
        name='projects-new'),
    url(r'^(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')/',
        include([
            url(r'^$', ProjectsDetailView.as_view(), name='projects-detail'),
            url(r'^manage/$', ProjectsManageView.as_view(),
                name='projects-manage'),
            url(r'^flag/$', ProjectsFlagView.as_view(), name='projects-flag'),
            url(r'^describe/$', ProjectsDescribeView.as_view(),
                name='projects-describe'),
            url(r'^rename/$', ProjectsRenameView.as_view(),
                name='projects-rename'),
            url(r'^delete/$', ProjectsDeleteView.as_view(),
                name='projects-delete'),
            url(r'^pages/(?P<page>' + EXTENDED_URL_REGEX + ')/$', PagesDetailView.as_view(),
                name='projects-pages-detail'),
            url(r'^pages/(?P<page>' + EXTENDED_URL_REGEX + ')/edit/$',
                PagesUpdateView.as_view(), name='projects-pages-edit'),
            url(r'^star/$', ProjectsStarView.as_view(), name='projects-star'),
        ]))
]
