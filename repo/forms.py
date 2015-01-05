from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Fieldset, Layout, HTML, Div
from django import forms
from django.core import validators
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from repo.models import Project, Namespace, Organization, RepoUser, Permission, Version, File, Flag
from repo.regexs import EXTENDED_NAME_REGEX


class ProjectForm(forms.ModelForm):

    namespace = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create project'))

        namespace = self.fields['namespace']
        namespace.queryset = Namespace.objects.select_subclasses(Organization, RepoUser).filter(
            Q(repouser=user) |
            (Q(organization__teams__users=user) & (Q(organization__teams__is_owner_team=True) | Q(organization__teams__permissions__slug='project.create')))
        )

        namespace.initial = user.id

    class Meta:
        model = Project
        fields = ['name', 'namespace', 'description']

class FlagForm(forms.ModelForm):
    REASON_CHOICES = (
        ('inappropriate', 'Inappropriate'),
        ('spam', 'Spam')
    )
    flag_type = forms.ChoiceField(choices=REASON_CHOICES)
    extra_comments = forms.CharField(widget=forms.Textarea(attrs={'rows': '6'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FlagForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Flag Content'))

    class Meta:
        model = Flag
        fields = ['flag_type', 'extra_comments']

class ProjectDescriptionForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))

    def __init__(self, *args, **kwargs):
        namespace = kwargs.pop('namespace')
        project = kwargs.pop('project')
        super(ProjectDescriptionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.form_class = 'form-horizontal project-description-form'
        self.helper._form_action = reverse('repo-projects-describe',
                                           kwargs=dict(namespace=namespace, project=project))

        self.helper.layout = Layout(
            'description',
            Div(
                ButtonHolder(
                    Submit('submit', 'Change description', css_class='btn-default'),
                    css_class='col-md-offset-2 col-md-10'
                ),
                css_class='form-group',
            ),
            Div(
                css_class='clearfix'
            )
        )

    class Meta:
        model = Project
        fields = ['description']


class ProjectRenameForm(forms.ModelForm):

    name = forms.CharField(max_length=32,
                           validators=[
                               validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a valid project name.', 'invalid')
                           ])

    def __init__(self, *args, **kwargs):
        namespace = kwargs.pop('namespace')
        project = kwargs.pop('project')
        super(ProjectRenameForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper._form_action = reverse('repo-projects-rename',
                                           kwargs=dict(namespace=namespace, project=project))

        self.helper.layout = Layout(
            Div(
                Fieldset('',
                    HTML('''
                    <p>Are you sure you wish to rename this project?</p>
                     <p>While this operation is reversible, no redirects of any kind are set up and former links to your project may not work as expected.</p>
                '''),
                    'name',
                ),
                css_class='modal-body'
            ),
            ButtonHolder(
                Submit('submit', 'Rename', css_class='btn-warning'),
                css_class='modal-footer'
            )
        )


    class Meta:
        model = Project
        fields = ['name']



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


class NewVersionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewVersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset('Version', 'name', 'description')
        )

    class Meta:
        model = Version
        fields = ('name', 'description')

class NewFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

BaseNewVersionInnerFileFormset = modelformset_factory(File, form=NewFileForm)
class NewVersionInnerFileFormset(BaseNewVersionInnerFileFormset):

    def __init__(self, *args, **kwargs):
        super(NewVersionInnerFileFormset, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset('File', 'name', 'description', 'file')
        )
