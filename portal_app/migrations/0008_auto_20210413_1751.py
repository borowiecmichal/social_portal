# Generated by Django 3.1.7 on 2021-04-13 17:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal_app', '0007_auto_20210413_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupe',
            name='to_join',
            field=models.ManyToManyField(null=True, related_name='groups_to_join', to=settings.AUTH_USER_MODEL),
        ),
    ]
