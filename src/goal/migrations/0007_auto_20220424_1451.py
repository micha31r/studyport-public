# Generated by Django 3.2.4 on 2022-04-24 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0006_goal_current'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='end_date_option',
        ),
        migrations.AddField(
            model_name='goal',
            name='end_option',
            field=models.CharField(choices=[('before', 'End before'), ('on', 'End on')], default='before', max_length=255),
        ),
    ]