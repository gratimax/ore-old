from ore.core.models import Namespace, Organization
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AnonymousUser, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _t
import hashlib
from ore.core.util import UserFilteringQuerySet
from reversion import revisions as reversion


OreUserManagerBase = BaseUserManager.from_queryset(UserFilteringQuerySet)


class OreUserManager(OreUserManagerBase):

    def create_user(self, name, password=None, email=None, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            **extra_fields
        )
        user.set_password(password)

        # we'll create a superuser if this is the only user
        if not self.exists():
            user.is_staff = True
            user.is_superuser = True

        user.save(using=self._db)
        return user

    def create_superuser(self, name, password, email=None, **extra_fields):
        user = self.create_user(name, password, email, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class OreUser(AbstractBaseUser, PermissionsMixin, Namespace):
    # All taken from AbstractUser
    # name from Namespace
    email = models.EmailField('email', blank=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin '
                                             'site.')
    external_id = models.CharField(default=None, blank=True, null=True, max_length=64, unique=True)
    date_joined = models.DateTimeField(
        _t('creation date'), default=timezone.now)

    objects = OreUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    @staticmethod
    def is_visible_q(user):
        if user.is_anonymous():
            return Q(status='active')
        elif user.is_superuser:
            return Q()

        return (
            Q(status='active') |
            (
                ~Q(status='deleted') &
                Q(id=user.id)
            )
        )

    @property
    def is_active(self):
        return self.status == OreUser.STATUS.active

    @property
    def avatar(self):
        return "//www.gravatar.com/avatar/%s?d=mm" % hashlib.md5(
            self.email.encode('UTF-8').strip().lower()
        ).hexdigest()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def user_has_permission(self, user, perm_slug, project=None):
        if isinstance(user, AnonymousUser):
            return False
        elif user.is_superuser:
            return True
        return user == self

    def owned_organizations(self):
        return Organization.objects.filter(
            teams__is_owner_team=True,
            teams__users=self
        )

    def __str__(self):
        props = (['staff'] if self.is_staff else []) + \
                (['active'] if self.is_active else [])
        return '%s <%s> [%s]' % (self.name, self.email, ' '.join(props))


reversion.register(OreUser, follow=['namespace_ptr'])
