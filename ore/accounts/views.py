from ore.accounts.models import OreUser
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, FormView
from django.db import IntegrityError

from ore.core.views import RequiresLoggedInMixin, SettingsMixin
from ore.accounts import forms


def loginview(request):
    return auth_views.login(
        request,
        template_name='accounts/login.html',
        authentication_form=forms.AuthenticationForm
    )


class LogoutView(TemplateView):
    template_name = 'accounts/logout_confirm.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(
            self.request, "You have been logged out successfully."
        )
        return redirect('/')


class RegisterView(FormView):
    template_name = 'accounts/new.html'
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        # Create a new user account
        username = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = OreUser.objects.create_user(
                username,
                email=email,
                password=password
            )
            user.save()
        except IntegrityError:
            form.add_error('name', 'That username is already taken.')
            return self.form_invalid(form)

        user = authenticate(username=username, password=password)
        if user is None:
            raise ValueError("User I just created has a different password?")
        login(self.request, user)
        messages.success(
            self.request,
            'Your user account has been created and you have been logged in.'
        )

        return redirect('/')


class ProfileSettings(RequiresLoggedInMixin, SettingsMixin, TemplateView):
    template_name = 'accounts/settings/profile.html'
    settings_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        data = None
        submitted_form = None
        if not settings.DISCOURSE_SSO_ENABLED:
            submitted_form = request.POST.get('form', None)
            if request.method == 'POST':
                data = request.POST

        self.profile_form = self.get_profile_form(
            request.user, submitted_form, data)
        self.password_form = self.get_password_change_form(
            request.user, submitted_form, data)

        return super().dispatch(request, *args, **kwargs)

    def get_profile_form(self, instance, submitted_form=None, data=None):
        if submitted_form != 'profile':
            data = None

        return forms.ProfileSettingsForm(
            data,
            instance=instance,
            prefix='profile'
        )

    def get_password_change_form(self, instance, submitted_form=None, data=None):
        if submitted_form != 'password':
            data = None

        return forms.PasswordChangeForm(
            data,
            user=instance,
            prefix='password'
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['profile_form'] = self.profile_form
        data['password_form'] = self.password_form
        data['using_sso'] = settings.DISCOURSE_SSO_ENABLED
        return data

    def post(self, request, *args, **kwargs):
        submitted_form = request.POST.get('form', None)

        if submitted_form == 'profile':
            if self.profile_form.is_valid():
                self.profile_form.save()
                messages.success(request, "Your profile has been updated.")
                self.profile_form = self.get_profile_form(request.user)
        elif submitted_form == 'password':
            if self.password_form.is_valid():
                self.password_form.save()
                messages.success(
                    request, "Your password was changed successfully.")
                # log them in again(!)
                user = authenticate(
                    username=request.user.name,
                    password=self.password_form.cleaned_data.get(
                        'new_password')
                )
                login(request, user)

        return self.get(request)
