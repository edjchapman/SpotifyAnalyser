DJANGO_BUILTIN_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_APPS = ["accounts"]

INSTALLED_APPS = DJANGO_BUILTIN_APPS + CUSTOM_APPS
