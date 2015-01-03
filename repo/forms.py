from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db.models import Q
from repo.models import Project, Namespace, Organization, RepoUser


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

