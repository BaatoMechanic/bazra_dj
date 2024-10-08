from permission.permission_maps.user_permission_map import (
    get_anonymous_permission_map,
    get_consumer_permission_map,
    get_mechanic_permission_map,
    get_superuser_permission_map,
    get_unverified_permission_map,
)


def get_permission_map():
    return {
        "Anonymous": get_anonymous_permission_map(),
        "Superuser": get_superuser_permission_map(),
        "Consumer": get_consumer_permission_map(),
        "Mechanic": get_mechanic_permission_map(),
        "Unverified": get_unverified_permission_map(),
    }
