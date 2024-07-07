import decouple

DEBUG = decouple.config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG
