import decouple

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": decouple.config("POSTGRES_DB"),
        "USER": decouple.config("POSTGRES_USER"),
        "PASSWORD": decouple.config("POSTGRES_PASSWORD"),
        "HOST": decouple.config("POSTGRES_DB_HOST"),
        "PORT": decouple.config("POSTGRES_DB_PORT", cast=int),
    }
}
