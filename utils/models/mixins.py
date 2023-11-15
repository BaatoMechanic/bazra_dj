from django.db import models

from shortuuidfield import ShortUUIDField


class BaseModel(models.Model):
    idx = ShortUUIDField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_obsolete = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True
