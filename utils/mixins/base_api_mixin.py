from permission.permissions import BazraPermission


class BaseAPIMixin():
    permission_classes = [BazraPermission]

    class Meta:
        abstract = True
