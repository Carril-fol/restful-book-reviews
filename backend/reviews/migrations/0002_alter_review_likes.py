# Generated by Django 5.0.1 on 2024-02-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes_reviews', to='profiles.profile'),
        ),
    ]
