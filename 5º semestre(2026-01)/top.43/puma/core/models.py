from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

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
    aluno_agendado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitorias_agendadas', verbose_name="Aluno Agendado")

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
    
# Adicione a tupla de dias da semana
DIAS_DA_SEMANA = (
    (0, 'Segunda-feira'),
    (1, 'Terça-feira'),
    (2, 'Quarta-feira'),
    (3, 'Quinta-feira'),
    (4, 'Sexta-feira'),
    (5, 'Sábado'),
    (6, 'Domingo'),
)

class PadraoSemanal(models.Model):
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    dia_da_semana = models.IntegerField(choices=DIAS_DA_SEMANA, verbose_name="Dia da Semana")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    local = models.CharField(max_length=200, blank=True, null=True)
    data_inicio = models.DateField(help_text="Data de início do semestre ou da monitoria")
    data_fim = models.DateField(help_text="Data de término do semestre ou da monitoria")

    def save(self, *args, **kwargs):
        # Verifica se é um registro novo (ainda não tem ID no banco)
        novo_registro = self.pk is None 
        super().save(*args, **kwargs) # Salva o Padrão Semanal primeiro
        
        # Se for novo, dispara o gatilho para gerar os horários individuais
        if novo_registro:
            self.gerar_horarios_individuais()

    def gerar_horarios_individuais(self):
        # Calcula quantos dias existem entre a data de início e o fim do semestre
        delta_dias = self.data_fim - self.data_inicio
        
        # Faz um loop por todos esses dias
        for i in range(delta_dias.days + 1):
            dia_atual = self.data_inicio + timedelta(days=i)
            
            # Se o dia atual da repetição for igual ao dia da semana escolhido (ex: Quarta == Quarta)
            if dia_atual.weekday() == self.dia_da_semana:
                # Cria um HorarioDisponivel invisivelmente no banco de dados
                HorarioDisponivel.objects.create(
                    responsavel=self.responsavel,
                    turma=self.turma,
                    data=dia_atual,
                    hora_inicio=self.hora_inicio,
                    hora_fim=self.hora_fim,
                    local=self.local,
                    status='VERDE' # Todo horário gerado nasce como disponível
                )

    def __str__(self):
        return f"{self.turma.nome} - {self.get_dia_da_semana_display()}"