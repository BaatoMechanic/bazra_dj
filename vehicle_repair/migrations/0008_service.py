# Generated by Django 4.2.7 on 2023-12-10 01:01

from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_repair', '0007_rename_created_on_vehiclecategory_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('body_repair', 'Body_repair'), ('engine_repair', 'Engine_repair'), ('electric_repair', 'Electric_repair'), ('wheell_repair', 'Wheell_repair'), ('painting', 'Painting'), ('other', 'Other')], default='engine_repair', max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_image')),
                ('parts_included', models.ManyToManyField(related_name='services', to='vehicle_repair.vehiclepart')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]