

from permission.app_permissions_list.autho_permission import LOGIN_API


def get_anonymous_permission_map():
    return [
        LOGIN_API
    ]


def get_superuser_permission_map():
    return [
        LOGIN_API
    ]
