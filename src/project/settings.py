import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Secrets!

SECRET_KEY = str(os.getenv('SECRET_KEY'))
DATABASE_SECRET = str(os.getenv('DATABASE_SECRET'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_SECRET'))
KAMAR_KEY = str(os.getenv('KAMAR_KEY'))
KAMAR_SECRET = str(os.getenv('KAMAR_SECRET'))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'studyport.co',
    'connect.studyport.co',
]

LOGIN_URL = "usermgmt:login"


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = ""


# Notifications
DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True}


# Application definition

LOCAL_APPS = [
    'connect',
    'dashboard',
    'insight',
    'ncea',
    'docs',
    # Ordered by migration order
    'verification',
    'settings',
    'standards',
    'group',
    'usermgmt',
    'focus',
    'playground',
    'stats',
    'results',
    'goal',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'background_task',
    'colorfield',
    'django_hosts',
    'django_feather',
    'notifications',

    # OAuth settings
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'csp.middleware.CSPMiddleware',
]


# Security Options

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# Becareful with options below!

SECURE_HSTS_SECONDS = 15768000 # 6 month
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Content Security Policy

CSP_DEFAULT_SRC = ("'self'",)

CSP_CONNECT_SRC = (
    "translate.googleapis.com",
)

CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "cdnjs.cloudflare.com",
    "p.typekit.net",
    "use.typekit.net",
    "fonts.adobe.com",
    "translate.google.com",
    "translate.googleapis.com",
)

CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "cdn.jsdelivr.net",
    "translate.google.com",
    "translate.googleapis.com",
    "translate-pa.googleapis.com",
    "gstatic.com",
)

CSP_IMG_SRC = (
    "'self'",
    "blob:",
    "www.google.com",
    "translate.google.com",
    "translate.googleapis.com",
    "translate-pa.googleapis.com",
    "www.gstatic.com",
)

CSP_FONT_SRC = (
    "'self'",
    "use.typekit.net",
    "fonts.adobe.com",
)


# Templates and URLs

ROOT_URLCONF = 'project.urls'
ROOT_HOSTCONF = 'project.hosts'
DEFAULT_HOST = 'none'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "project/templates")],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Logging
# https://docs.djangoproject.com/en/dev/howto/logging/

LOGGING_ROOT = os.path.join(BASE_DIR.parent.parent, 'logs/')
if not os.path.exists(LOGGING_ROOT):
    os.mkdir(LOGGING_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} line {lineno} | {message}',
            'datefmt': "%b %d/%m/%Y %H:%M:%S",
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {name} | {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'app_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'app.log'),
            'formatter': 'verbose',
            'when': 'D',
            'interval': 1,
        },
        'django_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose',
            'when': 'D',
            'interval': 1,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

for app in LOCAL_APPS:
    LOGGING["loggers"][app] = {
        'handlers': ['console', 'app_file'],
        'level': 'WARNING',
        'propagate': True,
    }


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql', # <-- UPDATED line 
        'NAME'    : 'studyport',                 # <-- UPDATED line 
        'USER'    : 'dev',                     # <-- UPDATED line
        'PASSWORD': DATABASE_SECRET,              # <-- UPDATED line
        'HOST'    : 'localhost',                # <-- UPDATED line
        'PORT'    : '3306',
        # https://stackoverflow.com/questions/63141740/django-db-utils-operationalerror-1366-incorrect-string-value-django-mysql
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'usermgmt.backends.EmailBackend',
]


SITE_ID = 1
LOGIN_REDIRECT_URL = '/user/login'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET= True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'email',
            'profile',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent.parent, "storage/static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "project/static")
]


# # Media files
# # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, 'storage/media')


# Kamar cache files

KAMAR_CACHE_ROOT = os.path.join(BASE_DIR.parent.parent, 'storage/kamar_cache')



