# Generated by Django 4.2.7 on 2023-11-26 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0025_alter_mechanicprofile_mechanic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=367679, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 26, 9, 2, 28, 308880, tzinfo=datetime.timezone.utc)),
        ),
    ]