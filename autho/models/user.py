import re

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.http import HttpRequest

from autho.exceptions import InvalidRecoveryCodeError, InvalidVerificationCodeError
from utils.mixins.base_model_mixin import BaseModelMixin


class UserManager(BaseUserManager):
    def create_user(self, set_unusable_password=False, **fields):
        from autho.models import UserBlackList

        donot_send_code = fields.pop("donot_send_code", None)
        email = fields.pop("email", None)
        phone = fields.pop("phone", None)
        password = fields.pop("password", None)
        if not email and not phone:
            raise ValueError(
                "Either of both of 'email and mobile' is required to create an user."
            )

        if not password and not set_unusable_password:
            raise ValueError("Password is required to create an user.")

        if email:
            email = super().normalize_email(email)

        if phone:
            phone = self.normalize_phone_number(phone)

        UserBlackList.exists(phone, email)

        user: User = self.model(email=email, phone=phone, **fields)

        user.set_password(password)
        user.save(using=self._db)
        if not donot_send_code:
            try:
                user.gen_verification_code().send()
            except Exception:
                pass

        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email", email)
        extra_fields.setdefault("phone", phone)
        extra_fields.setdefault("password", password)
        return self.create_user(**extra_fields)

    @staticmethod
    def normalize_phone_number(phone_number):
        """
        Normalize the phone number by removing any special characters or formatting.
        """

        normalized_phone_number = (
            phone_number.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace("+", "")
        )
        return normalized_phone_number


AUTH_PROVIDER_EMAIL = "email"
AUTH_PROVIDER_MOBILE = "mobile"
AUTH_PROVIDER_GOOGLE = "google"
AUTH_PROVIDER_FACEBOOK = "facebook"

AUTH_PROVIDER_CHOICES = [
    (AUTH_PROVIDER_EMAIL, AUTH_PROVIDER_EMAIL.capitalize()),
    (AUTH_PROVIDER_MOBILE, AUTH_PROVIDER_MOBILE.capitalize()),
    (AUTH_PROVIDER_GOOGLE, AUTH_PROVIDER_GOOGLE.capitalize()),
    (AUTH_PROVIDER_FACEBOOK, AUTH_PROVIDER_FACEBOOK.capitalize()),
]


class User(AbstractBaseUser, PermissionsMixin, BaseModelMixin):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOCES = [
        (GENDER_MALE, GENDER_MALE.capitalize()),
        (GENDER_FEMALE, GENDER_FEMALE.capitalize()),
        (GENDER_OTHER, GENDER_OTHER.capitalize()),
    ]

    DATE_TYPE_BS = "bs"
    DATE_TYPE_AD = "ad"

    DATE_TYPE_CHOICES = (
        (DATE_TYPE_BS, DATE_TYPE_BS.capitalize()),
        (DATE_TYPE_AD, DATE_TYPE_AD.capitalize()),
    )

    USERNAME_FIELD = "email"
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=16, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOCES, default=GENDER_MALE)
    auth_provider = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AUTH_PROVIDER_CHOICES,
        default=AUTH_PROVIDER_EMAIL,
    )
    image = models.ImageField(upload_to="users/profile", null=True, blank=True)

    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, db_index=True)

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

    primary_role = models.ForeignKey(
        "permission.Role",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
    )
    roles = models.ManyToManyField("permission.Role", related_name="users", blank=True)
    # additional_attributes = models.JSONField(default=dict, blank=True, null=True)
    dob_type = models.CharField(
        max_length=2, choices=DATE_TYPE_CHOICES, default=DATE_TYPE_AD
    )
    dob = models.DateField(null=True, blank=True)

    verified_on = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.idx

    def can_retrieve(self, request: HttpRequest) -> bool:
        return True

    def isa(self, role: str) -> bool:
        """
        Check if the user has the given role.

        Args:
            role: The role to check.

        Returns:
            True if the user has the given role, False otherwise.
        """
        return (
            self.primary_role is not None and self.primary_role.name == role
        ) or self.roles.filter(name=role).exists()

    def get_roles(self) -> list:
        roles = [role.name for role in self.roles.all()]
        if self.primary_role is not None:
            roles.append(self.primary_role.name)
        return roles

    def add_roles(self, roles) -> list:
        if not isinstance(roles, models.query.QuerySet) and not isinstance(roles, list):
            roles = [roles]
        self.roles.add(*roles)

    def delete(self) -> None:
        self.__class__.objects.filter(id=self.id).update(
            is_active=False, is_obsolete=True
        )

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    @property
    def ratings(self) -> int:
        from vehicle_repair.models.rating_review import RatingAndReview

        return RatingAndReview.objects.filter(user=self).aggregate(Sum("rating"))[
            "rating__sum"
        ]

    @property
    def total_rating(self):
        from autho.models import RatingAndReview

        return RatingAndReview.objects.filter(user=self).count()

    def gen_verification_code(self):
        """Generate a verification code for the user.

        Returns:
            The generated verification code, or None if the user is already verified.
        """
        from .verification_code import VerificationCode

        if self.is_verified:
            raise Exception("User is already verified.")
        if hasattr(self, "verification_code"):
            return self.verification_code.update_code()
        verification_code, _ = VerificationCode.objects.get_or_create(user=self)
        return verification_code

    def gen_recovery_code(self):
        from .recovery_code import RecoveryCode

        if hasattr(self, "recovery_code"):
            return self.recovery_code.update_code()
        return RecoveryCode.generate_recovery_code(self)

    @classmethod
    def verify_recovery_code(cls, id, code, verification_token=None):
        user = cls.get_user_by_identifier(id)
        if not user:
            raise InvalidRecoveryCodeError

        if not hasattr(user, "recovery_code"):
            raise InvalidRecoveryCodeError

        if user.recovery_code.equals(code, verification_token):
            user.recovery_code.delete()
            return user
        else:
            user.recovery_code.increment_retries()
            raise InvalidRecoveryCodeError

    @classmethod
    def verify_verification_code(cls, id, code, verification_token=None):
        user = cls.get_user_by_identifier(id)
        if not user:
            raise InvalidVerificationCodeError

        if not hasattr(user, "verification_code"):
            raise InvalidVerificationCodeError

        if user.verification_code.equals(code, verification_token):
            user.verification_code.delete()
            return user
        else:
            user.verificstion_code.increment_retries()
            raise InvalidVerificationCodeError

    @classmethod
    def get_user_by_identifier(cls, id):
        try:
            if re.match(r"^\d{10}$", str(id)):
                return cls.objects.get(phone=id)

            if re.match(r"^(.+?)@(.+?)\.(.+?)$", id):
                return cls.objects.get(email=id)
        except cls.DoesNotExist:
            return None

    def get_basic_attributes(self) -> dict:
        return {
            "is_phone_verified": self.is_phone_verified,
            "is_email_verified": self.is_email_verified,
            "is_verified": self.is_verified,
        }
