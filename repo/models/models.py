from collections import namedtuple


# These should all be kept the same as the database tables
# Order matters as well

User = namedtuple(
    'User',
    ['id',
     'email',
     'password'])

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

File = namedtuple(
    'File',
    ['id',
     'project_id',
     'name',
     'description',
     'hash'])

Session = namedtuple(
    'Session',
    ['sid',
     'user_id'])