from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Hidden
from io import BytesIO
from PIL import Image

from . import models


class AvatarFileInput(widgets.ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <img src="%(initial_url)s" alt="Current avatar"> %(clear_template)s<br />%(input_text)s: %(input)s'
    )


class OrganizationSettingsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', readonly=True),
            Field('avatar_image', css_class='js-crop-field',
                  data_width_field="input[name='avatar_width']",
                  data_height_field="input[name='avatar_height']",
                  data_x_field="input[name='avatar_x']",
                  data_y_field="input[name='avatar_y']",
                  data_max_width="800",
                  data_max_height="800"
                  ),
            Hidden('avatar_width', ''),
            Hidden('avatar_height', ''),
            Hidden('avatar_x', ''),
            Hidden('avatar_y', ''),
            Submit('submit', 'Update profile'),
        )
        self.fields['avatar_image'].widget = AvatarFileInput()
        self.fields['avatar_width'] = forms.IntegerField(required=False)
        self.fields['avatar_height'] = forms.IntegerField(required=False)
        self.fields['avatar_x'] = forms.IntegerField(required=False)
        self.fields['avatar_y'] = forms.IntegerField(required=False)

    def clean_name(self):
        return self.instance.name

    def clean(self):
        try:
            self.crop_avatar_if_necessary()
        except ValidationError as ex:
            self.add_error('avatar_image', ex.message)

    def crop_avatar_if_necessary(self):
        avatar_f = self.cleaned_data.get('avatar_image')
        if not avatar_f:
            # user is probably trying to clear, or not submitting with avatar
            return

        # although the avatar is on the .image attribute of avatar_f, we can't use it
        # because the file handle has imploded at this point(?)
        if hasattr(avatar_f, 'temporary_file_path'):
            avatar_fp = avatar_f.temporary_file_path()
        elif hasattr(avatar_f, 'read'):
            avatar_fp = BytesIO(avatar_f.read())
        else:
            avatar_fp = BytesIO(avatar_f['content'])

        avatar = Image.open(avatar_fp)
        touched = False

        if avatar.width > 800 or avatar.height > 800:
            raise ValidationError(
                'This image is too large - avatars can be at most 800x800 pixels.')

        try:
            avatar.load()
        except Exception:
            raise ValidationError(
                'Upload a valid image. The image you uploaded appears to be malformed or invalid.')

        avcrop = None
        try:
            avcrop_width = int(self.cleaned_data['avatar_width'])
            avcrop_height = int(self.cleaned_data['avatar_height'])
            avcrop_x = int(self.cleaned_data['avatar_x'])
            avcrop_y = int(self.cleaned_data['avatar_y'])

            if (
                avcrop_width == avcrop_height and
                avcrop_width > 0 and
                avcrop_height > 0 and
                avcrop_x >= 0 and
                avcrop_y >= 0 and
                avcrop_x < avatar.width and
                avcrop_y < avatar.height and
                (avcrop_x + avcrop_width) <= avatar.width and
                (avcrop_y + avcrop_height) <= avatar.height
            ):
                avcrop = (
                    avcrop_x, avcrop_y,
                    avcrop_x + avcrop_width,
                    avcrop_y + avcrop_height,
                )
        except Exception:
            pass

        # we want to ensure that this image is square.
        # make the image square.
        if avatar.width != avatar.height or avcrop:
            if not avcrop:
                new_dimension = min(avatar.width, avatar.height)
                avcrop = (0, 0, new_dimension, new_dimension)
            avatar = avatar.crop(box=avcrop)
            touched = True

        if avatar.width > 200:
            avatar = avatar.resize((200, 200))
            touched = True

        if touched:
            avatar_bytes = BytesIO()
            avatar.save(avatar_bytes, format='PNG')
            self.cleaned_data['avatar_image'] = InMemoryUploadedFile(
                file=avatar_bytes, field_name='avatar_image', name='avatar.png', content_type='image/png',
                size=len(avatar_bytes.getbuffer()), charset=None
            )

    class Meta:
        model = models.Organization
        fields = ['name', 'avatar_image']
