from repo.models.sessions import save_new_session
from tornado import gen

SID_COOKIE = 'sid_v1'

@gen.coroutine
def perform_login(handler, user):

    sid = yield save_new_session(user.id)
    handler.set_secure_cookie(SID_COOKIE, sid)
