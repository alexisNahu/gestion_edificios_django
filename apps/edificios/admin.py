from django.contrib import admin

from apps.edificios.models import Edificios, Departamentos

# Register your models here.

admin.site.register(Edificios)
admin.site.register(Departamentos)