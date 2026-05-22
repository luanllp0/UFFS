from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    TIPO_USUARIO = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    curso = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo}'


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='turmas_ministradas'
    )
    nome = models.CharField(max_length=50)
    semestre = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.disciplina.codigo} - {self.nome} - {self.semestre}'


class Monitoria(models.Model):
    aluno_monitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='monitorias'
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='monitorias'
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('aluno_monitor', 'turma')

    def __str__(self):
        return f'{self.aluno_monitor.username} - {self.turma}'


class HorarioDisponivel(models.Model):
    STATUS_HORARIO = [
        ('VERDE', 'Livre para agendamento direto'),
        ('AMARELO', 'Livre com confirmação'),
        ('VERMELHO', 'Ocupado'),
    ]

    responsavel = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='horarios_disponiveis'
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_HORARIO)
    local = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('responsavel', 'data', 'hora_inicio', 'hora_fim')

    def __str__(self):
        return f'{self.responsavel.username} - {self.turma} - {self.data}'


class Agendamento(models.Model):
    STATUS_AGENDAMENTO = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('RECUSADO', 'Recusado'),
        ('CANCELADO', 'Cancelado'),
        ('REALIZADO', 'Realizado'),
    ]

    horario = models.OneToOneField(
        HorarioDisponivel,
        on_delete=models.CASCADE,
        related_name='agendamento'
    )
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agendamentos_solicitados'
    )
    status = models.CharField(max_length=20, choices=STATUS_AGENDAMENTO)
    assunto = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.aluno.username} - {self.horario} - {self.status}'


class Notificacao(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'