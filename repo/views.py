from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, View, CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse
from repo import forms, decorators
from repo.forms import ProjectDescriptionForm, ProjectRenameForm, FlagForm
from repo.models import Organization, Project, Namespace, RepoUser, Version, File, Flag
from django.contrib.contenttypes.models import ContentType


class RequiresPermissionMixin(object):
    permissions = []

    def get_permissions(self):
        return self.permissions

    def dispatch(self, request, *args, **kwargs):
        return decorators.permission_required(self.get_permissions())(super(RequiresPermissionMixin, self).dispatch)(request, *args, **kwargs)


class HomeView(View, TemplateResponseMixin, ContextMixin):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return self.render_to_response(template='home/user.html', context=context)
        else:
            return self.render_to_response(template='home/index.html', context=context)

    def render_to_response(self, context, template, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )


class ExploreView(ListView):

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).select_related('namespace')

    template_name = 'repo/projects/index.html'
    context_object_name = 'projects'


class NamespaceDetailView(DetailView):

    model = Namespace
    slug_field = 'name'
    slug_url_kwarg = 'namespace'

    def get_queryset(self, *args, **kwargs):
        qs = super(NamespaceDetailView, self).get_queryset(*args, **kwargs)
        qs = qs.select_subclasses()
        qs = qs.prefetch_related('projects')
        return qs

    def get_template_names(self):
        obj = self.object
        if isinstance(obj, RepoUser):
            return ['repo/users/detail.html']
        elif isinstance(obj, Organization):
            return ['repo/orgs/detail.html']

        return super(NamespaceDetailView, self).get_template_names()

class ProjectsNewView(FormView):

    template_name = 'repo/projects/new.html'
    form_class = forms.ProjectForm

    def get_form_kwargs(self):
        kwargs = super(ProjectsNewView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        name = form.cleaned_data['name']
        namespace = form.cleaned_data['namespace']
        description = form.cleaned_data['description']

        if namespace.projects.filter(name=name).count():
            form.add_error('name', 'That project already exists for the given namespace')
            return self.form_invalid(form)

        if isinstance(namespace, Organization) and not namespace.user_has_permission(self.request.user, 'project.create'):
            form.add_error('name', 'You do not have permission to create a project for that namespace')
            return self.form_invalid(form)

        project = Project.objects.create(name=name, namespace=namespace, description=description)
        project.save()

        messages.success(self.request, "Your project has been created")

        return redirect(reverse('repo-projects-detail', args=(namespace.name, project.name)))


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectsNewView, self).dispatch(request, *args, **kwargs)




class ProjectsDetailView(DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/detail.html'
    context_object_name = 'proj'

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).filter(namespace__name=self.kwargs['namespace'])


class ProjectsManageView(RequiresPermissionMixin, DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'

    permissions = ['project.edit']

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(self.request.user).select_subclasses(), name=self.kwargs['namespace'])
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


class ProjectsDescribeView(RequiresPermissionMixin, UpdateView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'

    permissions = ['project.edit']

    form_class = ProjectDescriptionForm

    fields = ['description']

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(self.request.user).select_subclasses(), name=self.kwargs['namespace'])
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
        messages.success(self.request, "The project's description has been changed.")
        return redirect(reverse('repo-projects-manage',
                                kwargs=dict(namespace=self.get_namespace().name, project=self.object.name)))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return super(ProjectsDescribeView, self).dispatch(request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)


class ProjectsRenameView(RequiresPermissionMixin, UpdateView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'

    permissions = ['project.rename']

    form_class = ProjectRenameForm

    fields = ['name']

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(self.request.user).select_subclasses(), name=self.kwargs['namespace'])
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
        messages.success(self.request, "The project's name has been changed.")
        return redirect(reverse('repo-projects-manage',
                                kwargs=dict(namespace=self.get_namespace().name, project=self.object.name)))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return super(ProjectsRenameView, self).dispatch(request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)


class ProjectsDeleteView(RequiresPermissionMixin, DeleteView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/projects/manage.html'
    context_object_name = 'proj'

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


class ProjectsVersionsListView(DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'repo/versions/list.html'
    context_object_name = 'proj'

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])


class FormTestView(FormView):
    form_class = forms.TeamPermissionsForm
    template_name = 'form_test.html'

    def form_valid(self, form):
        from pprint import pformat
        return HttpResponse(pformat(form.get_selected_permissions()), content_type='text/plain')


class VersionsNewView(RequiresPermissionMixin, CreateView):

    model = Version
    template_name = 'repo/versions/new.html'

    form_class = forms.NewVersionForm
    prefix = 'version'

    multi_form_class = forms.NewVersionInnerFileFormset
    multi_prefix = 'file'
    multi_initial = {}

    permissions = ['version.create', 'file.create']

    def get_project(self):
        return get_object_or_404(Project, name=self.kwargs['project'], namespace__name=self.kwargs['namespace'])

    def get_multi_form_class(self):
        return self.multi_form_class

    def get_multi_form_kwargs(self):
        kwargs = {
            'initial': self.get_multi_initial(),
            'prefix': self.get_multi_prefix(),
            'queryset': File.objects.none(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_multi_initial(self):
        return self.multi_initial.copy()

    def get_multi_prefix(self):
        return self.multi_prefix

    def get_multi_form(self, form_class):
        return form_class(**self.get_multi_form_kwargs())

    def get(self, request, *args, **kwargs):
        self.object = None

        multi_form_class = self.get_multi_form_class()
        multi_form = self.get_multi_form(multi_form_class)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form, multi_form=multi_form, proj=self.get_project()))

    def post(self, request, *args, **kwargs):
        self.object = None

        multi_form_class = self.get_multi_form_class()
        multi_form = self.get_multi_form(multi_form_class)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid() and multi_form.is_valid():
            return self.form_valid(form, multi_form)
        else:
            return self.form_invalid(form, multi_form)

    def form_invalid(self, form, multi_form):
        return self.render_to_response(self.get_context_data(form=form, multi_form=multi_form, proj=self.get_project()))

    def form_valid(self, form, multi_form):
        self.object = form.save()

        self.multi_objects = multi_form.save(commit=False)
        import posixpath
        for multi_object in self.multi_objects:
            multi_object.version = self.object
            _, multi_object.file_extension = posixpath.splitext(multi_object.file.name)
            multi_object.file_size = multi_object.file.size
            multi_object.save()

        return super(CreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        if 'instance' not in kwargs or not kwargs['instance']:
            instance = self.model(project=self.get_project())
            kwargs.update({
                'instance': instance,
            })
        return kwargs


class VersionsDetailView(DetailView):

    model = Version
    slug_field = 'name'
    slug_url_kwarg = 'version'
    template_name = 'repo/versions/detail.html'

    def get_queryset(self):
        return Version.objects.as_user(self.request.user).filter(project__namespace__name=self.kwargs['namespace'], project__name=self.kwargs['project']).select_related('project')

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_context_data(self, **kwargs):
        context = super(VersionsDetailView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['proj'] = context['version'].project
        return context


class FileDownloadView(RedirectView, SingleObjectMixin):
    
    model = File
    slug_field = 'name'
    slug_url_kwarg = 'file'
    
    def get_queryset(self):
        return File.objects.as_user(self.request.user).filter(version__project__namespace__name=self.kwargs['namespace'], version__project__name=self.kwargs['project'], version__name=self.kwargs['version'])

    def get_redirect_url(self, **kwargs):
        return self.get_object().file.url

class FlagView(FormView):
    template_name = 'repo/flag.html'
    form_class = forms.FlagForm

    def get_form_kwargs(self):
        kwargs = super(FlagView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        flag_type = form.cleaned_data['flag_type']
        extra_comments = form.cleaned_data['extra_comments']
        flagger = self.request.user
        content = self._get_model().objects.get(name=self.kwargs[self._get_string()])

        Flag.create_flag(content, flag_type, flagger, extra_comments)
        messages.success(self.request, "You have successfully flagged the content.")

        return redirect(reverse('index'))

    def _get_model(self):
        return Flag
    def _get_string(self):
        return 'flag'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FlagView, self).dispatch(request, *args, **kwargs)

class ProjectsFlagView(FlagView):
    def _get_model(self):
        return Project
    def _get_string(self):
        return 'project'
