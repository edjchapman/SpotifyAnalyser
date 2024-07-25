from .base_dir import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"  # The URL endpoint for static files.
STATIC_ROOT = BASE_DIR / "staticfiles"  # Location where static files will be collected

STATICFILES_DIRS = [
    BASE_DIR / "static",
]  # Locations where Django will look for additional static files

# Media files (Uploaded by users)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
