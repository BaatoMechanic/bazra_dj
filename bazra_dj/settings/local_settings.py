ALLOWED_HOSTS = [
    "192.168.1.86",
    "192.168.1.151",
    "192.168.1.83",
    "localhost",
    "127.0.0.1",
    "192.168.49.1",
    "192.168.1.68",
    "192.168.1.71",
    "192.168.1.74",
    "192.168.1.79",
    "192.168.1.81",
    "192.168.100.24",
    "192.168.100.25",
    "192.168.100.74",
    "192.168.101.18",
    "192.168.1.126",
    "100.89.65.72",
    "test.krishna-rimal.com.np",
    "api.krishna-rimal.com.np",
    "debug.krishna-rimal.com.np",
]

CORS_ALLOWED_ORIGINS = ["https://api.krishna-rimal.com.np"]


# For smtp4dev
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "192.168.1.83"
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = "26"

# For gmail
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "your google id"
# EMAIL_HOST_PASSWORD = "your password"
