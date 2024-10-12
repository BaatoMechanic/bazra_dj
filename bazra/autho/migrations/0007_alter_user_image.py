# Generated by Django 5.1.1 on 2024-10-12 12:36

import utils.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("autho", "0006_verificationcode_meta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True, null=True, storage=utils.storage.PrivateMediaStorage(), upload_to="users/profile"
            ),
        ),
    ]
