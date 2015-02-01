from ore.core.models import Namespace
from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from ore.projects.models import Project


def permission_required(permission_slug, raise_exception=False):
    if isinstance(permission_slug, (list, tuple)):
        perms = permission_slug
    else:
        perms = (permission_slug, )

    def _permission_required(f):
        @wraps(f)
        def _permission_required(request, *args, **kwargs):
            if not request.user.is_authenticated():
                # fail fast, if they're not logged in
                return _permission_fail(request, "User is not logged in.")
            if 'fail' in perms:
                return _permission_fail(request, "Permission 'fail' is never granted.")

            namespace = kwargs.get('namespace')
            if namespace is None:
                raise TypeError('namespace must be set')

            project = kwargs.get('project')

            if project:
                obj = get_object_or_404(Project, name=project, namespace__name=namespace)
            else:
                obj = get_object_or_404(Namespace.objects.select_subclasses(), name=namespace)

            for perm in perms:
                if not obj.user_has_permission(request.user, perm):
                    return _permission_fail(request, "You don't have permission to do that!")
            return f(request, *args, **kwargs)

        def _permission_fail(request, err):
            if raise_exception or request.user.is_authenticated():
                raise PermissionDenied(err)
            return redirect_to_login(request.path)
        return _permission_required
    return _permission_required
