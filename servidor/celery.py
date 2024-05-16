from celery import Celery
from celery.schedules import crontab

celery_app = Celery("server", broker="redis://redis:6379/0")

celery_app.conf.beat_schedule = {
    "rodar-lancamentos-recorrentes": {
        "task": "contextos.historico.executores.tarefas.rodar_lancamentos_recorrentes",
        "schedule": crontab(minute=1),
        "args": (),
    },
}
celery_app.conf.timezone = "UTC"
