import momoko
from repo.services.users import redirect_to_user_page
from repo.models import models
from repo.db import map_one, db
from repo.handlers.base import BaseHandler
from repo.services.secure import check_password
from repo.services.session import perform_login, SID_COOKIE, perform_logout
from tornado import gen


class LoginHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        authenticated = yield self.authenticated

        if authenticated:
            current_user = yield self.current_user_secure
            yield redirect_to_user_page(self, current_user)
        else:
            self.render('sessions/login.html', errors=[])

    @gen.coroutine
    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        user = None
        if username == '' or password == '':
            self.render('sessions/login.html', errors=['Email and password must not be empty'])
            return
        user = yield map_one(models.User, 'select * from users where name = %s', (username,))
        if user is None:
            self.render('sessions/login.html', errors=['User does not exist'])
        elif not check_password(password, user.password):
            self.render('sessions/login.html', errors=['Incorrect password'])
        else:
            yield perform_login(self, user)
            self.redirect('/')


class LogoutHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        auth = yield self.authenticated
        if auth:
            yield momoko.Op(db.execute, 'delete from sessions where sid = %s', (self.get_secure_cookie(SID_COOKIE), ))
        perform_logout(self)
        self.redirect('/')


class SessionsClearHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        yield self.auth()
        current_user = yield self.current_user_secure
        yield momoko.Op(db.execute, 'delete from sessions where user_id = %s', (current_user.id,))
        perform_logout(self)
        self.redirect('/accounts')
