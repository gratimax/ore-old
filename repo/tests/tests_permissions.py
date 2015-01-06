from django.test import TestCase
from .. import models


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.permission_foo = models.Permission.objects.create(slug='foo.do', name='Do Foo', description='Performs foo')
        self.permission_bar = models.Permission.objects.create(slug='foo.bar', name='Bar', description='Bars foo')
        self.permission_baz = models.Permission.objects.create(slug='baz.do', name='Do Baz', description='Bazzes the widget')

    def test_unrelated_people_cant_do_anything_on_organization(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        self.assertFalse(organization_sponge.user_has_permission(user_john, 'foo.do'), 'John can\'t foo.do')
        self.assertFalse(organization_sponge.user_has_permission(user_john, 'foo.bar'), 'John can\'t foo.bar')
        self.assertFalse(organization_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_unrelated_people_cant_do_anything_on_organization_project(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge',
            )
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        self.assertFalse(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can\'t foo.do')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can\'t foo.bar')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_organization_owner_can_do_everything_on_organization(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')

        team = organization_sponge.teams.get(is_owner_team=True)

        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        team.users = [user_john]

        self.assertTrue(organization_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(organization_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertTrue(organization_sponge.user_has_permission(user_john, 'baz.do'), 'John can baz.do')

    def test_organization_owner_can_do_everything_on_project(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge'
        )

        team = organization_sponge.teams.get(is_owner_team=True)

        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        team.users = [user_john]

        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can baz.do')

    def test_project_owner_can_do_everything_on_project(self):
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=user_john, description='Sponge'
        )

        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can baz.do')

    def test_organization_all_project_teams_grant_permissions_on_projects(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge'
        )
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        team = models.OrganizationTeam.objects.create(
            name='People',
            organization=organization_sponge,
            is_all_projects=True,
            is_owner_team=False,
            )
        team.users = [user_john]
        team.permissions = [self.permission_foo, self.permission_bar]

        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_organization_all_project_teams_grant_permissions_on_organisations(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        team = models.OrganizationTeam.objects.create(
            name='People',
            organization=organization_sponge,
            is_all_projects=True,
            is_owner_team=False,
            )
        team.users = [user_john]
        team.permissions = [self.permission_foo, self.permission_bar]

        self.assertTrue(organization_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(organization_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertFalse(organization_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_organization_limited_project_teams_grant_permissions_on_selected_projects(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge'
        )
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        team = models.OrganizationTeam.objects.create(
            name='People',
            organization=organization_sponge,
            is_all_projects=False,
            is_owner_team=False,
            )
        team.users = [user_john]
        team.permissions = [self.permission_foo, self.permission_bar]
        team.projects = [project_sponge]

        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can foo.do')
        self.assertTrue(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can foo.bar')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_organization_limited_project_teams_dont_grant_permissions_on_unselected_projects(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge'
        )
        project_spongeapi = models.Project.objects.create(
            name='SpongeAPI', namespace=organization_sponge, description='Sponge'
        )
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        team = models.OrganizationTeam.objects.create(
            name='People',
            organization=organization_sponge,
            is_all_projects=False,
            is_owner_team=False,
            )
        team.users = [user_john]
        team.permissions = [self.permission_foo, self.permission_bar]
        team.projects = [project_spongeapi]

        self.assertFalse(project_sponge.user_has_permission(user_john, 'foo.do'), 'John can\'t foo.do')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'foo.bar'), 'John can\'t foo.bar')
        self.assertFalse(project_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')

    def test_organization_limited_project_teams_dont_grant_permissions_on_organisations(self):
        organization_sponge = models.Organization.objects.create(name='Sponge')
        project_sponge = models.Project.objects.create(
            name='Sponge', namespace=organization_sponge, description='Sponge'
        )
        user_john = models.RepoUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        team = models.OrganizationTeam.objects.create(
            name='People',
            organization=organization_sponge,
            is_all_projects=False,
            is_owner_team=False,
            )
        team.users = [user_john]
        team.permissions = [self.permission_foo, self.permission_bar]
        team.projects = [project_sponge]

        self.assertFalse(organization_sponge.user_has_permission(user_john, 'foo.do'), 'John can\'t foo.do')
        self.assertFalse(organization_sponge.user_has_permission(user_john, 'foo.bar'), 'John can\'t foo.bar')
        self.assertFalse(organization_sponge.user_has_permission(user_john, 'baz.do'), 'John can\'t baz.do')