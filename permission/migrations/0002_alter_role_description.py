# Generated by Django 4.2.7 on 2023-11-25 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
