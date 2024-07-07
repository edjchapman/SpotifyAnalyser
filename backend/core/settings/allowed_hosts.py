import decouple

ALLOWED_HOSTS = decouple.config("ALLOWED_HOSTS", default="localhost", cast=decouple.Csv())
