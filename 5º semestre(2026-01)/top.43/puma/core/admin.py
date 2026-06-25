from django.contrib import admin
from .models import (
    Disciplina,
    Turma,
    HorarioDisponivel,
    PadraoSemanal,
)

admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(HorarioDisponivel)
admin.site.register(PadraoSemanal)