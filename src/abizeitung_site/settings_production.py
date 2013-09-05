from abizeitung_site.settings import *

USER_PASSWORD_SECRET = "Sonne2013"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql", # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "NAME": "abizeitung",                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        "USER": "abizeitung",
        "PASSWORD": "",
        "HOST": "localhost",                      # Empty for localhost through domain sockets or "127.0.0.1" for localhost through TCP.
        "PORT": "",                      # Set to empty string for default.
    }
}

SECRET_KEY = "42"