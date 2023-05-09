import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "tests"
]

DATABASES = { "default": {'ENGINE': 'django.db.backends.sqlite3',  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),}}

DJANGO_TEST_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
