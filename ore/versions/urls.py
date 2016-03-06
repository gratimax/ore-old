from ore.core.regexs import EXTENDED_URL_REGEX, TRIM_URL_REGEX
from django.conf.urls import url, include
from ore.flags.views import VersionsFlagView
from ore.projects.views import FileDownloadView
from ore.versions.views import VersionsNewView, ProjectsVersionsListView, VersionsDetailView, \
    DeleteChannelView, EditChannelView, ChannelsListView, VersionsManageView, VersionsDeleteView, \
    VersionsUploadView, FileDeleteView

urlpatterns = [
    url(r'^(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')/', include([
        url(r'^upload/$', VersionsNewView.as_view(), name='versions-new'),
        url(r'^versions/$', ProjectsVersionsListView.as_view(), name='versions-list'),
        url(r'^versions/(?P<version>' + TRIM_URL_REGEX + ')/', include([
                url(r'^$', VersionsDetailView.as_view(), name='versions-detail'),
                url(r'^manage/$', VersionsManageView.as_view(), name='versions-manage'),
                url(r'^upload/$', VersionsUploadView.as_view(), name='versions-upload'),
                url(r'^flag/$', VersionsFlagView.as_view(), name='versions-flag'),
                url(r'^delete/$', VersionsDeleteView.as_view(), name='versions-delete'),
                url(r'^(?P<file>' + TRIM_URL_REGEX + r')(?P<file_extension>\.[a-zA-Z0-9\-]+)/delete/$', FileDeleteView.as_view(), name='versions-files-delete'),
                url(r'^(?P<file>' + TRIM_URL_REGEX + r')(?P<file_extension>\.[a-zA-Z0-9\-]+)$',
                    FileDownloadView.as_view(), name='versions-files-download'),
        ])),
        url(r'^manage/channels/', include([
            url(r'^$', ChannelsListView.as_view(), name='project-channels'),
            url(r'^(?P<channel>' + EXTENDED_URL_REGEX + ')/', include([
                url(r'^$', EditChannelView.as_view(), name='channel-edit'),
                url(r'^delete/$', DeleteChannelView.as_view(), name='channel-delete'),
            ])),
        ]))
    ]))
]
