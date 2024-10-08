# Generated by Django 5.0.6 on 2024-05-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('telegram', models.CharField(blank=True, max_length=255, null=True)),
                ('tmdb_token', models.CharField(blank=True, max_length=500, null=True)),
                ('link_section', models.BooleanField(default=False)),
                ('preview_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
