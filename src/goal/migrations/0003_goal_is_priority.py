# Generated by Django 3.2.4 on 2022-01-29 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0002_auto_20220129_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='is_priority',
            field=models.BooleanField(default=False),
        ),
    ]