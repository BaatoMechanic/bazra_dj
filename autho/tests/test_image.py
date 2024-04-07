from django.test import TestCase

from autho.admin import User
from model_bakery import baker


class TestGetImage(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = baker.make(User)

    def test_for_no_image(self):
        result = self.user.get_image_url()
        self.assertIsNone(result)

    def test_for_image(self):
        user = baker.make(User, image="test.png")
        result = user.get_image_url()
        self.assertEquals(result, user.image.url)
