import zipfile
import posixpath
import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from ore.projects.models import Channel
from ore.versions.models import File, Version
from ore.util import plugalyzer
from ore.core.regexs import TRIM_NAME_REGEX

FILE_EXTENSION_RE = re.compile(r'^\.[a-zA-Z0-9\-]+$')
TRIM_NAME_RE = re.compile(TRIM_NAME_REGEX)


def filename_is_valid(filename):
    file_name, file_extension = posixpath.splitext(
            posixpath.basename(filename))
    if not TRIM_NAME_RE.match(file_name):
        raise ValidationError("Only letters, numbers, underscores, hyphens and spaces are permitted in filenames for compatibility reasons.")
    if not FILE_EXTENSION_RE.match(file_extension):
        raise ValidationError("File extensions must consist only of letters, numbers, and hyphens.")

    return file_name, file_extension


class NewChannelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        used_colours = set(kwargs.pop('used_colours', set()))
        super(NewChannelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal colour-form"
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        label = 'Create new channel' if not self.instance.id else 'Edit channel'
        if self.instance.id:
            used_colours.remove(self.instance.hex)
        self.helper.layout = Layout(
            Field('name', autocomplete='off'),
            Field('hex', css_class="colour-selector only-without-js"),
            Submit('submit', label, css_class="col-lg-offset-2")
        )
        self.fields['hex'].choices = [
            (hex, name) for (hex, name) in self.fields['hex'].choices if hex not in used_colours]

    class Meta:
        model = Channel
        fields = ('name', 'hex')

    COLOUR_CHOICES = (
        ('001F3F', 'Navy'),
        ('0074D9', 'Blue'),
        ('7FDBFF', 'Aqua'),
        ('39CCCC', 'Teal'),
        ('3D9970', 'Olive'),
        ('2ECC40', 'Green'),
        ('01FF70', 'Lime'),
        ('FFDC00', 'Yellow'),
        ('FF851B', 'Orange'),
        ('FF4136', 'Red'),
        ('85144B', 'Maroon'),
        ('F012BE', 'Fuchsia'),
        ('B10DC9', 'Purple'),
        ('111111', 'Black'),
        ('AAAAAA', 'Gray'),
        ('DDDDDD', 'Silver'),
    )

    hex = forms.ChoiceField(
        choices=COLOUR_CHOICES, required=True, label='Colour')


class ChannelDeleteForm(forms.Form):

    def __init__(self, project, current_channel, *args, **kwargs):
        super(ChannelDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        get_out_of_here = reverse(
            'project-channels', kwargs={'namespace': project.namespace.name, 'project': project.name})
        self.helper.layout = Layout(
            'transfer_to',
            Submit(
                'submit', 'Delete it!', css_class='btn-danger col-lg-offset-2'),
            HTML(
                "<a href=\"{}\" class='btn'>Get me out of here!</a>".format(get_out_of_here))
        )
        channels = Channel.objects.filter(
            project=project).exclude(id=current_channel.id)
        choices = [('DEL', 'None, delete them.'), ] + \
            [(str(channel.id), channel.name) for channel in channels]
        self.fields['transfer_to'] = forms.ChoiceField(
            choices=choices, required=False)


class NewVersionForm(forms.Form):

    file = forms.FileField(label='Plugin JAR', widget=forms.FileInput, required=True, allow_empty_file=False)
    channel = forms.ChoiceField(label='Channel', required=True, choices=[])

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(NewVersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('file'),
            Field('channel'),
        )
        channel_choices = []
        for channel in Channel.objects.filter(project=self.project):
            channel_choices.append((channel.id, channel.name))
        self.fields['channel'].choices = channel_choices

    def clean_file(self):
        file = self.cleaned_data['file']

        file_name, file_extension = filename_is_valid(file.name)
        if file_extension != '.jar':
            raise forms.ValidationError('Ore currently only supports direct .jar uploads of your plugin.', code='must_be_a_jar')

        self.cleaned_data['file_name'] = file_name
        self.cleaned_data['file_extension'] = file_extension

        self.cleaned_data['file_size'] = file.size

        file.open('rb')
        try:
            plugins = plugalyzer.Plugalyzer.analyze(file)
        except zipfile.BadZipFile:
            raise forms.ValidationError('The uploaded file doesn\'t appear to be a valid JAR file.', code='plugalyzer_invalid_jar')
        except plugalyzer.ParseError as ex:
            raise forms.ValidationError('The uploaded plugin has an invalid \'dependencies\' attribute on the @Plugin annotation: "{}"'.format(ex), code='plugalyzer_parse_error')

        if len(plugins) < 1:
            raise forms.ValidationError('The uploaded JAR doesn\'t seem to contain a Sponge plugin (there are no classes annotated with @Plugin).', code='plugalyzer_no_plugins')
        if len(plugins) > 1:
            raise forms.ValidationError('The uploaded JAR appears to contain more than one class annotated with @Plugin, which isn\'t presently supported.', code='plugalyzer_multiple_plugins')

        plugin = plugins[0]
        errors = plugin.validate()
        if errors:
            raise forms.ValidationError([forms.ValidationError(e) for e in errors])

        self.cleaned_data['plugin'] = plugin

        # validate uniqueness too
        # two paths: we've got files with IDs, or we don't
        has_previous_files = File.objects.filter(project=self.project).exclude(plugin_id=None).exists()
        if has_previous_files:
            # check if we've previously used this project ID
            if not File.objects.filter(project=self.project, plugin_id=plugin.data['id']).exists():
                previous_ids = set(File.objects.filter(project=self.project).exclude(plugin_id=None).values_list('plugin_id', flat=True).distinct())
                raise forms.ValidationError(
                    "This plugin doesn't use the same plugin ID you've been using previously (it uses '{}', but you've previously used '{}') - consider checking you're uploading to the right project, or contact a staff member.".format(
                        plugin.data['id'],
                        "', '".join(previous_ids),
                    ),
                    code='plugalyzer_different_plugin_id'
                )

            # check if we've previously used this version string
            if File.objects.filter(project=self.project, version__name=plugin.data['version']).exists():
                raise forms.ValidationError(
                    "This plugin reuses the version of a file you've previously uploaded - this is probably a bad idea!",
                    code='plugalyzer_conflicting_version'
                )
        else:
            # check if someone else has previously used this project ID
            if File.objects.filter(plugin_id=plugin.data['id']).exists():
                raise forms.ValidationError(
                    "This plugin uses the same plugin ID as a different plugin already uploaded to Ore. Consider changing it, or contact a staff member.",
                    code='plugalyzer_conflicting_plugin_id'
                )

        return self.cleaned_data['file']


class EditVersionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditVersionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('description', css_class='oredown'),
            Submit('submit', 'Set description'),
        )
        self.helper.form_show_labels = False

    class Meta:
        model = Version
        fields = ('description',)


class NewFileForm(forms.Form):

    file = forms.FileField(label='Additional file', widget=forms.FileInput, required=True, allow_empty_file=False)

    def __init__(self, *args, **kwargs):
        self.version = kwargs.pop('version')
        super(NewFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('file'),
            Submit('submit', 'Upload additional file'),
        )

    def clean_file(self):
        file = self.cleaned_data['file']

        file_name, file_extension = filename_is_valid(file.name)
        self.cleaned_data['file_name'] = file_name
        self.cleaned_data['file_extension'] = file_extension

        if self.version.files.filter(file_name=file_name, file_extension=file_extension).exists():
            raise forms.ValidationError("Don't be silly, you can't upload multiple files with the same name to the same version.", code='duplicate-filename')

        return file
