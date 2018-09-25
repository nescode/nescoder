from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = ['*']

DEBUG = False
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qng*is5n(&q5!^@j7f^fwf9xb_!dzit8xqrt!oe$y=1eowhfvd'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


try:
    from .local_settings import *
except ImportError:
    pass
