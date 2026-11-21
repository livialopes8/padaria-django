# Padaria Doce Trigo (Django)

Site de padaria com cardápio, carrinho e pedido online (retirada sem fila ou entrega).

## Como rodar
```
python -m venv venv
venv\Scripts\activate        # Windows (Linux/Mac: source venv/bin/activate)
pip install django pillow
python manage.py migrate
python manage.py popular      # cadastra produtos de exemplo
python manage.py createsuperuser
python manage.py runserver
```
Site: http://127.0.0.1:8000 · Admin: http://127.0.0.1:8000/admin
