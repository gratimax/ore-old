from django.contrib.auth import forms as auth_forms
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from . import models

class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Log In'))


class RegistrationForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    email_verify = forms.CharField(widget=forms.EmailInput)

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
        email1 = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email_verify')

        if not email2:
            raise forms.ValidationError("You must confirm your email address.")
        if email1 != email2:
            raise forms.ValidationError("Your email addresses need to match.")
        return email2
