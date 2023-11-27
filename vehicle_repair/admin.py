from django.contrib import admin

from vehicle_repair.models import VehicleCategory, VehiclePart, VehicleRepairRequest
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo

# Register your models here.


@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(VehiclePart)
class VehiclePartAdmin(admin.ModelAdmin):
    list_display = ("name", "vehicle_type", "position", "is_multiple")


class VehicleRepairRequestImageInline(admin.TabularInline):
    model = VehicleRepairRequestImage
    max_num = 1


class VehicleRepairRequestVideoInline(admin.TabularInline):
    model = VehicleRepairRequestVideo
    max_num = 1


@admin.register(VehicleRepairRequest)
class VehicleRepairRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "vehicle_type", "vehicle_part", "status")
    readonly_fields = ("title", "description", "status", "user", "preferred_mechanic",
                       "assigned_mechanic", "vehicle_type", "vehicle_part")
    inlines = [VehicleRepairRequestImageInline, VehicleRepairRequestVideoInline]
