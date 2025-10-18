from django.contrib import admin
# Register your models here.
from .models import Socios,Planes,Subscripcion,Pago

# Register your models here.
admin.site.register(Socios)
admin.site.register(Planes)
admin.site.register(Subscripcion)
admin.site.register(Pago)


