from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os
import sys
import dj_database_url
from google.oauth2 import service_account

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRETKEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

ALLOWED_HOSTS = ["159.203.181.125","needer.com.co"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'captcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'tinymce',
    'needer',
    'users',
    'main',
    'social',
    'chat',
    'channels',
    
]

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

]



ROOT_URLCONF = 'needer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

FIXTURE_DIRS = [os.path.join(BASE_DIR, "fixtures")]

ASGI_APPLICATION = 'needer.asgi.application'


if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }


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

AUTH_USER_MODEL = 'users.User'


LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = False

STATIC_URL = 'static/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}





# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Captcha:

RECAPTCHA_PRIVATE_KEY = os.environ["RE_CAPTCHA_SECRET"]
RECAPTCHA_PUBLIC_KEY = os.environ["RE_CAPTCHA_PUBLIC"]

# MEDIA FILES

MEDIA_ROOT =  os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg", 'PNG': ".png"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


# ALLAUTH SETTINGS:


SOCIALACCOUNT_FORMS = {'signup': 'users.forms.SocialCustomForm'}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
            'secret': os.environ['GOOGLE_OAUTH_PASSWORD'],
            'key': ''
        }
    }
}

# Redirects

LOGOUT_REDIRECT_URL = 'home-view'

# Account options

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL='account_login'

SOCIALACCOUNT_ADAPTER = "users.adapter.SocialAccountAdapter"
LANGUAGE_CODE = 'es'



# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
# TODO ARREGLAR EL SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = os.environ['GMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['GMAIL_PASSWORD'] 
EMAIL_USE_SSL = False



TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "menubar": False,
    "resize":False,
    "height": 500,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,noneditable,media,table,paste,"
    "emoticons,code,help,wordcount code",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor emoticons| link | alignleft aligncenter "
    "outdent indent"
}


""" Cuando se realice el despliegue se usara el CDN """
if DEBUG is True:
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        
    ]
else:
    STATIC_ROOT = BASE_DIR / "static"

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR,"credentials.json"))  
    GOOGLE_APPLICATION_CREDENTIALS = '/path/service-account.json'
    ## STATIC FILES ##  

    STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder', 
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', 
    )   
    

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'needer'

    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

