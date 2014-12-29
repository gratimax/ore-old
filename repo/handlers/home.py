from repo.handlers.base import BaseHandler
from repo.lib.avatar import avatar_url
from repo.lib.users import get_user_page
from repo.models.orgs import namespace_of
from tornado import gen


class HomeHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        authenticated = yield self.authenticated

        if authenticated:
            current_user = yield self.current_user
            namespace = yield namespace_of(current_user)
            avatar = avatar_url(current_user.email, 18)
            self.render("home/user.html", user=current_user, namespace=namespace, avatar=avatar)
        else:
            self.render("home/index.html")
