from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import HorarioDisponivel, Turma
from .forms import HorarioDisponivelForm, CadastroForm, PadraoSemanalForm
from django.http import JsonResponse

# Importações para a API de feriados
import urllib.request
import json
from datetime import datetime

def home(request):
    data = {}
    data['turmas'] = Turma.objects.all() # Envia as turmas para o filtro HTML
    
    # Verifica os papéis do utilizador logado
    if request.user.is_authenticated:
        data['is_monitor_ou_prof'] = request.user.groups.filter(name__in=['PROFESSOR', 'MONITOR']).exists()
        data['is_aluno'] = request.user.groups.filter(name='ALUNO').exists()
    else:
        data['is_monitor_ou_prof'] = False
        data['is_aluno'] = False
        
    # CORREÇÃO: Definição da variável ano_atual antes de entrar no bloco try
    ano_atual = datetime.now().year
    try:
        url = f'https://brasilapi.com.br/api/feriados/v1/{ano_atual}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            feriados = json.loads(response.read().decode('utf-8'))
            hoje = datetime.now().date()
            feriados_futuros = []
            for f in feriados:
                data_feriado = datetime.strptime(f['date'], '%Y-%m-%d').date()
                if data_feriado >= hoje:
                    f['data_formatada'] = data_feriado.strftime('%d/%m/%Y')
                    feriados_futuros.append(f)
            data['feriados'] = feriados_futuros[:3]
    except Exception:
        data['feriados'] = []

    return render(request, 'index.html', data)

def ajudar_cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Faz login automático logo após registar
            return redirect('/')
    else:
        form = CadastroForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def cadastrar_horario(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.responsavel = request.user
            horario.save()
            return redirect('/')
    else:
        form = HorarioDisponivelForm()
    return render(request, 'cadastrar_horario.html', {'form': form})

@login_required
def editar_horario(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = HorarioDisponivelForm(instance=horario)
    return render(request, 'editar_horario.html', {'form': form, 'horario': horario})

@login_required
def deletar_horario(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    horario.delete()
    return redirect('/')

@login_required
def cadastrar_padrao(request):
    if request.method == 'POST':
        form = PadraoSemanalForm(request.POST)
        if form.is_valid():
            padrao = form.save(commit=False)
            padrao.responsavel = request.user
            padrao.save() # É aqui que aquele gatilho mágico que criámos antes vai ser disparado!
            return redirect('/')
    else:
        form = PadraoSemanalForm()
    
    return render(request, 'cadastrar_padrao.html', {'form': form})

def api_horarios(request):
    turma_id = request.GET.get('turma')
    
    # ALTERAÇÃO: Se for Professor ou Monitor, filtra para exibir APENAS os horários dele
    if request.user.is_authenticated and request.user.groups.filter(name__in=['PROFESSOR', 'MONITOR']).exists():
        filtros = {'responsavel': request.user}
    else:
        # Alunos e visitantes continuam vendo todos os horários disponíveis para poderem agendar
        filtros = {}

    # Se houver um filtro de turma selecionado no dropdown, combina os filtros
    if turma_id:
        filtros['turma_id'] = turma_id
        
    horarios = HorarioDisponivel.objects.filter(**filtros)
    
    eventos = []
    for h in horarios:
        cor = '#28a745'
        if h.status == 'AMARELO':
            cor = '#ffc107'
        elif h.status == 'VERMELHO':
            cor = '#dc3545'

        start = f"{h.data.strftime('%Y-%m-%d')}T{h.hora_inicio.strftime('%H:%M:%S')}"
        end = f"{h.data.strftime('%Y-%m-%d')}T{h.hora_fim.strftime('%H:%M:%S')}"

        eventos.append({
            'id': h.id,
            'title': f"{h.turma.disciplina.nome} ({h.local})",
            'start': start,
            'end': end,
            'color': cor,
            'status': h.status,
            'tem_aluno': h.aluno_agendado is not None
        })
        
    return JsonResponse(eventos, safe=False)

# Permite ao professor/monitor confirmar a solicitação pendente
@login_required
def confirmar_agendamento(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    # Garante que apenas o criador do horário pode confirmar e se o status for Amarelo
    if horario.responsavel == request.user and horario.status == 'AMARELO':
        horario.status = 'VERMELHO' # Transforma o horário em Ocupado/Confirmado
        horario.save()
    return redirect('/')

@login_required
def solicitar_agendamento(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    
    # Apenas Alunos podem interagir
    if request.user.groups.filter(name='ALUNO').exists():
        # Regra 1: Agendamento Instantâneo (Verde para Vermelho)
        if horario.status == 'VERDE' and not horario.aluno_agendado:
            horario.status = 'VERMELHO' 
            horario.aluno_agendado = request.user
            horario.save()
            
        # Regra 2: Solicitar Agendamento (Amarelo, continua Amarelo mas regista o aluno)
        elif horario.status == 'AMARELO' and not horario.aluno_agendado:
            horario.status = 'AMARELO'
            horario.aluno_agendado = request.user
            horario.save()
            
    return redirect('/')