# Generated by Django 3.2.4 on 2022-04-20 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assessment_type',
            field=models.CharField(choices=[('i', 'Internal'), ('e', 'External')], default='i', max_length=1),
        ),
    ]