from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from Spec.make_slug import unique_slug_generator

import uuid

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True, help_text = "Leave Blank")

    def get_absolute_url(self):
        return f'/category/{self.slug}/'

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

class Quality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True, help_text = "Leave Blank")
    genre_id = models.CharField(max_length=255)

    def get_absolute_url(self):
        return f'/genre/{self.slug}/'

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Genre)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
class Link(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=2500, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_absolute_url(self):
        return f'/link/{self.uuid}/send/'

    def __str__(self):
        return self.name