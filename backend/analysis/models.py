from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    user = models.ForeignKey(User, related_name='files')
    # name of the uploaded file
    name = models.CharField(max_length=255)
    content = models.FileField(upload_to='files')
    # current processing status
    status = models.CharField(max_length=50)
