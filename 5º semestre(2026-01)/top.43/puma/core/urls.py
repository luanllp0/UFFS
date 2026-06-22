from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('novo-horario/', views.cadastrar_horario),
]