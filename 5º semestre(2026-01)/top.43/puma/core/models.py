from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

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
        related_name='turmas_ministradas',
        help_text="Professor principal/responsável pela criação da turma"
    )
    nome = models.CharField(max_length=50)
    semestre = models.CharField(max_length=20)

    professores = models.ManyToManyField(User, related_name='turmas_prof', blank=True, verbose_name="Professores Vinculados")
    monitores = models.ManyToManyField(User, related_name='turmas_monitor', blank=True, verbose_name="Monitores Vinculados")
    alunos = models.ManyToManyField(User, related_name='turmas_aluno', blank=True, verbose_name="Alunos Vinculados")

    def __str__(self):
        return f'{self.disciplina.codigo} - {self.nome} - {self.semestre}'


class HorarioDisponivel(models.Model):
    STATUS_HORARIO = (
        ('VERDE', 'Disponível (Instantâneo)'),
        ('AMARELO', 'Disponível (Requer Aprovação)'),
        ('LARANJA', 'Solicitação Pendente'),
        ('VERMELHO', 'Ocupado / Confirmado'),
    )

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
    status = models.CharField(max_length=20, choices=STATUS_HORARIO, default='VERDE')
    local = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    aluno_agendado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitorias_agendadas', verbose_name="Aluno Agendado")

    class Meta:
        unique_together = ('responsavel', 'data', 'hora_inicio', 'hora_fim')

    def __str__(self):
        return f'{self.responsavel.username} - {self.turma} - {self.data}'

    
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