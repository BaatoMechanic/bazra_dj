

from permission.app_permissions_list.autho_permission import (
    AUTH_API,
    REVIEWS_READ_ONLY_API,
    REVIEWS_WRITE_API,
    VERIFY_TOKEN_API
)


def get_anonymous_permission_map():
    return [
        AUTH_API
    ]


def get_superuser_permission_map():
    return [
        AUTH_API,
        VERIFY_TOKEN_API,
        REVIEWS_READ_ONLY_API,
        REVIEWS_WRITE_API,

    ]


def get_consumer_permission_map():
    return [
        AUTH_API,
        REVIEWS_READ_ONLY_API,
        REVIEWS_WRITE_API
    ]


def get_mechanic_permission_map():
    return [
        AUTH_API,
        REVIEWS_READ_ONLY_API,
    ]
