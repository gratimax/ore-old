from django.views.generic import DetailView

from .models import DiscourseProjectThread
from ore.projects.models import Project
from ore.projects.views import ProjectNavbarMixin


class ProjectsDiscussView(ProjectNavbarMixin, DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'projects/discuss.html'
    context_object_name = 'proj'
    active_project_tab = 'discuss'

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).filter(namespace__name=self.kwargs['namespace'])

    def get_context_data(self, **kwargs):
        context_data = super(
            ProjectsDiscussView, self).get_context_data(**kwargs)
        context_data['active_page'] = 'discuss'
        context_data['project_thread'] = DiscourseProjectThread.objects.update_or_create_for_project(self.object)
        return context_data
