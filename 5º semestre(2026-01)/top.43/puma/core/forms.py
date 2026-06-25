from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import HorarioDisponivel, PadraoSemanal

class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = ['turma', 'data', 'hora_inicio', 'hora_fim', 'local', 'status', 'aluno_agendado']
        widgets = {
            'data': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'aluno_agendado': forms.Select(attrs={'class': 'form-control'}),
        }

class PadraoSemanalForm(forms.ModelForm):
    class Meta:
        model = PadraoSemanal
        fields = ['turma', 'dia_da_semana', 'hora_inicio', 'hora_fim', 'local', 'data_inicio', 'data_fim']
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'dia_da_semana': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CadastroForm(UserCreationForm):
    TIPO_USUARIO = (
        ('ALUNO', 'Aluno'),
        ('MONITOR', 'Monitor'),
        ('PROFESSOR', 'Professor'),
    )
    tipo = forms.ChoiceField(choices=TIPO_USUARIO, label="Tipo de Utilizador", widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Vincula o utilizador ao grupo correspondente (cria o grupo se não existir)
            tipo = self.cleaned_data['tipo']
            grupo, created = Group.objects.get_or_create(name=tipo)
            user.groups.add(grupo)
        return user