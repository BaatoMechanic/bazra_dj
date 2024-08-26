from rest_framework.viewsets import ModelViewSet

from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer
from utils.mixins.base_api_mixin import BaseAPIMixin


class FeedbackViewSet(BaseAPIMixin, ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}
