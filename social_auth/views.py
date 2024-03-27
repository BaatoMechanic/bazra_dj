from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import GenericAPIView

from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthViewSet(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


# from rest_framework_jwt.settings import api_settings

# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# class GoogleSocialAuthViewSet(APIView):
#     authentication_classes = []
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         token = request.data.get('access_token')
#         r = requests.get(
#             f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')
#         if r.status_code == 200:
#             data = r.json()
#             if data['aud'] == 'YOUR_CLIENT_ID_HERE':
#                 payload = jwt_payload_handler(data)
#                 token = jwt_encode_handler(payload)
#                 return Response({'token': token})
#             else:
#                 return Response({'error': 'Invalid client ID'})
#         else:
#             return Response({'error': 'Invalid token'})
