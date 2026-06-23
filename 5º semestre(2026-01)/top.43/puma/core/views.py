from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q # <--- NOVA IMPORTAÇÃO PARA O FILTRO

from .models import HorarioDisponivel, Turma
from .forms import HorarioDisponivelForm, CadastroForm, PadraoSemanalForm

import urllib.request
import json
from datetime import datetime

def home(request):
    data = {}
    
    if request.user.is_authenticated:
        data['is_monitor_ou_prof'] = request.user.groups.filter(name__in=['PROFESSOR', 'MONITOR']).exists()
        data['is_aluno'] = request.user.groups.filter(name='ALUNO').exists()
        
        # FILTRO NOVO: Apenas turmas vinculadas ao usuário logado
        if request.user.is_superuser:
            data['turmas'] = Turma.objects.all() # Administrador vê todas
        else:
            data['turmas'] = Turma.objects.filter(
                Q(professores=request.user) | 
                Q(monitores=request.user) | 
                Q(alunos=request.user)
            ).distinct()
    else:
        data['is_monitor_ou_prof'] = False
        data['is_aluno'] = False
        data['turmas'] = Turma.objects.none() # Visitantes não veem turmas no dropdown
        
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
            login(request, user)
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
        # NOVO: Verifica se veio uma data na URL (ex: ?data=2026-06-23)
        data_via_url = request.GET.get('data')
        if data_via_url:
            # Passa a data como valor inicial para o formulário
            form = HorarioDisponivelForm(initial={'data': data_via_url})
        else:
            form = HorarioDisponivelForm()
        
    if not request.user.is_superuser:
        form.fields['turma'].queryset = Turma.objects.filter(
            Q(professores=request.user) | 
            Q(monitores=request.user) | 
            Q(alunos=request.user)
        ).distinct()
        
    return render(request, 'cadastrar_horario.html', {'form': form})
        
    # FILTRO NOVO: Limita as turmas no formulário de criação
    if not request.user.is_superuser:
        form.fields['turma'].queryset = Turma.objects.filter(
            Q(professores=request.user) | 
            Q(monitores=request.user) | 
            Q(alunos=request.user)
        ).distinct()
        
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
        
    # FILTRO NOVO: Limita as turmas no formulário de edição
    if not request.user.is_superuser:
        form.fields['turma'].queryset = Turma.objects.filter(
            Q(professores=request.user) | 
            Q(monitores=request.user) | 
            Q(alunos=request.user)
        ).distinct()
        
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
            padrao.save()
            return redirect('/')
    else:
        form = PadraoSemanalForm()
        
    # FILTRO NOVO: Limita as turmas no formulário de padrão semanal
    if not request.user.is_superuser:
        form.fields['turma'].queryset = Turma.objects.filter(
            Q(professores=request.user) | 
            Q(monitores=request.user) | 
            Q(alunos=request.user)
        ).distinct()
        
    return render(request, 'cadastrar_padrao.html', {'form': form})

def api_horarios(request):
    turma_id = request.GET.get('turma')
    filtros = {}
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name__in=['PROFESSOR', 'MONITOR']).exists():
            filtros['responsavel'] = request.user
            
        if not turma_id and not request.user.is_superuser:
            turmas_vinculadas = Turma.objects.filter(
                Q(professores=request.user) | 
                Q(monitores=request.user) | 
                Q(alunos=request.user)
            ).distinct()
            filtros['turma__in'] = turmas_vinculadas

    if turma_id:
        filtros['turma_id'] = turma_id
        
    horarios = HorarioDisponivel.objects.filter(**filtros)
    
    eventos = []
    for h in horarios:
        cor = '#28a745' # Verde
        if h.status == 'AMARELO':
            cor = '#ffc107' # Amarelo (Disponível para solicitar)
        elif h.status == 'LARANJA':
            cor = '#fd7e14' # Laranja (Já foi solicitado, pendente de aprovação)
        elif h.status == 'VERMELHO':
            cor = '#dc3545' # Vermelho (Ocupado)

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

@login_required
def solicitar_agendamento(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    if request.user.groups.filter(name='ALUNO').exists():
        if horario.status == 'VERDE' and not horario.aluno_agendado:
            horario.status = 'VERMELHO' # Agendamento direto
            horario.aluno_agendado = request.user
            horario.save()
        elif horario.status == 'AMARELO' and not horario.aluno_agendado:
            horario.status = 'LARANJA' # Muda para Laranja para bloquear outros alunos
            horario.aluno_agendado = request.user
            horario.save()
    return redirect('/')

@login_required
def confirmar_agendamento(request, id):
    horario = HorarioDisponivel.objects.get(id=id)
    # Agora o professor confirma a partir do status Laranja
    if horario.responsavel == request.user and horario.status == 'LARANJA':
        horario.status = 'VERMELHO'
        horario.save()
    return redirect('/')