from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/add/<int:pk>/', views.adicionar, name='adicionar'),
    path('carrinho/diminuir/<int:pk>/', views.diminuir, name='diminuir'),
    path('carrinho/remover/<int:pk>/', views.remover, name='remover'),
    path('finalizar/', views.checkout, name='checkout'),
    path('pedido/<int:pk>/', views.confirmacao, name='confirmacao'),
]