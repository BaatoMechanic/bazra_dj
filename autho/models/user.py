

from django.db import models
from django.contrib.auth.models import  AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager

from autho.models.verification_code import VerificationCode

from utils.models.mixins import BaseModel

from autho.models.user_blacklist import UserBlackList


class UserManager(BaseUserManager):
    def create_user(self,  **fields):
        donot_send_code = fields.pop("donot_send_code", None)
        email = fields.get('email')
        phone = fields.get('phone')
        password = fields.get('password')
        if not email and not phone:
            raise Exception("Either of both of 'email and mobile' is required to create an user.")

        if not password:
            raise Exception("Password is required to create an user.")

        if phone:
            phone = self.normalize_phone_number(phone)

        UserBlackList.exists(phone, email)

        user: User = self.model(**fields)
        user.set_password(password)
        user.save()
        if not donot_send_code:
            try:
                user.gen_verification_code().send()
            except Exception:
                pass

        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email', email)
        extra_fields.setdefault('phone', phone)
        extra_fields.setdefault('password', password)
        return self.create_user(**extra_fields)

    @staticmethod
    def normalize_phone_number(phone_number):
        """
        Normalize the phone number by removing any special characters or formatting.
        """

        normalized_phone_number = phone_number.replace(' ', '').replace(
            '-', '').replace('(', '').replace(')', '').replace('+', '')
        return normalized_phone_number


AUTH_PROVIDER_EMAIL = 'email'
AUTH_PROVIDER_MOBILE = 'mobile'
AUTH_PROVIDER_GOOGLE = 'google'
AUTH_PROVIDER_FACEBOOK = 'facebook'

AUTH_PROVIDER_CHOICES = [
    (AUTH_PROVIDER_EMAIL, AUTH_PROVIDER_EMAIL.capitalize()),
    (AUTH_PROVIDER_MOBILE, AUTH_PROVIDER_MOBILE.capitalize()),
    (AUTH_PROVIDER_GOOGLE, AUTH_PROVIDER_GOOGLE.capitalize()),
    (AUTH_PROVIDER_FACEBOOK, AUTH_PROVIDER_FACEBOOK.capitalize()),
]


GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER_OTHER = 'other'

GENDER_CHOCES = [
    (GENDER_MALE, GENDER_MALE.capitalize()),
    (GENDER_FEMALE, GENDER_FEMALE.capitalize()),
    (GENDER_OTHER, GENDER_OTHER.capitalize())]

DATE_TYPE_BS = 'bs'
DATE_TYPE_AD = 'ad'


DATE_TYPE_CHOICES = (
    (DATE_TYPE_BS, DATE_TYPE_BS.capitalize()),
    (DATE_TYPE_AD, DATE_TYPE_AD.capitalize()),
)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    USERNAME_FIELD = "email"
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=16, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOCES, default=GENDER_MALE)
    auth_provider = models.CharField(
        max_length=50, blank=False, null=False, choices=AUTH_PROVIDER_CHOICES, default=AUTH_PROVIDER_EMAIL)
    is_verified = models.BooleanField(default=False, db_index=True)

    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    primary_role = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    roles = models.ManyToManyField("permission.Role", related_name="users")
    dob_type = models.CharField(max_length=2, choices=DATE_TYPE_CHOICES, default="AD")
    dob = models.DateField(null=True, blank=True)

    verified_on = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def gen_verification_code(self):
        if self.is_verified:
            raise Exception("User is already verified.")
        if hasattr(self, 'verification_code'):
            return self.verification_code.update_code()
        verification_code, _ = VerificationCode.objects.get_or_create(user=self)
        return verification_code
