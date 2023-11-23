

from permission.app_permissions_list.autho_permission import AUTH_API, VERIFY_TOKEN_API


def get_anonymous_permission_map():
    return [
        AUTH_API
    ]


def get_superuser_permission_map():
    return [
        AUTH_API,
        VERIFY_TOKEN_API,
    ]
