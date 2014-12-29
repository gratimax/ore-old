import momoko
from repo.db import db, map_one
from repo.handlers.base import BaseHandler
from repo.services import secure
from repo.services.session import perform_login
from repo.services.users import redirect_to_user_page
from repo.models import models
from repo.models.users import validate_username, validate_email
from tornado import gen


class AccountsHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        yield self.auth()
        yield redirect_to_user_page(self)


class AccountsNewHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        authenticated = yield self.authenticated
        if authenticated:
            self.render('accounts/new.html', errors=['You are already logged in'])
        else:
            self.render('accounts/new.html', errors=[])


    @gen.coroutine
    def post(self):

        authenticated = yield self.authenticated

        if authenticated:
            self.render('accounts/new.html', errors=['You are already logged in'])

        username = self.get_body_argument('username')
        email = self.get_body_argument('email')
        confirm_email = self.get_body_argument('confirm_email')
        password = self.get_body_argument('password')

        if '' in [username, email, confirm_email, password]:
            self.render('accounts/new.html', errors=['Nothing can be empty'])
            return

        username_valid = yield validate_username(username)

        if username_valid != '':
            self.render('accounts/new.html', errors=[username_valid])
            return

        email_valid = validate_email(email)

        if email_valid != '':
            self.render('accounts/new.html', errors=[email_valid])
            return

        if email != confirm_email:
            self.render('accounts/new.html', errors=['Emails must match'])
            return

        password_hashed = secure.hash_password(password)

        yield momoko.Op(db.execute, 'begin')
        yield momoko.Op(db.execute, 'insert into users (email, password) values (%s, %s)', (email, password_hashed))
        user = yield map_one(models.User, 'select * from users where email = %s', (email,))
        yield momoko.Op(db.execute, 'insert into orgs (name, is_namespace, namespace) values (%s, %s, %s)', (username, True, user.id))
        yield momoko.Op(db.execute, 'commit')

        yield perform_login(self, user)
        yield redirect_to_user_page(self, user)


class AccountsRecoveryHandler(BaseHandler):

    pass
