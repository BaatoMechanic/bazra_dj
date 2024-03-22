VEHICLE_REPAIR_REQUEST_READ_API = [
    ("repair_requests-list", "get"),
    ("repair_requests-detail", "get"),
    ("repair_requests-service-type", "get"),
    ("repair_requests-user-recent-repair-requests", "get"),
    ("repair_requests-user-active-repair-requests", "get"),
]


VEHICLE_REPAIR_REQUEST_WRITE_API = [
    ("repair_requests-list", "post"),
    ("repair_requests-detail", "put"),
    ("repair_requests-detail", "patch"),
    ("repair_requests-detail", "delete"),

]


VEHICLE_REPAIR_REQUEST_IMAGES_READ_API = [
    ("repair_request-images-list", "get"),
    ("repair_request-images-detail", "get"),
]


VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API = [
    ("repair_request-images-list", "post"),
    ("repair_request-images-detail", "put"),
    ("repair_request-images-detail", "patch"),
    ("repair_request-images-detail", "delete"),
]

VEHICLE_REPAIR_REQUEST_REVIEWS_READ_API = [
    ("reviews-list", "get"),
    ("reviews-detail", "get"),
    ("reviews-mechanic-reviews", "get"),
]

VEHICLE_REPAIR_REQUEST_REVIEWS_WRITE_API = [
    ("reviews-list", "post"),
    ("reviews-detail", "put"),
    ("reviews-detail", "patch"),
    ("reviews-detail", "delete"),
]

VEHICLE_REPAIR_REQUEST_VIDEOS_READ_API = [
    ("repair_request-videos-list", "get"),
    ("repair_request-videos-detail", "get"),

]


VEHICLE_REPAIR_REQUEST_VIDEOS_WRITE_API = [
    ("repair_request-videos-list", "post"),
    ("repair_request-videos-detail", "put"),
    ("repair_request-videos-detail", "patch"),
]


SERVICE_READ_API = [
    ("services-list", "get"),
    ("services-detail", "get"),
]

SERVICE_WRITE_API = [
    ("services-list", "post"),
    ("services-detail", "put"),
    ("services-detail", "patch"),

]


VEHICLE_CATEOGRY_READ_API = [
    ("vehicle-categories-list", "get"),
    ("vehicle-categories-detail", "get"),
]

VEHICLE_CATEOGRY_WRITE_API = [
    ("vehicle-categories-list", "post"),
    ("vehicle-categories-detail", "put"),
    ("vehicle-categories-detail", "patch"),
]


REPAIR_STEP_READ_API = [
    ("repair_request-steps-list", "get"),
    ("repair_request-steps-detail", "get"),
]


REPAIR_STEP_WRITE_API = [
    ("repair_request-steps-list", "post"),
    ("repair_request-steps-detail", "put"),
    ("repair_request-steps-detail", "patch"),
]


REPAIR_REQUEST_WEBSOCKET_API = [
    ("websocket-repair-request", "any"),
    ("websocket-mechanic-location", "any"),
]

REPAIR_STEP_WEBSOCKET_API = [
    ("websocket-repair-steps", "any"),
]


CUSTOMER_CREATE_API = [
    ("customers-list", "post"),
]
CUSTOMER_API = [
    ("customers-detail", "get"),
    ("customers-me", "get"),

]


MECHANIC_API = [
    ("mechanics-list", "get"),
    ("mechanics-detail", "get"),
    ("mechanics-recommended-mechanics", "get"),
]
