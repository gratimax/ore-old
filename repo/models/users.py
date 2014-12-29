from repo.models.orgs import namespace_exists
from tornado import gen
import re

username_regex = re.compile('[\w-]+')
# Thanks to http://stackoverflow.com/a/719543/1952271
email_regex = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def validate_email(email):
    if email_regex.match(email) is None:
        return 'Not a valid email'
    else:
        return ''

@gen.coroutine
def validate_username(username):

    if username_regex.match(username) is None:
        raise gen.Return('Username can only contain hyphenated or alphanumeric characters')

    # TODO generate this from URLs
    if username in ['accounts', 'sessions', 'help', 'projects']:
        raise gen.Return('Username is already taken')

    name_exists = yield namespace_exists(username)

    if name_exists:
        raise gen.Return('Username is already taken')

    raise gen.Return('')
