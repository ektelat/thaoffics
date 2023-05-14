import datetime
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0y$eg3c9$lb2h3yd&^n_novbkz-*u5byrw-9fy93@5w3s(lzi+'
ROOT_URLCONF = 'thaoffics.urls'
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'storages',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thaoffics.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thioffices',
        'USER': 'admin',
        'PASSWORD': 'Prada1945',
        'HOST': 'thioffices.cl6lviu7mlw3.eu-central-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}

# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # other settings...
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=120),
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


AUTH_USER_MODEL = 'users.User'

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = [
    'http://10.29.158.66:4200',
    'http://localhost:4200',
    'http://197.230.122.195:4200',
    'https://thioffices-front.herokuapp.com',
    'http://www.thaoffices.com',
    'http://www.thaoffices.com',
    'https://thioffices.herokuapp.com'
]

CORS_ALLOWED_ORIGINS = [
    'http://10.29.158.66:4200',
    'http://localhost:4200',
    'http://197.230.122.195:4200',
    'https://thioffices-front.herokuapp.com',
    'http://www.thaoffices.com',
    'http://www.thaoffices.com',
    'https://thioffices.herokuapp.com'
]

CSRF_TRUSTED_ORIGINS = [
    'http://10.29.158.66:4200',
    'http://localhost:4200',
    'http://197.230.122.195:4200',
    'https://thioffices-front.herokuapp.com',
    'http://www.thaoffices.com',
    'http://www.thaoffices.com',
    'https://thioffices.herokuapp.com'
]

TWILIO_ACCOUNT_SID = "AC1798c23655ffb0b74287e43740d5a0ad"
TWILIO_AUTH_TOKEN = "8f1269d199eb0af73459c5a13e002be7"
PHONE_VERIFY_CODE_LENGTH = 6
PHONE_VERIFY_CODE_EXPIRATION = 180  # 3 minutes
PHONE_VERIFY_SENDER = 'Thioffices'
TWILIO_FROM_NUMBER = '+972526936250'
PHONE_VERIFY_MESSAGE = 'verification code is {code}'

PHONE_VERIFY_BACKEND = 'phone_verify.backends.twilio.TwilioBackend'
PHONE_VERIFY_BACKEND_KWARGS = {
    'twilio_account_sid': TWILIO_ACCOUNT_SID,
    'twilio_auth_token': TWILIO_AUTH_TOKEN,
    'twilio_from_number': TWILIO_FROM_NUMBER,
    'message': PHONE_VERIFY_MESSAGE,
}

PHONE_VERIFICATION = {'PHONE_FIELD': 'phone'}

FRONTEND_URL = "http://localhost:4200"

STATIC_ROOT = 'templates'

APP_ID = "721384089772532",
APP_SECRET = "ce3622cfbd68e8199aacf31fe7d52933",
VERSION = "v13.0",
PHONE_NUMBER_ID = "<<YOUR-WHATSAPP-BUSINESS-PHONE-NUMBER-ID>>",
ACCESS_TOKEN = "fca3320c25392e5c6ecaf7e59722b5ce"
## AWS Config

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_ACCESS_KEY_ID = 'AKIA5EM7VLRZ7IZ47NZG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'thaoffices'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_OBJECT_PARAMETERS = {
    'ACL': 'public-read',
}
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_LOCATION = 'static'
AWS_MEDIA = 'media'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL='https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN,AWS_MEDIA )
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
