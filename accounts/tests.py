from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="12345678"
        )

        self.assertEqual(user.username, "testuser")

        self.assertEqual(user.email, "test@test.com")

        self.assertTrue(user.check_password("12345678"))