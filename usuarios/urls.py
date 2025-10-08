from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
<<<<<<< HEAD
    path('pacientes/', views.pacientes, name='pacientes'),

=======
    path('login/', views.login, name='login'),
>>>>>>> login
]