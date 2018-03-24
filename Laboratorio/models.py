from django.db import models

# Create your models here.

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()

class Document(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='')