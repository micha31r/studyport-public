# Generated by Django 3.2.4 on 2022-04-24 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0006_alter_assessment_weighting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assessment_code',
            field=models.CharField(max_length=5),
        ),
    ]
