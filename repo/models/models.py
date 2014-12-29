from collections import namedtuple


# These should all be kept the same as the database tables
# Order matters as well

User = namedtuple(
    'User',
    ['id',
     'name',
     'email',
     'password'])


Session = namedtuple(
    'Session',
    ['sid',
     'user_id'])

Organization = namedtuple(
    'Organization',
    ['id',
     'name',
     'is_namespace',
     'namespace'])

OrgMembership = namedtuple(
    'OrgMembership',
    ['user_id',
     'org_id',
     'role'])

Project = namedtuple(
    'Project',
    ['id',
     'owner_id',
     'name',
     'description'])

ProjMembership = namedtuple(
    'ProjMembership',
    ['user_id',
     'project_id',
     'role'])

Version = namedtuple(
    'Version',
    ['id',
     'project_id',
     'name',
     'description',
     'file_hash'])
