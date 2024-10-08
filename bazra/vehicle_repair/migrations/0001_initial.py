# Generated by Django 4.2.7 on 2024-02-20 05:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mechanic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("description", models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RepairStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("name", models.CharField(max_length=255)),
                ("text_description", models.CharField(blank=True, max_length=500, null=True)),
                ("audio_description", models.FileField(blank=True, null=True, upload_to="repair_steps")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In_progress"),
                            ("complete", "Complete"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=500)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("body_repair", "Body_repair"),
                            ("engine_repair", "Engine_repair"),
                            ("electric_repair", "Electric_repair"),
                            ("wheell_repair", "Wheell_repair"),
                            ("painting", "Painting"),
                            ("other", "Other"),
                        ],
                        default="engine_repair",
                        max_length=50,
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="service/icons")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VehicleCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=500)),
                ("image", models.ImageField(blank=True, null=True, upload_to="vehicle_categories")),
            ],
            options={
                "verbose_name": "vehicle category",
                "verbose_name_plural": "vehicle categories",
            },
        ),
        migrations.CreateModel(
            name="VehicleRepairRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("waiting_for_user_acceptance", "Waiting_for_user_acceptance"),
                            ("waiting_for_advance_payment", "Waiting_for_advance_payment"),
                            ("waiting_for_mechanic", "Waiting_for_mechanic"),
                            ("in_progress", "In_progress"),
                            ("halt", "Halt"),
                            ("waiting_for_completion_acceptance", "Waiting_for_completion_acceptance"),
                            ("complete", "Complete"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=255,
                    ),
                ),
                (
                    "advance_payment_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("complete", "Complete"),
                            ("payment_on_arrival", "Payment_on_arrival"),
                        ],
                        default="pending",
                        max_length=255,
                    ),
                ),
                ("location", models.JSONField(default=dict)),
                (
                    "assigned_mechanic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_repairs_assigned_mechanic",
                        to="vehicle_repair.mechanic",
                    ),
                ),
                (
                    "preferred_mechanic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vehicle_repairs_preferred_mechanic",
                        to="vehicle_repair.mechanic",
                    ),
                ),
                (
                    "service_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_repair",
                        to="vehicle_repair.service",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_repair_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_repair",
                        to="vehicle_repair.vehiclecategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VehicleRepairRequestVideo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("video", models.ImageField(upload_to="vehicle_repair_request/videos")),
                (
                    "repair_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="videos",
                        to="vehicle_repair.vehiclerepairrequest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VehicleRepairRequestImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("image", models.ImageField(upload_to="vehicle_repair_request/images")),
                (
                    "repair_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="vehicle_repair.vehiclerepairrequest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VehiclePart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=500)),
                ("image", models.ImageField(blank=True, null=True, upload_to="vehicle_parts")),
                ("is_multiple", models.BooleanField(default=False)),
                ("position", models.CharField(max_length=255)),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_parts",
                        to="vehicle_repair.vehiclecategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="service",
            name="parts_included",
            field=models.ManyToManyField(related_name="services", to="vehicle_repair.vehiclepart"),
        ),
        migrations.AddField(
            model_name="service",
            name="vehicles_included",
            field=models.ManyToManyField(related_name="services", to="vehicle_repair.vehiclecategory"),
        ),
        migrations.CreateModel(
            name="RepairStepReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                (
                    "repair_step",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="report",
                        to="vehicle_repair.repairstep",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RepairStepBillImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                ("image", models.ImageField(upload_to="repair_steps/bill_images")),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bill_images",
                        to="vehicle_repair.repairstepreport",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="repairstep",
            name="repair_request",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="repair_steps",
                to="vehicle_repair.vehiclerepairrequest",
            ),
        ),
        migrations.CreateModel(
            name="RatingAndReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                (
                    "rating",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("review", models.TextField()),
                (
                    "repair_request",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="review_and_ratings",
                        to="vehicle_repair.vehiclerepairrequest",
                    ),
                ),
                (
                    "review_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating_and_reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="mechanic",
            name="service_speciality",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="vehicle_repair.service"
            ),
        ),
        migrations.AddField(
            model_name="mechanic",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mechanic_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="mechanic",
            name="vehicle_speciality",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="vehicle_repair.vehiclecategory"
            ),
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idx", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_obsolete", models.BooleanField(db_index=True, default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]