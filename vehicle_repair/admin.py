from django.contrib import admin
from django.utils.html import format_html
from vehicle_repair.models import VehicleCategory, VehiclePart, VehicleRepairRequest
from vehicle_repair.models.repair_step import RepairStep, RepairStepBillImage, RepairStepReport
from vehicle_repair.models.service import Service
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo

# Register your models here.


@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "description")


@admin.register(VehiclePart)
class VehiclePartAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "vehicle_type", "position", "is_multiple")


class VehicleRepairRequestImageInline(admin.TabularInline):
    model = VehicleRepairRequestImage
    max_num = 1


class VehicleRepairRequestVideoInline(admin.TabularInline):
    model = VehicleRepairRequestVideo
    max_num = 1


@admin.register(VehicleRepairRequest)
class VehicleRepairRequestAdmin(admin.ModelAdmin):
    list_display = ("idx", "title", "vehicle_type", "service_type", "status")
    readonly_fields = ("title", "description", "user", "preferred_mechanic",
                       "assigned_mechanic", "vehicle_type", "service_type")
    inlines = [VehicleRepairRequestImageInline, VehicleRepairRequestVideoInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "type")
    filter_horizontal = ("parts_included", "vehicles_included")


class VehicleRepairRequestImageInline(admin.TabularInline):
    model = VehicleRepairRequestImage
    max_num = 1


@admin.register(RepairStep)
class RepairStepAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "status")


class RepairStepBillImageInline(admin.TabularInline):
    model = RepairStepBillImage
    extra = 0
    readonly_fields = ("thumbnail",)

    def thumbnail(self, instance):
        if instance.image.name:
            return format_html(f'<img src="{instance.image.url}" width="100", object-fit="cover"  />')
        else:
            return ""


@admin.register(RepairStepReport)
class RepairStepReportAdmin(admin.ModelAdmin):
    model = RepairStepReport
    list_display = ("idx",)
    inlines = [RepairStepBillImageInline,]
