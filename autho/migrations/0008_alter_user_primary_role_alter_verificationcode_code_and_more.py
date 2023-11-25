# Generated by Django 4.2.7 on 2023-11-22 16:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
        ('autho', '0007_alter_verificationcode_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='primary_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='permission.role'),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=142689, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 16, 57, 7, 906771, tzinfo=datetime.timezone.utc)),
        ),
    ]