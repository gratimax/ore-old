from repo.models.sessions import user_for_session
import tornado.web
from tornado import gen


class BaseHandler(tornado.web.RequestHandler):

    def unauthenticated(self):
        self.set_status(405)
        self.render("error/unauthorized.html")

    # User-related things

    @gen.coroutine
    def auth(self):
        authenticated = yield self.authenticated
        if not authenticated:
            self.unauthenticated()
            raise gen.Return(True)
        else:
            raise gen.Return(False)

    @property
    @gen.coroutine
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = yield self.get_current_user()
        raise gen.Return(self._current_user)

    @gen.coroutine
    def get_current_user(self):
        sid = self.get_secure_cookie('sid', None)
        if sid is None:
            raise gen.Return(None)
        sess = yield user_for_session(sid)
        raise gen.Return(sess)

    @property
    @gen.coroutine
    def authenticated(self):
        current_user = yield self.current_user
        raise gen.Return(current_user is not None)
