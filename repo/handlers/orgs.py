from repo.db import map_one, map_all
from repo.handlers.base import BaseHandler
from repo.lib.avatar import avatar_url
from repo.models import models
from tornado import gen


class OrgsHandler(BaseHandler):

    @gen.coroutine
    def get(self, name):
        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (name,))
        if org is None:
            self.err(404)
        projects = yield map_all(models.Project, 'select * from projects where owner_id = %s', (org.id,))
        user = yield map_one(models.User, 'select * from users where id = %s', (org.namespace,))
        avatar = avatar_url(user.email, 120)
        self.render('orgs/view.html', org=org, projects=projects, avatar=avatar)
