
from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import UserRegistrationForm


from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationFormTest(TestCase):

    def test_valid_form(self):
        """Test that form is valid when all required fields are provided correctly."""
        form_data = {
            'email': 'test@example.com',
            'password1': 'password123Test.',
            'password2': 'password123Test.',
            'first_name': 'John',
            'last_name': 'Doe',
            'honeypot': ''  # Honeypot should be empty
        }
        form = UserRegistrationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test form errors when required fields are missing."""
        form_data = {
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
            'honeypot': ''  # Honeypot should still be empty
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_invalid_email(self):
        """Test form error when an invalid email is provided."""
        form_data = {
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'honeypot': ''
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0],
                         "Enter a valid email address.")

    def test_honeypot_field(self):
        """Test form error when honeypot field is filled (spam detection)."""
        form_data = {
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'honeypot': 'spam'  # Simulate a bot filling in this field
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('honeypot', form.errors)
        self.assertEqual(form.errors['honeypot'][0], "Spam detected")

    def test_password_mismatch(self):
        """Test form error when passwords do not match."""
        form_data = {
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'differentpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'honeypot': ''
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'][0], forms.ValidationError(
            'The two password fields didn’t match.').messages[0])
