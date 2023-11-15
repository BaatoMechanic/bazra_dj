

from rest_framework.permissions import BasePermission

from .helpers import has_permission


class BazraPermission(BasePermission):
    def has_permission(self, request, view):

        return has_permission(request)
