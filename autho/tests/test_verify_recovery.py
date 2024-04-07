from django.test import TestCase
import pytest
from autho.admin import User
from autho.exceptions import InvalidRecoveryCodeError
from autho.models.recovery_code import RecoveryCode


class TestVerifyRecoveryCode(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create_user(phone="1234567890", password="test1234")
        cls.user.gen_recovery_code()

    def test_for_invaild_identifier(self):
        id = "097654321"
        code = "123456"
        with pytest.raises(InvalidRecoveryCodeError):
            User.verify_recovery_code(id, code)

    def test_for_no_recovery_code(self):
        id = "1234567890"
        code = "098765"
        self.user.recovery_code.delete()
        with pytest.raises(InvalidRecoveryCodeError):
            User.verify_recovery_code(id, code)

    @pytest.mark.django_db
    def test_for_vaild_code(self):
        id = "1234567890"
        code = "123456"
        result = User.verify_recovery_code(id, code)
        self.assertIsInstance(result, User)


class TestGenRecoverycode(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(phone="1234567890", password="test1234")

    def test_for_no_recovery_code(self):
        self.assertFalse(RecoveryCode.objects.filter(user=self.user).exists())
        result = self.user.gen_recovery_code()
        self.assertIsInstance(result, RecoveryCode)
        self.assertTrue(RecoveryCode.objects.filter(user=self.user).exists())
        self.assertTrue(result.user == self.user)

    def test_for_recovery_code(self):
        old_recoverycode = self.user.gen_recovery_code()
        old_code = old_recoverycode.code
        result = self.user.gen_recovery_code()
        self.assertNotEquals(result.code, old_code)
        self.assertEquals(old_recoverycode.id, result.id)
