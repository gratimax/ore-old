from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AnonymousUser
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _t
from django.utils import timezone
from django.db.models.signals import post_save

from model_utils.managers import InheritanceManager
import reversion
import hashlib

# Regex that includes a few other characters other than word characters
EXTENDED_CHAR_REGEX = r'[\w.@+-]+'

# A regex that validates only a name that contains the extended characters
EXTENDED_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + r'$'

# A regex that permits spaces along with the extended characters, but not at the ends
TRIM_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + r'([\w.@+ -]*' + EXTENDED_CHAR_REGEX + r')?$'

Q = models.Q


@reversion.register
class Namespace(models.Model):

    name = models.CharField('name', max_length=32, unique=True,
                            validators=[
                                validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a namespace organization name.', 'invalid')
                            ])

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Namespace %s>' % self.name

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

    @property
    def avatar(self):
        return "//www.gravatar.com/avatar/" + hashlib.md5(self.email.strip().lower()).hexdigest()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def user_has_permission(self, user, perm_slug, project=None):
        if isinstance(user, AnonymousUser):
            return False
        return user == self

    def __repr__(self):
        props = (['staff'] if self.is_staff else []) + (['active'] if self.is_active else [])
        return '<RepoUser %s <%s> [%s]>' % (self.name, self.email, ' '.join(props))

reversion.register(RepoUser, follow=['namespace_ptr'])


class Organization(Namespace):

    def user_has_permission(self, user, perm_slug, project=None):
        if isinstance(user, AnonymousUser):
            return False

        ownerships = user.__dict__.setdefault('_organization_ownerships', dict())
        permissions = user.__dict__.setdefault('_organization_permissions', dict())
        if ownerships.get(self.id) is None:
            qs = self.teams.filter(users=user)
            qs = qs.filter(Q(is_all_projects=True) | Q(projects=project))
            if qs.filter(is_owner_team=True).count():
                ownerships[self.id] = True
            else:
                permissions[self.id] = qs.values_list('permissions__slug', flat=True)

        if self.id in ownerships:
            return True
        if perm_slug in permissions.get(self.id, []):
            return True

        return False

    def __repr__(self):
        return '<Organization %s>' % self.name

reversion.register(Organization, follow=['namespace_ptr'])


@reversion.register
class Project(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a valid project name.', 'invalid')
                            ])
    namespace = models.ForeignKey(Namespace, related_name='projects')
    description = models.TextField('description')

    def user_has_permission(self, user, perm_slug):
        if isinstance(user, AnonymousUser):
            return False

        ownerships = user.__dict__.setdefault('_project_ownerships', dict())
        permissions = user.__dict__.setdefault('_project_permissions', dict())
        if ownerships.get(self.id) is None:
            qs = self.teams.filter(users=user)
            if qs.filter(is_owner_team=True).count():
                ownerships[self.id] = True
            else:
                permissions[self.id] = qs.values_list('permissions__slug', flat=True)

        if self.id in ownerships:
            return True
        if perm_slug in permissions.get(self.id, []):
            return True

        return Namespace.objects.get_subclass(id=self.namespace_id).user_has_permission(user, perm_slug, project=self)

    def __repr__(self):
        return '<Project %s by %s>' % (self.name, self.namespace.name)


@reversion.register
class Version(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(TRIM_NAME_REGEX, 'Enter a valid version name.', 'invalid')
                            ])
    description = models.TextField('description')
    project = models.ForeignKey(Project, related_name='versions')

    def __repr__(self):
        return '<Version %s of %s>' % (self.name, self.project.name)


@reversion.register
class File(models.Model):

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(TRIM_NAME_REGEX, 'Enter a valid file name.', 'invalid')
                            ])
    description = models.TextField('description')
    version = models.ForeignKey(Version, related_name='files')

    def __repr__(self):
        return '<File %s in %s of %s>' % (self.name, self.version.name, self.version.project.name)


@reversion.register
class Permission(models.Model):
    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    applies_to_project = models.BooleanField(default=True)

    def __repr__(self):
        props = ['applies_to_project'] if self.applies_to_project else []
        return '<Permission %s [%s]>' % (self.slug, ' '.join(props))


class Team(models.Model):
    name = models.CharField('name', max_length=80, null=False, blank=False)
    users = models.ManyToManyField(RepoUser, related_name='%(class)ss', blank=True)
    permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    is_owner_team = models.BooleanField(default=False)

    def check_consistent(self):
        return True

    def make_consistent(self):
        return

    class Meta:
        abstract = True


@reversion.register
class OrganizationTeam(Team):
    organization = models.ForeignKey(Organization, related_name='teams')
    projects = models.ManyToManyField(Project, related_name='organizationteams', blank=True)
    is_all_projects = models.BooleanField(default=False)

    def make_consistent(self):
        self.projects = self.projects.filter(namespace=self.organization)
        self.save()

    def check_consistent(self):
        return self.projects.exclude(namespace=self.organization).count() == 0

    def __repr__(self):
        props = (['all_projects'] if self.is_all_projects else []) + (['owner'] if self.is_owner_team else [])
        return '<OrganizationTeam %s in %s [%s]>' % (self.name, self.organization.name, ' '.join(props))


@reversion.register
class ProjectTeam(Team):
    project = models.ForeignKey(Project, related_name='teams')

    def __repr__(self):
        props = ['owner'] if self.is_owner_team else []
        return '<ProjectTeam %s in %s [%s]>' % (self.name, self.project.name, ' '.join(props))

    # TODO: we need to check here that if we're a user's project and we're the owner team, that that user is in us!

def create_project_owner_team(sender, instance, created, **kwargs):
    if instance and created:
        owning_namespace = Namespace.objects.get_subclass(id=instance.namespace_id)
        if isinstance(owning_namespace, RepoUser):
            team = ProjectTeam.objects.create(
                    project=instance,
                    is_owner_team=True,
                    name='Owners',
            )
            team.users = [owning_namespace]
            team.save()
post_save.connect(create_project_owner_team, sender=Project)

def create_organization_owner_team(sender, instance, created, **kwargs):
    if instance and created:
        OrganizationTeam.objects.create(
                name='Owners',
                organization=instance,
                is_all_projects=True,
                is_owner_team=True,
        )
post_save.connect(create_organization_owner_team, sender=Organization)
