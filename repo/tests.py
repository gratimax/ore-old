from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from . import models

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        self.user_sally = models.RepoUser.objects.create_user('sally', 'password', 'sally@ore.spongepowered.org')
        self.user_sue = models.RepoUser.objects.create_user('sue', 'password', 'sue@ore.spongepowered.org')

        self.organization_sponge = models.Organization.objects.create(name='Sponge')

        self.permission_foo = models.Permission.objects.create(slug='foo.do', name='Do Foo', description='Performs foo')
        self.permission_bar = models.Permission.objects.create(slug='foo.bar', name='Bar', description='Bars foo')
        self.permission_baz = models.Permission.objects.create(slug='baz.do', name='Do Baz', description='Bazzes the widget')

        self.project_sponge = models.Project.objects.create(name='Sponge', namespace=self.organization_sponge, description='SPONGE') 
        self.project_sponge_api = models.Project.objects.create(name='SpongeAPI', namespace=self.organization_sponge, description='SPONGE') 
        self.project_bookit = models.Project.objects.create(name='Bookit', namespace=self.user_john, description='BOOkit')
        self.project_nar = models.Project.objects.create(name='Nar', namespace=self.user_sally, description='NAR')

        self.oteam_owners = self.organization_sponge.teams.get(is_owner_team=True, organization=self.organization_sponge)
        self.oteam_owners.users = [self.user_john]

        self.oteam_peons = models.OrganizationTeam.objects.create(name='Peons', organization=self.organization_sponge)
        self.oteam_peons.users = [self.user_sue]
        self.oteam_peons.projects = [self.project_sponge]
        self.oteam_peons.permissions = [self.permission_foo]

        self.pteam_serpents = models.ProjectTeam.objects.create(name='Serpents', project=self.project_sponge)
        self.pteam_serpents.users = [self.user_sue, self.user_sally]
        self.pteam_serpents.permissions = [self.permission_bar, self.permission_foo]

    def test_organization_owner_team(self):
        self.assertTrue(self.project_sponge.user_has_permission(self.user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(self.project_sponge.user_has_permission(self.user_john, 'foo.bar'), 'John can foo.bar')
        self.assertTrue(self.project_sponge.user_has_permission(self.user_john, 'baz.do'), 'John can baz.do')

    def test_organization_teams(self):
        self.assertTrue(self.project_sponge.user_has_permission(self.user_sue, 'foo.do'), 'Sue can foo.do on Sponge')
        self.assertFalse(self.project_sponge_api.user_has_permission(self.user_sue, 'foo.do'), 'Sue can\'t foo.do on SpongeAPI')

    def test_project_teams(self):
        self.assertTrue(self.project_sponge.user_has_permission(self.user_sue, 'foo.bar'), 'Sue can foo.bar on Sponge')
        self.assertTrue(self.project_sponge.user_has_permission(self.user_sally, 'foo.bar'), 'Sally can foo.bar on Sponge')

        self.assertFalse(self.project_sponge_api.user_has_permission(self.user_sue, 'foo.bar'), 'Sue can\'t foo.bar on SpongeAPI')
        self.assertFalse(self.project_sponge_api.user_has_permission(self.user_sally, 'foo.bar'), 'Sally can\'t foo.bar on SpongeAPI')

        self.assertFalse(self.project_bookit.user_has_permission(self.user_sue, 'foo.bar'), 'Sue can\'t foo.bar on Bookit')
        self.assertFalse(self.project_bookit.user_has_permission(self.user_sally, 'foo.bar'), 'Sally can\'t foo.bar on Bookit')
        self.assertFalse(self.project_bookit.user_has_permission(self.user_sue, 'baz.do'), 'Sue can\'t baz.do on Bookit')
        self.assertFalse(self.project_bookit.user_has_permission(self.user_sally, 'baz.do'), 'Sally can\'t baz.do on Bookit')

        self.assertFalse(self.project_sponge_api.user_has_permission(self.user_sue, 'baz.do'), 'Sue can\'t baz.do on SpongeAPI')
        self.assertFalse(self.project_sponge_api.user_has_permission(self.user_sally, 'baz.do'), 'Sally can\'t baz.do on SpongeAPI')

class VisibilityTestCase(TestCase):
    def setUp(self):
        self.user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        self.user_sally = models.RepoUser.objects.create_user('sally', 'password', 'sally@ore.spongepowered.org')
        self.user_sue = models.RepoUser.objects.create_user('sue', 'password', 'sue@ore.spongepowered.org')
        self.user_joe = models.RepoUser.objects.create_user('joe', 'password', 'joe@ore.spongepowered.org')

        self.organization_sponge = models.Organization.objects.create(name='Sponge')
        self.organization_powbang = models.Organization.objects.create(name='PowBang!', status=models.Organization.STATUS.deleted)

        self.permission_foo = models.Permission.objects.create(slug='foo.do', name='Do Foo', description='Performs foo')
        self.permission_bar = models.Permission.objects.create(slug='foo.bar', name='Bar', description='Bars foo')
        self.permission_baz = models.Permission.objects.create(slug='baz.do', name='Do Baz', description='Bazzes the widget')

        self.project_sponge = models.Project.objects.create(name='Sponge', namespace=self.organization_sponge, description='SPONGE', status=models.Project.STATUS.deleted) 
        self.project_sponge_api = models.Project.objects.create(name='SpongeAPI', namespace=self.organization_sponge, description='SPONGE', status=models.Project.STATUS.deleted) 
        self.project_bookit = models.Project.objects.create(name='Bookit', namespace=self.user_john, description='BOOkit', status=models.Project.STATUS.deleted)
        self.project_nar = models.Project.objects.create(name='Nar', namespace=self.user_sally, description='NAR', status=models.Project.STATUS.deleted)
        self.project_powbang = models.Project.objects.create(name='PowBang!', namespace=self.organization_powbang, description='PowBang!')
        self.project_powbang_redux = models.Project.objects.create(name='PowBongRedux', namespace=self.user_joe, description='PowBang v2.0')

        self.oteam_owners = self.organization_sponge.teams.get(is_owner_team=True)
        self.oteam_owners.users = [self.user_john]

        self.oteam_pb_owners = self.organization_powbang.teams.get(is_owner_team=True)
        self.oteam_pb_owners.users = [self.user_joe]

        self.oteam_peons = models.OrganizationTeam.objects.create(name='Peons', organization=self.organization_sponge)
        self.oteam_peons.users = [self.user_sue]
        self.oteam_peons.projects = [self.project_sponge_api]
        self.oteam_peons.permissions = [self.permission_foo]

        self.pteam_serpents = models.ProjectTeam.objects.create(name='Serpents', project=self.project_sponge)
        self.pteam_serpents.users = [self.user_sue, self.user_sally]
        self.pteam_serpents.permissions = [self.permission_bar, self.permission_foo]

        self.version_powbang_zero = models.Version.objects.create(name='v0', project=self.project_powbang, status=models.Version.STATUS.deleted)
        self.version_powbang_one = models.Version.objects.create(name='v1', project=self.project_powbang)
        self.version_sponge_zero = models.Version.objects.create(name='v0', project=self.project_sponge, status=models.Version.STATUS.deleted)
        self.version_sponge_one = models.Version.objects.create(name='v1', project=self.project_sponge)
        self.version_powbang_redux_zero = models.Version.objects.create(name='v0', project=self.project_powbang_redux, status=models.Version.STATUS.deleted)
        self.version_powbang_redux_one = models.Version.objects.create(name='v1', project=self.project_powbang_redux)

        self.file_powbang_zero_zip = models.File.objects.create(name='ZIP', version=self.version_powbang_zero, status=models.File.STATUS.deleted)
        self.file_powbang_zero_jar = models.File.objects.create(name='JAR', version=self.version_powbang_zero)
        self.file_sponge_zero_zip = models.File.objects.create(name='ZIP', version=self.version_sponge_zero, status=models.File.STATUS.deleted)
        self.file_sponge_zero_jar = models.File.objects.create(name='JAR', version=self.version_sponge_zero)
        self.file_powbang_redux_zero_zip = models.File.objects.create(name='ZIP', version=self.version_powbang_redux_zero, status=models.File.STATUS.deleted)
        self.file_powbang_redux_zero_jar = models.File.objects.create(name='JAR', version=self.version_powbang_redux_zero)
        self.file_powbang_one_zip = models.File.objects.create(name='ZIP', version=self.version_powbang_one, status=models.File.STATUS.deleted)
        self.file_powbang_one_jar = models.File.objects.create(name='JAR', version=self.version_powbang_one)
        self.file_sponge_one_zip = models.File.objects.create(name='ZIP', version=self.version_sponge_one, status=models.File.STATUS.deleted)
        self.file_sponge_one_jar = models.File.objects.create(name='JAR', version=self.version_sponge_one)
        self.file_powbang_redux_one_zip = models.File.objects.create(name='ZIP', version=self.version_powbang_redux_one, status=models.File.STATUS.deleted)
        self.file_powbang_redux_one_jar = models.File.objects.create(name='JAR', version=self.version_powbang_redux_one)

    def test_visible_anonymous(self):
        self.assertQuerysetEqual(models.Project.objects.as_user(AnonymousUser()), [
            repr(self.project_powbang_redux),
        ], ordered=False)
        self.assertQuerysetEqual(models.Version.objects.as_user(AnonymousUser()), [
            repr(self.version_powbang_redux_one),
        ], ordered=False)
        self.assertQuerysetEqual(models.File.objects.as_user(AnonymousUser()), [
            repr(self.file_powbang_redux_one_jar),
        ], ordered=False)

    def test_visible_joe(self):
        self.assertQuerysetEqual(models.Project.objects.as_user(self.user_joe), [
            repr(self.project_powbang), repr(self.project_powbang_redux),
        ], ordered=False)
        self.assertQuerysetEqual(models.Version.objects.as_user(self.user_joe), [
            repr(self.version_powbang_redux_zero), repr(self.version_powbang_redux_one),
            repr(self.version_powbang_zero), repr(self.version_powbang_one),
        ], ordered=False)
        self.assertQuerysetEqual(models.File.objects.as_user(self.user_joe), [
            repr(self.file_powbang_redux_one_zip), repr(self.file_powbang_redux_one_jar),
            repr(self.file_powbang_redux_zero_zip), repr(self.file_powbang_redux_zero_jar),
            repr(self.file_powbang_one_zip), repr(self.file_powbang_one_jar),
            repr(self.file_powbang_zero_zip), repr(self.file_powbang_zero_jar),
        ], ordered=False)

    def test_visible_john(self):
        self.assertQuerysetEqual(models.Project.objects.as_user(self.user_john), [
            repr(self.project_sponge), repr(self.project_sponge_api), repr(self.project_bookit), repr(self.project_powbang_redux),
        ], ordered=False)
        self.assertQuerysetEqual(models.Version.objects.as_user(self.user_john), [
            repr(self.version_powbang_redux_one),
            repr(self.version_sponge_zero), repr(self.version_sponge_one),
        ], ordered=False)
        self.assertQuerysetEqual(models.File.objects.as_user(self.user_john), [
            repr(self.file_powbang_redux_one_jar),
            repr(self.file_sponge_one_zip), repr(self.file_sponge_one_jar),
            repr(self.file_sponge_zero_zip), repr(self.file_sponge_zero_jar),
        ], ordered=False)

    def test_visible_sally(self):
        self.assertQuerysetEqual(models.Project.objects.as_user(self.user_sally), [
            repr(self.project_sponge), repr(self.project_nar), repr(self.project_powbang_redux),
        ], ordered=False)
        self.assertQuerysetEqual(models.Version.objects.as_user(self.user_sally), [
            repr(self.version_powbang_redux_one),
            repr(self.version_sponge_zero), repr(self.version_sponge_one),
        ], ordered=False)
        self.assertQuerysetEqual(models.File.objects.as_user(self.user_sally), [
            repr(self.file_powbang_redux_one_jar),
            repr(self.file_sponge_one_zip), repr(self.file_sponge_one_jar),
            repr(self.file_sponge_zero_zip), repr(self.file_sponge_zero_jar),
        ], ordered=False)

    def test_visible_sue(self):
        self.assertQuerysetEqual(models.Project.objects.as_user(self.user_sue), [
            repr(self.project_sponge), repr(self.project_sponge_api), repr(self.project_powbang_redux),
        ], ordered=False)
        self.assertQuerysetEqual(models.Version.objects.as_user(self.user_sue), [
            repr(self.version_powbang_redux_one),
            repr(self.version_sponge_zero), repr(self.version_sponge_one),
        ], ordered=False)
        self.assertQuerysetEqual(models.File.objects.as_user(self.user_sue), [
            repr(self.file_powbang_redux_one_jar),
            repr(self.file_sponge_one_zip), repr(self.file_sponge_one_jar),
            repr(self.file_sponge_zero_zip), repr(self.file_sponge_zero_jar),
        ], ordered=False)
