from ore.core.views import RequiresPermissionMixin, RequiresLoggedInMixin, SettingsMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse

from . import models, forms


class OrganizationSettingsView(RequiresLoggedInMixin, RequiresPermissionMixin, SettingsMixin, UpdateView):
    template_name = 'organizations/settings/organization.html'
    model = models.Organization
    slug_url_kwarg = 'namespace'
    slug_field = 'name'
    form_class = forms.OrganizationSettingsForm
    permissions = ('project.edit',)

    @property
    def settings_name(self):
        return self.kwargs['namespace']

    def get_success_url(self):
        return reverse('organizations-settings', kwargs={'namespace': self.kwargs['namespace']})
