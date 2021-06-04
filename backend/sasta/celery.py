from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

import logging
logger = logging.getLogger('sasta')

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sasta.settings')
app = Celery('sasta')
#  broker=settings.CELERY_BROKER_URL,
#              backend=settings.CELERY_BACKEND)
logger.info(settings.CELERY_BROKER_URL)
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
