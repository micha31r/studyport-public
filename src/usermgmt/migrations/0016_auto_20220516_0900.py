# Generated by Django 3.2.4 on 2022-05-15 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0008_remove_assessment_weighting'),
        ('usermgmt', '0015_auto_20220513_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='assessments',
            field=models.ManyToManyField(blank=True, to='standards.Assessment'),
        ),
        migrations.AlterField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='standards.Subject'),
        ),
    ]
