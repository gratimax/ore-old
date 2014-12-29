from repo.services.session import SID_COOKIE
from repo.models.sessions import user_for_session
import tornado.web
from tornado import gen


class BaseHandler(tornado.web.RequestHandler):

    # Errors

    def write_error(self, status_code, **kwargs):
        if status_code == 405:
            self.render("error/unauthorized.html")
        elif status_code == 404:
            self.render("error/notfound.html")
        else:
            self.render("error/server.html", status_code=self._status_code, message=self._reason)


    @staticmethod
    def err(code):
        raise tornado.web.HTTPError(code)

    # User-related things

    @gen.coroutine
    def auth(self):
        authenticated = yield self.authenticated
        if not authenticated:
            self.err(405)

    @property
    @gen.coroutine
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = yield self.get_current_user()
        raise gen.Return(self._current_user)

    @gen.coroutine
    def get_current_user(self):
        sid = self.get_secure_cookie(SID_COOKIE, None)
        if sid is None:
            raise gen.Return(None)
        sess = yield user_for_session(sid)
        raise gen.Return(sess)

    @property
    @gen.coroutine
    def authenticated(self):
        current_user = yield self.current_user
        raise gen.Return(current_user is not None)
