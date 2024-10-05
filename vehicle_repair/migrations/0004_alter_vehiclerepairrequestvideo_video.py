# Generated by Django 4.2.7 on 2024-07-17 21:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicle_repair", "0003_vehiclerepairrequest_service_charge"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehiclerepairrequestvideo",
            name="video",
            field=models.FileField(
                null=True,
                upload_to="vehicle_repair_request/videos",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                    )
                ],
            ),
        ),
    ]
