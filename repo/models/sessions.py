import uuid
import momoko
from repo.models import models
from repo.db import db, map_one, map_all
from tornado import gen


def gen_session_id():
    return uuid.uuid4().hex

@gen.coroutine
def user_sessions(u_id):
    cursor = yield map_all(models.Session, 'select * from sessions where user_id = %s', (u_id,))
    raise gen.Return(cursor)

@gen.coroutine
def user_for_session(sid):
    session = yield map_one(
        models.Session,
        "select * from sessions where sid = %s",
        (sid,))

    if session is None:
        raise gen.Return(None)

    user = yield map_one(
        models.User,
        'select * from users where id = %s',
        (session.user_id,))

    raise gen.Return(user)


@gen.coroutine
def save_new_session(user_id):
    sid = gen_session_id()
    yield momoko.Op(db.execute, "insert into sessions (user_id, sid) values (%s, %s)", (user_id, sid))
    raise gen.Return(sid)

# def create_session(user):
#     return Session(user, gen_session_id())
#
# @gen.coroutine
# def session_from_sid(sid):
#     user = yield user_for_session(sid)
#     if user is None:
#         raise gen.Return(None)
#     else:
#         raise gen.Return(Session(user, sid))
