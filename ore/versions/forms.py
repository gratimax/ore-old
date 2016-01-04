from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms
from django.forms import modelformset_factory
from ore.projects.models import Channel
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
        self.fields['channel'] = forms.ModelChoiceField(
            queryset=Channel.objects.filter(project_id=kwargs['instance'].project.id))

    class Meta:
        model = Version
        fields = ('name', 'description', 'channel')

        # def validate_unique(self):
        #     exclude = self._get_validation_exclusions()
        #     exclude.remove('version')
        #
        #     try:
        #         self.instance.validate_unique(exclude=exclude)
        #     except ValidationError as e:
        #         self._update_errors(e.message_dict)


class NewChannelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewChannelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset('Channel', 'name', 'hex')
        )

    class Meta:
        model = Channel
        fields = ('name','hex')

    COLOUR_CHOICES=(
        ('001f3f', 'Navy'),
        ('0074D9', 'Blue'),
        ('7FDBFF', 'Aqua'),
        ('39CCCC', 'Teal'),
        ('3D9970', 'Olive'),
        ('2ECC40', 'Green'),
        ('01FF70', 'Lime'),
        ('FFDC00', 'Yellow'),
        ('FF851B', 'Orange'),
        ('FF4136', 'Red'),
        ('85144b', 'Maroon'),
        ('F012BE', 'Fuchsia'),
        ('B10DC9', 'Purple'),
        ('111111', 'Black'),
        ('AAAAAA', 'Gray'),
        ('DDDDDD', 'Silver'),

    )

    hex = forms.ChoiceField(choices=COLOUR_CHOICES, required=True)


class ChannelDeleteForm(forms.Form):
    def __init__(self, project, currentChannel, *args, **kwargs):
        super(ChannelDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        channels = Channel.objects.filter(project=project)
        choices = (('DEL', 'None, Delete them.'),)
        for channel in channels:
            if channel.id == currentChannel.id:
                continue
            choices = choices + ((str(channel.id), channel.name),)
        self.fields['transfer_to'] = forms.ChoiceField(choices=choices,required=False)




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
