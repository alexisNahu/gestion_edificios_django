# core/django_setup.py
import django
import os

def init_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()