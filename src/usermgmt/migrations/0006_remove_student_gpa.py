# Generated by Django 3.2.4 on 2022-04-26 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0005_auto_20220426_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='gpa',
        ),
    ]
