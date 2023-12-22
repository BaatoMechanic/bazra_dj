import re
from rest_framework import serializers

from rest_framework.fields import get_attribute, is_simple_callable


class PhoneNumberField(serializers.CharField):

    def to_internal_value(self, num):
        num = str(num)
        pattern = r"(9[678][0124568]\d{7})|(0\d{8,9})"

        if not re.match(pattern, num):
            raise serializers.ValidationError(
                "Phone number should be either a valid phone number (e.g. 98xxxxxxxx) "
                "or a valid landline number with district code (e.g. 014484xxx)"
            )
        return num


class PasswordField(serializers.CharField):

    def to_internal_value(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("The password should at least be 8 characters long.")
        if len(password) > 100:
            raise serializers.ValidationError("The password should be shorter than 100 characters.")

        return password


class EmailField(serializers.EmailField):

    def to_internal_value(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError("The email should be a valid email address.")

        return email


class UserIdentifierField(serializers.CharField):

    def to_internal_value(self, identifier):
        if not self.validate_id_for_phone(identifier) and not self.validate_id_for_email(identifier):
            raise serializers.ValidationError(
                "The identifier should be either a valid phone number (e.g. 98xxxxxxxx) "
                "or a valid email address"
            )
        return identifier

    def validate_id_for_phone(self, identifier: str) -> bool:
        num = str(identifier)
        pattern = r"(9[678][0124568]\d{7})|(0\d{8,9})"

        if not re.match(pattern, num):
            return False
        return True

    def validate_id_for_email(self, identifier: str) -> bool:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            return False
        return True
