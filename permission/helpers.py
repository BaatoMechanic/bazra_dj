

from typing import List
from django.http import HttpRequest
from django.urls import resolve

from .models import Permission, Role

from autho.models import User


def has_permission(request: HttpRequest) -> bool:
    """
    Checks if the user has permission to access the requested URL.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        bool: True if the user has permission, False otherwise.
    """
    user: User = request.user
    url_name: str = resolve(request.path_info).url_name
    method: str = request.method.lower()

    if not user.is_authenticated or user.is_obsolete:
        return anonymous_has_permission(url_name, method)

    if user.isa("Superuser"):
        return True

    if user.is_verified:
        return verified_has_permission(user, url_name, method)

    return unverified_has_permission(user, url_name, method)


def anonymous_has_permission(name: str, method: str) -> bool:
    '''
    Returns true if the requested permission has been granted to the anonymous role.

    Args:
        name: The name of the permission.
        method: The method of the permission.

    Returns:
        bool: True if the permission has been granted, False otherwise.
    '''
    roles: List[Role] = Role.objects.filter(name="Anonymous")
    return Permission.is_permission_granted(name=name, method=method, roles=roles)


def verified_has_permission(user: User, name: str, method: str) -> bool:
    '''
    Returns true if the requested permission has been granted to the verified role

    Args:
        user (User): The user object
        name (str): The name of the permission
        method (str): The method of the permission

    Returns:
        bool: True if the permission has been granted, False otherwise
    '''
    roles: List[Role] = list(user.roles.all())
    roles.append(user.primary_role)
    return Permission.is_permission_granted(name=name, method=method, roles=roles)


def unverified_has_permission(user: User, name: str, method: str) -> bool:
    '''
    Returns true if the requested permission has been granted to the unverified role

    Args:
        user (User): The user object
        name (str): The name of the permission
        method (str): The HTTP method of the permission

    Returns:
        bool: True if the permission has been granted, False otherwise
    '''
    roles: List[Role] = Role.objects.filter(name="Unverified")
    return Permission.is_permission_granted(name=name, method=method, roles=roles)
