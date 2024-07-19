from django.contrib.messages import constants as messages
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_CONFIG = {
    'USER': os.getenv('SERVER_CONFIG_USER'),
    'PEM_FOLDER_PATH': os.path.join(os.path.dirname(__file__), '..', 'pem'),
}

AUTH_USER_MODEL = 'users.CustomUser'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '34.214.109.145', '192.168.1.23', 'link2globe.com', 'www.link2globe.com']
CSRF_TRUSTED_ORIGINS = ['https://www.link2globe.com', 'https://link2globe.com']

# defined crontab jobs

CRONJOBS = [
    ('* * * * *', 'cluster.tasks.download_and_save2db'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'django_crontab',
    'users',
    'cluster',
    'IP_resource',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware', # Ensure this middleware is at the top or near the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'client.middleware.Custom404Middleware',  # Add your custom middleware here
]

ROOT_URLCONF = 'client.urls'

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

WSGI_APPLICATION = 'client.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us' # 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Define available languages
LANGUAGES = [
    ('en-us', 'English'),
    ('zh-hans', '简体中文'),
    # Add more languages
]

# define translation file location
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# use this static folder for img, js and css, be careful chmod 777 for folder static
# STATIC_ROOT = '/var/www/link2globe.com/static'

# Compressor settings
COMPRESS_ROOT = STATIC_ROOT

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # 如果有其他的静态文件目录，可以继续添加
    # os.path.join(BASE_DIR, "another_static_directory"),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# uncomment to use logger (currently used in crontab jobs)
# log for debug

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'users.tasks': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP 服务器地址
EMAIL_PORT = 587  # SMTP 服务器端口
EMAIL_USE_TLS = True  # 是否使用 TLS 加密
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # SMTP 用户名
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # SMTP 密码
