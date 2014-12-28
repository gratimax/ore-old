from repo.db import map_one
from repo.handlers.base import BaseHandler
from repo.models import models
from tornado import gen


class OrgsHandler(BaseHandler):

    @gen.coroutine
    def get(self, name):
        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (name,))
        if org is None:
            self.err(404)
