from .common import *  # noqa

DEBUG = True
SECRET_KEY = 'fake-secret-key-for-test'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'core.tests',
]
