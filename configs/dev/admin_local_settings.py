# Django settings for ssadmin project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'admin.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SS_WEB_SERVER_HOST = 'http://127.0.0.1:8000'
SS_WEB_OAUTH_KEY = ''
SS_WEB_OAUTH_SECRET = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8001/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Space Definition
SS_SPACE_DEFINITIONS = [
    {
        'section': 'location',
        'fields': [
            {
                'name': 'Campus',
                'value': {
                    'key': 'extended_info.campus'
                }
            },
            {
                'name': 'Building',
                'value': {
                    'key': 'location.building_name'
                }
            },
            {
                'name': 'Description',
                'value': {
                    'key': 'extended_info.location_description'
                }
            },
            {
                'name': 'Orientation',
                'value': {
                    'key': 'extended_info.orientation'
                }
            },
            {
                'name': 'Lat & Long',
                'value': [
                    {
                        'key': 'location.latitude'
                    },
                    {
                        'key': 'location.longitude'
                    }
                ]
            }
        ]
    },
    {
        'section': 'hours',
        'fields': [
            {
                'name': 'Notes',
                'value': {
                    'key': 'extended_info.hours_notes'
                }
            },
            {
                'name': 'Cafe Hours',
                'value': {
                    'key': 'extended_info.cafe_hours'
                }
            }
        ]
    },
    {
        'section': 'access',
        'fields': [
            {
                'name': 'Access Notes',
                'value': {
                    'key': 'extended_info.access_notes'
                }
            },
            {
                'name': 'Reservability',
                'value': {
                    'key': 'extended_info.reservable',
                    'map': {
                        'true': 'canreserve',
                        'reservations': 'mustreserve'
                    },
                    'format': '<em>%s</em>'
                }
            },
            {
                'value': {
                    'key': 'extended_info.reservation_notes'
                }
            }
        ]
    },
    {
        'section': 'resources & environment',
        'fields': [
            {
                'name': 'Resources',
                'value': [
                    {
                        'key': 'extended_info.has_outlets',
                        'boolean': {
                            'true': 'outlets'
                        }
                    },
                    {
                        'key': 'extended_info.has_projector',
                        'boolean': {
                            'true': 'projector'
                        }
                    },
                    {
                        'key': 'extended_info.has_displays',
                        'boolean': {
                            'true': 'displays'
                        }
                    },
                    {
                        'key': 'extended_info.has_whiteboards',
                        'boolean': {
                            'true': 'whiteboards'
                        }
                    },
                    {
                        'key': 'extended_info.has_printing',
                        'boolean': {
                            'true': 'printing'
                        }
                    },
                    {
                        'key': 'extended_info.has_scanner',
                        'boolean': {
                            'true': 'scanner'
                        }
                    },
                    {
                        'key': 'extended_info.has_computers',
                        'boolean': {
                            'true': 'computers'
                        }
                    }
                ]
            },
            {
                'name': 'Capacity',
                'value': {
                    'key': 'capacity',
                    'format': 'Seats %s'
                }
            },
            {
                'name': 'Lighting',
                'value': {
                    'key': 'extended_info.has_natural_light',
                    'boolean': {
                        'true': 'natural',
                        'false': 'unnatural'
                    }
                }
            },
            {
                'name': 'Noise Level',
                'value': {
                    'key': 'extended_info.noise_level'
                }
            },
            {
                'name': 'Food & Coffee',
                'value': {
                    'key': 'extended_info.food_nearby'
                }
            }
        ]
    },
    {
        'section': 'images'
    }
]
