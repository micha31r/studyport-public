# Generated by Django 3.2.4 on 2022-04-24 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0004_alter_assessment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='points',
            field=models.FloatField(blank=True, null=True),
        ),
    ]