from django.core.management.base import BaseCommand
from loja.models import Categoria, Produto


class Command(BaseCommand):
    help = 'Cadastra categorias e produtos de exemplo'

    def handle(self, *args, **opts):
        dados = {
            'Pães': [('Pão francês (un.)', 'Crocante por fora, macio por dentro.', 0.80),
                     ('Pão de queijo (un.)', 'Assado na hora.', 3.50)],
            'Bolos': [('Bolo de chocolate (fatia)', 'Com cobertura de brigadeiro.', 8.00),
                      ('Bolo de cenoura (fatia)', 'Com calda de chocolate.', 7.00)],
            'Salgados': [('Coxinha', 'Frango cremoso.', 6.50),
                         ('Empada de palmito', 'Massa amanteigada.', 6.00)],
            'Bebidas': [('Café coado', 'Fresquinho.', 4.00),
                        ('Suco de laranja', 'Natural, 300 ml.', 7.00)],
        }
        for cat, itens in dados.items():
            c, _ = Categoria.objects.get_or_create(nome=cat)
            for nome, desc, preco in itens:
                Produto.objects.get_or_create(nome=nome, defaults={'descricao': desc, 'preco': preco, 'categoria': c})
        self.stdout.write(self.style.SUCCESS('Produtos de exemplo criados!'))
