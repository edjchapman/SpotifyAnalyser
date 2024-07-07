import decouple


EMAIL_HOST = decouple.config("EMAIL_HOST", default="localhost")
EMAIL_PORT = decouple.config("EMAIL_PORT", default=25, cast=int)
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER", default="")
EMAIL_USE_TLS = decouple.config("EMAIL_USE_TLS", default=False, cast=bool)
