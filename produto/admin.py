from django.contrib import admin
from . import models

# Register your models here.

# Inlines
class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

# Admin Model

@admin.register(models.Produto)
class AdminProduto(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promo_formatado']
    inlines = [VariacaoInline,]

@admin.register(models.Variacao)
class AdminVariacao(admin.ModelAdmin):
    ...