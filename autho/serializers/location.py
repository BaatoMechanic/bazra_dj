from autho.models.location import UserLocation
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin


class UserLocationSerializer(BaseModelSerializerMixin):

    class Meta:
        model = UserLocation
        fields = ['idx', 'latitude', 'longitude', 'altitude', 'timestamp',
                  'accuracy', 'heading', 'speed', 'speed_accuracy', 'location_name']

    def save(self, **kwargs):
        self.validated_data['user_id'] = kwargs.get('user').id
        return super().save(**kwargs)
