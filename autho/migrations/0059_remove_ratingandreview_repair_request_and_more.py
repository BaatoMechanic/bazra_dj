# Generated by Django 4.2.7 on 2024-01-21 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0058_remove_mechanicprofile_vehicle_part_speciality_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratingandreview',
            name='repair_request',
        ),
        migrations.RemoveField(
            model_name='ratingandreview',
            name='review_by',
        ),
        migrations.RemoveField(
            model_name='ratingandreview',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='additional_attributes',
        ),
        migrations.DeleteModel(
            name='MechanicProfile',
        ),
        migrations.DeleteModel(
            name='RatingAndReview',
        ),
    ]