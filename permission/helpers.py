

from django.http import HttpRequest
from django.urls import resolve

from .models import Permission, Role

from ..autho.models.user import User


def has_permission(request: HttpRequest):

    # Name of permission which is usually name of a url.
    # Except for rest url which is model_name-action-name. e.g. mechanic-list
    user: User = request.user
    url_name = resolve(request.path_info).url_name
    method = request.method.lower()

    if user.is_authenticated and not user.is_obsolete:
        if user.is_verified:
            return verified_has_permission(user, url_name, method)
        else:
            return unverified_has_permission(user, url_name, method)
    return anonymous_has_permission(url_name, method)


def anonymous_has_permission(name, method):
    '''
    Returns true if the requested permission has been granted to the annonymous role
    '''
    roles = Role.objects.filter(name="Anonymous")
    return Permission.is_permission_granted(name=name, method=method, roles=roles)


def verified_has_permission(user: User, name, method):
    '''
    Returns true if the requested permission has been granted to the verified role
    '''
    roles = user.roles.all()
    return Permission.is_permission_granted(name=name, method=method, roles=roles)


def unverified_has_permission(user: User, name, method):
    '''
    Returns true if the requested permission has been granted to the unverified role
    '''
    # For now it works the same as annonymous role
    # will change if different permissions are added for the unverified role
    return anonymous_has_permission(name, method)
