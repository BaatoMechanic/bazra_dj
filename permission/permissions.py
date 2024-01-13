

from rest_framework.permissions import BasePermission

from .helpers import has_permission


class BazraPermission(BasePermission):
    def has_permission(self, request, view):

        return has_permission(request)

    def has_object_permission(self, request, view, obj):
        try:
            model = view.serializer_class.Meta.model or view.queryset.model or view.model
        except AttributeError:
            raise Exception("It seems the view is not associated with any model.\
        Please overwrite this method as per need.")

        try:
            method_name = "can_{}".format(view.action or request.method.lower())
            return not not getattr(obj, method_name)(request)
        except AttributeError as e:
            print(e)
            raise Exception("Please implement {}.{}.".format(model, method_name))
