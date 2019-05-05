from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django_dict import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_dict.settings')

app = Celery('django_dict', broker=settings.BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
