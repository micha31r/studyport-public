# Generated by Django 4.0.6 on 2022-08-01 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0020_remove_student_assessments_remove_student_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
