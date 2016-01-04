from ore.core.views import RequiresPermissionMixin, RequiresLoggedInMixin, SettingsMixin, MultiFormMixin, LockedDeleteView
from django.contrib import messages
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse

from . import models, forms


class OrganizationSettingsMixin(RequiresLoggedInMixin, RequiresPermissionMixin, SettingsMixin, MultiFormMixin):

    # override to some sensible defaults
    template_name = 'organizations/settings/organization.html'
    model = models.Organization
    slug_url_kwarg = 'namespace'
    slug_field = 'name'
    context_object_name = 'org'

    @property
    def settings_name(self):
        return self.kwargs['namespace']

    def construct_forms(self):
        return {
            'settings_form': forms.OrganizationSettingsForm(instance=self.object),
            'delete_form': forms.OrganizationDeleteForm(instance=self.object),
            'rename_form': forms.OrganizationRenameForm(instance=self.object)
        }


class OrganizationSettingsView(OrganizationSettingsMixin, UpdateView):

    form_class = forms.OrganizationSettingsForm
    form_name = 'settings_form'

    permissions = ('project.edit',)

    def get_success_url(self):
        return reverse('organizations-settings', kwargs={'namespace': self.kwargs['namespace']})


class OrganizationRenameView(OrganizationSettingsMixin, UpdateView):

    form_class = forms.OrganizationRenameForm
    form_name = 'rename_form'

    permissions = ('project.rename',)

    def get_success_url(self):
        return reverse('organizations-settings', kwargs={'namespace': self.object.name})

    def form_valid(self, form):
        resp = super(OrganizationRenameView, self).form_valid(form)
        messages.success(self.request, "Your organization was renamed successfully!")
        return resp


class OrganizationDeleteView(OrganizationSettingsMixin, LockedDeleteView):

    success_url = '/'
    success_message = 'The organization was deleted successfully.'

    form_class = forms.OrganizationDeleteForm
    form_name = 'delete_form'

    permissions = ('project.delete',)

    def get_form_kwargs(self):
        kwargs = super(OrganizationDeleteView, self).get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrganizationDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrganizationDeleteView, self).post(request, *args, **kwargs)