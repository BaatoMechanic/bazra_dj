from django.db import models

from utils.models.mixins import BaseModel


class UserBlackList(BaseModel):

    email = models.EmailField(blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=16, unique=True)
    created_by = models.ForeignKey(
        "autho.User",
        related_name="blacklist_creators",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        "autho.User", related_name="blacklist_modifiers", on_delete=models.SET_NULL, null=True)
    modified_on = models.DateTimeField(auto_now=True)
    removed_by = models.ForeignKey(
        "autho.User", related_name="blacklist_removers", on_delete=models.SET_NULL, null=True)
    removed_on = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False, db_index=True)
    remarks = models.CharField(max_length=150)

    @classmethod
    def exists(cls, email=None, mobile=None):
        queryset = cls.objects.filter(is_removed=False)
        if email:
            if queryset.filter(email=email).exists():
                raise Exception("Email address is blacklist")
        elif mobile:
            if queryset.filter(mobile=mobile).exists():
                raise Exception("Mobile number is blacklist")

        else:
            raise Exception("Email or mobile is required")

        return False
