import momoko
from repo.models import models
from repo.db import map_one, db
from repo.handlers.base import BaseHandler
from repo.lib.secure import check_password
from repo.lib.session import perform_login
from tornado import gen


class LoginHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        authenticated = yield self.authenticated
        if authenticated:
            self.render('sessions/session.html', user=self.current_user)
        else:
            self.render('sessions/login.html', errors=[])

    @gen.coroutine
    def post(self):
        email = self.get_body_argument('email')
        password = self.get_body_argument('password')
        user = None
        if email == '' or password == '':
            self.render('sessions/login.html', errors=['Email and password must not be empty'])
            return
        user = yield map_one(models.User, 'select * from users where email = %s', (email,))
        if user is None:
            self.render('sessions/login.html', errors=['User does not exist'])
        elif not check_password(password, user.password):
            self.render('sessions/login.html', errors=['Incorrect password'])
        else:
            perform_login(self, user)
            self.redirect('/')


class LogoutHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        auth = yield self.authenticated
        if auth:
            yield momoko.Op(db.execute, 'delete from sessions where sid = %s', self.get_secure_cookie('sid'))
        self.clear_cookie('sid')
        self.redirect('/')


class SessionsClearHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        auth = yield self.auth()
        if auth:
            return
        current_user = yield self.current_user
        yield momoko.Op(db.execute, 'delete from sessions where user_id = %s', (current_user.id,))
        self.clear_cookie('sid')
        self.redirect('/accounts')
