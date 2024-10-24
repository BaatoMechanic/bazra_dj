# Generated by Django 5.1.1 on 2024-10-12 12:36

import utils.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicle_repair", "0007_alter_vehiclerepairrequest_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repairstepbillimage",
            name="image",
            field=models.ImageField(storage=utils.storage.PrivateMediaStorage(), upload_to="repair_steps/bill_images"),
        ),
        migrations.AlterField(
            model_name="vehiclerepairrequestimage",
            name="image",
            field=models.ImageField(
                storage=utils.storage.PrivateMediaStorage(), upload_to="vehicle_repair_request/images"
            ),
        ),
    ]