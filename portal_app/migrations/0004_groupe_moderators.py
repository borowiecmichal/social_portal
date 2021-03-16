# Generated by Django 3.1.7 on 2021-03-16 20:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal_app', '0003_auto_20210314_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupe',
            name='moderators',
            field=models.ManyToManyField(related_name='moderating_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
