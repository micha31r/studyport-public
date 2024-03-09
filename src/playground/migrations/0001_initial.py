# Generated by Django 3.2.4 on 2022-01-27 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New Playground', max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermgmt.student')),
            ],
            options={
                'ordering': ['student__user__last_name', 'student__user__first_name', '-timestamp'],
            },
        ),
    ]