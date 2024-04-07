from django.test import TestCase
import pytest

from autho.admin import User
from autho.exceptions import InvalidVerificationCodeError
from autho.models.verification_code import VerificationCode


class TestVerifyVerificationCode(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(phone="1234567890", password="test1234")

    def test_for_invalid_identifier(self):
        id = "1234567000"
        code = "123456"
        with pytest.raises(InvalidVerificationCodeError):
            User.verify_verification_code(id, code)

    def test_for_no_verification_code(self):
        id = "1234567890"
        code = "098765"
        self.user.verification_code.delete()
        with pytest.raises(InvalidVerificationCodeError):
            User.verify_verification_code(id, code)

    def test_for_vaild_code(self):
        id = "1234567890"
        code = "123456"
        result = User.verify_verification_code(id, code)
        self.assertIsInstance(result, User)


class TestGenVerificationCode(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create_user(phone="1234567890", password="test1234")

    def test_for_no_verification_code(self):
        self.user.verification_code.delete()
        self.assertFalse(VerificationCode.objects.filter(user=self.user).exists())
        result = self.user.gen_verification_code()
        self.assertTrue(VerificationCode.objects.filter(user=self.user).exists())
        self.assertIsInstance(result, VerificationCode)
        self.assertTrue(result.user == self.user)

    def test_for_recovery_code(self):
        old_verificationcode = self.user.gen_verification_code()
        old_code = old_verificationcode.code
        result = self.user.gen_verification_code()
        self.assertNotEquals(result.code, old_code)
        self.assertEquals(old_verificationcode.id, result.id)
        self.assertNotEquals(old_code, result.code)

    def test_for_verified(self):
        self.user.is_verified = True
        with pytest.raises(Exception):
            User.gen_verification_code()
