# Generated by Django 3.1.7 on 2021-03-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_app', '0002_auto_20210310_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
