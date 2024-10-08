# Generated by Django 4.2.7 on 2024-03-24 11:54

from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("vehicle_repair", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ratingandreview",
            name="repair_request",
        ),
        migrations.AddField(
            model_name="mechanic",
            name="occupied",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="ratingandreview",
            name="content_type",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ratingandreview",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="icon_data",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="vehiclerepairrequest",
            name="advance_charge",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.CreateModel(
            name="MechanicTip",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("tip", models.CharField(max_length=500)),
                (
                    "mechanic",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mechanic_tips",
                        to="vehicle_repair.mechanic",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
