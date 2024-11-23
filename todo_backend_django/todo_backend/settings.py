from pathlib import Path
import os  # Provides functions for interacting with the operating system
from datetime import timedelta  # Imports timedelta for setting token expiration times
import environ  # To manage environment variables securely

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Setup environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # Read variables from .env file


# # Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP for sending emails
# EMAIL_HOST = env('EMAIL_HOST')  # Load SMTP host from .env file
# EMAIL_PORT = env.int('EMAIL_PORT')  # Load SMTP port from .env file
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'  # Load TLS setting from .env file
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Load email username from .env file
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # Load email password from .env file
# DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')  # Load default sender email from .env file

# ... existing code ...

# Email Configuration - Development Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'  # This can be any email for development

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-l6_ofy!w%t@r+ef-__@clfmi__agng-l!z^akz^(50+ar$*tcq')

# Configure Django REST Framework and JWT settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWT
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Require authentication by default
    ),
}

# Configure JWT settings
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30000),  # Access token lifespan set to 30 minutes
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token lifespan set to 1 day
#     'AUTH_HEADER_TYPES': ('Bearer',),  # Specifies the 'Bearer' type for authorization headers
# }

SIMPLE_JWT = {
    'TOKEN_OBTAIN_PAIR_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer',
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []  # Add your production domain or IP here when you deploy

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Adds Django REST Framework for building API endpoints
    'users',  # Registers the "users" app
    'todos',  # Registers the "todos" app
    'drf_yasg',        # Add 'drf_yasg' here
    'corsheaders',
    'rest_framework_swagger',       # Swagger 


]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #custom middleware
    'middleware.middleware.RequestLoggingMiddleware',  # Your custom middleware

]

ROOT_URLCONF = 'todo_backend.urls'

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

WSGI_APPLICATION = 'todo_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Specifies MySQL as the database engine
        'NAME': env('DB_NAME', default='django_todo'),  # The name of the MySQL database
        'USER': env('DB_USER', default='root'),  # MySQL database username
        'PASSWORD': env('DB_PASSWORD', default='toor'),  # Password for the MySQL user
        'HOST': env('DB_HOST', default='localhost'),  # Database host (localhost for local development)
        'PORT': env('DB_PORT', default='3306'),  # MySQL's default port number
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Specify the custom user model
AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
