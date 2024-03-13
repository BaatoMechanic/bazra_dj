from django.contrib import admin
from django.utils.html import format_html
from vehicle_repair import models

# Register your models here.


@admin.register(models.VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "description")


@admin.register(models.VehiclePart)
class VehiclePartAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "vehicle_type", "position", "is_multiple")


class VehicleRepairRequestImageInline(admin.TabularInline):
    model = models.VehicleRepairRequestImage
    max_num = 1


@admin.register(models.MechanicTip)
class MechanicTipAdmin(admin.ModelAdmin):
    list_display = (
        "mechanic",
        "tip",
    )


class VehicleRepairRequestVideoInline(admin.TabularInline):
    model = models.VehicleRepairRequestVideo
    max_num = 1


@admin.register(models.VehicleRepairRequest)
class VehicleRepairRequestAdmin(admin.ModelAdmin):
    list_display = ("idx", "title", "vehicle_type", "service_type", "status")
    readonly_fields = (
        "title",
        "description",
        "user",
        "preferred_mechanic",
        "vehicle_type",
        "service_type",
        "location",
    )
    inlines = [VehicleRepairRequestImageInline, VehicleRepairRequestVideoInline]


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "type")
    filter_horizontal = ("parts_included", "vehicles_included")


class VehicleRepairRequestImageInline(admin.TabularInline):
    model = models.VehicleRepairRequestImage
    max_num = 1


@admin.register(models.RepairStep)
class RepairStepAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "status")


class RepairStepBillImageInline(admin.TabularInline):
    model = models.RepairStepBillImage
    extra = 0
    readonly_fields = ("thumbnail",)

    def thumbnail(self, instance):
        if instance.image.name:
            return format_html(
                f'<img src="{instance.image.url}" width="100", object-fit="cover"  />'
            )
        else:
            return ""


@admin.register(models.RepairStepReport)
class RepairStepReportAdmin(admin.ModelAdmin):
    model = models.RepairStepReport
    list_display = ("idx",)
    inlines = [
        RepairStepBillImageInline,
    ]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("idx", "name")

    def name(self, obj):
        return obj.user.name


@admin.register(models.Mechanic)
class MechanicAttributeAdmin(admin.ModelAdmin):
    list_display = ("idx", "vehicle_speciality", "service_speciality")


@admin.register(models.RatingAndReview)
class RatingAndReviewAdmin(admin.ModelAdmin):
    list_display = ("idx", "review_by", "rating", "review")
    readonly_fields = ("user", "review_by", "rating", "review")
