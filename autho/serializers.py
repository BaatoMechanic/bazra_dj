from typing import Any, Dict

from django.contrib.auth.models import update_last_login

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib import auth

from autho.models.rating_review import RatingAndReview


class LoginSerializer(serializers.Serializer):
    '''
        This serializer overrides the TokenObtainPairSerializer of simple jwt to use custom field
        user_identifier and password to create the access and refresh token
    '''
    user_identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        data = super().validate(attrs)
        print('here')
        user_identifier = data.get('user_identifier')
        password = data.get('password')

        user = auth.authenticate(self.context.get('request'), user_identifier=user_identifier, password=password)
        # auth.login(self.context.get('request'), user)

        refresh = RefreshToken.for_user(user)

        update_last_login(None, user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class RatingAndReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingAndReview
        fields = ['rating', 'review', 'user', 'review_by']

    def validate(self, attrs):

        review_by = self.context.get('request').user
        attrs['review_by'] = review_by

        user = attrs.get("user")

        if review_by == user:
            raise serializers.ValidationError({"user": ["You can't rate yourself."]})

        # if attrs['rating'] < 1 or attrs['rating'] > 5:
        #     raise serializers.ValidationError({"rating": ["Rating must be between 1 and 5."]})

        return super().validate(attrs)
