AUTH_API = [
    ("token_obtain_pair", "post"),
    ("token_refresh", "post"),
]


VERIFY_TOKEN_API = [
    ("token_verify", "post"),
]


RECOVERY_API = [
    ("account_recovery-send-otp-uid", "post"),
    ("account_recovery-send-otp-password", "post"),
    ("account_recovery-resend", "post"),
    ("account_recovery-verify-otp", "post"),
    ("account_recovery-check-otp", "post"),
]

VERIFICATION_API = [
    ("account_verification-send-otp-uid", "post"),
    ("account_verification-resend", "post"),
    ("account_verification-verify-otp", "post"),
    ("account_verification-verify-account-otp", "post"),
    ("account_verification-check-otp", "post"),
]

FCM_DEVICE_REGISTER_API = [
    ("fcmdevice-list", "post"),
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
IDENTIFIER_VERIFICATION_TOKEN_API = [
    ("users_management-identifier-verification-token", "post"),
    ("users_management-verify-identifier", "post"),
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
