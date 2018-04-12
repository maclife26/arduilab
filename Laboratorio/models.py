from django.db import models

# Create your models here.

from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor



executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler( executors=executors, job_defaults=job_defaults)
scheduler.start()


class Document(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='')