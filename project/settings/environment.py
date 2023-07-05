from pathlib import Path
import os
from typing import List


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURITY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: List[str] = []

# DEBUG TOOLBAR
INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'author:login'
