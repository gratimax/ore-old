from ore.accounts.models import OreUser
from ore.core.models import Permission, Namespace, Organization
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from ore.core.util import validate_not_prohibited
from ore.projects.models import Project
from ore.core.regexs import EXTENDED_NAME_REGEX
from reversion import revisions as reversion


class Team(models.Model):
    name = models.CharField('name', max_length=80, null=False, blank=False,
                            validators=[
                                validators.RegexValidator(
                                    EXTENDED_NAME_REGEX, 'Enter a valid team name.', 'invalid'),
                                validate_not_prohibited,
                            ])
    description = models.CharField(
        default='', blank=True, null=False, max_length=140, verbose_name="Description (optional)")
    users = models.ManyToManyField(
        OreUser, related_name='%(class)ss', blank=True)
    permissions = models.ManyToManyField(
        Permission, related_name='+', blank=True)
    is_owner_team = models.BooleanField(default=False)

    def __str__(self):
        props = ['owner'] if self.is_owner_team else []
        return '%s [%s]' % (self.name, ' '.join(props))

    def check_consistent(self):
        return True

    def make_consistent(self):
        return

    class Meta:
        abstract = True


@reversion.register
class OrganizationTeam(Team):
    organization = models.ForeignKey(Organization, related_name='teams')
    projects = models.ManyToManyField(
        Project, related_name='organizationteams', blank=True)
    is_all_projects = models.BooleanField(default=False)

    def make_consistent(self):
        self.projects = self.projects.filter(namespace=self.organization)
        self.save()

    def check_consistent(self):
        return self.projects.exclude(namespace=self.organization).count() == 0

    def get_member_add_url(self):
        return reverse('organizations-team-add-member', kwargs={
            'namespace': self.project.namespace.name,
            'team': self.name,
        })

    def __str__(self):
        props = (['all_projects'] if self.is_all_projects else []) + \
                (['owner'] if self.is_owner_team else [])
        return '%s in %s [%s]' % (self.name, self.organization.name, ' '.join(props))

    class Meta:
        unique_together = ('organization', 'name')


@reversion.register
class ProjectTeam(Team):
    project = models.ForeignKey(Project, related_name='teams')

    def __str__(self):
        props = ['owner'] if self.is_owner_team else []
        return '%s in %s [%s]' % (self.name, self.project.name, ' '.join(props))

    def get_member_add_url(self):
        return reverse('projects-team-add-member', kwargs={
            'namespace': self.project.namespace.name,
            'project': self.project.name,
            'team': self.name,
        })

    # TODO: we need to check here that if we're a user's project and we're the
    # owner team, that that user is in us!

    class Meta:
        unique_together = ('project', 'name')


@receiver(post_save, sender=Organization)
def create_organization_owner_team(sender, instance, created, **kwargs):
    if instance and created:
        OrganizationTeam.objects.create(
            name='Owners',
            organization=instance,
            is_all_projects=True,
            is_owner_team=True,
        )
