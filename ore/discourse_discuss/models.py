import requests
import posixpath

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse

from ore.projects.models import Project, Page
from ore.core.models import Namespace
from ore.accounts.models import OreUser


def retrieve_userid_from_discourse(username):
    resp = requests.get(
        posixpath.join(settings.DISCOURSE_DISCUSS_API, "users", username),
        params={
            'api_key': settings.DISCOURSE_DISCUSS_API_KEY,
            'api_username': 'system',
        },
        headers={
            'Accept': 'application/json'
        }
    )
    resp.raise_for_status()
    return resp.json()['user']['id']


class DiscourseProjectThreadManager(models.Manager):

    def get_or_create_for_project(self, project):
        try:
            thread = self.get(project=project)
            return thread, False
        except self.model.DoesNotExist:
            thread = DiscourseProjectThread(project=project)
            thread.create_on_discourse()
            thread.save()
            return thread, True

    def update_or_create_for_project(self, project):
        thread, updated = self.get_or_create_for_project(project)
        if not updated:  # not created
            updated = thread.update_on_discourse()
            if updated:
                thread.save()
        return thread


class DiscourseProjectThread(models.Model):
    project = models.OneToOneField(Project, primary_key=True)
    post_id = models.PositiveIntegerField(null=False, blank=False)
    topic_id = models.PositiveIntegerField(null=False, blank=False)

    objects = DiscourseProjectThreadManager()

    @property
    def responsible_user(self):
        # this logic for this is fairly weird
        # since for projects namespaced under a user, it's trivial
        # but for those under an organisation it's somewhat non-trivial
        # for the moment if it's an org, we'll use 'system'
        namespace = Namespace.objects.get_subclass(id=self.project.namespace.id)
        if isinstance(namespace, OreUser):
            return namespace.name
        return "system"

    @property
    def post_content(self):
        page_content = Page.objects.get(project=self.project, title='Home').content

        return '**See this project on Ore: {}**\r\n\r\n---\r\n\r\n{}'.format(
            posixpath.join(
                settings.DISCOURSE_DISCUSS_ORE_SITE_BASE,
                reverse('projects-detail', kwargs={'namespace': self.project.namespace.name, 'project': self.project.name}).lstrip('/')
            ),
            page_content
        )

    def create_on_discourse(self):
        if self.post_id is not None:
            return  # do nothing, we already exist

        resp = requests.post(
            posixpath.join(settings.DISCOURSE_DISCUSS_API, "posts"),
            data={
                'api_key': settings.DISCOURSE_DISCUSS_API_KEY,
                'api_username': self.responsible_user,
                'title': '{}/{}'.format(self.project.namespace.name, self.project.name),
                'raw': self.post_content,
                'category': settings.DISCOURSE_DISCUSS_CATEGORY,
                'skip_validations': 'true',
            }
        )
        resp.raise_for_status()
        self.post_id = resp.json()['id']
        self.topic_id = resp.json()['topic_id']

    def update_on_discourse(self):
        if self.post_id is None:
            return  # err, no

        current_content_resp = requests.get(
            posixpath.join(settings.DISCOURSE_DISCUSS_API, "posts", str(self.post_id)),
            params={
                'api_key': settings.DISCOURSE_DISCUSS_API_KEY,
                'api_username': 'system',
            },
            headers={
                'Accept': 'application/json'
            }
        )
        current_content_resp.raise_for_status()
        current_content = current_content_resp.json()

        must_update = False
        must_update = must_update or current_content['raw'] != self.post_content
        must_update = must_update or current_content['username'] != self.responsible_user

        if not must_update:
            return False

        # we need the responsible user's Discourse ID
        resp_user = self.responsible_user
        resp_uid = -1
        if resp_user != 'system':
            resp_uid = retrieve_userid_from_discourse(resp_user)

        payload = {
            'api_key': settings.DISCOURSE_DISCUSS_API_KEY,
            'api_username': 'system',
            'skip_validations': 'true',
            'post[raw]': self.post_content,
            'post[user_id]': resp_uid,
            'post[edit_reason]': 'Ore automatic update'
        }
        resp = requests.put(
            posixpath.join(settings.DISCOURSE_DISCUSS_API, "posts", str(self.post_id)),
            data=payload
        )
        resp.raise_for_status()
        self.topic_id = resp['post']['topic_id']
        return True


@receiver(post_save, sender=Project)
def project_save_handler(sender, instance=None, **kwargs):
    if not settings.DISCOURSE_DISCUSS_ENABLED:
        return
    if not instance:
        return
    DiscourseProjectThread.objects.update_or_create_for_project(instance)


@receiver(post_save, sender=Page)
def page_save_handler(sender, instance=None, **kwargs):
    if not settings.DISCOURSE_DISCUSS_ENABLED:
        return
    if not instance:
        return
    if instance.title != 'Home':
        return
    DiscourseProjectThread.objects.update_or_create_for_project(instance.project)
