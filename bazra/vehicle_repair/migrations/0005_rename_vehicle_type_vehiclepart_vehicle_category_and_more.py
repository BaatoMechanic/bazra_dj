# Generated by Django 4.2.7 on 2024-07-25 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vehicle_repair", "0004_alter_vehiclerepairrequestvideo_video"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vehiclepart",
            old_name="vehicle_type",
            new_name="vehicle_category",
        ),
        migrations.RenameField(
            model_name="vehiclerepairrequest",
            old_name="service_type",
            new_name="service",
        ),
        migrations.RenameField(
            model_name="vehiclerepairrequest",
            old_name="vehicle_type",
            new_name="vehicle_category",
        ),
    ]