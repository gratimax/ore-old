from unittest.mock import Mock, patch, call

from ore.core import decorators
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.test import TestCase
from ore.projects.models import Project


__author__ = 'max'


class PermissionRequiredTestCase(TestCase):
    def make_request(self, authenticated=True):
        f = Mock()
        user = Mock(**{'is_authenticated.return_value': authenticated})
        request = Mock(user=user)
        return f, user, request

    def test_fails_if_not_authenticated(self):
        f, user, request = self.make_request(False)

        decorators.permission_required('foo.bar')(f)(request, namespace='wat', project='wat')

        self.assertEqual(f.call_count, 0, "f should not be called")
        self.assertEqual(user.user_has_permission.call_count, 0, "user_has_permission should not be called")

    def test_returns_redirect_on_fail_if_not_logged_in(self):
        f, user, request = self.make_request(False)

        resp = decorators.permission_required('fail')(f)(request, namespace='wat', project='wat')

        self.assertIsInstance(resp, HttpResponseRedirect, "should return a redirect")
        self.assertTrue(resp['Location'].startswith('/accounts/login/'), "redirect should be to /accounts/login/")

    def test_fails_if_fail_requested(self):
        f, user, request = self.make_request()

        with self.assertRaises(PermissionDenied):
            decorators.permission_required('fail')(f)(request, namespace='wat', project='wat')

        self.assertEqual(f.call_count, 0, "f should not be called")
        self.assertEqual(user.user_has_permission.call_count, 0, "user_has_permission should not be called")

    def test_throws_exception_if_requested(self):
        f, user, request = self.make_request(False)

        with self.assertRaises(PermissionDenied):
            decorators.permission_required('fail', raise_exception=True)(f)(request, namespace='wat', project='wat')

        self.assertEqual(f.call_count, 0, "f should not be called")
        self.assertEqual(user.user_has_permission.call_count, 0, "user_has_permission should not be called")

    def test_always_throws_exception_if_logged_in(self):
        f, user, request = self.make_request()

        with self.assertRaises(PermissionDenied):
            decorators.permission_required('fail', raise_exception=False)(f)(request, namespace='wat', project='wat')

        self.assertEqual(f.call_count, 0, "f should not be called")
        self.assertEqual(user.user_has_permission.call_count, 0, "user_has_permission should not be called")

    @patch('repo.decorators.get_object_or_404')
    def test_fails_if_does_not_have_permission(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        project = Mock()
        mock_get_object_or_404.return_value = project
        project.user_has_permission.return_value = False

        with self.assertRaises(PermissionDenied):
            resp = decorators.permission_required('foo.bar', raise_exception=True)(f)(request, namespace='wat', project='wat')

        self.assertEqual(f.call_count, 0, "f should not be called")
        project.user_has_permission.assert_called_once_with(user, 'foo.bar')

    @patch('repo.decorators.get_object_or_404')
    def test_succeeds_if_has_permission(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        project = Mock()
        mock_get_object_or_404.return_value = project
        project.user_has_permission.return_value = True

        resp = decorators.permission_required('foo.bar', raise_exception=True)(f)(request, namespace='wat', project='wat')

        f.assert_called_with(request, namespace='wat', project='wat')
        project.user_has_permission.assert_called_once_with(user, 'foo.bar')

    @patch('repo.decorators.get_object_or_404')
    def test_returns_value_from_wrapped_function(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        project = Mock()
        mock_get_object_or_404.return_value = project
        project.user_has_permission.return_value = True

        resp = decorators.permission_required('foo.bar', raise_exception=True)(f)(request, namespace='wat', project='wat')

        self.assertEquals(resp, f())

    @patch('repo.decorators.get_object_or_404')
    def test_looks_up_project(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        decorators.permission_required('foo.bar')(f)(request, namespace='namespace', project='project')
        mock_get_object_or_404.assert_called_once_with(Project, namespace__name='namespace', name='project')

    @patch('repo.decorators.get_object_or_404')
    @patch('repo.decorators.models.Namespace')
    def test_looks_up_namespace(self, mock_namespace, mock_get_object_or_404):
        f, user, request = self.make_request()

        mock_select_subclasses_qs = Mock()
        mock_namespace.objects.select_subclasses.return_value = mock_select_subclasses_qs

        decorators.permission_required('foo.bar')(f)(request, namespace='namespace')
        mock_get_object_or_404.assert_called_once_with(mock_select_subclasses_qs, name='namespace')

    @patch('repo.decorators.get_object_or_404')
    def test_checks_multiple_permissions_if_specified(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        project = Mock()
        mock_get_object_or_404.return_value = project
        project.user_has_permission.return_value = True

        decorators.permission_required(('foo.bar', 'baz.fern'))(f)(request, namespace='namespace')

        project.user_has_permission.assert_has_calls([call(user, 'foo.bar'), call(user, 'baz.fern')])

    @patch('repo.decorators.get_object_or_404')
    def test_fails_if_any_permission_missing(self, mock_get_object_or_404):
        f, user, request = self.make_request()

        project = Mock()
        mock_get_object_or_404.return_value = project
        project.user_has_permission.side_effect = [True, False]

        with self.assertRaises(PermissionDenied):
            decorators.permission_required(('foo.bar', 'baz.fern'))(f)(request, namespace='namespace')

        project.user_has_permission.assert_has_calls([call(user, 'foo.bar'), call(user, 'baz.fern')])
