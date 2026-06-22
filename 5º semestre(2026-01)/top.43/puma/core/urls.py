from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('novo-horario/', views.cadastrar_horario),
    path('editar-horario/<int:id>/', views.editar_horario),
    path('deletar-horario/<int:id>/', views.deletar_horario),
]