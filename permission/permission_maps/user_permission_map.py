from permission.app_permissions_list.autho_permissions import (
    AUTH_API,
    MECHANIC_TIPS_READ_API,
    MECHANIC_TIPS_WRITE_API,
    RECOVERY_API,
    REGISTER_API,
    USER_API,
    USER_CHANGE_PASSWORD_API,
    USER_PUBLIC_API,
    USER_UPDATE_LOCATION_API,
    VERIFY_TOKEN_API,
    USER_DELETE_API,
)
from permission.app_permissions_list.gis_permissions import GIS_API
from permission.app_permissions_list.vehicle_repair_permissions import (
    CUSTOMER_API,
    CUSTOMER_CREATE_API,
    MECHANIC_API,
    REPAIR_REQUEST_WEBSOCKET_API,
    REPAIR_STEP_WEBSOCKET_API,
    REPAIR_STEP_READ_API,
    REPAIR_STEP_WRITE_API,
    SERVICE_READ_API,
    SERVICE_WRITE_API,
    VEHICLE_CATEOGRY_READ_API,
    VEHICLE_CATEOGRY_WRITE_API,
    VEHICLE_REPAIR_REQUEST_IMAGES_READ_API,
    VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API,
    VEHICLE_REPAIR_REQUEST_READ_API,
    VEHICLE_REPAIR_REQUEST_REVIEWS_READ_API,
    VEHICLE_REPAIR_REQUEST_REVIEWS_WRITE_API,
    VEHICLE_REPAIR_REQUEST_VIDEOS_READ_API,
    VEHICLE_REPAIR_REQUEST_VIDEOS_WRITE_API,
    VEHICLE_REPAIR_REQUEST_WRITE_API,
)


def get_general_permission_map():
    return [
        RECOVERY_API,
        MECHANIC_API,
        CUSTOMER_API,
        SERVICE_READ_API,
        VEHICLE_REPAIR_REQUEST_REVIEWS_READ_API,
    ]


def get_anonymous_permission_map():
    return get_general_permission_map() + [
        AUTH_API,
        REGISTER_API,
        MECHANIC_TIPS_READ_API,
        REPAIR_REQUEST_WEBSOCKET_API,
        REPAIR_STEP_WEBSOCKET_API,
        GIS_API,
    ]


def get_unverified_permission_map():
    return (
        get_general_permission_map()
        + get_anonymous_permission_map()
        + [
            USER_API,
            USER_DELETE_API,
            VEHICLE_REPAIR_REQUEST_READ_API,
            CUSTOMER_CREATE_API,
            USER_CHANGE_PASSWORD_API,
        ]
    )


def get_superuser_permission_map():
    return get_general_permission_map() + [
        AUTH_API,
        VERIFY_TOKEN_API,
        VEHICLE_REPAIR_REQUEST_READ_API,
        VEHICLE_REPAIR_REQUEST_WRITE_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_READ_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_READ_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_WRITE_API,
        USER_API,
        USER_PUBLIC_API,
        SERVICE_WRITE_API,
        MECHANIC_TIPS_READ_API,
        MECHANIC_TIPS_WRITE_API,
        VEHICLE_CATEOGRY_READ_API,
        VEHICLE_CATEOGRY_WRITE_API,
    ]


def get_consumer_permission_map():
    return get_general_permission_map() + [
        AUTH_API,
        VEHICLE_REPAIR_REQUEST_READ_API,
        VEHICLE_REPAIR_REQUEST_WRITE_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_READ_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_READ_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_WRITE_API,
        USER_API,
        USER_PUBLIC_API,
        USER_DELETE_API,
        MECHANIC_TIPS_READ_API,
        REPAIR_STEP_READ_API,
        REPAIR_STEP_WRITE_API,
        VEHICLE_CATEOGRY_READ_API,
        USER_UPDATE_LOCATION_API,
        VEHICLE_REPAIR_REQUEST_REVIEWS_WRITE_API,
        USER_CHANGE_PASSWORD_API,
    ]


def get_mechanic_permission_map():
    return get_general_permission_map() + [
        AUTH_API,
        VEHICLE_REPAIR_REQUEST_READ_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_READ_API,
        VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_READ_API,
        VEHICLE_REPAIR_REQUEST_VIDEOS_WRITE_API,
        USER_API,
        VEHICLE_CATEOGRY_READ_API,
    ]
