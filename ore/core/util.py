from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F
from model_utils.managers import InheritanceQuerySetMixin, InheritanceManagerMixin


def validate_not_prohibited(value):
    if value.lower() in settings.PROHIBITED_NAMES:
        raise ValidationError('%s is not allowed.' % value)

def add_prefix(prefix, q, sep='__'):
    if hasattr(q, 'children'):
        cloned = q.clone()
        cloned.children = [add_prefix(prefix, child, sep) for child in q.children]
        return cloned
    elif isinstance(q, tuple) and len(q) == 2:
        return add_prefix(prefix, q[0], sep), add_prefix_value(prefix, q[1], sep)
    else:
        return prefix + sep + q

def add_prefix_value(prefix, v, sep='__'):
    if isinstance(v, F):
        return F(add_prefix(prefix, v.name, sep))
    else:
        return v

class UserFilteringQuerySet(models.QuerySet):

    def as_user(self, user):
        return self.filter(self.model.is_visible_q(user))

UserFilteringManager = models.Manager.from_queryset(UserFilteringQuerySet)


class UserFilteringInheritanceQuerySet(InheritanceQuerySetMixin, UserFilteringQuerySet):
    pass


class UserFilteringInheritanceManager(InheritanceManagerMixin, UserFilteringManager):

    def get_queryset(self):
        return UserFilteringInheritanceQuerySet(self.model, using=self._db)
