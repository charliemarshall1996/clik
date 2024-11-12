
from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import CustomUser
# Create your tests here.


class CustomUserTests(TestCase):

    def test_create_user(self):
        email = "normal@user.com"
        email_verified = False
        first_name = "John"
        last_name = "Doe"
        is_active = True
        is_staff = False

        user = CustomUser.objects.create(email=email,
                                         email_verified=email_verified,
                                         first_name=first_name,
                                         last_name=last_name,
                                         is_active=is_active,
                                         is_staff=is_staff)

        user.save()

        self.assertEqual(user.email, email)
        self.assertEqual(user.email_verified, email_verified)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.is_active, is_active)
        self.assertEqual(user.is_staff, is_staff)
