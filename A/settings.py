"""
Django settings for A project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--@-g&8hr^w6d8da+c^!#n75hx%sif=6wdxa^e1f1zr&js3qdjb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed apps
    'account.apps.AccountConfig',
    'articles.apps.ArticlesConfig',
    'userPanel_module.apps.UserpanelModuleConfig',
    # third party apps
    'django_celery_beat',
    'storages',
    'django_render_partial',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'A.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
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

WSGI_APPLICATION = 'A.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379',
#     }
# }

# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

# media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = "/account/auth/login/"

# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'ta.guilan.ap@gmail.com'
EMAIL_HOST_USER = 'ta.guilan.ap@gmail.com'
EMAIL_HOST_PASSWORD = 'cxunvvjyuezsfkii'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



# ARVAN CLOUD STORAGE
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = '69733d8a-7e9c-4abd-818f-3ba648482344'
AWS_SECRET_ACCESS_KEY = 'b867f62ca5a8b0768e178d57735582e35ff89b5df7a29db3e4ff3c8701171e54'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.ir'
AWS_STORAGE_BUCKET_NAME = 'django-article'
AWS_SERVICE_NAME = 's3'
AWS_S3_FILE_OVERWRITE = False
AWS_LOCAL_STORAGE = f'{BASE_DIR}/aws/'

# RichText
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'basic',
        'height': 300,
        'width': 1200,
    },
}
