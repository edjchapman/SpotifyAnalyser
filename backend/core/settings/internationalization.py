# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

import decouple

TIME_ZONE = "UTC"

LANGUAGE_CODE = decouple.config("LANGUAGE_CODE", default="en-GB")

USE_I18N = True

USE_TZ = True
