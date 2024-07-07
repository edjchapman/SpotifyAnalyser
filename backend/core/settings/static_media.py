from .base_dir import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"  # Location static files are collected from.

# Media files (Uploaded by users)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
