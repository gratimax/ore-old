from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _t
from django.utils import timezone


EXTENDED_CHAR_REGEX = r'[\w.@+-]+'
EXTENDED_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + r'$'
TRIM_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + r'([\w.@+ -]*' + EXTENDED_CHAR_REGEX + r')?$'


class Namespace(models.Model):

    name = models.CharField('name', max_length=32, unique=True,
                            validators=[
                                validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a namespace organization name.', 'invalid')
                            ])

class RepoUserManager(UserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(name=username, email=email, is_staff=is_staff, is_active=True, is_superuser=True, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class RepoUser(AbstractBaseUser, PermissionsMixin, Namespace):

    # All taken from AbstractUser
    # name from Namespace
    email = models.EmailField('email', blank=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin '
                                             'site.')
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(_t('creation date'), default=timezone.now)

    objects = RepoUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Organization(Namespace):

    pass


class Project(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a valid project name.', 'invalid')
                            ])
    namespace = models.ForeignKey(Namespace, related_name='projects')
    description = models.TextField('description')


class Version(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(TRIM_NAME_REGEX, 'Enter a valid version name.', 'invalid')
                            ])
    description = models.TextField('description')
    project = models.ForeignKey(Project, related_name='versions')


class File(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(TRIM_NAME_REGEX, 'Enter a valid file name.', 'invalid')
                            ])
    description = models.TextField('description')
    version = models.ForeignKey(Version, related_name='files')
