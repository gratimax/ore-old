from django.test import TestCase
from . import models

# Create your tests here.

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
