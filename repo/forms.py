from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Fieldset, Layout
from django import forms
from django.db.models import Q
from repo.models import Project, Namespace, Organization, RepoUser, Permission


class ProjectForm(forms.ModelForm):

    namespace = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create project'))

        # TODO this doesn't exactly work, we're looking for orgs where user has permission project.create
        namespace = self.fields['namespace']
        namespace.queryset = Namespace.objects.select_subclasses(Organization, RepoUser).filter(
            Q(repouser=user) |
            Q(organization__teams__users=user))

        namespace.initial = user.id

    class Meta:
        model = Project
        fields = ['name', 'namespace', 'description']


class TeamPermissionsForm(forms.Form):
    def _get_permission_queryset(self):
        return Permission.objects.all()

    def _get_field_groups(self, known_slugs):
        groupings = [
            (
                'Version Management',
                [
                    'version.create',
                    'version.edit',
                    'version.delete',
                ]
            ),
            (
                'File Management',
                [
                    'file.create',
                    'file.edit',
                    'file.delete',
                ]
            ),
            (
                'Project Management',
                [
                    'project.create',
                    'project.edit',
                    'project.rename',
                    'project.transfer',
                    'project.delete',
                ]
            ),
            (
                'Project Team Management',
                [
                    'project.team.create',
                    'project.team.edit',
                    'project.team.manage',
                    'project.team.delete',
                ]
            ),
            (
                'Organization Team Management',
                [
                    'org.team.create',
                    'org.team.edit',
                    'org.team.manage',
                    'org.team.delete',
                ]
            )
        ]
        groupings = [
            (group_name, [
                perm_slug for perm_slug in group_perm_slugs if perm_slug in known_slugs
            ])
            for group_name, group_perm_slugs in groupings
        ]
        groupings = [(group_name, group_perm_slugs) for group_name, group_perm_slugs in groupings if len(group_perm_slugs) > 0]
        return groupings

    def __init__(self, *args, **kwargs):
        super(TeamPermissionsForm, self).__init__(*args, **kwargs)

        permissions = self._get_permission_queryset()
        self._permissions = {}

        known_perm_slugs = set()

        for i, permission in enumerate(permissions):
            field_name = 'permission_%s' % permission.slug
            self.fields[field_name] = forms.BooleanField(label=permission.name, required=False)
            self._permissions[field_name] = permission
            known_perm_slugs.add(permission.slug)

        layout_list = []
        for group_name, group_perm_slugs in self._get_field_groups(known_perm_slugs):
            layout_list.append(Fieldset(group_name, *['permission_%s' % perm_slug for perm_slug in group_perm_slugs]))
        layout_list.append(ButtonHolder(Submit('submit', 'Save')))

        self.helper = FormHelper()
        self.helper.layout = Layout(*layout_list)

    def get_selected_permissions(self):
        return [self._permissions[name] for name, value in self.cleaned_data.items() if name.startswith('permission_') and value]


class ProjectTeamPermissionsForm(TeamPermissionsForm):
    def _get_permission_queryset(self):
        qs = super(ProjectTeamPermissionsForm, self)._get_permission_queryset()
        return qs.filter(applies_to_project=True)


class OrganizationTeamPermissionsForm(TeamPermissionsForm):
    pass
