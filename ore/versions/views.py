from ore.core.models import Namespace
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import DetailView, CreateView
from ore.projects.models import Project
from ore.projects.views import ProjectNavbarMixin
from ore.core.views import RequiresPermissionMixin
from ore.versions.forms import NewVersionForm, NewVersionInnerFileFormset
from ore.versions.models import Version, File


class ProjectsVersionsListView(ProjectNavbarMixin, DetailView):

    model = Project
    slug_field = 'name'
    slug_url_kwarg = 'project'

    template_name = 'versions/list.html'
    context_object_name = 'proj'
    active_project_tab = 'versions'

    def get_queryset(self):
        return Project.objects.filter(namespace__name=self.kwargs['namespace'])


class MultiFormMixin(object):
    multi_form_class = None
    multi_prefix = 'file'
    multi_initial = {}

    def get_multi_form_class(self):
        if self.multi_form_class is None:
            raise ValueError(
                "You must define multi_form_class or override get_multi_form_class!")
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

        return self.render_to_response(self.get_context_data(form=form, multi_form=multi_form))

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
        return self.render_to_response(self.get_context_data(form=form, multi_form=multi_form))

    def form_valid(self, form, multi_form):
        self.object = form.save()
        self.multi_objects = multi_form.save()

        return super(MultiFormMixin, self).form_valid(form)


class VersionsNewView(MultiFormMixin, RequiresPermissionMixin, ProjectNavbarMixin, CreateView):

    model = Version
    template_name = 'versions/new.html'

    form_class = NewVersionForm
    prefix = 'version'
    active_project_tab = 'versions'

    multi_form_class = NewVersionInnerFileFormset
    multi_prefix = 'file'
    multi_initial = {}

    permissions = ['version.create', 'file.create']

    def get_project(self):
        return get_object_or_404(Project, name=self.kwargs['project'], namespace__name=self.kwargs['namespace'])

    def get_multi_form_kwargs(self):
        kwargs = super(VersionsNewView, self).get_multi_form_kwargs()
        kwargs.update({
            'queryset': File.objects.none(),
        })
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(VersionsNewView, self).get_context_data(**kwargs)
        data.update({
            'proj': self.get_project()
        })
        return data

    def form_valid(self, form, multi_form):

        name = form.cleaned_data['name']

        if self.get_project().versions.filter(name=name).count():
            form.add_error(
                'name', 'That version name already exists in this project')
            return self.form_invalid(form, multi_form)

        self.object = form.save()

        self.multi_objects = multi_form.save(commit=False)
        for multi_object in self.multi_objects:
            multi_object.version = self.object
            multi_object.project = self.get_project()
            multi_object.save()

        return super(VersionsNewView, self).form_valid(form, multi_form)

    def get_form_kwargs(self):
        kwargs = super(VersionsNewView, self).get_form_kwargs()
        if 'instance' not in kwargs or not kwargs['instance']:
            instance = self.model(project=self.get_project())
            kwargs.update({
                'instance': instance,
            })
        return kwargs


class VersionsDetailView(ProjectNavbarMixin, DetailView):

    model = Version
    slug_field = 'name'
    slug_url_kwarg = 'version'
    template_name = 'versions/detail.html'
    active_project_tab = 'versions'

    def get_queryset(self):
        return Version.objects.as_user(self.request.user).filter(project__namespace__name=self.kwargs['namespace'], project__name=self.kwargs['project']).select_related('project')

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.as_user(
                self.request.user).select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_context_data(self, **kwargs):
        context = super(VersionsDetailView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['proj'] = context['version'].project
        return context
