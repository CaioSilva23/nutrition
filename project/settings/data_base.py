from .environment import BASE_DIR

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'meu_db',
#         'USER': 'postgres',
#         'PASSWORD': '1010',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }