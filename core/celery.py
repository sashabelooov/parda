# core/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-telegram-report-daily': {
        'task': 'parda.tasks.export_to_telegram_task',
        'schedule': crontab(hour=19, minute=30),  # Har kuni soat 19:00 da
    },
}

app.conf.timezone = 'Asia/Tashkent'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')