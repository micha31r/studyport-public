# Generated by Django 3.2.4 on 2022-04-24 06:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0005_alter_assessment_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='weighting',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]