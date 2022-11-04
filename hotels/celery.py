from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','hotels.settings')

app=Celery('hotels')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

#celery beat settings
app.conf.beat_schedule={
    'send-mail-everyday-at-this-time':{
        'task':'contact.tasks.send_mail_everyday',
        'schedule': crontab(hour=16,minute=40)
        #'args':(any_argument,)
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
