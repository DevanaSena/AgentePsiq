from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from usuarios.models import Pacientes
from .models import Gravacoes

# View para listar e adicionar gravações de um paciente
def consultas(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if request.method == 'GET':
        gravacoes = Gravacoes.objects.filter(paciente__id=id).order_by('data')
        return render(request, 'consultas.html', {'paciente': paciente})
    elif request.method == 'POST':
        gravacao = request.FILES.get('gravacao')
        data = request.POST.get('data')
        transcript = request.POST.get('transcript') == 'on'

        gravacao = Gravacoes(
            video=gravacao,
            data=data,  
            transcrever=transcript,
            paciente=paciente,
        )

        gravacao.save()

        return redirect(reverse('consultas', kwargs={'id': id}))
# View para exibir detalhes de uma gravação específica
def gravacao(request, id):
    gravacao = get_object_or_404(Gravacoes, id=id)
    return render(request, 'gravacao.html', {'gravacao': gravacao})

# View para o chat
def chat(request, id):
    if request.method == 'GET':
        paciente = get_object_or_404(Pacientes, id=id)
        return render(request, 'chat.html', {'paciente': paciente})
    
