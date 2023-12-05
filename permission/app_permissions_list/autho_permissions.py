

AUTH_API = [
    ("token_obtain_pair", "post"),
    ("token_refresh", "post"),
]


VERIFY_TOKEN_API = [
    ("token_verify", "post"),
]


USER_API = [
    ("users_info-me", "get"),
]


REGISTER_API = [
    ("users_management-register", "post"),
]
USER_DELETE_API = [
    ("users_management-delete-user", "delete"),
]


REVIEWS_READ_ONLY_API = [
    ("reviews-list", "get"),
    ("reviews-mechanic-reviews", "get"),
]


REVIEWS_WRITE_API = [
    ("reviews-list", "post"),
    ("reviews-detail", "put"),
    ("reviews-detail", "patch"),
]
