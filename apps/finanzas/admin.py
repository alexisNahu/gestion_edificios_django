from django.contrib import admin

from apps.finanzas.models import Pagos, Abonos

# Register your models here.

admin.site.register(Pagos)
admin.site.register(Abonos)