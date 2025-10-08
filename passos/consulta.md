## Consultas - Consultas

Crie o APP consultas:

```python
python3 manage.py startapp consultas
```

## Instale o APP!

Crie a model para armazenar as gravações:
consulta/model
```python
class Gravacoes(models.Model):
    video = models.FileField(upload_to='gravacoes')
    data = models.DateTimeField()
    transcrever = models.BooleanField(default=False)
    paciente = models.ForeignKey(Pacientes, on_delete=models.DO_NOTHING)
    humor = models.IntegerField(default=0)
    transcricao = models.TextField()
    resumo = models.JSONField(default=list, blank=True)
    segmentos = models.JSONField(default=list, blank=True)

```

Adicione a URL para consultas:

```python
path('consultas/', include('consultas.urls'))
```

Crie URL para cadastrar uma consulta para o usuário:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.consultas, name='consultas'),
]
```

A lógica das consultas:

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from usuarios.models import Pacientes
from .models import Gravacoes

def consultas(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if request.method == 'GET':
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
    
```

Adicione o consultas.html

```html
{% extends "base.html" %}
{% load static %}
{% block 'body' %}
    <header class="absolute inset-x-0 top-0 z-50 flex h-16 border-b border-gray-900/10">
        <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
            <div class="flex flex-1 items-center gap-x-6">
                <a href="{% url 'pacientes' %}"><img src="{% static 'logo.png' %}" alt="PsiQuê" class="h-12 w-auto" /></a>
            </div>
            <nav class="hidden md:flex md:gap-x-11 md:text-sm/6 md:font-semibold md:text-gray-700">
                <a href="#">Consultas</a>
                <a href="#">Usuários</a>
            </nav>
            <div class="flex flex-1 items-center justify-end gap-x-8">
                <a href="#" class="-m-1.5 p-1.5">
                    <span class="sr-only">Seu perfil</span>
                    <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                         alt=""
                         class="size-8 rounded-full bg-gray-100 outline -outline-offset-1 outline-black/5" />
                </a>
            </div>
        </div>
    </header>
    <main>
        <header class="relative isolate pt-16">
            <div aria-hidden="true" class="absolute inset-0 -z-10 overflow-hidden">
                <div class="absolute top-full left-16 -mt-16 transform-gpu opacity-50 blur-3xl xl:left-1/2 xl:-ml-80">
                    <div style="clip-path: polygon(100% 38.5%, 82.6% 100%, 60.2% 37.7%, 52.4% 32.1%, 47.5% 41.8%, 45.2% 65.6%, 27.5% 23.4%, 0.1% 35.3%, 17.9% 0%, 27.7% 23.4%, 76.2% 2.5%, 74.2% 56%, 100% 38.5%)"
                         class="aspect-1154/678 w-288.5 bg-linear-to-br from-[#FF80B5] to-[#9089FC]"></div>
                </div>
                <div class="absolute inset-x-0 bottom-0 h-px bg-gray-900/5"></div>
            </div>
            <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
                <div class="mx-auto flex max-w-2xl items-center justify-between gap-x-8 lg:mx-0 lg:max-w-none">
                    <div class="flex items-center gap-x-6">
                        <img class="object-cover w-full rounded-t-lg h-18 md:h-auto md:w-18 md:rounded-none md:rounded-s-lg"
                             src="{{ paciente.foto.url }}"
                             alt="">
                        <p class="text-2xl font-bold">{{ paciente.nome }}</p>
                    </div>
                    <a href="#"
                       class="ml-auto flex items-center gap-x-1 rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-green-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        <svg xmlns="http://www.w3.org/2000/svg"
                             fill="none"
                             viewBox="0 0 24 24"
                             stroke-width="1.5"
                             stroke="currentColor"
                             class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.068.157 2.148.279 3.238.364.466.037.893.281 1.153.671L12 21l2.652-3.978c.26-.39.687-.634 1.153-.67 1.09-.086 2.17-.208 3.238-.365 1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
                        </svg>
                        Chat
                    </a>
                </div>
            </div>
        </header>
        <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <div class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
                <div class="lg:col-start-3 lg:row-end-1 overflow-auto">
                    <div class="rounded-lg p-6 bg-gray-50 shadow-xs outline-1 outline-gray-900/5">
                        <table class="min-w-full divide-y divide-gray-300">
                            <thead>
                                <tr>
                                    <th scope="col"
                                        class="py-3.5 pr-3 pl-4 text-left text-sm font-semibold text-gray-900 sm:pl-3">
                                        Gravação
                                    </th>
                                    <th scope="col"
                                        class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Data</th>
                                    <th scope="col"
                                        class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                        Transcricao
                                    </th>
                                    <th scope="col"
                                        class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Resumo</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white">
                                
                                    <tr class="even:bg-gray-50">
                                        <td class="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-3">
                                            <a href="#">Gravação 1</a>
                                        </td>
                                        <td class="px-3 py-4 text-sm whitespace-nowrap text-gray-500">Data</td>
                                        <td class="px-3 py-4 text-sm whitespace-nowrap">
                                             ✅  
                                        </td>
                                        <td class="px-3 py-4 text-sm whitespace-nowrap">
                                            ✅
                                        </td>
                                    </tr>
                                
                            </tbody>
                        </table>
                    </div>
                </div>
                <!-- Invoice -->
                <div class="-mx-4 px-4 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16  xl:pb-20">
                    <div>
                        <form action="" method="POST">

                            <label class="block text-sm/6 font-medium text-gray-900">Gravação</label>
                            <input type="file"
                                   name="gravacao"
                                   class="mt-2 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
                        </div>
                        <div class="mt-2">
                            <label class="block text-sm/6 font-medium text-gray-900">Data</label>
                            <input type="date"
                                   name="data"
                                   class="mt-2 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
                        </div>
                        <div class="mt-6 space-y-6">
                            <div class="flex gap-3">
                                <div class="flex h-6 shrink-0 items-center">
                                    <div class="group grid size-4 grid-cols-1">
                                        <input id="transcript"
                                               type="checkbox"
                                               name="transcript"
                                               checked
                                               aria-describedby="comments-description"
                                               class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto" />
                                        <svg viewBox="0 0 14 14"
                                             fill="none"
                                             class="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-gray-950/25">
                                            <path d="M3 8L6 11L11 3.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-0 group-has-checked:opacity-100" />
                                            <path d="M3 7H11" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-0 group-has-indeterminate:opacity-100" />
                                        </svg>
                                    </div>
                                </div>
                                <div class="text-sm/6">
                                    <label for="comments" class="font-medium text-gray-900">Transcrever</label>
                                    <p id="comments-description" class="text-gray-500">
                                        Ao marcar essa opção os dados serão usados para treinamendo da IA.
                                    </p>
                                </div>
                            </div>
                            <div class="mt-2">
                                <button type="submit"
                                        class="inline-flex cursor-pointer items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                    Adicionar gravação
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            
        </main>

    {% endblock 'body' %}
```

Envie o formulário para as views:

```html
<form action="{% url 'consultas' paciente.id %}" method="POST" enctype='multipart/form-data'>
```

Busque todas as gravações:

```python
gravacoes = Gravacoes.objects.filter(paciente__id=id).order_by('data')
```

Liste no HTML:

```html
{% for gravacao in gravacoes %}
    <tr class="even:bg-gray-50">
        <td class="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-3">
            <a href="">{{ gravacao.video.name }}</a>
        </td>
        <td class="px-3 py-4 text-sm whitespace-nowrap text-gray-500">{{ gravacao.data }}</td>
        <td class="px-3 py-4 text-sm whitespace-nowrap">
            {% if gravacao.transcricao %}
                <span class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-green-800 text-xs font-medium">
                    ✅
                </span>
            {% else %}
                <span class="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-red-800 text-xs font-medium">X</span>
            {% endif %}
        </td>
        <td class="px-3 py-4 text-sm whitespace-nowrap">
            {% if gravacao.resumo %}
                <span class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-green-800 text-xs font-medium">
                    ✅
                </span>
            {% else %}
                <span class="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-red-800 text-xs font-medium">X</span>
            {% endif %}
        </td>
    </tr>
{% endfor %}
```

…
…

## Transcrição, resumo e RAG - Consultas


consultas/signals.py

Crie um signals:

1. Certifique-se de que o pacote django-q está instalado
No terminal, execute o seguinte comando para instalar o pacote:
```python
pip install django-q
```
2. Verifique se o pacote está listado no INSTALLED_APPS
Abra o arquivo settings.py do seu projeto e adicione 'django_q' à lista de INSTALLED_APPS, caso ainda não esteja:
```python
INSTALLED_APPS = [
    # ... outras apps ...
    'django_q',
]

```
3. Configure o django-q no arquivo settings.py
Adicione a configuração básica para o django-q no mesmo arquivo settings.py. Por exemplo:

```python
Q_CLUSTER = {
    'name': 'DjangoQ',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'orm': 'default',  # Use o banco de dados padrão
}

```
4. Execute as migrações
Depois de configurar o django-q, execute as migrações para criar as tabelas necessárias no banco de dados:

```python
python3 manage.py migrate
```
5. Teste a Importação
Agora, a importação from django_q.tasks import async_task, Chain deve funcionar corretamente. Reinicie o servidor de desenvolvimento para garantir que as alterações sejam aplicadas:
```python
python3 manage.py runserver
```

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Gravacoes
from django_q.tasks import async_task, Chain
from .tasks import transcribe_recording, summary_recording, task_rag

@receiver(post_save, sender=Gravacoes)
def signals_gravacoes_transcricao_resumos(sender, instance, created, **kwargs):
    if created:
        if instance.transcrever:
            #transcribe_recording(instance.id)
            chain = Chain()
            chain.append(transcribe_recording, instance.id)
            chain.append(summary_recording, instance.id)
            chain.append(task_rag, instance.id)
            chain.run()
```

Crie a função para as tasks:

consultas/tasks.py

```python
def transcribe_recording():
    ...

def summary_recording():
    ...

def task_rag():
    ...
```

Crie a base para os agentes:

```python
class BaseAgent:
    ...

class SummaryAgent(BaseAgent):
    ...

class EvaluationAgent(BaseAgent):
    ...

class RAGContext:
    ...
```

..

.

## Gravação - Consultas

Crie uma URL para gravação:

consultas/urls

```python
path('gravacao/<int:id>', views.gravacao, name='gravacao'),
```

Construa a view:

consultas/views

```python
def gravacao(request, id):
    gravacao = get_object_or_404(Gravacoes, id=id)
    return render(request, 'gravacao.html', {'gravacao': gravacao})
```

O HTML para as gravações:

consultas/templetes/gravacao.html

```python
{% extends "base.html" %}
{% load static %}

{% block 'body' %}
    <header class="absolute inset-x-0 top-0 z-50 flex h-16 border-b border-gray-900/10">
        <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
            <div class="flex flex-1 items-center gap-x-6">
                <img src="{% static 'logo.png' %}" alt="PsiQuê" class="h-12 w-auto" />
            </div>
            <nav class="hidden md:flex md:gap-x-11 md:text-sm/6 md:font-semibold md:text-gray-700">
                <a href="#">Consultas</a>
                <a href="#">Usuários</a>
            </nav>
            <div class="flex flex-1 items-center justify-end gap-x-8">
                <a href="#" class="-m-1.5 p-1.5">
                    <span class="sr-only">Seu perfil</span>
                    <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                         alt=""
                         class="size-8 rounded-full bg-gray-100 outline -outline-offset-1 outline-black/5" />
                </a>
            </div>
        </div>
    </header>
    <main>
        <div class="relative isolate overflow-hidden pt-16">
            <!-- Secondary navigation -->
            <header class="pt-6 pb-4 sm:pb-6">
                <div class="mx-auto flex max-w-7xl flex-wrap items-center gap-6 px-4 sm:flex-nowrap sm:px-6 lg:px-8">
                    <a href="{% url 'consultas' gravacao.paciente.id  %}"><img class="object-cover w-full rounded-t-lg h-18 md:h-auto md:w-18 md:rounded-none md:rounded-s-lg"
                             src="{{ gravacao.paciente.foto.url }}"
                             alt=""></a>
                    <h1 class="text-base/7 font-semibold text-gray-900">Gravação 1</h1>
                    <a href="#"
                       class="ml-auto flex items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-red-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        - Excluir
                    </a>
                </div>
            </header>
            <!-- Stats -->
            <div class="border-b border-b-gray-900/10 lg:border-t lg:border-t-gray-900/5">
                <dl class="mx-auto grid max-w-7xl grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 lg:px-2 xl:px-0">
                    <div class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-t border-gray-900/5 px-4 py-10 sm:px-6 lg:border-t-0 xl:px-8">
                        <dt class="text-sm/6 font-medium text-gray-500">Transcrição</dt>
                        <dd class="w-full flex-none text-3xl/10 font-medium tracking-tight text-gray-900">
                            10 <span class="text-sm text-gray-400">palavras</span>
                        </dd>
                    </div>
                    <div class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-t border-gray-900/5 px-4 py-10 sm:border-l sm:px-6 lg:border-t-0 xl:px-8">
                        <dt class="text-sm/6 font-medium text-gray-500">Tarefas</dt>
                        <dd class="w-full flex-none text-3xl/10 font-medium tracking-tight text-gray-900">
                            10 <span class="text-sm text-gray-400">Tarefas / lembretes</span> 
                        </dd>
                    </div>
                    <div class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-t border-gray-900/5 px-4 py-10 sm:px-6 lg:border-t-0 lg:border-l xl:px-8">
                        <dt class="text-sm/6 font-medium text-gray-500">Humor médio</dt>
                        <dd class="w-full flex-none text-3xl/10 font-medium tracking-tight text-gray-900">
                            3 <span class="text-sm text-gray-400">de 5</span>
                        </dd>
                    </div>
                    <div class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-t border-gray-900/5 px-4 py-10 sm:border-l sm:px-6 lg:border-t-0 xl:px-8">
                        <dt class="text-sm/6 font-medium text-gray-500">Humor da sessão</dt>
                        <dd class="w-full flex-none text-3xl/10 font-medium tracking-tight text-gray-900">
                            3 <span class="text-sm text-gray-400">de 5</span>
                        </dd>
                    </div>
                </dl>
            </div>
            <div aria-hidden="true"
                 class="absolute top-full left-0 -z-10 mt-96 origin-top-left translate-y-40 -rotate-90 transform-gpu opacity-20 blur-3xl sm:left-1/2 sm:-mt-10 sm:-ml-96 sm:translate-y-0 sm:rotate-0 sm:opacity-50">
                <div style="clip-path: polygon(100% 38.5%, 82.6% 100%, 60.2% 37.7%, 52.4% 32.1%, 47.5% 41.8%, 45.2% 65.6%, 27.5% 23.4%, 0.1% 35.3%, 17.9% 0%, 27.7% 23.4%, 76.2% 2.5%, 74.2% 56%, 100% 38.5%)"
                     class="aspect-1154/678 w-288.5 bg-linear-to-br from-[#FF80B5] to-[#9089FC]"></div>
            </div>
        </div>
        <div class="space-y-16 py-16 xl:space-y-20">
            <!-- Recent activity table -->
            <div>
                <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <h2 class="mx-auto max-w-2xl text-base font-semibold text-gray-900 lg:mx-0 lg:max-w-none">Transcrição</h2>
                </div>
                <div class="mt-6 overflow-hidden border-t border-gray-100">
                    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div class="mx-auto mt-6 max-w-2xl lg:mx-0 lg:max-w-none">
                            <div class="overflow-hidden rounded-xl outline outline-gray-200 ">
                                <div class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6">
                                    Transcriçao aqui
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Recent client list-->
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="mx-auto max-w-2xl lg:mx-0 lg:max-w-none">
                    <div class="flex items-center justify-between">
                        <h2 class="text-base/7 font-semibold text-gray-900">Tarefas</h2>
                        <a href="#"
                           class="text-sm/6 font-semibold text-indigo-600 hover:text-indigo-500">Ver todas</a>
                    </div>
                    <ul role="list" class="divide-y divide-gray-100">
                        
                            <li class="relative flex items-center space-x-4 py-4">
                                <div class="min-w-0 flex-auto">
                                    <div class="flex items-center gap-x-3">
                                        <div class="flex-none rounded-full bg-green-100 p-1 text-green-500">
                                            <div class="size-2 rounded-full bg-current"></div>
                                        </div>
                                        <h2 class="min-w-0 text-sm/6 font-semibold text-gray-900">
                                            <a href="#" class="flex gap-x-2">Tarefa 1: Fazer mindfulness</a>
                                        </h2>
                                    </div>
                                </div>
                                <div class="flex-none rounded-full bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700 inset-ring inset-ring-indigo-700/10">
                                    Resumo
                                </div>
                            </li>
                        
                    </ul>
                </div>
                <a href="" class="ml-auto cursor-pointer items-center gap-x-1 rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-green-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                    Enviar resumo
                </a>
            </div>
        </div>
    </main>
{% endblock 'body' %}

```

## Chat - Consultas

URL para chat:

consultas/urls

```python
path('chat/<int:id>', views.chat, name='chat'),
```

Views do CHAT:

consultas/views

```python
def chat(request, id):
    if request.method == 'GET':
        paciente = get_object_or_404(Pacientes, id=id)
        return render(request, 'chat.html', {'paciente': paciente})
```

Não esqueça o HTML:

consultas/chat

```python
{% extends "base.html" %}
{% load static %}
{% block 'body' %}
    <main>
        <header class="relative isolate bg-indigo-200/80">
            <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
                <div class="mx-auto flex max-w-2xl items-center justify-between gap-x-8 lg:mx-0 lg:max-w-none">
                    <div class="flex items-center gap-x-6">
                        <a href="{% url 'consultas' paciente.id  %}"><img src="{{ paciente.foto.url }}" alt="" class="w-10 rounded-md"></a>
                        <h1>
                            <div class="mt-1 text-base font-semibold text-gray-900">Ana</div>
                        </h1>
                    </div>
                </div>
            </div>
        </header>
        <div class="px-4 md:px-0">
            <div class="mx-auto bg-slate-50 mt-8 max-w-4xl px-4 py-16 sm:px-6 lg:px-8 border border-slate-200/60 rounded-md">
                <!-- Container principal empilhando tudo -->
                <div class="flex flex-col gap-6" id="chat">
                    <!-- Mensagem do assistente -->
                    <div class="flex items-start gap-2.5">
                        <img class="w-12 h-12 rounded-full"
                             src="{% static 'assistente_virtual.png' %}">
                        <div class="flex flex-col gap-1 w-full max-w-[320px]">
                            <div class="flex items-center space-x-2 rtl:space-x-reverse">
                                <span class="text-sm font-semibold text-gray-900">PsiQuete</span>
                                <span class="text-sm font-normal text-gray-500">11:46</span>
                            </div>
                            <div class="flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-200 rounded-e-xl rounded-es-xl">
                                <p class="text-sm font-normal py-2.5 text-gray-900">Olá, eu sou sua assistente virtual. Como posso ajudar?</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="px-4 md:px-0">
            <div class="mx-auto bg-slate-50 mt-6 max-w-4xl px-4 py-4 sm:px-6 lg:px-8 border border-slate-200/60 rounded-md">
                <form id="form-pergunta">
                    <div class="flex items-center gap-4">
                        <input type="text"
                               name="pergunta"
                               id="pergunta"
                               placeholder="Digite sua pergunta..."
                               class="flex-1 border border-slate-300 rounded-md px-4 py-2 text-sm text-gray-800 bg-white">
                        <button type="submit"
                                class="rounded-md cursor-pointer bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                            Enviar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </main>
    <script>
        document.getElementById('form-pergunta').addEventListener('submit', async function(event){
            event.preventDefault();
            const pergunta = document.getElementById('pergunta').value
            const formData = new FormData();
            formData.append('pergunta', pergunta)
            const response = await fetch("{% url 'chat' paciente.id %}", {
                method: "POST",
                body: formData
            })
            const data = await response.json()
            const perguntaId = data.id

            const novaMensagem1 = document.createElement("div");
            novaMensagem1.className = "flex items-start gap-2.5 justify-end";
            novaMensagem1.innerHTML = `
                <div class="flex flex-col gap-1 w-full max-w-[320px] text-right">
                    <div class="flex items-center justify-end space-x-2 rtl:space-x-reverse">
                    <span class="text-sm font-normal text-gray-500">11:46</span>
                    <span class="text-sm font-semibold text-gray-900">Você</span>
                    </div>
                        <div class="flex flex-col leading-1.5 p-4 bg-indigo-200 text-gray-900 rounded-s-xl rounded-ee-xl">
                        <p class="text-sm font-normal py-2.5">
                            ${pergunta}
                        </p>
                    </div>
                </div>`;

            document.getElementById("chat").appendChild(novaMensagem1);
            
            const novaMensagem = document.createElement("div");
            novaMensagem.className = "flex items-start gap-2.5";
           
            novaMensagem.innerHTML = `
                <img class="w-12 h-12 rounded-full" src="{% static 'assistente_virtual.png' %}" alt="Pythonete">
                <div class="flex flex-col gap-1 w-full max-w-[320px]">
                    <div class="flex items-center space-x-2 rtl:space-x-reverse">
                        <span class="text-sm font-semibold text-gray-900">PsiQuete</span>
                        <span class="text-sm font-normal text-gray-500">10:00</span>
                    </div>
                    <div class="flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-200 rounded-e-xl rounded-es-xl">
                        <p id="resposta-pythonete-${perguntaId}" class="text-sm font-normal py-2.5 text-gray-900"></p>
                    </div>
                   <a href="/consultas/ver_referencias/${perguntaId}" class="text-sm font-normal text-gray-500 dark:text-gray-400">Confira as fontes</a>
                </div>
            `;

            document.getElementById("chat").appendChild(novaMensagem);
            
            const streamResponse = await fetch("{% url 'stream_response' paciente.id %}",{
                method: "POST",
                headers: {
                     "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({id_pergunta: perguntaId})
            });
            
            const reader = streamResponse.body.getReader()
            const decoder = new TextDecoder("utf-8")
            const respostaElemento = document.getElementById(`resposta-pythonete-${perguntaId}`)

            while (true){
                const {done, value} = await reader.read()
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true})
                respostaElemento.innerText += chunk

            }
        })
        
    </script>
{% endblock 'body' %}

```

..






...