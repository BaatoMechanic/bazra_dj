AUTH_API = [
    ("token_obtain_pair", "post"),
    ("token_refresh", "post"),
]


VERIFY_TOKEN_API = [
    ("token_verify", "post"),
]


RECOVERY_API = [
    ("account_recovery-send-otp", "post"),
    ("account_recovery-resend", "post"),
    ("account_recovery-verify-otp", "post"),
]


USER_API = [
    ("user_info-me", "get"),
    ("user_info-location", "get"),
    ("user_info-me", "patch"),
]

USER_PUBLIC_API = [
    ("user_info-detail", "get"),
]


REGISTER_API = [
    ("users_management-register", "post"),
]
USER_DELETE_API = [
    ("users_management-delete-user", "delete"),
]

USER_UPDATE_LOCATION_API = [
    ("users_management-update-location", "post"),
]

USER_CHANGE_PASSWORD_API = [
    ("users_management-change-password", "post"),
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
