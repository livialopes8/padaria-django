from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from .models import Pedido

HORA_ABRE = 6     # padaria abre às 6h
HORA_FECHA = 20   # último horário de retirada: 20h
ANTECEDENCIA_MIN = 30  # tempo mínimo para preparar o pedido


def horarios_disponiveis():
    """Gera os horários de retirada (de 30 em 30 min) a partir de agora."""
    agora = timezone.localtime()
    minimo = agora + timedelta(minutes=ANTECEDENCIA_MIN)
    # arredonda para o próximo horário "redondo" (:00 ou :30)
    base = minimo.replace(second=0, microsecond=0)
    base += timedelta(minutes=30 - base.minute % 30)

    horarios = []
    for dia in (0, 1):  # hoje e amanhã
        abertura = agora.replace(hour=HORA_ABRE, minute=0, second=0, microsecond=0) + timedelta(days=dia)
        fechamento = agora.replace(hour=HORA_FECHA, minute=0, second=0, microsecond=0) + timedelta(days=dia)
        t = max(base, abertura)
        while t <= fechamento:
            texto = ('Hoje' if dia == 0 else 'Amanhã') + t.strftime(' às %H:%M')
            horarios.append((t.isoformat(), texto))
            t += timedelta(minutes=30)
    return horarios


class PedidoForm(forms.ModelForm):
    horario_retirada = forms.ChoiceField(label='Horário de retirada', required=False)

    class Meta:
        model = Pedido
        fields = ['nome', 'telefone', 'tipo', 'endereco', 'horario_retirada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # a lista é recalculada a cada vez que a página é aberta
        self.fields['horario_retirada'].choices = [('', 'Escolha um horário')] + horarios_disponiveis()

    def clean(self):
        dados = super().clean()
        tipo = dados.get('tipo')
        if tipo == 'entrega':
            if not dados.get('endereco'):
                self.add_error('endereco', 'Informe o endereço de entrega.')
            dados['horario_retirada'] = None
        elif tipo == 'retirada':
            horario = dados.get('horario_retirada')
            if not horario:
                self.add_error('horario_retirada', 'Escolha o horário de retirada.')
            else:
                dados['horario_retirada'] = datetime.fromisoformat(horario)
            dados['endereco'] = ''
        return dados