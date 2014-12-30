
from repo.db import map_one
from repo.models import models
from tornado import gen


@gen.coroutine
def namespace_of(user):
    org = yield map_one(
        models.Organization,
        'select * from orgs where is_namespace = true and namespace = %s',
        (user.id,))
    raise gen.Return(org)


@gen.coroutine
def namespace_exists(name):
    org = yield map_one(
        models.Organization,
        'select * from orgs where lower(name) = lower(%s)',
        (name,)
    )
    raise gen.Return(org is not None)
