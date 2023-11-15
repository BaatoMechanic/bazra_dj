from django.contrib import admin

from autho.models.user import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
