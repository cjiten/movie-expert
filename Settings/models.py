from django.db import models

# Create your models here.

class Org(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    tmdb_token = models.CharField(max_length=500, null=True, blank=True)
    link_section = models.BooleanField(default=False)
    preview_img = models.ImageField(upload_to='', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name