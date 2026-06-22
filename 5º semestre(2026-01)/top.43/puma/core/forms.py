from django.forms import ModelForm
from django import forms
from .models import HorarioDisponivel, Agendamento

class HorarioDisponivelForm(ModelForm):
    class Meta:
        model = HorarioDisponivel
        # Definimos quais campos o professor/monitor vai preencher ao criar um horário
        fields = ['turma', 'data', 'hora_inicio', 'hora_fim', 'status', 'local', 'observacao']
        
        # O dicionário 'widgets' aplica as classes do Bootstrap (form-control)
        # diretamente nos inputs do HTML, garantindo a responsividade exigida.
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sala 203 ou Link do Meet'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AgendamentoForm(ModelForm):
    class Meta:
        model = Agendamento
        # O aluno só precisa preencher o assunto e a descrição ao solicitar a reserva
        fields = ['assunto', 'descricao']
        
        widgets = {
            'assunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qual a sua dúvida principal?'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva detalhadamente o que você precisa de ajuda...'}),
        }