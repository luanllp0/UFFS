from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HorarioDisponivel
from .forms import HorarioDisponivelForm

# Importações nativas do Python para consumir a API de feriados
import urllib.request
import json
from datetime import datetime

def home(request):
    data = {}
    data['horarios'] = HorarioDisponivel.objects.all()
    
    # INTEGRAÇÃO COM API EXTERNA (Brasil API - Feriados Nacionais)
    ano_atual = datetime.now().year
    try:
        url = f'https://brasilapi.com.br/api/feriados/v1/{ano_atual}'
        # Faz a requisição disfarçada de navegador para não ser bloqueada
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            feriados = json.loads(response.read().decode('utf-8'))
            hoje = datetime.now().date()
            feriados_futuros = []
            
            # Filtra apenas os feriados que ainda não passaram
            for f in feriados:
                data_feriado = datetime.strptime(f['date'], '%Y-%m-%d').date()
                if data_feriado >= hoje:
                    f['data_formatada'] = data_feriado.strftime('%d/%m/%Y')
                    feriados_futuros.append(f)
                    
            # Envia apenas os próximos 3 feriados para a tela
            data['feriados'] = feriados_futuros[:3] 
    except Exception as e:
        data['feriados'] = [] # Se a API falhar ou estiver sem internet, não quebra o site

    return render(request, 'index.html', data)

@login_required # Protege a rota
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

@login_required # Protege a rota
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

@login_required # Protege a rota
def deletar_horario(request, id):
    # Busca o horário e o apaga diretamente
    horario = HorarioDisponivel.objects.get(id=id)
    horario.delete()
    return redirect('/')