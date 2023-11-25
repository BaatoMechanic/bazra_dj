# Generated by Django 4.2.7 on 2023-11-25 04:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_repair', '0001_initial'),
        ('autho', '0010_alter_user_roles_alter_verificationcode_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=447386, max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 4, 8, 15, 98494, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='MechanicAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('mechanic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mechanic_attribute', to=settings.AUTH_USER_MODEL)),
                ('vehicle_part_speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle_repair.vehiclepart')),
                ('vehicle_speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle_repair.vehiclecategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]