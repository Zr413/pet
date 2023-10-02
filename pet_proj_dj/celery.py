import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_proj_dj.settings')

app = Celery('pet_proj_dj')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'blog.tasks.send_email_every_monday',
        'schedule': crontab(),
        # 'args': (), hour=8, minute=0, day_of_week='monday'
    },
}