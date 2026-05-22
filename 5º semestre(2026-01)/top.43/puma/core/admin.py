from django.contrib import admin
from .models import (
    Perfil,
    Disciplina,
    Turma,
    Monitoria,
    HorarioDisponivel,
    Agendamento,
    Notificacao,
)


admin.site.register(Perfil)
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(Monitoria)
admin.site.register(HorarioDisponivel)
admin.site.register(Agendamento)
admin.site.register(Notificacao)