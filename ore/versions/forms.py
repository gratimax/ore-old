from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms
from django.forms import modelformset_factory
from ore.versions.models import Version, File


class NewVersionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewVersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'name',
            'description',
        )

    class Meta:
        model = Version
        fields = ('name', 'description')

    # def validate_unique(self):
    #     exclude = self._get_validation_exclusions()
    #     exclude.remove('version')
    #
    #     try:
    #         self.instance.validate_unique(exclude=exclude)
    #     except ValidationError as e:
    #         self._update_errors(e.message_dict)


class NewFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'file'
        )
        if kwargs['prefix'] == 'file-0':
            self.fields['file'].label = 'Primary file'
        else:
            self.fields['file'].label = 'Additional file'

    class Meta:
        model = File
        fields = ('file',)

BaseNewVersionInnerFileFormset = modelformset_factory(File, form=NewFileForm, max_num=5, validate_max=True)


class NewVersionInnerFileFormset(BaseNewVersionInnerFileFormset):

    def __init__(self, *args, **kwargs):
        super(NewVersionInnerFileFormset, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            #Fieldset('File', 'name', 'file')
            'file'
        )
