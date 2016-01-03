from ore.core.regexs import EXTENDED_URL_REGEX
from ore.core.views import HomeView, ExploreView, FormTestView, NamespaceDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='core-index'),
    url(r'^explore/$', ExploreView.as_view(), name='core-explore'),
    url(r'^test/$', FormTestView.as_view()),

    url(r'^(?P<namespace>' + EXTENDED_URL_REGEX + ')/$',
        NamespaceDetailView.as_view(), name='core-namespace'),
]
