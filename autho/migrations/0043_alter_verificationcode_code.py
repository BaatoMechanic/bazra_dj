# Generated by Django 4.2.7 on 2023-12-15 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0042_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=538949, max_length=6),
        ),
    ]
