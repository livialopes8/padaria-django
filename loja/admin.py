from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido


class ItemInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel')
    list_filter = ('categoria', 'disponivel')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo', 'status', 'total', 'criado_em')
    list_editable = ('status',)
    inlines = [ItemInline]


admin.site.register(Categoria)
