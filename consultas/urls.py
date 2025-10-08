from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.consultas, name='consultas'),
    path('gravacao/<int:id>', views.gravacao, name='gravacao'),

]