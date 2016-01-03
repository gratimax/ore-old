from ore.core.views import RequiresLoggedInMixin, SettingsMixin
from django.views.generic import TemplateView


class OrganizationSettingsView(RequiresLoggedInMixin, SettingsMixin, TemplateView):
    template_name = 'organizations/settings/organization.html'

    @property
    def settings_name(self):
        return self.kwargs['organization_slug']
