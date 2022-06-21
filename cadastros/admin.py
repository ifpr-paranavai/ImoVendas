from django.contrib import admin

from .models import Cidade, Estado, Imovel, Tipo

# Register your models here.
admin.site.register(Imovel)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Tipo)