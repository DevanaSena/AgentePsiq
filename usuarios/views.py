from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User


# view para cadastro de usuário
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'Senha e confirmar senha não são iguais.')
            return redirect('cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'Sua senha deve ter pelo meno 6 caracteres.')
            return redirect('cadastro')

        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(request, constants.ERROR,
                                 'Já existe um usuário com esse username.')
            return redirect('cadastro')

        User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('login')
<<<<<<< HEAD
    
    # cadastro de paciente
from .models import Pacientes

def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        paciente = Pacientes(
            foto=foto,
            nome=nome,
            descricao=descricao,
        )

        paciente.save()

        return redirect('pacientes')
    
    
    
=======

# view para login

from django.contrib.auth import authenticate


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username,  password=senha)

        if user:
            auth.login(request, user)
            return redirect('pacientes')

        messages.add_message(request, constants.ERROR,
                             'Username ou senha inválidos.')
        return redirect('login')
>>>>>>> login
