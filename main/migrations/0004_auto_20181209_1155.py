# Generated by Django 2.1.1 on 2018-12-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181021_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itr',
            name='sem',
            field=models.CharField(choices=[('FA', 'Fall'), ('SP', 'Spring'), ('SU', 'Summer'), ('WI', 'Winter')], default='FA', max_length=2, verbose_name='Semester'),
        ),
    ]
