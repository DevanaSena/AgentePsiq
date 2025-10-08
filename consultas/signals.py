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