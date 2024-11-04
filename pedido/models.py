from django.db import models
from django.contrib.auth.models import User

"""
        ItemPedido:
            pedido - FK pedido
            produto - Char
            produto_id - Int
            variacao - Char
            variacao_id - Int
            preco - Float
            preco_promocional - Float
            quantidade - Int
            imagem - Char
"""


# Create your models here.
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,
                              default='C',
                              choices=(
                                    ('A', 'Aprovado'),
                                    ('C', 'Criado'),
                                    ('R', 'Reprovado'),
                                    ('P', 'Pendente'),
                                    ('E', 'Enviado'),
                                    ('F', 'Finalizado'),
                                    )
                                    )
    
    def __str__(self) -> str:
        return f'Pedido N. {self.pk}'
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'Item do {self.pedido}'
    
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'