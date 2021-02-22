ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.2.35']

ADMINS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Media and static files for deployment
MEDIA_URL = '/arc/media/'
STATIC_URL = '/arc/static/'

SECRET_KEY = 'somethingrandomlygenerateddefinitelynotthis'
EMAIL_HOST = ''
EMAIL_PORT = '465'
EMAIL_HOST_USER = ''
SERVER_EMAIL = 'NISER Archive'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = ''
