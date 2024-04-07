from django.test import TestCase
import pytest

from autho.admin import User


class TestGetUserByIdentifier(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(phone="1234567890", password="test1234")
        self.user1 = User.objects.create_user(email="abc@abc.com", password="test1234")

    @pytest.mark.django_db
    def test_for_invaild_identifier(self):
        id = "1287898765"
        result = User.get_user_by_identifier(id)
        self.assertEquals(result, None)

    def test_for_vaild_phone_number(self):
        id = "1234567890"
        result = User.get_user_by_identifier(id)
        self.assertEquals(result, self.user)

    def test_for_vaild_email(self):
        id = "abc@abc.com"
        result = User.get_user_by_identifier(id)
        self.assertEquals(result, self.user1)


class TestGetBasicAttributes(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(phone="1234567890", password="test1234")

    def test_for_phone_not_verified(self):
        result = self.user.get_basic_attributes()
        self.assertFalse(result["is_phone_verified"])

    def test_for_verified_phone(self):
        self.user.is_phone_verified = True
        result = self.user.get_basic_attributes()
        self.assertTrue(result["is_phone_verified"])

    def test_for_email_not_verified(self):
        result = self.user.get_basic_attributes()
        self.assertFalse(result["is_email_verified"])

    def test_for_verified_email(self):
        self.user.is_email_verified = True
        result = self.user.get_basic_attributes()
        self.assertTrue(result["is_email_verified"])

    def test_for_not_verified(self):
        result = self.user.get_basic_attributes()
        self.assertFalse(result["is_verified"])

    def test_for_verified(self):
        self.user.is_verified = True
        result = self.user.get_basic_attributes()
        self.assertTrue(result["is_verified"])
