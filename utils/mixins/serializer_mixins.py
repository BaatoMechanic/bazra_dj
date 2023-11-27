from shortuuidfield import ShortUUIDField

from rest_framework import serializers


class BaseModelSerializerMixin(serializers.ModelSerializer):
    # idx = serializers.CharField(read_only=True)
    idx = ShortUUIDField()

    class Meta:

        exclude = ("id", "modified_on", "is_obsolete")
        extra_kwargs = {
            "created_on": {"read_only": True},
            "modified_on": {"read_only": True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.PrimaryKeyRelatedField):
                related_instance = getattr(instance, field_name)
                representation[field_name] = getattr(related_instance, "idx", related_instance.id)
        return representation
