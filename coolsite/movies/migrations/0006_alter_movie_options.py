# Generated by Django 4.2.1 on 2023-06-20 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_category_slug_alter_movie_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['time_create', 'title'], 'verbose_name': 'Кращі кінофільми', 'verbose_name_plural': 'Кращі кінофільми'},
        ),
    ]