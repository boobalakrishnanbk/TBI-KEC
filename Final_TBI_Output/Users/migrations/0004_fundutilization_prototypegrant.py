# Generated by Django 4.0.4 on 2022-06-01 16:22

import Users.functions
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_remove_fundutilization_prototypegrant'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundutilization',
            name='prototypeGrant',
            field=models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Only numbers are allowed', regex='^[0-9,]*$'), Users.functions.MinValueValidators], verbose_name='Prototype Grant'),
        ),
    ]