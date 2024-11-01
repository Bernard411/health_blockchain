"""
Django settings for health_blockchain project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!sv*i4ax_@0^=a%j*&p_g_a%qxzak2f=a0@cu5m@q9&hd31hlt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core'
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

ROOT_URLCONF = 'health_blockchain.urls'

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

WSGI_APPLICATION = 'health_blockchain.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ 
    BASE_DIR / "static",
    ]

#MEDIA
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

BLOCKCHAIN_PROVIDER_URL = "https://sepolia.infura.io/v3/8dcbb55008924db8ac9f20ad26c64e1e"

CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "patientId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "doctor",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "diagnosis",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "treatment",
                "type": "string"
            }
        ],
        "name": "RecordAdded",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "patientId",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "diagnosis",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "treatment",
                "type": "string"
            }
        ],
        "name": "addRecord",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "patientId",
                "type": "uint256"
            }
        ],
        "name": "getRecord",
        "outputs": [
            {
                "internalType": "address",
                "name": "doctor",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "diagnosis",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "treatment",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "records",
        "outputs": [
            {
                "internalType": "address",
                "name": "doctor",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "diagnosis",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "treatment",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

CONTRACT_ADDRESS = "0x605D25C3dC49AAaEA03C46a7fDc3bA2cebD11aa2"
DOCTOR_PRIVATE_KEY = "2182c82942eb17fe568eac16cc5e9d676ca505487c6d2006784799766cef283b"  # Use a test account's private key for signing transactions

