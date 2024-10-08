from typing import Any, Dict, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.fields import get_attribute, is_simple_callable


class IDXOnlyObject(object):
    """
    This is a mock object, used for when we only need the idx of the object
    instance, but still want to return an object with a .idx attribute,
    in order to keep the same interface as a regular model instance.
    """

    def __init__(self, idx):
        self.pk = idx

    def __str__(self):
        return "%s" % self.idx


class BPrimaryRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, obj):
        return obj.idx

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(idx=data)
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

        return super().to_internal_value(data)

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            try:
                instance = get_attribute(instance, self.source_attrs[:-1])
                value = instance.serializable_value(self.source_attrs[-1])
                if is_simple_callable(value):
                    value = value().idx
                else:
                    value = getattr(instance, self.source_attrs[-1]).idx
                return IDXOnlyObject(idx=value)
            except AttributeError:
                pass


class DetailRelatedField(serializers.RelatedField):
    """
    A custom related field for representing detailed related data.
    """

    ModelType = TypeVar("ModelType")

    def __init__(self, model: ModelType | None = None, **kwargs: Dict[str, Any]) -> None:
        """
        Initializes the BDetailRelatedField.
        Args:
        - model: The related model.
        - **kwargs: Additional keyword arguments.
        Keyword Args:
        - read_only: Indicates if the field is read-only.
        - lookup: The lookup field.
        - is_method: Indicates if the representation attribute is a method.
        - representation: The representation attribute.
        - source: The related object source.
        """
        if kwargs.get("write_only"):
            if not model:
                # set tempoaray queryset to avoid getting no queryset error during super().__init__. Queryset will
                # be set during binding in bind() method below
                # I did this because field has not been initialized yet and we don't have the parent access here
                self.queryset = QuerySet()
                self.is_queryset_set = False
            else:
                self.queryset = model.objects.all()
                self.is_queryset_set = True
        else:
            kwargs["read_only"] = True
        self.lookup = kwargs.pop("lookup", None) or "idx"
        self.is_method = kwargs.pop("is_method", False)
        try:
            self.representation_attribute = kwargs.pop("representation")
            # If no source is present then it means that the value is directly accessible from the object.
            # Here source means the related object.
            # Also if source is absent then give representation as source to parent class as source is required
            # for the Related Field.
            """
            Example: if representation="user.name" then no need for source. but if representation="name" then
            need to pass source as "user"
            """
            self.no_source = False
            if not kwargs.get("source"):
                self.no_source = True
                kwargs["source"] = self.representation_attribute
        except KeyError:
            raise Exception("Please provide the representation attribute")
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        if self.write_only and not self.is_queryset_set:
            model = parent.Meta.model
            if not self.read_only:
                self.queryset = model.objects.all()

    def to_representation(self, obj: Any) -> Any:
        """
        Returns the serialized representation of the object.

        Args:
        - obj: The object to be serialized.

        Returns:
        - The serialized representation of the object.
        """
        if self.no_source:
            return obj
        if self.is_method:
            try:
                return get_attribute(obj, self.representation_attribute)()
            except AttributeError:
                return getattr(obj, self.representation_attribute)()
        return getattr(obj, self.representation_attribute)

    def to_internal_value(self, data: Any) -> ModelType:
        """
        Converts the external representation of data to the internal value.

        Args:
        - data: The external representation of the data.

        Returns:
        - The internal value of the data.
        """
        try:
            return self.queryset.get(**{self.lookup: data})
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist")
