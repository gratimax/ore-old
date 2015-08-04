
from django.contrib.auth.models import AnonymousUser
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, F

from model_utils import Choices
from model_utils.fields import StatusField
from ore.core.models import Namespace
from ore.core.util import validate_not_prohibited, UserFilteringManager, add_prefix
from ore.core.regexs import EXTENDED_NAME_REGEX
import reversion


@reversion.register
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
    description = models.TextField('description', blank=True, null=False)

    objects = UserFilteringManager()

    def get_absolute_url(self):
        return reverse('repo-projects-detail', kwargs={'namespace': self.namespace.name, 'project': self.name})

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

    def __repr__(self):
        return '<Project %s by %s>' % (self.name, self.namespace.name)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('namespace', 'name')
