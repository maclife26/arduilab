from django.db import models

# Create your models here.

class Document(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='')