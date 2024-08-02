from shortuuidfield import ShortUUIDField

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import get_attribute, is_simple_callable


class IDXOnlyObject:
    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return "%s" % self.idx


class IdxRelatedField(serializers.PrimaryKeyRelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid idx "{pk_value}" - object does not exist.'),
        "incorrect_type": _(
            "Incorrect type. Expected idx value, received {data_type}."
        ),
    }

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            # Optimized case, return a mock object only containing the pk attribute.
            try:
                instance = get_attribute(instance, self.source_attrs[:-1])
                value = instance.serializable_value(self.source_attrs[-1])
                if is_simple_callable(value):
                    # Handle edge case where the relationship `source` argument
                    # points to a `get_relationship()` method on the model
                    value = value().idx
                else:
                    value = getattr(instance, self.source_attrs[-1]).idx
                return IDXOnlyObject(idx=value)
            except AttributeError:
                pass

    def to_representation(self, obj):
        return obj.idx

    def to_internal_value(self, data):
        try:
            return self.queryset.get(idx=data)
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)


class BaseModelSerializerMixin(serializers.ModelSerializer):
    serializer_related_field = IdxRelatedField
    idx = ShortUUIDField()

    class Meta:
        serializers = {}

        exclude = ("id", "modified_at", "is_obsolete")
        extra_kwargs = {
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.PrimaryKeyRelatedField):
                related_instance = getattr(instance, field_name, None)
                if not related_instance:
                    continue
                if hasattr(self.Meta, "serializers") and self.Meta.serializers.get(
                    field_name
                ):
                    serializer = self.Meta.serializers.get(field_name)
                    representation[field_name] = serializer(related_instance).data
                else:
                    representation[field_name] = getattr(
                        related_instance, "idx", related_instance.id
                    )
            elif isinstance(field, serializers.ManyRelatedField):
                related_instances = getattr(instance, field_name).all()
                representation[field_name] = [
                    getattr(related_instance, "idx", related_instance.id)
                    for related_instance in related_instances
                ]
        return representation
