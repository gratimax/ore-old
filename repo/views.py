from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, View, CreateView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from repo import forms, decorators
from repo.models import Organization, Project, Namespace, RepoUser


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

    def get_namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = get_object_or_404(Namespace.objects.select_subclasses(), name=self.kwargs['namespace'])
            return self._namespace
        else:
            return self._namespace

    def get_queryset(self):
        return Project.objects.filter(namespace=self.get_namespace())

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        context['namespace'] = self.get_namespace()
        context['proj'].namespace = context['namespace']
        return context
