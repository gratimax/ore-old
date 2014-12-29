from repo.models import models
from repo.models.sessions import save_new_session
from tornado import gen
import json

SID_COOKIE = 'sid_v1'

USER_COOKIE = 'user_v1'

@gen.coroutine
def perform_login(handler, user):

    sid = yield save_new_session(user.id)
    handler.set_secure_cookie(SID_COOKIE, sid)

    save_user_into_session(handler, user)


def perform_logout(handler):
    handler.clear_cookie(USER_COOKIE)
    handler.clear_cookie(SID_COOKIE)


def save_user_into_session(handler, user):
    handler.set_secure_cookie(USER_COOKIE, json.dumps(user))


def load_user_from_session(handler):
    u = handler.get_secure_cookie(USER_COOKIE)

    if u is None:
        return None

    return models.User._make(json.loads(u))
