from django.db.models import Q
from ore.core.models import Namespace, Organization
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, RedirectView, FormView
from django.views.generic.detail import SingleObjectMixin
from ore.projects.forms import ProjectForm, ProjectDescriptionForm, ProjectRenameForm
from ore.projects.models import Project, Page
from ore.core.views import RequiresPermissionMixin
from ore.versions.models import File


class ProjectNavbarMixin(object):

    def get_active_project_tab(self):
        return self.active_project_tab

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_project_tab'] = self.get_active_project_tab()
        return context


class ProjectsDetailView(ProjectNavbarMixin, DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/detail.html'
    context_object_name = 'proj'
    active_project_tab = 'docs'

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).filter(namespace__name=self.kwargs['namespace'])

    def get_context_data(self, **kwargs):
        context_data = super(ProjectsDetailView, self).get_context_data(**kwargs)
        home_page = Page.objects.get(
            project=self.get_object(),
            slug='home'
        )
        context_data['home_page'] = home_page
        context_data['active_page'] = 'home'
        context_data['listed_pages'] = home_page.listed.as_user(self.request.user).all()
        return context_data

class ProjectsManageView(RequiresPermissionMixin, ProjectNavbarMixin, DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'
    active_project_tab = 'manage'

    permissions = ['project.edit']

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(
                self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).filter(namespace=self.get_namespace())

    def get_context_data(self, **kwargs):
        context = super(ProjectsManageView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['description_form'] = ProjectDescriptionForm(
            project=self.object.name, namespace=self.get_namespace().name,
            initial=dict(description=self.object.description))
        context['rename_form'] = ProjectRenameForm(
            project=self.object.name, namespace=self.get_namespace().name,
            initial=dict(name=self.object.name))
        return context


class ProjectsDescribeView(RequiresPermissionMixin, ProjectNavbarMixin, UpdateView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'
    active_project_tab = 'manage'

    permissions = ['project.edit']

    form_class = ProjectDescriptionForm

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(
                self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_context_data(self, **kwargs):
        context = super(ProjectsDescribeView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['rename_form'] = ProjectRenameForm(
            project=self.object.name, namespace=self.get_namespace().name,
            initial=dict(name=self.object.name))
        context['description_form'] = kwargs['form']
        return context

    def get_form_kwargs(self):
        kwargs = super(ProjectsDescribeView, self).get_form_kwargs()
        kwargs['project'] = self.object.name
        kwargs['namespace'] = self.get_namespace().name
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request, "The project's description has been changed.")
        return redirect(reverse('repo-projects-manage',
                                kwargs=dict(namespace=self.get_namespace().name, project=self.object.name)))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return super(ProjectsDescribeView, self).dispatch(request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)


class ProjectsRenameView(RequiresPermissionMixin, ProjectNavbarMixin, UpdateView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'
    active_project_tab = 'manage'

    permissions = ['project.rename']

    form_class = ProjectRenameForm

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(
                self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_context_data(self, **kwargs):
        context = super(ProjectsRenameView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['rename_form'] = kwargs['form']
        context['show_modal'] = 'rename-modal'
        context['description_form'] = ProjectDescriptionForm(
            project=self.object.name, namespace=self.get_namespace().name,
            initial=dict(description=self.object.description))
        return context

    def get_form_kwargs(self):
        kwargs = super(ProjectsRenameView, self).get_form_kwargs()
        kwargs['project'] = self.object.name
        kwargs['namespace'] = self.get_namespace().name
        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        name = form.cleaned_data['name']
        namespace = form.cleaned_data['namespace']

        if namespace.projects.filter(name=name).count():
            form.add_error(
                'name', 'That project already exists for the given namespace')
            return self.form_invalid(form)

        messages.success(self.request, "The project's name has been changed.")
        return redirect(reverse('repo-projects-manage',
                                kwargs=dict(namespace=self.get_namespace().name, project=self.object.name)))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return super(ProjectsRenameView, self).dispatch(request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)


class ProjectsDeleteView(RequiresPermissionMixin, ProjectNavbarMixin, DeleteView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'
    active_project_tab = 'manage'

    permissions = ['project.delete']

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])

    def get_success_url(self):
        return reverse('repo-namespace', kwargs=dict(namespace=self.object.namespace.name))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return super(ProjectsDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)


class FileDownloadView(RedirectView, SingleObjectMixin):

    model = File
    slug_field = 'file_name'
    slug_url_kwarg = 'file'
    permanent = False

    def get_queryset(self):
        return File.objects.as_user(self.request.user).filter(
            version__project__namespace__name=self.kwargs['namespace'],
            version__project__name=self.kwargs['project'],
            version__name=self.kwargs['version']
        )

    def get_redirect_url(self, **kwargs):
        return self.get_object().file.url


class ProjectsNewView(FormView):

    template_name = 'repo/projects/new.html'
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super(ProjectsNewView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        name = form.cleaned_data['name']
        namespace = form.cleaned_data['namespace']
        description = form.cleaned_data['description']

        if namespace.projects.filter(name=name).count():
            form.add_error(
                'name', 'That project already exists for the given namespace')
            return self.form_invalid(form)

        if isinstance(namespace, Organization) and not namespace.user_has_permission(self.request.user, 'org.project.create'):
            form.add_error(
                'name', 'You do not have permission to create a project for that namespace')
            return self.form_invalid(form)

        project = Project.objects.create(
            name=name, namespace=namespace, description=description)
        project.save()

        messages.success(self.request, "Your project has been created")

        return redirect(reverse('repo-projects-detail', args=(namespace.name, project.name)))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectsNewView, self).dispatch(request, *args, **kwargs)


class PagesDetailView(ProjectNavbarMixin, DetailView):

    model = Page
    slug_field = 'slug'
    slug_url_kwarg = 'page'

    template_name = 'repo/projects/pages/detail.html'
    context_object_name = 'page'
    active_project_tab = 'docs'

    def get_queryset(self):
        return Page.objects.as_user(self.request.user).filter(
            Q(
                project__namespace__name=self.kwargs['namespace'],
                project__name=self.kwargs['project'],
            ) & ~Q(slug='home')).select_related('project')

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(
                self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_context_data(self, **kwargs):
        context_data = super(PagesDetailView, self).get_context_data(**kwargs)
        context_data['namespace'] = self.get_namespace()
        context_data['proj'] = context_data['page'].project
        context_data['active_page'] = self.get_object().slug
        context_data['listed_pages'] = self.get_object().listed.as_user(self.request.user).all()
        context_data['listed_by'] = self.get_object().listed_by.as_user(self.request.user).all()
        return context_data
