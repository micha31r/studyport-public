# Generated by Django 3.2.4 on 2022-05-09 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0015_alter_goal_completion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
