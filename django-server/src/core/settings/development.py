from .base import *  # noqa: F403

DEBUG = True

DEV = True

TEST_RUN = False

SECRET_KEY = '*04#mel_b@x9=6*awfl#)m8%n2r_s*oagxfm-+f$jcev2t7!a4'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.goldenequatorconsulting.com']

WSGI_APPLICATION = 'core.wsgi.development.application'

CORS = '*'

CUSTOM_MIDDLEWARE = [
    'core.middleware.CorsMiddleware'
]

MIDDLEWARE = CUSTOM_MIDDLEWARE + MIDDLEWARE  # noqa: F405

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'NAME': 'insights_lite',
        'HOST': '127.0.0.1',
        'PORT': 27017
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

API_AUTH_TOKEN = 'zBeQgQwpGE6Eg3lH9PFSuqW4hCAzg3SV'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static/'))  # noqa: F405, E501
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'media/'))  # noqa: F405, E501
