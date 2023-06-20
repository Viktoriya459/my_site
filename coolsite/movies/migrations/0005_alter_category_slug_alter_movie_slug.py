# Generated by Django 4.2.1 on 2023-06-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_category_slug_movie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
    ]
