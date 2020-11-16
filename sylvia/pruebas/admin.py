from django.contrib import admin
from registro.models import InstitucionModel,UsuarioModel
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UsuarioModelAdmin(admin.StackedInline):
    model=UsuarioModel
    can_delete = False
    verbose_name_plural = 'usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioModelAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
