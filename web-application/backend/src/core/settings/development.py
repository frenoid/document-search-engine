from .base import *  # noqa: F403
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7*g1)uklkaxcagq68_@^#y3ig0w-m($eyowtw)nb1-5p8^(hao'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEV = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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
# APPEND_SLASH = False
LOGOUT_ON_PASSWORD_CHANGE = ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static resource settings
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static/'))  # noqa: F405, E501
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'media/'))  # noqa: F405, E501
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]