import os
import uuid

from django.contrib.auth.models import User
from django.db import models

def get_file_path(instance, filename):
    return os.path.join('files', 'uploads', f'{uuid.uuid4()}', filename)

class File(models.Model):
    # TODO: users
    #user = models.ForeignKey(User, related_name='files', on_delete=models.PROTECT)
    # name of the uploaded file
    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=get_file_path)
    # current processing status
    status = models.CharField(max_length=50)
