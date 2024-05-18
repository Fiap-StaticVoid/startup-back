from datetime import timedelta

from celery import Celery

celery_app = Celery("server", broker="redis://redis:6379/0")


celery_app.conf.beat_schedule = {
    "rodar-lancamentos-recorrentes": {
        "task": "contextos.historico.executores.tarefas.rodar_lancamentos_recorrentes",
        "schedule": timedelta(seconds=60),
        "args": (),
    },
}
celery_app.conf.timezone = "America/Sao_Paulo"
