# Django settings for server_proj project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

FEEDBACK_EMAIL_RECIPIENT = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'web.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SS_WEB_SERVER_HOST = 'http://127.0.0.1:8000'
# Run ./manage.py create_consumer on the server and copy the key and secret below. You'll also need to go into the admin and make the oauth client "Trusted."
SS_WEB_OAUTH_KEY = ''
SS_WEB_OAUTH_SECRET = ''

DEFAULT_CENTER_LATITUDE = '47.655003'
DEFAULT_CENTER_LONGITUDE = '-122.306864'
DEFAULT_ZOOM_LEVEL = '15'

# Disable django compressor
COMPRESS_ENABLED = False
COMPRESS_PRECOMPILERS = ()

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'spacescout-web'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''
