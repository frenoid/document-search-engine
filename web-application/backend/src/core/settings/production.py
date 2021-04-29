from .base import *  # noqa: F403

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd6u*wn$6wj6x$4--!hvw1t5(xv(*1*=))3fd71@q^-p4$09f+0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEV = False

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'prod_wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# change to rds
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'document_search'),
        'USER': os.environ.get('POSTGRES_USER', 'document_search_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Django rest all auth account configuration
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 500
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
REST_USE_JWT = True
APPEND_SLASH = False
LOGOUT_ON_PASSWORD_CHANGE = ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# LinkedIn login settings
LINKENDIN_REDIRECT_URL = ''

# AWS Settings settings
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = 'XSeyM/'
AWS_STORAGE_BUCKET_NAME = 'document_search'
AWS_GROUP_NAME = "document_search"
AWS_USERNAME = "document_search"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'media/'), ]  # noqa: F405
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static/'))  # noqa: F405, E501
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'media/'))  # noqa: F405, E501
