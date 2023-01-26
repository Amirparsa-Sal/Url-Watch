import os
from celery import Celery
from datetime import timedelta
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_watch.settings")
app = Celery("url_watch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'monitor': {
        'task': 'url_monitor',
        'schedule': timedelta(seconds=settings.MONITORING_INTERVAL),
    },
} 