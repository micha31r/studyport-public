# Generated by Django 3.2.4 on 2022-04-24 03:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0007_auto_20220424_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('success', 'Success'), ('fail', 'Failed')], default='ongoing', max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('goal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='goal.goal')),
            ],
        ),
    ]
