# Generated by Django 4.2.7 on 2024-01-21 17:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle_repair', '0016_remove_vehiclerepairrequest_vehicle_part_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingAndReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField()),
                ('repair_request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_and_ratings', to='vehicle_repair.vehiclerepairrequest')),
                ('review_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_and_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('service_speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle_repair.service')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mechanic_profile', to=settings.AUTH_USER_MODEL)),
                ('vehicle_speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle_repair.vehiclecategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
