from django.contrib import admin
from . import models

# Register your models here.

# Inlines

class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

# Admin Model

@admin.register(models.Pedido)
class AdminPedido(admin.ModelAdmin):
    inlines = ItemPedidoInline,

@admin.register(models.ItemPedido)
class AdminItemPedido(admin.ModelAdmin):
    ...
