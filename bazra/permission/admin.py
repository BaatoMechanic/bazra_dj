from django.contrib import admin

from permission.models import Permission, Role

# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url", "method", "is_obsolete")
    search_fields = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "permissions",
        "parents",
    )
    search_fields = ("name",)
