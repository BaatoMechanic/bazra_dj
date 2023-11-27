

from autho.serializers import UserSerializer
from autho.models import User

from rest_framework.decorators import action

from rest_framework.response import Response

from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.viewsets import GenericViewSet


class UserInfoViewSet(BaseAPIMixin, GenericViewSet):
    '''
    This file is responsible to perform all the user info logic for the project.
    Any user information logic should be added here.
    '''

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = User.objects.get(
            id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
