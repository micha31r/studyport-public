# Generated by Django 3.2.4 on 2022-01-29 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='comparitor',
            new_name='comparator',
        ),
        migrations.AlterField(
            model_name='goal',
            name='filters',
            field=models.CharField(default='{}', max_length=255),
        ),
        migrations.AlterField(
            model_name='goal',
            name='model_name',
            field=models.CharField(choices=[('results.Result', 'Result'), ('focus.FocusPeriod', 'FocusPeriod')], max_length=255),
        ),
    ]
