from feedback.models import Feedback

from rest_framework import serializers

from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin


class FeedbackSerializer(BaseModelSerializerMixin):

    class Meta:
        model = Feedback
        fields = ["idx", "subject", "message", "user"]

    def create(self, validated_data):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError({"detail": "User is required."})
        validated_data["user"] = user
        return super().create(validated_data)
