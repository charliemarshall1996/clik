
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django import forms
from django.test import TestCase
from django.utils import timezone
import pytest

from users.forms import UserRegistrationForm, ProfileRegistrationForm


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


@pytest.fixture
def test_user(db):
    """Fixture to create a test user."""
    return User.objects.create_user(email='testuser@example.com', password='password123')


@pytest.fixture
def profile_data():
    """Fixture to provide valid profile data."""
    return {
        # 18 years old
        'date_of_birth': (timezone.now() - timedelta(days=365 * 18)).date(),
        'address_line_1': '123 Test Street',
        'address_line_2': 'Apt 4B',
        'town': 'Aldershot',
        'county': 'Hampshire',
        'postalcode': 'GU11 1AA'
    }


@pytest.mark.django_db
@patch('users.models.get_coordinates')
@patch('users.models.calculate_distance')
def test_valid_form_submission(mock_calculate_distance, mock_get_coordinates, test_user, profile_data):
    """Test a valid form submission."""
    mock_get_coordinates.return_value = (
        51.2488, -0.7588)  # Sample coordinates for valid area
    mock_calculate_distance.return_value = 5  # Within allowed distance

    form = ProfileRegistrationForm(data=profile_data)
    form.instance.user = test_user

    assert form.is_valid(), "Form should be valid with correct data"

    # Save the form and verify the profile is created correctly
    profile = form.save()
    print(f"dob: {profile.date_of_birth}")
    assert profile.user == test_user
    assert profile.date_of_birth.date() == profile_data['date_of_birth']
    assert profile.town == profile_data['town']


@pytest.mark.django_db
@patch('users.models.get_coordinates')
def test_invalid_address(mock_get_coordinates, test_user, profile_data):
    """Test form submission with an invalid address that fails geocoding."""
    mock_get_coordinates.return_value = None  # Simulate invalid address

    form = ProfileRegistrationForm(data=profile_data)
    form.instance.user = test_user

    assert not form.is_valid()
    assert "Address is invalid." in str(form.errors)


@pytest.mark.django_db
@patch('users.models.get_coordinates')
@patch('users.models.calculate_distance')
def test_out_of_area_address(mock_calculate_distance, mock_get_coordinates, test_user, profile_data):
    """Test form submission with a valid address outside the allowed area."""
    mock_get_coordinates.return_value = (
        51.2488, -0.7588)  # Sample coordinates
    mock_calculate_distance.return_value = 50  # Outside allowed distance

    form = ProfileRegistrationForm(data=profile_data)
    form.instance.user = test_user

    assert not form.is_valid()
    assert "Address is not within the allowed area" in str(form.errors)


@pytest.mark.django_db
@patch('users.models.get_coordinates')
def test_underage_user(mock_get_coordinates, test_user, profile_data):
    """Test form submission with a user under the age limit."""
    profile_data['date_of_birth'] = (
        timezone.now() - timedelta(days=365 * 15)).date()  # 15 years old
    mock_get_coordinates.return_value = (51.2488, -0.7588)

    form = ProfileRegistrationForm(data=profile_data)
    form.instance.user = test_user

    assert not form.is_valid()
    assert "Users must be at least 16 years old." in str(form.errors)


@pytest.mark.django_db
def test_missing_required_fields(test_user):
    """Test form submission with missing required fields."""
    incomplete_data = {
        'date_of_birth': (timezone.now() - timedelta(days=365 * 18)).date(),
        'town': 'Aldershot',
        'county': 'Hampshire',
    }  # Missing address_line_1 and postalcode

    form = ProfileRegistrationForm(data=incomplete_data)
    form.instance.user = test_user

    assert not form.is_valid()
    assert 'address_line_1' in form.errors
    assert 'postalcode' in form.errors
