

import sys
from django.http import HttpRequest
from django.urls import resolve

from .models import Permission, Role

from autho.models.user import User


from typing import Union, List


def has_permission(request: HttpRequest) -> Union[bool, str]:
    """
    Determine if the user has permission to access the requested URL.

    Args:
        request (HttpRequest): The request object.

    Returns:
        Union[bool, str]: True if the user has permission, False otherwise. If the user is not authenticated, a string
        indicating the reason for the permission denial is returned.
    """

    user: User = request.user
    url_name: str = resolve(request.path_info).url_name
    method: str = request.method.lower()
    if user.is_authenticated and not user.is_obsolete:
        if user.is_verified:
            return verified_has_permission(user, url_name, method)
        else:
            return unverified_has_permission(user, url_name, method)
    return anonymous_has_permission(url_name, method)


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
    roles: List[Role] = user.roles.all()
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
    # For now it works the same as anonymous role
    # will change if different permissions are added for the unverified role
    return anonymous_has_permission(name, method)
