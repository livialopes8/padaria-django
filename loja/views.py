from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Produto, Pedido, ItemPedido
from .forms import PedidoForm


def _carrinho(request):
    """Lê o carrinho guardado na sessão e calcula itens e total."""
    dados = request.session.get('carrinho', {})
    itens, total = [], 0
    for pid, qtd in dados.items():
        produto = Produto.objects.filter(pk=pid).first()
        if produto:
            sub = produto.preco * qtd
            total += sub
            itens.append({'produto': produto, 'qtd': qtd, 'subtotal': sub})
    return itens, total


def home(request):
    destaques = Produto.objects.filter(disponivel=True)[:4]
    return render(request, 'loja/home.html', {'destaques': destaques})


def produtos(request):
    cat = request.GET.get('categoria')
    lista = Produto.objects.filter(disponivel=True)
    if cat:
        lista = lista.filter(categoria_id=cat)
    return render(request, 'loja/produtos.html', {
        'produtos': lista, 'categorias': Categoria.objects.all(), 'cat': cat})


def adicionar(request, pk):
    carrinho = request.session.get('carrinho', {})
    carrinho[str(pk)] = carrinho.get(str(pk), 0) + 1
    request.session['carrinho'] = carrinho
    return redirect('carrinho')


def remover(request, pk):
    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(pk), None)
    request.session['carrinho'] = carrinho
    return redirect('carrinho')


def carrinho(request):
    itens, total = _carrinho(request)
    return render(request, 'loja/carrinho.html', {'itens': itens, 'total': total})


def checkout(request):
    itens, total = _carrinho(request)
    if not itens:
        return redirect('produtos')
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.total = total
        pedido.save()
        for i in itens:
            ItemPedido.objects.create(pedido=pedido, produto=i['produto'],
                                      quantidade=i['qtd'], preco=i['produto'].preco)
        request.session['carrinho'] = {}
        return redirect('confirmacao', pk=pedido.pk)
    return render(request, 'loja/checkout.html', {'form': form, 'itens': itens, 'total': total})


def confirmacao(request, pk):
    return render(request, 'loja/confirmacao.html', {'pedido': get_object_or_404(Pedido, pk=pk)})
