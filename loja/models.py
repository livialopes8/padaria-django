from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    TIPOS = [('retirada', 'Retirada na padaria (sem fila)'), ('entrega', 'Entrega')]
    STATUS = [('novo', 'Novo'), ('preparo', 'Em preparo'), ('pronto', 'Pronto'), ('entregue', 'Entregue')]
    nome = models.CharField('Nome', max_length=100)
    telefone = models.CharField('Telefone', max_length=20)
    tipo = models.CharField('Tipo', max_length=10, choices=TIPOS, default='retirada')
    endereco = models.CharField('Endereço (se for entrega)', max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido #{self.pk} - {self.nome}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
