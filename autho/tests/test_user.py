from django.test import TestCase

from autho.admin import User


# Create your tests here.
class TestGetUserByIdentifier(TestCase):

    def setup(self):

        self.user = User.objects.create_user(phone="1234567890", password="test1234")
        self.user1 = User.objects.create_user(email="abc@abc.com", password="test1234")

    def test_for_invaild_identifier(self):
        id = "1234567890"
        result = User.get_user_by_identifier(id)
        self.assertEquals(result, None)

    def test_for_vaild_phone_number(self):
        id = "1234567890"
        result = User.get_user_by_identifier(phone=id)
        self.assertEquals(result, self.user)

    def test_for_vaild_email(self):
        id = "abc@abc.com"
        result = User.get_user_by_identifier(email=id)
        self.assertEquals(result, self.user1)


class TestGetBasicAttributes(TestCase):

    def setup(self):
        self.user = User.objects.create_user(phone="1234567890", password="test1234")

    def test_for_false_attributes(self):
        pass
