"""
Django settings for mylittlefacewhen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import secrets
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ("62.78.185.109")

ALLOWED_HOSTS = ["mlfw.info", "mylittlefacewhen.com", "www.mlfw.info", "www.mylittlefacewhen.com"]

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/cache-manifest", ".appcache", True)
    mimetypes.add_type("image/webp", ".webp", True)

ADMINS = (
    ('Taivastiuku', 'taivastiuku@mylittlefacewhen.com'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'registration',
    'tagging',
    'viewer',
    'resizor',
)

MIDDLEWARE_CLASSES = (
    'viewer.middleware.RedirectDomain',
    'viewer.middleware.RedirectIE9',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'viewer.middleware.NoCache',
    'viewer.middleware.AllowPieforkMiddleware',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'viewer.templatetags.mustache.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    os.path.join(BASE_DIR, "static/mustache"),
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
ROOT_URLCONF = 'mylittlefacewhen.urls'

WSGI_APPLICATION = 'mylittlefacewhen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

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

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = False

USE_L10N = False

USE_TZ = True

FILE_UPLOAD_PERMISSIONS = 0644

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
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
        },
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'INFO',  # message level to be written to console
        }

    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
            # this tells logger to send logging message
            # to its parent (will send if set to True)
        },
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
