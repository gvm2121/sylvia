from django.contrib import admin
from .models import UsuarioModel

class UsuarioModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(UsuarioModel, UsuarioModelAdmin)

