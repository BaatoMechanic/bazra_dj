# Generated by Django 4.2.7 on 2023-12-22 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0055_rename_is_mobile_verified_user_is_phone_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default='', max_length=6),
        ),
    ]