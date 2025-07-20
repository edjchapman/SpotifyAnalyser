CELERY_BROKER_URL = decouple.config("CELERY_BROKER", "redis://redis:6379")
CELERY_RESULT_BACKEND = decouple.config("CELERY_BROKER", "redis://redis:6379")
CELERY_CACHE_BACKEND = decouple.config("CELERY_BROKER", "redis://redis:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/London"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
