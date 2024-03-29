# Generated by Django 3.2.4 on 2022-04-26 02:34

from django.db import migrations, models
import usermgmt.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0006_remove_student_gpa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='viewing_year_level',
            new_name='viewing_year',
        ),
        migrations.AlterField(
            model_name='student',
            name='year_joined',
            field=models.DateField(default=usermgmt.models.get_year),
        ),
    ]
