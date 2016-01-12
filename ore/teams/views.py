from ore.core.views import RequiresPermissionMixin, SettingsMixin, MultiFormMixin, LockedDeleteView
from ore.projects.models import Project
from ore.core.models import Namespace, Organization
from .models import OrganizationTeam, ProjectTeam
from .forms import ProjectTeamForm, OrganizationTeamForm, MembershipManageForm, TeamDeleteForm
from django.views.generic import UpdateView, CreateView, FormView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404


class TeamManagementMixin(MultiFormMixin):

    def construct_forms(self):
        return {
            'member_add_form': MembershipManageForm(user=self.request.user, team=self.object, direction='add'),
            'settings_form': self.get_settings_form(self.object),
            'delete_form': TeamDeleteForm(instance=self.object),
        }


class NamespaceMixin(object):

    namespace_cls = Namespace

    def get_namespace(self):
        return get_object_or_404(
            self.namespace_cls.objects.as_user(self.request.user),
            name=self.kwargs['namespace']
        )


class BaseTeamUpdateView(RequiresPermissionMixin, TeamManagementMixin, NamespaceMixin, UpdateView):

    slug_url_kwarg = 'team'
    slug_field = 'name'

    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'teams': self.teams,
        })
        return super(BaseTeamUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.namespace = self.get_namespace()
        self.queryset = self.teams = self.get_teams()
        return super(BaseTeamUpdateView, self).dispatch(request, *args, **kwargs)


class BaseTeamNewView(RequiresPermissionMixin, NamespaceMixin, CreateView):

    context_object_name = 'team'

    def dispatch(self, request, *args, **kwargs):
        self.namespace = self.get_namespace()
        self.queryset = self.teams = self.get_teams()
        return super(BaseTeamNewView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(BaseTeamNewView, self).get_context_data(**kwargs)
        kwargs.update({
            'settings_form': kwargs['form'],
        })
        return kwargs


class ProjectTeamMixin(object):

    def get_context_data(self, **kwargs):
        kwargs.update({
            'proj': self.project,
        })
        return super(ProjectTeamMixin, self).get_context_data(**kwargs)

    def get_settings_form(self, team):
        return ProjectTeamForm(instance=team)

    def get_project(self):
        return get_object_or_404(
            Project.objects.as_user(self.request.user),
            namespace__name=self.kwargs['namespace'],
            name=self.kwargs['project']
        )

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_project()
        if not self.project.should_have_teams:
            raise Http404("Organization-owned projects cannot have teams")

        return super(ProjectTeamMixin, self).dispatch(request, *args, **kwargs)

    def get_teams(self):
        return ProjectTeam.objects.filter(
            project=self.project,
        )

    def get_team(self):
        return get_object_or_404(
            ProjectTeam.objects.all(),
            project=self.project,
            name=self.kwargs['team']
        )


class BaseTeamManageMembershipView(RequiresPermissionMixin, TeamManagementMixin, FormView):

    form_class = MembershipManageForm
    direction = 'add'

    def form_valid(self, form):
        team = self.get_team()
        if self.direction == 'add':
            team.users.add(*form.cleaned_data['user'])
        else:
            team.users.remove(*form.cleaned_data['user'])

        ctx = self.get_context_data()
        ctx.update({
            'form': form,
            self.form_name: form,
        })

        return self.render_to_response(ctx)

    def get_form_kwargs(self):
        kwargs = super(BaseTeamManageMembershipView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'team': self.get_team(),
            'direction': self.direction,
        })
        return kwargs


class ProjectTeamUpdateView(SettingsMixin, ProjectTeamMixin, BaseTeamUpdateView):

    form_class = ProjectTeamForm
    settings_name = 'team'

    template_name = 'projects/team_manage.html'
    form_name = 'settings_form'

    def get_permissions(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return ('project.edit', 'project.team.edit',)
        return ('project.edit',)

    def get_success_url(self):
        return reverse('projects-team-manage', kwargs={
            'namespace': self.kwargs['namespace'],
            'project': self.kwargs['project'],
            'team': self.object.name
        })


class ProjectTeamNewView(SettingsMixin, ProjectTeamMixin, BaseTeamNewView):

    form_class = ProjectTeamForm
    permissions = ('project.edit', 'project.team.create',)
    settings_name = 'team'

    template_name = 'projects/team_create.html'

    def get_success_url(self):
        return reverse('projects-team-manage', kwargs={
            'namespace': self.kwargs['namespace'],
            'project': self.kwargs['project'],
            'team': self.object.name
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = self.initial.copy()
        initial['namespace'] = self.namespace
        initial['project'] = self.project
        return initial


class ProjectTeamManageMembershipView(SettingsMixin, ProjectTeamMixin, BaseTeamManageMembershipView):

    permissions = ('project.edit', 'project.team.manage',)
    settings_name = 'team'
    template_name = 'projects/team_manage.html'

    @property
    def object(self):
        return self.get_team()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'team': self.get_team()
        })
        return super(ProjectTeamManageMembershipView, self).get_context_data(**kwargs)


class ProjectTeamAddMemberView(ProjectTeamManageMembershipView):

    form_name = 'member_add_form'
    direction = 'add'


class ProjectTeamRemoveMemberView(ProjectTeamManageMembershipView):

    form_name = 'member_remove_form'
    direction = 'remove'


class ProjectTeamDeleteView(TeamManagementMixin, SettingsMixin, ProjectTeamMixin, LockedDeleteView):

    success_url = '/'
    success_message = 'The team was deleted successfully.'

    form_class = TeamDeleteForm
    form_name = 'delete_form'

    settings_name = 'team'
    template_name = 'projects/team_manage.html'

    permissions = ('project.team.delete',)

    def get_object(self):
        return self.get_team()

    def get_form_kwargs(self):
        kwargs = super(ProjectTeamDeleteView, self).get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProjectTeamDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProjectTeamDeleteView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'team': self.get_team(),
            'show_modal': 'delete-modal',
        })
        return super(ProjectTeamDeleteView, self).get_context_data(**kwargs)
