from ore.accounts.models import OreUser
from ore.core import decorators
from ore.core.models import Namespace, Organization
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import FormView, DetailView, ListView, View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import DeletionMixin, ProcessFormView, FormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.contrib.auth.decorators import login_required
from ore.projects.models import Project
from ore.teams.forms import TeamPermissionsForm


class RequiresPermissionMixin(object):
    permissions = []

    def get_permissions(self, request, *args, **kwargs):
        return self.permissions

    def dispatch(self, request, *args, **kwargs):
        return decorators.permission_required(
            self.get_permissions(request, *args, **kwargs)
        )(
            super(RequiresPermissionMixin, self).dispatch
        )(request, *args, **kwargs)


class RequiresLoggedInMixin(object):

    def dispatch(self, request, *args, **kwargs):
        return login_required()(
            super(RequiresLoggedInMixin, self).dispatch
        )(request, *args, **kwargs)


class HomeView(View, TemplateResponseMixin, ContextMixin):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return self.render_to_response(template='home/user.html', context=context)
        else:
            return self.render_to_response(template='home/home.html', context=context)

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
        if isinstance(obj, OreUser):
            return ['core/users/detail.html']
        elif isinstance(obj, Organization):
            return ['core/orgs/detail.html']

        return super(NamespaceDetailView, self).get_template_names()


class ExploreView(ListView):

    def get_queryset(self):
        return Project.objects.as_user(self.request.user).select_related('namespace')

    template_name = 'projects/index.html'
    context_object_name = 'projects'


class FormTestView(FormView):
    form_class = TeamPermissionsForm
    template_name = 'form_test.html'

    def form_valid(self, form):
        from pprint import pformat
        return HttpResponse(pformat(form.get_selected_permissions()), content_type='text/plain')


class SettingsMixin(object):

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['active_settings'] = self.settings_name
        return data


class MultiFormMixin(object):

    form_name = 'form'

    def construct_forms(self):
        return {}

    def get_context_data(self, **inkwargs):

        kwargs = self.construct_forms()
        kwargs.update(inkwargs)

        kwargs = super(
            MultiFormMixin, self
        ).get_context_data(**kwargs)

        # alias form to some other, more useful name
        kwargs[self.form_name] = kwargs['form']
        kwargs['submitted_form'] = self.form_name

        return kwargs


class LockedDeleteView(SingleObjectTemplateResponseMixin, DeletionMixin, SingleObjectMixin, FormMixin, ProcessFormView):
    # NB: the lock is bypassed if the HTTP action is "DELETE". This is
    # intentional.

    success_message = None

    def post(self, request, *args, **kwargs):
        # need to bypass DeletionMixin's handler for POST
        return ProcessFormView.post(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        resp = super(LockedDeleteView, self).delete(request, *args, **kwargs)

        success_message = self.get_success_message()
        if success_message:
            messages.success(request, success_message)

        return resp

    def get_success_message(self):
        return self.success_message

    def form_valid(self, form):
        return self.delete(self.request, self.args, self.kwargs)


@requires_csrf_token
def error404(request, exception):
    return render(request, 'error/404.html', context={'exception': exception}, status=404)


@requires_csrf_token
def error500(request, exception):
    try:
        return render(request, 'error/500.html', context={'exception': exception}, status=500)
    except:
        return render_to_response('error/500fallback.html', context={'exception': exception}, status=500)


@requires_csrf_token
def error400(request, exception):
    return render(request, 'error/400.html', context={'exception': exception}, status=400)


@requires_csrf_token
def error403(request, exception):
    return render(request, 'error/403.html', context={'exception': exception}, status=403)
