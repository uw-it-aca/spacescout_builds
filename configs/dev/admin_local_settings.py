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

# Leading portion of the URL representing the location
# the web server is configured to expose in the application's URL
APP_URL_ROOT = '/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8001/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Fields required for space creation
SS_SPACE_CREATION_FIELDS = [
    {
        'name': 'Campus',
        'value': {
            'key': 'extended_info.campus',
            'edit': {
                'tag': 'select'
                }
            }
        },
    {
        'name': 'Space Name',
        'required': True,
        'value': {
            'key': 'name'
            }
        },
    {
        'name': 'Space Type',
        'required': True,
        'help': 'choose_up_to_2',
        'value': {
            'key': 'type',
            'edit': {
                'multi_select': True
                }
            }
        },
    {
        'name': 'Owner',
        'required': True,
        'value': {
            'key': 'manager',
            'edit': {
                'default': '{{ username }}'
                }
            }
    }
]

# Key Used to Describe Spaces
SS_SPACE_DESCRIPTION = 'extended_info.location_description'

# Space Definition
SS_SPACE_DEFINITIONS = [
    {
        'section': 'basic',
        'fields': [
            {
                'name': 'Space Name',
                'help': 'space_name_help',
                'required': True,
                'value': {
                    'key': 'name'
                }
            },
            {
                'name': 'Space Type',
                'required': True,
                'help': 'space_type_help',
                'value': {
                    'key': 'type',
                    'edit': {
                        'multi_select': True,
                        'limit': 2
                    }
                }
            },
            {
                'name': 'Owner',
                'required': True,
                'help': 'owner_help',
                'value': {
                    'key': 'manager'
                }
            },
            {
                'name': 'Editors',
                'help': 'editors_help',
                'value': {
                    'key': 'editors'
                }
            }
        ]
    },
    {
        'section': 'location',
        'fields': [
            {
                'name': 'Campus',
                'value': {
                    'key': 'extended_info.campus',
                    'edit': {
                        'tag': 'select'
                     }
                }
            },
            {
                'name': 'Building',
                'required': True,
                'value': {
                    'key': 'location.building_name'
                }
            },
            {
                'name': 'Floor',
                'help': 'floor_help',
                'value': {
                    'key': 'location.floor'
                }
            },
            {
                'name': 'room_number',
                'help': 'room_number_help',
                'value': {
                    'key': 'location.room_number'
                }
            },
            {
                'name': 'Description',
                'help': 'description_help',
                'required': True,
                'value': {
                    'key': 'extended_info.location_description'
                }
            },
            {
                'name': 'latlong',
                'help': 'latlong_help',
                'required': True,
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
        # hours field managed internally
        'section': 'hours_access',
        'fields': [
            {
                'name': 'Hours Notes',
                'help': 'hours_notes_help',
                'value': {
                    'key': 'extended_info.hours_notes',
                    'edit': {
                        'tag': 'textarea'
                    }
                }
            },
            {
                'name': 'cafe_hours',
                'help': 'cafe_hours_help',
                'value': {
                    'key': 'extended_info.cafe_hours',
                    'edit': {
                        'tag': 'textarea'
                    }
                }
            },
            {
                'name': 'access_notes',
                'help': 'access_notes_help',
                'more_help': 'access_notes_more_help',
                'value': {
                    'key': 'extended_info.access_notes',
                    'edit': {
                        'tag': 'textarea'
                    }
                }
            },
            {
                'name': 'Reservability',
                'help': 'reservability_help',
                'value': {
                    'key': 'extended_info.reservable',
                    'edit': {
                        'default': 0,
                        'requires': 'extended_info.reservation_notes'
                    },
                    'map': {
                        'true': 'canreserve',
                        None: 'cannotreserve',
                        'reservations': 'mustreserve'
                    },
                    'format': '<em>{0}</em>'
                }
            },
            {
                'name': 'Reservation Notes',
                'help': 'reservation_notes_help',
                'more_help': 'reservation_notes_more_help',
                'value': {
                    'key': 'extended_info.reservation_notes',
                    'edit': {
                        'tag': 'textarea'
                    }
                }
            }
        ]
    },
    {
        'section': 'resources',
        'fields': [
            {
                'name': 'Resources',
                "help": "resources_help",
                'value': [
                    {
                        'key': 'extended_info.has_outlets'
                    },
                    {
                        'key': 'extended_info.has_projector'
                    },
                    {
                        'key': 'extended_info.has_displays'
                    },
                    {
                        'key': 'extended_info.has_whiteboards'
                    },
                    {
                        'key': 'extended_info.has_printing'
                    },
                    {
                        'key': 'extended_info.has_scanner'
                    },
                    {
                        'key': 'extended_info.has_computers'
                    }
                ]
            },
            {
                'name': 'Capacity',
                'help': 'capacity_help',
                'value': {
                    'key': 'capacity',
                    'format': 'Seats {0}'

                }
            },
            {
                'name': 'Lighting',
                'value': {
                    'key': 'extended_info.has_natural_light'
                }
            },
            {
                'name': 'noise_level',
                'help': 'noise_level_help',
                'more_help': 'noise_level_more_help',
                'required': True,
                'value': {
                    'key': 'extended_info.noise_level'
                }
            },
            {
                'name': 'food_coffee',
                'help': 'food_coffee_help',
                'value': {
                    'key': 'extended_info.food_nearby',
                    'edit' : {
                        'allow_none': True
                    }
                }
            }
        ]
    },
    {
        # images managed dinternally
        'section': 'images'
    }
]
