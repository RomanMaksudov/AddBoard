import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')

app = Celery('board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_morning': {
        'task': 'board.tasks.send_message',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
}
