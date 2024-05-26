from django.db import models
from Spec.models import Category, Quality, Genre
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from Movie.make_slug import unique_slug_generator

# Create your models here.

class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=255, null=True, blank=True)
    adult = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, editable=True, blank=True)
    quality = models.ForeignKey(Quality, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.ManyToManyField(Genre, editable=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.CharField(max_length=10000, null=True, blank=True)
    release_date = models.CharField(max_length=255, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.ImageField(upload_to='posters/movie', null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True, help_text = "Leave Blank")
    is_published = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/movie/{self.slug}/'

    def __str__(self):
        return self.tmdb_id

@receiver(pre_save, sender=Movie)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)