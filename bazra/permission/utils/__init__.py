from permission.models import Permission
from permission.utils.helpers import assign_permissions, create_permissions


def update_permissions():
    """
    Creates permissions and assign them to respective roles.
    """

    create_permissions()
    assign_permissions()
    print("List of permissions", Permission.objects.all().count())
