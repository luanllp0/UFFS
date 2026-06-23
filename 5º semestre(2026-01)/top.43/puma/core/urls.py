from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('cadastro/', views.ajudar_cadastro, name='signup'),
    path('novo-horario/', views.cadastrar_horario),
    path('novo-padrao/', views.cadastrar_padrao),
    path('api/horarios/', views.api_horarios), 
    path('solicitar-agendamento/<int:id>/', views.solicitar_agendamento), 
    path('confirmar-agendamento/<int:id>/', views.confirmar_agendamento),
    path('editar-horario/<int:id>/', views.editar_horario),
    path('deletar-horario/<int:id>/', views.deletar_horario),
]