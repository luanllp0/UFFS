from django.shortcuts import render
from .models import HorarioDisponivel

def home(request):
    data = {}
    # Buscamos todos os horários cadastrados no banco de dados
    data['horarios'] = HorarioDisponivel.objects.all()
    
    # Renderiza a página index.html passando os dados do banco 
    return render(request, 'index.html', data)