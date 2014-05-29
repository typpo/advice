# Django settings for advice project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('ian', 'ianw_advice@ianww.com'),
)

# Link Profile model with User auth
AUTH_PROFILE_MODULE = 'notes.Profile'

# URL to login
LOGIN_URL = '/notes/login/'
LOGIN_REDIRECT_URL = '/notes/'

# Error string for template extras
TEMPLATE_STRING_IF_INVALID = 'ERROR'

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/home/ian/projects/advice/sql.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/ian/projects/advice/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/notes/static/'

# tinymce editor
TINYMCE_DEFAULT_CONFIG = {
    'theme' : 'advanced',
    'theme_advanced_buttons1' : 'bold,italic,underline,|,formatselect,|,blockquote,link,unlink,|,undo,redo',

    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3': '',
    'theme_advanced_buttons4': '',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align' : 'left',
}

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3tkyc76m3bk27g=p=c93zw5p1il#)+p@u7f^0)=@2ou6tsrty+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'advice.urls'

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    '/home/ian/projects/advice/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'notes'
)

TEMPLATE_CONTEXT_PROCESSORS = (
"django.core.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
)
#"django.core.context_processors.static",
#"django.contrib.messages.context_processors.messages"
