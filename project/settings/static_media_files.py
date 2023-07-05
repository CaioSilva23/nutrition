
import os
from .environment import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC
# URL STATIC FILES
STATIC_URL = '/static/'

# DIRS DE STATIC FILES
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)

# DIRS STATIC FILES EM PRODUTÇÃO // run of collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA
# DIRS MEDIA FILES
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL MEDIA FILES
MEDIA_URL = '/media/'