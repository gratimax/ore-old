from colour import Color
from django.contrib.auth.models import AnonymousUser
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from model_utils import Choices
from model_utils.fields import StatusField
from ore.accounts.models import OreUser
from ore.core.models import Namespace
from ore.core.util import validate_not_prohibited, UserFilteringManager, add_prefix
from ore.core.regexs import EXTENDED_NAME_REGEX
from reversion import revisions as reversion
from ore.util import markdown


@reversion.register(follow=['pages'])
class Project(models.Model):
    STATUS = Choices('active', 'deleted')
    status = StatusField()

    name = models.CharField('name', max_length=32,
                            validators=[
                                validators.RegexValidator(EXTENDED_NAME_REGEX, 'Enter a valid project name.',
                                                          'invalid'),
                                validate_not_prohibited,
                            ])
    namespace = models.ForeignKey(Namespace, related_name='projects')
    description = models.TextField(
        blank=True, null=False, help_text="Try to sum your plugin up in 140 characters or less.", verbose_name="Tagline (optional)")
    stargazers = models.ManyToManyField(OreUser, related_name='starred')

    objects = UserFilteringManager()

    def get_absolute_url(self):
        return reverse('projects-detail', kwargs={'namespace': self.namespace.name, 'project': self.name})

    @classmethod
    def is_visible_q(cls, user):
        if user.is_anonymous():
            return add_prefix('namespace', Namespace.is_visible_q(user)) & Q(status='active')
        elif user.is_superuser:
            return Q()

        return add_prefix('namespace', Namespace.is_visible_q(user)) & (
            Q(status='active') |
            cls.is_visible_if_hidden_q(user)
        )

    @staticmethod
    def is_visible_if_hidden_q(user):
        if user.is_anonymous():
            return Q()

        return ~Q(status='deleted') & (
            (Q(teams__users=user)) |
            (Q(namespace__oreuser=user)) |
            (
                (
                    Q(namespace__organization__teams__is_all_projects=True) |
                    Q(namespace__organization__teams__projects__id=F('id'))
                ) &
                Q(namespace__organization__teams__users=user)
            )
        )

    @property
    def is_visible(self):
        return self.namespace.is_visible and self.status == self.STATUS.active

    def full_name(self):
        return "{}/{}".format(self.namespace.name, self.name)

    def user_has_permission(self, user, perm_slug):
        if isinstance(user, AnonymousUser):
            return False
        elif user.is_superuser:
            return True

        ownerships = user.__dict__.setdefault('_project_ownerships', dict())
        permissions = user.__dict__.setdefault('_project_permissions', dict())
        if ownerships.get(self.id) is None:
            qs = self.teams.filter(users=user)
            if qs.filter(is_owner_team=True).count():
                ownerships[self.id] = True
            else:
                permissions[self.id] = qs.values_list(
                    'permissions__slug', flat=True)

        if self.id in ownerships:
            return True
        if perm_slug in permissions.get(self.id, []):
            return True

        return Namespace.objects.get_subclass(id=self.namespace_id).user_has_permission(user, perm_slug, project=self)

    def __str__(self):
        return '%s by %s' % (self.name, self.namespace.name)

    class Meta:
        unique_together = ('namespace', 'name')


class Channel(models.Model):
    name = models.CharField(max_length=100)
    hex = models.CharField(max_length=6, verbose_name="Colour")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @property
    def color_class(self):
        color = Color('#' + self.hex)
        # see http://stackoverflow.com/a/596243 for info on perceptive luminance
        perceptive_luminance = 1 - (0.299 * color.red + 0.587 * color.green + 0.114 * color.blue)

        if perceptive_luminance < 0.5:
            return 'channel-bg-light'
        else:
            return 'channel-bg-dark'

    def __str__(self):
        return self.name


@reversion.register
class Page(models.Model):
    STATUS = Choices('active', 'deleted')
    status = StatusField()

    project = models.ForeignKey(Project, related_name='pages')

    listed = models.ManyToManyField(
        'Page', related_name='listed_by', blank=True)

    title = models.CharField(max_length=64)
    slug = models.SlugField(editable=False)
    content = models.TextField()
    html = models.TextField(blank=True)

    objects = UserFilteringManager()

    def save(self, *args, **kwargs):
        self.html = markdown.compile(self.content, context={
                                     'namespace': self.project.namespace.name, 'project': self.project.name, 'page': self.slug})
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    @classmethod
    def is_visible_q(cls, user):
        if user.is_superuser:
            return Q()

        return add_prefix('project', Project.is_visible_q(user)) & (
            Q(status='active') |
            cls.is_visible_if_hidden_q(user)
        )

    @staticmethod
    def is_visible_if_hidden_q(user):
        if user.is_anonymous():
            return Q()

        return ~Q(status='deleted') & add_prefix('project', Project.is_visible_if_hidden_q(user))

    def get_absolute_url(self):
        if self.slug == 'home':
            return reverse('projects-detail', kwargs=dict(
                namespace=self.project.namespace.name,
                project=self.project.name
            ))
        else:
            return reverse('projects-pages-detail', kwargs=dict(
                namespace=self.project.namespace.name,
                project=self.project.name,
                page=self.slug
            ))

    def __str__(self):
        return '\'%s\' in project %s' % (self.title, self.project)

    class Meta:
        unique_together = (
            ('project', 'slug'),
            ('project', 'title')
        )


@receiver(post_save, sender=Project)
def create_home_page(sender, instance, created, **kwargs):
    if instance and created:
        home_page = Page.objects.create(
            project=instance,
            title='Home',
            content='Welcome to your new project!'
        )
        home_page.save()
