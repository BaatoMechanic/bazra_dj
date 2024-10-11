from permission.permissions import BazraPermission


class BaseAPIMixin:

    permission_classes = [BazraPermission]
    lookup_field = "idx"

    class Meta:
        abstract = True
