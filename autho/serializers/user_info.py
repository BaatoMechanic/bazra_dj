
from rest_framework import serializers

# from django.contrib.auth import get_user_model

# User = get_user_model()

from autho.models import User
from autho.models.mechanic_profile import MechanicProfile


class UserSerializer(serializers.ModelSerializer):
    additional_attributes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['idx', 'name', 'email', 'phone', 'image',
                  'primary_role', 'roles', 'additional_attributes']

    def get_additional_attributes(self, instance):
        attrs = {}
        if hasattr(instance, "mechanic_profile"):
            profile: MechanicProfile = instance.mechanic_profile
            if profile.vehicle_speciality:
                attrs['vehicle_speciality'] = profile.vehicle_speciality.name
            if profile.service_speciality:
                attrs['service_speciality'] = profile.service_speciality.name
            attrs['total_repairs'] = profile.total_repairs
            attrs['total_reviews'] = profile.total_reviews
            attrs['description'] = profile.mechanic_description
            attrs['rating'] = instance.total_rating
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.primary_role is not None:
            representation['primary_role'] = instance.primary_role.name
        representation['roles'] = [role.name for role in instance.roles.all()]

        return representation


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'image']
