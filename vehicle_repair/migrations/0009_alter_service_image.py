# Generated by Django 4.2.7 on 2023-12-10 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_repair', '0008_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='service/icons'),
        ),
    ]
