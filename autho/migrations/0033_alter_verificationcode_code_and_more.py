# Generated by Django 4.2.7 on 2023-12-10 01:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0032_alter_user_additional_attributes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=537797, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 1, 6, 29, 266407, tzinfo=datetime.timezone.utc)),
        ),
    ]