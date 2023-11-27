
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import authentication
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

import jwt

from rest_framework.request import Request

from django.db.models import Q

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.contrib.auth import get_user_model

from django.contrib.auth.models import update_last_login

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


class CustomSimpleJWTAuthentication(JWTAuthentication):

    def authenticate(self, request=None, **credentials):

        # token = request.META.get('HTTP_AUTHORIZATION')
        # using or beacuse user_identifier can be in username if login from admin panel and user_identifier
        # if login from api endpoints
        user_identifier = credentials.get('user_identifier') or credentials.get('username')
        password = credentials.get('password')

        if user_identifier is None or password is None:
            header = self.get_header(request)
            if header is not None:
                return self.get_user_from_token(header)
            return None

        user = User.objects.filter(Q(email=user_identifier) | Q(phone=user_identifier), is_obsolete=False).first()

        if user is None or not user.check_password(password):
            # If user is trying to login from admin panel then show the error message inside the form
            if request.path == '/admin/login/':
                raise ValidationError("No active account found with the given credentials")

            else:
                raise AuthenticationFailed("No active account found with the given credentials")

        payload = {}

        # return user, payload
        return user

    def get_user_from_token(self, header):
        raw_token = super().get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = super().get_validated_token(raw_token)

        return super().get_user(validated_token), validated_token

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
