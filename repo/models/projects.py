import re
from repo.db import map_one
from repo.models import models
from tornado import gen

project_name_regex = re.compile('^[\w-]+$')


@gen.coroutine
def validate_project_name(name, namespace):

    existing = yield map_one(models.Organization, 'select * from projects where lower(name) = lower(%s) and owner_id = %s', (name, namespace.id))

    if existing is not None:
        raise gen.Return('Project already exists')

    if project_name_regex.match(name) is None:
        raise gen.Return('Project name can only be hyphenated alphanumerics')

    if len(name) > 128:
        raise gen.Return('Project name can have a maximum length of 128 characters')

    raise gen.Return('')


def validate_project_description(description):

    if len(description) > 512:
        return 'Project description can have a maximum length of 512 characters'

    return ''
