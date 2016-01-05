from ore.core.models import Permission
from ore.accounts.models import OreUser
from .models import Team, OrganizationTeam, ProjectTeam
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, ButtonHolder, Submit, Layout, Field, Hidden, Div, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

__author__ = 'max'


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
                    'org.project.create',
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
        groupings = [(group_name, group_perm_slugs) for group_name,
                     group_perm_slugs in groupings if len(group_perm_slugs) > 0]
        return groupings

    def __init__(self, *args, **kwargs):
        super(TeamPermissionsForm, self).__init__(*args, **kwargs)

        permissions = self._get_permission_queryset()
        self._permissions = {}

        known_perm_slugs = set()

        for i, permission in enumerate(permissions):
            field_name = 'permission_%s' % permission.slug
            self.fields[field_name] = forms.BooleanField(
                label=permission.name, required=False)
            self._permissions[field_name] = permission
            known_perm_slugs.add(permission.slug)

        layout_list = []
        for group_name, group_perm_slugs in self._get_field_groups(known_perm_slugs):
            layout_list.append(Fieldset(
                group_name, *['permission_%s' % perm_slug for perm_slug in group_perm_slugs]))
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


class TeamForm(forms.ModelForm):

    @property
    def is_owner_team(self):
        inst = getattr(self, 'instance', None)
        return bool(inst and inst.is_owner_team)

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        
        readonly = {}
        if self.is_owner_team:
            readonly['readonly'] = 'readonly'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', **readonly),
            'description',
            Div(
                Field('permissions'), css_class='hide' if self.is_owner_team else ''
            ),
            Submit('save', 'Save')
        )

    def clean_name(self, *args, **kwargs):
        if self.is_owner_team:
            return self.instance.name
        return self.cleaned_data['name']

    def clean_permissions(self, *args, **kwargs):
        if self.is_owner_team:
            return self.instance.permissions.all()
        return self.cleaned_data['permissions']

    class Meta:
        model = Team
        fields = ['name', 'description', 'permissions']


class ProjectTeamForm(TeamForm):

    def __init__(self, *args, **kwargs):
        super(ProjectTeamForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.helper.form_action = reverse('projects-team-manage', kwargs={
                'namespace': self.instance.project.namespace.name,
                'project': self.instance.project.name,
                'team': self.instance.name,
            })

    def clean_name(self, *args, **kwargs):
        final_name = super(ProjectTeamForm, self).clean_name()
        project = self.initial.get('project', None)
        if self.instance.id:
            project = self.instance.project
        qs = ProjectTeam.objects.filter(project=project, name=final_name)
        if self.instance.id:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise ValidationError("That team name is already in use.")
        return final_name

    class Meta(TeamForm.Meta):
        model = ProjectTeam

class OrganizationTeamForm(TeamForm):

    class Meta(TeamForm.Meta):
        model = OrganizationTeam

class CommaSeparatedTextInput(forms.TextInput):

    def _format_value(self, value):
        return ', '.join(value)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if not value:
            return value
        return [v.strip() for v in value.split(',')]

class MembershipManageForm(forms.Form):

    user = forms.ModelMultipleChoiceField(queryset=None, to_field_name="name", widget=CommaSeparatedTextInput())
    #user = forms.ModelMultipleChoiceField(queryset=None, to_field_name="name")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        team = kwargs.pop('team')
        direction = kwargs.pop('direction')
        super(MembershipManageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user'),
            Submit('Add member', 'Add member'),
        )
        self.helper.form_action = team.get_member_add_url()
        if direction == 'add':
            self.fields['user'].queryset = OreUser.objects.as_user(user).exclude(id__in=team.users.values('id'))
        else:
            self.fields['user'].queryset = OreUser.objects.as_user(user).filter(id__in=team.users.values('id'))


class TeamDeleteForm(forms.Form):

    lock = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
            
        super(TeamDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        if isinstance(self.instance, ProjectTeam):
            self.helper.form_action = reverse(
                'projects-team-delete', kwargs={'namespace': self.instance.project.namespace.name, 'project': self.instance.project.name, 'team': self.instance.name},
            )
        self.helper.form_show_labels = False
        self.helper.form_class = "js-lock-form"
        self.helper.attrs = {
            'data-confirm': self.instance.name,
            'data-input': 'input[name="lock"]',
            'data-locks': 'button',
        }
        self.helper.layout = Layout(
            HTML("""
                <p>Removing this team will remove the additional permissions granted to all of its members.</p>
                <p>Please type the name of the team (<tt>{{ team.name }}</tt>) to confirm deletion.</p>
            """),
            FieldWithButtons(
                Field('lock'), StrictButton('<i class="fa fa-times"></i> Delete', css_class='btn-danger', type='submit')),
        )

    def clean_lock(self):
        lock = self.cleaned_data['lock']
        if lock != self.instance.name:
            raise ValidationError(
                'You must type the team name exactly, including any capitalisation.')
        return lock