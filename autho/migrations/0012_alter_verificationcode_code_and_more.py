# Generated by Django 4.2.7 on 2023-11-25 04:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0011_alter_verificationcode_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=557370, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 4, 13, 55, 657288, tzinfo=datetime.timezone.utc)),
        ),
    ]
