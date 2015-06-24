from django.contrib.auth import forms as auth_forms
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Hidden

from . import models


class AuthenticationForm(auth_forms.AuthenticationForm):
    username = forms.CharField(label="Username", max_length=32)

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Log In'))


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)
    email = forms.CharField(widget=forms.EmailInput, max_length=75)
    email_verify = forms.BooleanField(
        label='I have confirmed that my email is correct,' +
              ' stop worrying about it!'
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'password',
            'email',
            'email_verify',
            Submit('submit', 'Create account'),
        )

    def clean_email_verify(self):
        checked = self.cleaned_data.get('email_verify')

        if not checked:
            raise forms.ValidationError("Please confirm your email.")

        return checked


class ProfileSettingsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', readonly=True),
            'email',
            Hidden('form', 'profile'),
            Submit('submit', 'Update profile'),
        )

    def clean_name(self):
        return self.instance.name

    class Meta:
        model = models.OreUser
        fields = ['name', 'email']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput, max_length=128
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput, max_length=128, min_length=8
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password',
            'new_password',
            Hidden('form', 'password'),
            Submit('submit', 'Change password'),
        )
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "That wasn't quite right. Please re-enter your old password."
            )

        return old_password

    def save(self):
        self.user.set_password(self.cleaned_data.get('new_password'))
        return self.user.save()
