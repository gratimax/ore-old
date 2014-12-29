import momoko
from repo.db import map_one, db, map_all
from repo.handlers.base import BaseHandler
from repo.models import models
from repo.models.orgs import namespace_of
from repo.models.projects import validate_project_name, validate_project_description
from repo.services.users import redirect_to_user_page
from tornado import gen


class ProjectFinder(BaseHandler):

    @gen.coroutine
    def find(self, org_name, proj_name):
        org = yield map_one(models.Organization, 'select * from orgs where name = %s', (org_name,))
        if org is None:
            self.err(404)
        proj = yield map_one(models.Project, 'select * from projects where owner_id = %s and name = %s', (org.id, proj_name))
        if proj is None:
            self.err(404)
        raise gen.Return((org, proj))


class ProjectsHandler(ProjectFinder):

    @gen.coroutine
    def get(self, org_name, proj_name):

        (org, proj) = yield self.find(org_name, proj_name)

        current_user = yield self.current_user_secure

        authorized = current_user is not None and current_user.id == org.namespace

        self.render('projects/view.html', org=org, proj=proj, authorized=authorized)


class ProjectsNewHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        current_user = yield self.current_user_secure
        yield self.auth()
        self.render('projects/new.html', errors=[])

    @gen.coroutine
    def post(self):

        yield self.auth()

        current_user = yield self.current_user_secure

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


class ProjectManageHandler(ProjectFinder):

    @gen.coroutine
    def get(self, org_name, proj_name):

        yield self.auth()

        (org, proj) = yield self.find(org_name, proj_name)

        current_user = yield self.current_user_secure

        if org.namespace != current_user.id:
            self.err(405)

        self.render('projects/manage.html', proj=proj, org=org, rename_errors=[], description_errors=[])


class ProjectDeleteHandler(ProjectFinder):

    @gen.coroutine
    def post(self, org_name, proj_name):

        yield self.auth()

        (org, proj) = yield self.find(org_name, proj_name)

        current_user = yield self.current_user_secure

        if org.namespace != current_user.id:
            self.err(405)

        yield momoko.Op(db.execute, 'begin')
        yield momoko.Op(db.execute, 'delete from versions where project_id = %s', (proj.id,))
        yield momoko.Op(db.execute, 'delete from projects where id = %s', (proj.id,))
        yield momoko.Op(db.execute, 'commit')

        yield redirect_to_user_page(self, current_user)


class ProjectRenameHandler(ProjectFinder):

    @gen.coroutine
    def post(self, org_name, proj_name):

        yield self.auth()

        (org, proj) = yield self.find(org_name, proj_name)

        current_user = yield self.current_user_secure

        if org.namespace != current_user.id:
            self.err(405)

        name = self.get_body_argument('name')

        name_valid = yield validate_project_name(name, org)

        if name == '':
            self.render('projects/manage.html',
                        rename_errors=['Project name cannot be empty'],
                        description_errors=[], org=org, proj=proj)
            return

        if name_valid != '':
            self.render('projects/manage.html',
                        rename_errors=[name_valid],
                        description_errors=[],
                        org=org, proj=proj)
            return

        yield momoko.Op(db.execute, 'update projects set name = %s where id = %s', (name, proj.id))

        self.redirect('/' + org.name + '/' + name + '/manage')


class ProjectDescribeHandler(ProjectFinder):

    @gen.coroutine
    def post(self, org_name, proj_name):

        yield self.auth()

        (org, proj) = yield self.find(org_name, proj_name)

        current_user = yield self.current_user_secure

        if org.namespace != current_user.id:
            self.err(405)

        description = self.get_body_argument('description')

        description_valid = validate_project_description(description)

        if description == '':
            self.render('projects/manage.html',
                        rename_errors=[],
                        description_errors=['Description cannot be empty'], org=org, proj=proj)
            return

        if description_valid != '':
            self.render('projects/manage.html',
                        rename_errors=[],
                        description_errors=[description_valid],
                        org=org, proj=proj)
            return

        yield momoko.Op(db.execute, 'update projects set description = %s where id = %s', (description,))

        self.redirect('/' + org.name + '/' + proj.name + '/manage')


class ExploreHandler(BaseHandler):

    @gen.coroutine
    def get(self):

        projs = yield map_all(models.Project, 'select * from projects')

        projects = []
        for p in projs:
            org = yield map_one(models.Organization, 'select * from orgs where id = %s', (p.owner_id,))
            projects.append([p, org])

        self.render('projects/index.html', projects=projects)
