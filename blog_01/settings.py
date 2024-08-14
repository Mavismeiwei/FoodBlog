"""
Django settings for blog_01 project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

import django.core.cache.backends.locmem

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1-r^$!om1)jxgsegs2qm2ebdcbqe=^uf$7ewj)r&r)+79c_bvr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'api.apps.ApiConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.middleware_decode.Md1',
    'app01.middleware_decode.Statistical'
]

ROOT_URLCONF = 'blog_01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'blog_01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Mysql database configuration
# DATABASES = {
#     "default": {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'blog_2023',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': 3306
#     }
# }

# 云服务器配置
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foodblog',
        'USER': 'foodblog',
        'PASSWORD': 'saAPtLyrSAJEJY6Y',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}

# 配置在线人数缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Create third table
AUTH_USER_MODEL = "app01.UserInfo"

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

# LANGUAGE_CODE = 'zh-hans'
#
# TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# media configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# # 收集项目的静态文件
STATIC_ROOT = os.path.join(BASE_DIR, 'mimi_static')

# user upload files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 默认设置位5M

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Create third table
AUTH_USER_MODEL = "app01.UserInfo"

# 网站信息
SITE_TITLE = "Mimi's Food Blog"
# SITE_BEIAN = '湘ICP备10001000100号'
SITE_INFO = {
    'name': 'Mimi',
    'job': 'FUll Stack Engineer',
    'address': 'Boston, US',
    'link': 'https://mavismeiwei.github.io/meiwei_portfolio/',
    'date': '2023-7-29'  # 建站日期
}

# 发送邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'zhang.meiwei.mavis@gmail.com'
EMAIL_HOST_PASSWORD = 'efpe gqau agtd arhx'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
EMAIL_USER_TLS = False

# 七牛云密钥管理
QINIU_ACCESS_KEY = '-SaDQRkAzpJM74KzkjuvXQX3f0oOYpHZdwyU461o'
QINIU_SECRET_KEY = 'PnUOs1u6OEA_xBISe8BTMLIWLoXDAcAnqPW7gUCm'