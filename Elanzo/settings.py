"""
Django settings for Elanzo project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'shop',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'Elanzo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'shop.context_processors.cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'Elanzo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'mallava_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL ='/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL  = 'home'
LOGOUT_REDIRECT_URL = 'home'

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# SSL COMMERZE Payment setup
SSL_COMMERZE_STORE_ID = os.environ.get('SSL_COMMERZE_STORE_ID')
SSL_COMMERZE_STORE_PASSWORD = os.environ.get('SSL_COMMERZE_STORE_PASSWORD')
SSL_COMMERZE_PAYMENT_URL = os.environ.get('SSL_COMMERZE_PAYMENT_URL', 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php')
SSL_COMMERZE_VALIDATION_URL = os.environ.get('SSL_COMMERZE_VALIDATION_URL', 'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php')

# Email setup
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')

UNFOLD = {
    "SITE_TITLE": "Elanzo Admin",
    "SITE_HEADER": "Elanzo Dashboard",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",
    "COLORS": {
        "primary": {
            "50": "#FFF5EC",
            "100": "#FFE8D3",
            "200": "#FFCFA3",
            "300": "#FFB06B",
            "400": "#FF8B32",
            "500": "#ff6a00",  # Matches dashboard primary-color
            "600": "#E65000",
            "700": "#B33E00",
            "800": "#802C00",
            "900": "#521F00",
            "950": "#2E0F00",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Shop Management",
                "separator": True,
                "items": [
                    {
                        "title": "Products",
                        "icon": "inventory_2",
                        "link": "/admin/shop/product/",
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": "/admin/shop/category/",
                    },
                    {
                        "title": "Orders",
                        "icon": "shopping_cart",
                        "link": "/admin/shop/order/",
                    },
                    {
                        "title": "Order Items",
                        "icon": "list_alt",
                        "link": "/admin/shop/orderitem/",
                    },
                    {
                        "title": "Carts",
                        "icon": "shopping_basket",
                        "link": "/admin/shop/cart/",
                    },
                    {
                        "title": "Ratings",
                        "icon": "star_rate",
                        "link": "/admin/shop/rating/",
                    },
                ],
            },
            {
                "title": "Access & Authentication",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": "/admin/auth/user/",
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": "/admin/auth/group/",
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "shop.product",
                "shop.category",
            ],
            "items": [
                {
                    "title": "Products",
                    "link": "/admin/shop/product/",
                },
                {
                    "title": "Categories",
                    "link": "/admin/shop/category/",
                },
            ],
        },
    ],
    "DASHBOARD": {
        "navigation": [
            {
                "title": "Shop Analytics",
                "link": "/admin/",
                "icon": "dashboard",
            },
        ],
        # Kept commented to prevent crashes until the view is actually created
        # "widgets": [
        #     {
        #         "view": "admin.views.TotalOrdersWidget",
        #         "title": "Total Orders",
        #     },
        # ],
    },
}