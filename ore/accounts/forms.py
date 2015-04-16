from django.contrib.auth import forms as auth_forms
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


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
    email_verify = forms.BooleanField(label='I have confirmed that my email is correct, stop worrying about it!')

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
