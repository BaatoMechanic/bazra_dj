# Generated by Django 4.2.7 on 2023-11-25 16:29

from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_repair', '0003_alter_vehiclerepairrequest_preferred_mechanic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleRepairRequestImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('image', models.ImageField(upload_to='vehicle_repair_request/images', validators=[utils.validators.validate_file_size])),
                ('vehicle_repair_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vehicle_repair.vehiclerepairrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
