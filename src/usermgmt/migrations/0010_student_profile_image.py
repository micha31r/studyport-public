# Generated by Django 3.2.4 on 2022-05-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0009_auto_20220430_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_image',
            field=models.CharField(default='account', max_length=255),
        ),
    ]
