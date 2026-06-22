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

def editar_horario(request, id):
    # Busca o horário específico no banco de dados
    horario = HorarioDisponivel.objects.get(id=id)
    
    if request.method == 'POST':
        # Passa os novos dados (request.POST) e a instância atual para atualizar
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        # Carrega o formulário preenchido com os dados atuais
        form = HorarioDisponivelForm(instance=horario)
        
    return render(request, 'editar_horario.html', {'form': form, 'horario': horario})

def deletar_horario(request, id):
    # Busca o horário e o apaga diretamente
    horario = HorarioDisponivel.objects.get(id=id)
    horario.delete()
    return redirect('/')