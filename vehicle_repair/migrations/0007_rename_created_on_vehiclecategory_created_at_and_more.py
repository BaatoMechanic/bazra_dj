# Generated by Django 4.2.7 on 2023-12-06 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_repair', '0006_alter_vehiclerepairrequestimage_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiclecategory',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='vehiclecategory',
            old_name='modified_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='vehiclepart',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='vehiclepart',
            old_name='modified_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequest',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequest',
            old_name='modified_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequestimage',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequestimage',
            old_name='modified_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequestvideo',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='vehiclerepairrequestvideo',
            old_name='modified_on',
            new_name='modified_at',
        ),
    ]
