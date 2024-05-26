from django.db import models

import uuid

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    my_uuid = models.UUIDField(default=uuid.uuid4)
    
    def __str__(self):
        return self.name

class ClientLink(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    link = models.URLField(max_length=5000)
    
    def __str__(self):
        return self.link