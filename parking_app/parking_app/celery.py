import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_app.settings')

app = Celery('parking_app')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()