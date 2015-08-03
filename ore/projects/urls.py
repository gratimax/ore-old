from ore.core.regexs import EXTENDED_URL_REGEX
from django.conf.urls import url, patterns, include
from ore.flags.views import ProjectsFlagView
from ore.projects.views import ProjectsNewView, ProjectsDetailView, ProjectsManageView, ProjectsDescribeView, \
    ProjectsRenameView, ProjectsDeleteView

urlpatterns = patterns(
    '',
    url(r'^projects/new/$', ProjectsNewView.as_view(),
        name='repo-projects-new'),
    url(r'^(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')/', include(patterns('',
                                                                                                                 url(r'^$', ProjectsDetailView.as_view(
                                                                                                                 ), name='repo-projects-detail'),
                                                                                                                 url(
                                                                                                                     r'^manage/$', ProjectsManageView.as_view(), name='repo-projects-manage'),
                                                                                                                 url(
                                                                                                                     r'^flag/$', ProjectsFlagView.as_view(), name='repo-projects-flag'),
                                                                                                                 url(r'^describe/$', ProjectsDescribeView.as_view(),
                                                                                                                     name='repo-projects-describe'),
                                                                                                                 url(r'^rename/$', ProjectsRenameView.as_view(),
                                                                                                                     name='repo-projects-rename'),
                                                                                                                 url(r'^delete/$', ProjectsDeleteView.as_view(),
                                                                                                                     name='repo-projects-delete'),
                                                                                                                 )))
)
