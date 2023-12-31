# Generated by Django 4.2.7 on 2023-11-26 08:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0024_rename_mechanicattribute_mechanicprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mechanicprofile',
            name='mechanic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mechanic_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=222612, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 26, 8, 57, 36, 563379, tzinfo=datetime.timezone.utc)),
        ),
    ]
