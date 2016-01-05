from ore.core.regexs import EXTENDED_URL_REGEX
from django.conf.urls import url, include
from ore.flags.views import ProjectsFlagView
from ore.projects.views import ProjectsNewView, ProjectsDetailView, ProjectsManageView, ProjectsDescribeView, \
    ProjectsRenameView, ProjectsDeleteView, PagesDetailView, ProjectsStarView, PagesUpdateView
from ore.teams.views import ProjectTeamUpdateView, ProjectTeamNewView, ProjectTeamAddMemberView, ProjectTeamRemoveMemberView, ProjectTeamDeleteView

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
            url(r'^teams/new/$',
                ProjectTeamNewView.as_view(), name='projects-team-new'),
            url(r'^teams/(?P<team>' + EXTENDED_URL_REGEX + ')/$',
                ProjectTeamUpdateView.as_view(), name='projects-team-manage'),
            url(r'^teams/(?P<team>' + EXTENDED_URL_REGEX + ')/add/$',
                ProjectTeamAddMemberView.as_view(), name='projects-team-add-member'),
            url(r'^teams/(?P<team>' + EXTENDED_URL_REGEX + ')/remove/$',
                ProjectTeamRemoveMemberView.as_view(), name='projects-team-remove-member'),
            url(r'^teams/(?P<team>' + EXTENDED_URL_REGEX + ')/delete/$',
                ProjectTeamDeleteView.as_view(), name='projects-team-delete'),
        ]))
]
