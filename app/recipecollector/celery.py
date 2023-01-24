from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipecollector.settings')

app = Celery('recipecollector')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
