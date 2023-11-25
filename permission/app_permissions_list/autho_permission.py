

AUTH_API = [
    ("token_obtain_pair", "post"),
    ("token_refresh", "post"),
]


VERIFY_TOKEN_API = [
    ("token_verify", "post"),
]


REVIEWS_READ_ONLY_API = [
    ("reviews-list", "get"),
]


REVIEWS_WRITE_API = [
    ("reviews-list", "post"),
    ("reviews-detail", "put"),
    ("reviews-detail", "patch"),
]
