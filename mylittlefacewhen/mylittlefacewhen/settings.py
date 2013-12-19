import secrets

#fabric will set DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PISTON_DISPLAY_ERRORS = DEBUG

INTERNAL_IPS = ("192.168.56.1"
                "192.168.56.10")

ALLOWED_HOSTS = ["mlfw.info", "mylittlefacewhen.com"]

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/cache-manifest", ".appcache", True)
    mimetypes.add_type("image/webp", ".webp", True)

ADMINS = (
    ('Taivastiuku', 'taivastiuku@mylittlefacewhen.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets.DB_CONF["dbname"],
        'USER': secrets.DB_CONF["username"],
        'PASSWORD': secrets.DB_CONF["password"],
        'HOST': secrets.DB_CONF["host"],
        'PORT': secrets.DB_CONF["port"],
    }
}
DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
)


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
#USE_I18N = True
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
#USE_L10N = True
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/inopia/webapps/mlfw_media/'

# upload
FILE_UPLOAD_PERMISSIONS = 0644

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/inopia/webapps/static_root/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/media/admin/'

# Additional locations of static files
if DEBUG:
    STATICFILES_DIRS = (
        '/home/inopia/webapps/mylittlefacewhen/mylittlefacewhen/static/',
    )
else:
    STATICFILES_DIRS = (
        '/home/inopia/webapps/mlfw_static/',
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = secrets.SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'viewer.templatetags.mustache.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'viewer.middleware.RedirectDomain',
    'viewer.middleware.RedirectIE9',
    #'viewer.middleware.SpacelessHTML',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'viewer.middleware.ContentTypeMiddleware',
    'viewer.middleware.NoCache',
    'viewer.middleware.AllowPieforkMiddleware',
    #'viewer.middleware.DetectWebp',
    #'viewer.middleware.DetectMobile',
    #'viewer.middleware.Style',
    #'viewer.middleware.AppCache',
)

ROOT_URLCONF = 'mylittlefacewhen.urls'

TEMPLATE_DIRS = (
    "/home/inopia/webapps/mylittlefacewhen/mylittlefacewhen/templates",
    "/home/inopia/webapps/mylittlefacewhen/mylittlefacewhen/static/mustache",
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    "registration",
    "tagging",
    "south",
    # "devserver",
    "viewer",
    "resizor",
)

DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
    #'devserver.modules.profile.MemoryUseModule',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

FORCE_LOWERCASE_TAGS = True

LOGIN_URL = "/accounts/login/"
ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = secrets.EMAIL_CONF["username"]
EMAIL_HOST_PASSWORD = secrets.EMAIL_CONF["password"]
DEFAULT_FROM_EMAIL = 'server@mylittlefacewhen.com'
SERVER_EMAIL = 'server@mylittlefacewhen.com'
