import token
from rest_framework import authentication
from datetime import datetime, timedelta

import jwt

from rest_framework.request import Request

from django.db.models import Q

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.contrib.auth import get_user_model

from django.contrib.auth.models import update_last_login

# from autho.models import User

from django.contrib.auth.backends import ModelBackend

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomJWTAuthentication(authentication.BaseAuthentication):
    """
    A custom authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')

        if jwt_token is None:
            return None

        jwt_token = CustomJWTAuthentication.get_cleaned_token(jwt_token)

        # Decode and verify the signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        user_identifier = payload.get('user_identifier')
        if user_identifier is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(email=user_identifier).first()
        if user is None:
            user = User.objects.filter(phone=user_identifier).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        return user, payload

    def authenticate_header(self, request: Request) -> str:
        """
        Returns the authentication header for the given request.

        Args:
            request (Any): The request object.

        Returns:
            str: The authentication header.
        """
        return "Bearer"

    # def _get_user(self, id):
    #     try:
    #         if re.match("^\d{10}$", str(id)):
    #             return User.objects.get(mobile=id)

    #         if re.match("^(.+?)@(.+?)\.(.+?)$", id):
    #             return User.objects.get(email=id)
    #     except ObjectDoesNotExist:
    #         return None

    @classmethod
    def get_cleaned_token(cls, token: str) -> str:
        '''
        Cleans the token by removing 'Bearer' and spaces, and returns the cleaned token as a string
        '''
        auth_header_prefix = cls.authenticate_header()
        return token.replace(auth_header_prefix, '').replace(' ', '')

    @classmethod
    def create_access_jwt(cls, user: User):
        user_identifier: str = user.email if user.email else user.phone
        expiration_time: datetime = datetime.now() + settings.JWT_CONF['ACCESS_TOKEN_LIFETIME']
        payload = {
            "user_identifier": user_identifier,
            "exp": int(expiration_time.timestamp()),
            "iat": int(datetime.now().timestamp()),
            "email": user.email,
            "phone": user.phone,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @classmethod
    def create_refresh_jwt(cls, user: User):
        user_identifier: str = user.email if user.email else user.phone
        # expiration_time = datetime.now() + timedelta(minutes=settings.JWT_CONF['ACCESS_TOKEN_LIFETIME'])
        expiration_time: datetime = datetime.now() + settings.JWT_CONF['REFRESH_TOKEN_LIFETIME']
        payload = {
            "user_identifier": user_identifier,
            "exp": int(expiration_time.timestamp()),
            "iat": int(datetime.now().timestamp()),
            "email": user.email,
            "phone": user.phone,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class CustomSimpleJWTAuthentication(ModelBackend):

    def authenticate(self, request=None, **credentials):

        # token = request.META.get('HTTP_AUTHORIZATION')
        # using or beacuse user_identifier can be in username if login from admin panel and user_identifier if login from api endpoints
        user_identifier = credentials.get('user_identifier') or credentials.get('username')
        password = credentials.get('password')

        user = User.objects.filter(Q(email=user_identifier) | Q(phone=user_identifier), is_obsolete=False).first()

        if user is None or not user.check_password(password):

            raise AuthenticationFailed("No active account found with the given credentials")

        # refresh = RefreshToken.for_user(user)

        # payload = {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }
        payload = {}

        return user, payload

    @classmethod
    def create_tokens(cls, user: User):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
