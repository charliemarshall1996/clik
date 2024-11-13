
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
import pytest

from users.models import *
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


@pytest.mark.django_db
class TestProfileModel:
    @pytest.fixture
    def user(self):
        # Fixture to create a test user for the profile
        return CustomUser.objects.create(
            email="testuser@example.com",
            first_name="Test",
            last_name="User"
        )

    @pytest.fixture
    def valid_date_of_birth(self):
        # Fixture to create a valid date of birth (e.g., 20 years old)
        return timezone.now() - timedelta(days=365 * 20)

    @pytest.fixture
    def invalid_date_of_birth(self):
        # Fixture to create an invalid date of birth (e.g., 15 years old)
        return timezone.now() - timedelta(days=365 * 15)

    @pytest.fixture
    def valid_address(self):
        """Fixture for a valid address that returns coordinates within allowed area."""
        return {
            'address_line_1': "221 Weybourne Road",
            'town': "Aldershot",
            'county': "Hampshire",
            'post_code': "GU11 3NE"
        }

    @pytest.fixture
    def invalid_address(self):
        """Fixture for an invalid address that returns coordinates outside allowed area."""
        return {
            'address_line_1': "Invalid Street",
            'address_line_2': "Invalid Area",
            'town': "Invalid Town",
            'county': "Invalid County",
            'post_code': "INV123"
        }

    def test_profile_creation(self, user, valid_date_of_birth, valid_address):
        """Test profile can be created with valid data."""
        profile = Profile.objects.create(
            user=user,
            bio="This is a test bio.",
            date_of_birth=valid_date_of_birth,
            **valid_address
        )
        assert profile.user == user
        assert profile.bio == "This is a test bio."
        assert profile.date_of_birth == valid_date_of_birth
        assert profile.profile_pic.name == 'default_profile_pic.jpg'

    def test_clean_method_with_valid_age(self, user, valid_date_of_birth, valid_address):
        """Test clean method does not raise ValidationError for a valid age."""
        profile = Profile(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)
        try:
            profile.clean()
        except ValidationError:
            pytest.fail("ValidationError raised for valid age")

    def test_clean_method_with_invalid_age(self, user, invalid_date_of_birth):
        """Test clean method raises ValidationError for a user under 16."""
        profile = Profile(user=user, date_of_birth=invalid_date_of_birth)
        with pytest.raises(ValidationError, match="Users must be at least 16 years old."):
            profile.clean()

    def test_str_method(self, user, valid_date_of_birth, valid_address):
        """Test the __str__ method returns the user's email."""
        profile = Profile(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)
        assert str(profile) == user.email

    def test_profile_pic_default_value(self, user, valid_date_of_birth, valid_address):
        """Test that profile_pic has the default value if not specified."""
        profile = Profile.objects.create(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)
        assert profile.profile_pic.name == 'default_profile_pic.jpg'

    def test_clean_method_with_valid_address(self, user, valid_date_of_birth, valid_address, mocker):
        """Test clean method does not raise ValidationError for a valid address within allowed area."""
        profile = Profile(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)

        # Mock get_coordinates to return valid coordinates within allowed area
        mocker.patch('users.models.get_coordinates',
                     return_value=(51.2500, -0.7600))

        # Mock calculate_distance to always return a value within 7.5 km
        mocker.patch('users.models.calculate_distance', return_value=5.0)

        try:
            profile.clean()
        except ValidationError as e:
            pytest.fail(
                f"ValidationError raised for {valid_address} within allowed area: {e}")

    def test_clean_method_with_invalid_address(self, user, valid_date_of_birth, valid_address, mocker):
        """Test clean method raises ValidationError for an address outside the allowed area."""
        profile = Profile(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)

        # Mock get_coordinates to return coordinates outside allowed area
        mocker.patch('users.models.get_coordinates',
                     return_value=None)

        with pytest.raises(ValidationError, match="Address is invalid."):
            profile.clean()

    def test_clean_method_with_invalid_coordinates(self, user, valid_date_of_birth, valid_address, mocker):
        """Test clean method raises ValidationError for invalid address with no coordinates returned."""
        profile = Profile(
            user=user, date_of_birth=valid_date_of_birth, **valid_address)

        # Mock get_coordinates to return
        mocker.patch('users.models.get_coordinates',
                     return_value=(530.0000, -1.0000))

        with pytest.raises(ValidationError, match="Address is not within the allowed area. We currently only allow users in Rushmoor."):
            profile.clean()
