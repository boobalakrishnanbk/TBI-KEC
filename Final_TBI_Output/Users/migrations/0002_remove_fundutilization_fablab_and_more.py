# Generated by Django 4.0.4 on 2022-06-01 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundutilization',
            name='fabLab',
        ),
        migrations.RemoveField(
            model_name='fundutilization',
            name='operationExpenditure',
        ),
    ]
