

from typing import Optional

from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib import admin

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

from django.contrib.auth import get_user_model

from autho import models

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):

    def clean_email(self) -> Optional[str]:
        """
        Clean the email field and perform validations.

        Returns:
            Optional[str]: The cleaned email value, or None if email is not provided.

        Raises:
            forms.ValidationError: If the email is already taken or if neither email nor phone is provided.
        """
        email: Optional[str] = self.cleaned_data.get("email")
        phone: Optional[str] = self.cleaned_data.get("phone")

        # Check if either email or phone is provided
        if not email and not phone:
            self.add_error(
                "phone",
                "Either of both of 'email and mobile' is required to create an user."
            )
        # Check if email is already taken
        elif email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")

        return email

    def clean_phone(self) -> Optional[str]:
        """
        Clean the phone field and perform validations.

        Returns:
            Optional[str]: The cleaned phone value, or None if phone is not provided.

        Raises:
            forms.ValidationError: If the phone is already taken or if neither email nor phone is provided.
        """
        email: Optional[str] = self.cleaned_data.get("email")
        phone: Optional[str] = self.cleaned_data.get("phone")

        # Check if either email or phone is provided
        if not email and not phone:
            self.add_error(
                "email",
                "Either of both of 'email and mobile' is required to create an user."
            )
        # Check if phone is already taken
        elif phone and User.objects.filter(mobile=phone).exists():
            raise forms.ValidationError("User with this mobile already exists.")

        return phone


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = []


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    filter_horizontal = ('groups', 'user_permissions', 'roles')
    ordering = ('email', 'name')
    list_display = ("idx", "email", "phone", "name", "is_staff")
    search_fields = ("email", "name")
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {"fields": ("password", "email", "phone")}),
        (("Personal info"), {"fields": ("name", "gender", "dob_type", "dob")}),
        (None, {"fields": ("image", "auth_provider", )}),
        (("Roles"), {"fields": ("primary_role", "roles")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_email_verified",
                    "is_mobile_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_obsolete",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "verified_on")}),
    )


admin.site.register(User, UserAdmin)


@admin.register(models.RatingAndReview)
class RatingAndReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_by', 'rating', 'review')
    readonly_fields = ('user', 'review_by', 'rating', 'review')


@admin.register(models.MechanicProfile)
class MechanicAttributeAdmin(admin.ModelAdmin):
    list_display = ('mechanic', 'vehicle_speciality', 'vehicle_part_speciality')
