

from permission.permission_maps.user_permission_map import get_anonymous_permission_map, get_superuser_permission_map


def get_permission_map():
    return {
        "Anonymous": get_anonymous_permission_map(),
        "Superuser": get_superuser_permission_map()
    }
