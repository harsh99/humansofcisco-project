# Generated by Django 3.0.5 on 2020-05-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='reactcount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='story',
            name='viewcount',
            field=models.IntegerField(default=0),
        ),
    ]
