from ore.core.regexs import EXTENDED_URL_REGEX, TRIM_URL_REGEX
from django.conf.urls import patterns, url, include
from ore.flags.views import VersionsFlagView
from ore.projects.views import FileDownloadView
from ore.versions.views import VersionsNewView, ProjectsVersionsListView, VersionsDetailView

urlpatterns = patterns('',
    url(r'^(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')/',
        include(patterns('',
            url(r'^upload/$', VersionsNewView.as_view(), name='versions-new'),
            url(r'^versions/$', ProjectsVersionsListView.as_view(), name='versions-list'),
            url(r'^versions/(?P<version>' + TRIM_URL_REGEX + ')/',
                include(patterns('',
                    url(r'^$', VersionsDetailView.as_view(), name='versions-detail'),
                    url(r'^manage/$', VersionsDetailView.as_view(), name='versions-manage'),
                    url(r'^flag/$', VersionsFlagView.as_view(), name='versions-flag'),
                    url(r'^delete/$', VersionsDetailView.as_view(), name='versions-delete'),
                    url(r'^(?P<file>' + TRIM_URL_REGEX + ')(?P<file_extension>\.[a-zA-Z0-9-]+)',
                        FileDownloadView.as_view(), name='versions-files-download'),
                ))
            )
        ))
    )
)
