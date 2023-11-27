
from rest_framework import serializers

# from django.contrib.auth import get_user_model

# User = get_user_model()

from autho.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'email', 'phone']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'email', 'phone']
