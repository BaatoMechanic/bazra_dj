

AUTH_API = [
    ("token_obtain_pair", "post"),
    ("token_refresh", "post"),
]


VERIFY_TOKEN_API = [
    ("token_verify", "post"),
]


USER_API = [
    ("user_info-me", "get"),
    ("user_info-location", "get")
]

USER_PUBLIC_API = [

    ("user_info-detail", "get"),

]

MECHANIC_PUBLIC_API = [
    ("user_info-recommended-mechanics", "get")
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


MECHANIC_TIPS_READ_API = [
    ("mechanic_tips-list", "get"),
    ("mechanic_tips-detail", "get"),
]

MECHANIC_TIPS_WRITE_API = [
    ("mechanic_tips-list", "post"),
    ("mechanic_tips-detail", "put"),
    ("mechanic_tips-detail", "patch"),
]
