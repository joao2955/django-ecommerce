from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Perfil)
class AdminPerfil(admin.ModelAdmin):
    ...