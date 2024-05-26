from django.db import models
from Spec.models import Category, Quality, Genre
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from Movie.make_slug import unique_slug_generator

# Create your models here.

class Series(models.Model):
    tmdb_id = models.CharField(max_length=255)
    adult = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, editable=True, blank=True)
    quality = models.ForeignKey(Quality, on_delete=models.DO_NOTHING, null=True, blank=True)
    genre = models.ManyToManyField(Genre, editable=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.CharField(max_length=10000, null=True, blank=True)
    release_date = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.ImageField(upload_to='posters/tv/series', null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True, help_text = "Leave Blank")
    is_published = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/tv/{self.slug}/'

    def __str__(self):
        return self.title
    
@receiver(pre_save, sender=Series)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Season(models.Model):
    series = models.ForeignKey(Series, editable=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.CharField(max_length=10000, null=True, blank=True)
    season_number = models.IntegerField(null=True, blank=True)
    release_date = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.ImageField(upload_to='posters/tv/season', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)


    def get_absolute_url(self):
        return f'/tv/{self.series.slug}/season/{self.season_number}/'

    def __str__(self):
        return f'{self.series.title} - {self.title}'


class Episode(models.Model):
    season = models.ForeignKey(Season, editable=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.CharField(max_length=10000, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    release_date = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.ImageField(upload_to='posters/tv/episode', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)


    def get_absolute_url(self):
        return f'/tv/{self.season.series.slug}/season/{self.season.season_number}/episode/{self.episode_number}/'

    def __str__(self):
        return self.title