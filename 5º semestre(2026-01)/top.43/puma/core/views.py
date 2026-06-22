from django.shortcuts import render, redirect
from .models import HorarioDisponivel
from .forms import HorarioDisponivelForm

def home(request):
    data = {}
    data['horarios'] = HorarioDisponivel.objects.all()
    return render(request, 'index.html', data)

def cadastrar_horario(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            # Salva o formulário provisoriamente para injetar o usuário logado como responsável
            horario = form.save(commit=False)
            horario.responsavel = request.user
            horario.save()
            return redirect('/') # Redireciona de volta para a página inicial
    else:
        form = HorarioDisponivelForm()
        
    return render(request, 'cadastrar_horario.html', {'form': form})