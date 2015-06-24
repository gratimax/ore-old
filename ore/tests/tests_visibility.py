from django.contrib.auth.models import AnonymousUser
from ore.accounts.models import OreUser
from ore.core.models import Organization
from django.test import TestCase as TestCase
from ore.projects.models import Project
from ore.teams.models import OrganizationTeam, ProjectTeam
from ore.versions.models import Version, File


class VisibilityTestCase(TestCase):

    def make_project(self, name, namespace, status=Project.STATUS.active):
        proj = Project.objects.create(
            name=name, namespace=namespace,
            description='?', status=status,
        )
        return proj

    def make_user(self, username, status=OreUser.STATUS.active):
        user = OreUser.objects.create_user(
            username, 'password', '{}@ore.spongepowered.org'.format(username)
        )
        user.is_staff = False
        user.is_superuser = False
        user.status = status
        user.save()
        return user

    def make_superuser(self, *args, **kwargs):
        user = self.make_user(*args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def make_organization(self, name, owners=None, status=Organization.STATUS.active):
        org = Organization.objects.create(
            name=name, status=status,
        )
        if owners:
            org.teams.get(is_owner_team=True).users = owners
        return org

    def make_version(self, name, project, status=Version.STATUS.active):
        return Version.objects.create(
            name=name, project=project, status=status,
        )

    def make_organization_team(self, name, organization, users=None, projects=None, permissions=None, **kwargs):
        team = OrganizationTeam.objects.create(
            name=name, organization=organization, **kwargs
        )
        if users:
            team.users = users
        if projects:
            team.projects = projects
        if permissions:
            team.permissions = permissions
        return team

    def make_project_team(self, name, project, users=None, permissions=None, **kwargs):
        team = ProjectTeam.objects.create(
            name=name, project=project, **kwargs
        )
        if users:
            team.users = users
        if permissions:
            team.permissions = permissions
        return team

    def make_file(self, version, filetype, status=File.STATUS.active):
        return File.objects.create(
            version=version, filetype=filetype, status=status
        )

    def assertUserCanSee(self, model, user, item):
        self.assertIn(item, model.objects.as_user(user))

    def assertUserCanNotSee(self, model, user, item):
        self.assertNotIn(item, model.objects.as_user(user))


class RepoUserVisibilityTestCase(VisibilityTestCase):

    def test_user_visible_anonymously(self):
        user_joe = self.make_user('joe')
        self.assertUserCanSee(OreUser, AnonymousUser(), user_joe)

    def test_user_visible_randomer(self):
        user_joe = self.make_user('joe')
        user_jane = self.make_user('jane')
        self.assertUserCanSee(OreUser, user_jane, user_joe)

    def test_user_visible_themselves(self):
        user_joe = self.make_user('joe')
        self.assertUserCanSee(OreUser, user_joe, user_joe)

    def test_user_visible_staff(self):
        user_joe = self.make_user('joe')
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(OreUser, user_janet, user_joe)

    def test_deleted_user_not_visible_anonymously(self):
        user_joe = self.make_user('joe', status=OreUser.STATUS.deleted)
        self.assertUserCanNotSee(OreUser, AnonymousUser(), user_joe)

    def test_deleted_user_not_visible_randomer(self):
        user_joe = self.make_user('joe', status=OreUser.STATUS.deleted)
        user_jane = self.make_user('jane')
        self.assertUserCanNotSee(OreUser, user_jane, user_joe)

    def test_deleted_user_visible_staff(self):
        user_joe = self.make_user('joe', status=OreUser.STATUS.deleted)
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(OreUser, user_janet, user_joe)


class OrganizationVisibilityTestCase(VisibilityTestCase):

    def test_organization_visible_anonymously(self):
        org_sponge = self.make_organization('Sponge')
        self.assertUserCanSee(Organization, AnonymousUser(), org_sponge)

    def test_organization_visible_randomer(self):
        org_sponge = self.make_organization('Sponge')
        user_jane = self.make_user('jane')
        self.assertUserCanSee(Organization, user_jane, org_sponge)

    def test_organization_visible_owner(self):
        user_joe = self.make_user('joe')
        org_sponge = self.make_organization('Sponge', owners=[user_joe])
        self.assertUserCanSee(Organization, user_joe, org_sponge)

    def test_organization_visible_staff(self):
        org_sponge = self.make_organization('Sponge')
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(Organization, user_janet, org_sponge)

    def test_deleted_organization_not_visible_anonymously(self):
        org_sponge = self.make_organization(
            'Sponge', status=Organization.STATUS.deleted)
        self.assertUserCanNotSee(Organization, AnonymousUser(), org_sponge)

    def test_deleted_organization_not_visible_randomer(self):
        org_sponge = self.make_organization(
            'Sponge', status=Organization.STATUS.deleted)
        user_jane = self.make_user('jane')
        self.assertUserCanNotSee(Organization, user_jane, org_sponge)

    def test_deleted_organization_not_visible_owner(self):
        user_joe = self.make_user('joe')
        org_sponge = self.make_organization(
            'Sponge', owners=[user_joe], status=Organization.STATUS.deleted)
        self.assertUserCanNotSee(Organization, user_joe, org_sponge)

    def test_deleted_organization_visible_staff(self):
        org_sponge = self.make_organization(
            'Sponge', status=Organization.STATUS.deleted)
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(Organization, user_janet, org_sponge)


class UserNamespaceMixin(object):

    def make_namespace(self, **kwargs):
        user_joe = self.make_user('joe', **kwargs)
        return user_joe, user_joe


class OrganizationNamespaceMixin(object):

    def make_namespace(self, **kwargs):
        user_joe = self.make_user('joe')
        org_sponge = self.make_organization(
            'Sponge', owners=[user_joe], **kwargs)
        return user_joe, org_sponge


class ProjectVisibilityTestCaseMixin(object):

    def test_project_visible_anonymously(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        self.assertUserCanSee(Project, AnonymousUser(), proj_sponge)

    def test_project_visible_randomer(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_jane = self.make_user('jane')
        self.assertUserCanSee(Project, user_jane, proj_sponge)

    def test_project_visible_owner(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        self.assertUserCanSee(Project, user_joe, proj_sponge)

    def test_project_visible_project_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        pteam_spongers = self.make_project_team(
            'Spongers', proj_sponge, users=[user_jack])
        self.assertUserCanSee(Project, user_jack, proj_sponge)

    def test_project_visible_staff(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(Project, user_janet, proj_sponge)

    def test_namespace_deleted_project_not_visible_anonymously(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        self.assertUserCanNotSee(Project, AnonymousUser(), proj_sponge)

    def test_namespace_deleted_project_not_visible_randomer(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_jane = self.make_user('jane')
        self.assertUserCanNotSee(Project, user_jane, proj_sponge)

    def test_namespace_deleted_project_not_visible_owner(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        self.assertUserCanNotSee(Project, user_joe, proj_sponge)

    def test_namespace_deleted_project_not_visible_project_team_member(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        pteam_spongers = self.make_project_team(
            'Spongers', proj_sponge, users=[user_jack])
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_namespace_deleted_project_visible_staff(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(Project, user_janet, proj_sponge)

    def test_deleted_project_not_visible_anonymously(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        self.assertUserCanNotSee(Project, AnonymousUser(), proj_sponge)

    def test_deleted_project_not_visible_randomer(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_jane = self.make_user('jane')
        self.assertUserCanNotSee(Project, user_jane, proj_sponge)

    def test_deleted_project_not_visible_owner(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        self.assertUserCanNotSee(Project, user_joe, proj_sponge)

    def test_deleted_project_not_visible_project_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_jack = self.make_user('jack')
        pteam_spongers = self.make_project_team(
            'Spongers', proj_sponge, users=[user_jack])
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_deleted_project_visible_staff(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_janet = self.make_superuser('janet')
        self.assertUserCanSee(Project, user_janet, proj_sponge)


class UserProjectVisibilityTestCase(UserNamespaceMixin, ProjectVisibilityTestCaseMixin, VisibilityTestCase):
    pass


class OrganizationProjectVisibilityTestCase(OrganizationNamespaceMixin, ProjectVisibilityTestCaseMixin, VisibilityTestCase):

    def test_project_visible_irrelevant_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=False)
        self.assertUserCanSee(Project, user_jack, proj_sponge)

    def test_namespace_deleted_project_not_visible_irrelevant_organization_team_member(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=False)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_deleted_project_not_visible_irrelevant_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=False)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_project_visible_all_projects_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=True)
        self.assertUserCanSee(Project, user_jack, proj_sponge)

    def test_namespace_deleted_project_not_visible_all_projects_organization_team_member(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=True)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_deleted_project_not_visible_all_projects_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team(
            'Spongers', namespace, users=[user_jack], projects=[], is_all_projects=True)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_project_visible_project_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team('Spongers', namespace, users=[
                                                     user_jack], projects=[proj_sponge], is_all_projects=False)
        self.assertUserCanSee(Project, user_jack, proj_sponge)

    def test_namespace_deleted_project_not_visible_project_organization_team_member(self):
        user_joe, namespace = self.make_namespace(status='deleted')
        proj_sponge = self.make_project('Sponge', namespace)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team('Spongers', namespace, users=[
                                                     user_jack], projects=[proj_sponge], is_all_projects=False)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)

    def test_deleted_project_not_visible_project_organization_team_member(self):
        user_joe, namespace = self.make_namespace()
        proj_sponge = self.make_project(
            'Sponge', namespace, status=Project.STATUS.deleted)
        user_jack = self.make_user('jack')
        oteam_spongers = self.make_organization_team('Spongers', namespace, users=[
                                                     user_jack], projects=[proj_sponge], is_all_projects=False)
        self.assertUserCanNotSee(Project, user_jack, proj_sponge)
