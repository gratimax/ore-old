import momoko
from repo.db import map_one, db
from repo.handlers.base import BaseHandler
from repo.models import models
from repo.models.orgs import namespace_of
from repo.models.projects import validate_project_name, validate_project_description
from tornado import gen


class ProjectsHandler(BaseHandler):

    @gen.coroutine
    def get(self, org_name, proj_name):
        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (org_name,))
        if org is None:
            self.err(404)
        proj = yield map_one(models.Project, 'select * from projects where owner_id = %s and name = %s', (org.id, proj_name))
        if proj is None:
            self.err(404)

        current_user = yield self.current_user

        authorized = current_user is not None and current_user.id == org.namespace

        self.render('projects/view.html', org=org, proj=proj, authorized=authorized)


class ProjectsNewHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        current_user = yield self.current_user
        yield self.auth()
        self.render('projects/new.html', errors=[])

    @gen.coroutine
    def post(self):

        yield self.auth()

        current_user = yield self.current_user

        namespace = yield namespace_of(current_user)

        name = self.get_body_argument('name')
        description = self.get_body_argument('description')

        if '' in [name, description]:
            self.render('projects/new.html', errors=['Nothing can be empty'])
            return

        name_valid = yield validate_project_name(name, namespace)

        if name_valid != '':
            self.render('projects/new.html', errors=[name_valid])
            return

        description_valid = validate_project_description(description)

        if description_valid != '':
            self.render('projects/new.html', errors=[description_valid])
            return

        yield momoko.Op(db.execute, 'insert into projects (owner_id, name, description) values (%s, %s, %s)', (namespace.id, name, description))

        self.redirect('/' + namespace.name + '/' + name)


class ProjectSettingsHandler(BaseHandler):

    @gen.coroutine
    def get(self, org_name, proj_name):

        yield self.auth()

        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (org_name,))
        if org is None:
            self.err(404)
        proj = yield map_one(models.Project, 'select * from projects where owner_id = %s and name = %s', (org.id, proj_name))
        if proj is None:
            self.err(404)

        current_user = yield self.current_user

        if org.namespace != current_user.id:
            self.err(405)

        self.render('projects/settings.html', proj=proj, org=org)


class ProjectDeleteHandler(BaseHandler):

    @gen.coroutine
    def post(self, org_name, proj_name):

        yield self.auth()

        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (org_name,))
        if org is None:
            self.err(404)
        proj = yield map_one(models.Project, 'select * from projects where owner_id = %s and name = %s', (org.id, proj_name))
        if proj is None:
            self.err(404)

        current_user = yield self.current_user

        if org.namespace != current_user.id:
            self.err(405)

        yield momoko.Op(db.execute, 'begin')
        yield momoko.Op(db.execute, 'delete from files where project_id = %s', (proj.id,))
        yield momoko.Op(db.execute, 'delete from projects where id = %s', (proj.id,))
        yield momoko.Op(db.execute, 'commit')

        self.redirect('/')
