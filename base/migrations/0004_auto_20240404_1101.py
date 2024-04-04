# Generated by Django 3.2.19 on 2024-04-04 11:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_room_host'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='participaion',
            field=models.ManyToManyField(blank=True, related_name='participaion', to=settings.AUTH_USER_MODEL),
        ),
    ]
