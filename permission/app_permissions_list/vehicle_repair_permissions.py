

VEHICLE_REPAIR_REQUEST_READ_API = [
    ("repair_requests-list", "get"),
    ("repair_requests-detail", "get"),
]


VEHICLE_REPAIR_REQUEST_WRITE_API = [
    ("repair_requests-list", "post"),
    ("repair_requests-detail", "put"),
    ("repair_requests-detail", "patch"),
]


VEHICLE_REPAIR_REQUEST_IMAGES_READ_API = [
    ("repair_request-images-list", "get"),
    ("repair_request-images-detail", "get"),
]


VEHICLE_REPAIR_REQUEST_IMAGES_WRITE_API = [
    ("repair_request-images-list", "post"),
    ("repair_request-images-detail", "put"),
    ("repair_request-images-detail", "patch"),
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


REPAIR_STEP_READ_API = [
    ("repair_request-steps-list", "get"),
    ("repair_request-steps-detail", "get"),
]


REPAIR_STEP_WRITE_API = [
    ("repair_request-steps-list", "post"),
    ("repair_request-steps-detail", "put"),
    ("repair_request-steps-detail", "patch"),
]
