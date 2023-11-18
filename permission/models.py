
import sys
from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin


class Permission(BaseModelMixin):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
    is_obsolete = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = (("name", "method"),)

    def __str__(self) -> str:
        return f"{self.name} : {self.url} : {self.method}"

    @classmethod
    def is_permission_granted(cls, name, method, roles):
        '''
        If the permission is granted to any of the roles then return true else return false 
        '''
        # Permission name like customer-list, customer-create
        # Method like GET, POST
        # Roles like admin, superadmin, consumer,

        permissions = cls.objects.filter(name=name, method=method, roles__in=roles, is_obsolete=False)
        if permissions:
            return True
        return False


class Role(BaseModelMixin):
    name = models.CharField(max_length=100)
    parents = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="children",
    )
    description = models.CharField(max_length=255)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,

        related_name="roles",
    )
    is_protected = models.BooleanField(default=False)
    is_obsolete = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return self.name
