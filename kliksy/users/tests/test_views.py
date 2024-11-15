import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Profile
from users.tokens import email_verification_token

User = get_user_model()


@pytest.fixture
def create_user_with_profile(db):
    """Fixture to create a test user."""
    user = User.objects.create_user(
        email="testuser@example.com", password="password123")
    user.email_verified = False
    user.last_verification_email_sent = timezone.now()
    user.save()
    dob = timezone.datetime(1996, 1, 1)
    profile = Profile.objects.create(user=user, date_of_birth=dob)
    profile.save()
    return user, profile


@pytest.mark.django_db
def test_registration_view(client):
    url = reverse("users:register")

    # Combine form data for both UserRegistrationForm and ProfileRegistrationForm
    data = {
        # UserRegistrationForm fields
        "email": "newuser@example.com",
        "password1": "password123",
        "password2": "password123",
        "first_name": "Test",
        "last_name": "User",
        "honeypot": "",  # Honeypot must be empty for the form to pass

        # ProfileRegistrationForm fields
        "date_of_birth": "2000-01-01",
        "address_line_1": "123 Main St",
        "address_line_2": "",
        "town": "TestTown",
        "county": "TestCounty",
        "post_code": "12345",
        "email_comms_opt_in": True,
    }

    response = client.post(url, data)

    # Assert redirect on success
    assert response.status_code == 302  # Should redirect to 'users:login'

    # Assert that the user and profile are created
    user = User.objects.filter(email="newuser@example.com").first()
    assert user is not None  # Ensure user is created
    assert user.profile is not None  # Ensure profile is created
    assert user.profile.town == "TestTown"  # Check profile field


@pytest.mark.django_db
def test_registration_view(client):
    url = reverse("users:register")

    # Combine form data for both UserRegistrationForm and ProfileRegistrationForm
    data = {
        # UserRegistrationForm fields
        "email": "newuser@example.com",
        "password1": "password123",
        "password2": "password123",
        "first_name": "Test",
        "last_name": "User",
        "honeypot": "spam",  # Honeypot must be empty for the form to pass

        # ProfileRegistrationForm fields
        "date_of_birth": "2000-01-01",
        "address_line_1": "221 Weybourne Road",
        "address_line_2": "",
        "town": "Aldershot",
        "county": "Hampshire",
        "post_code": "GU11 3NE",
        "email_comms_opt_in": True,
    }

    response = client.post(url, data)

    # Assert redirect on success
    assert response.status_code == 302  # Should redirect to 'users:login'

    # Assert that the user and profile are created
    user = User.objects.filter(email="newuser@example.com").first()
    assert user is not None  # Ensure user is created
    assert user.profile is not None  # Ensure profile is created
    assert user.profile.town == "TestTown"  # Check profile field


@pytest.mark.django_db
def test_verify_email_view(client, create_user_with_profile):
    user, _ = create_user_with_profile
    token = email_verification_token.make_token(user)
    url = reverse("users:verify_email", args=[user.id, token])
    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 302
    assert user.email_verified


@pytest.mark.django_db
def test_verify_email_view_invalid_token(client, create_user_with_profile):
    user, _ = create_user_with_profile
    url = reverse("users:verify_email", args=[user.id, "invalidtoken"])
    response = client.get(url)
    assert response.status_code == 302
    assert not user.email_verified


@pytest.mark.django_db
def test_resend_verification_email_view(client, create_user_with_profile):
    user, _ = create_user_with_profile
    url = reverse("users:resend_verification_email")
    response = client.post(url, {"email": user.email, "honeypot": ""})
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.last_verification_email_sent > timezone.now() - \
        timezone.timedelta(seconds=5)


@pytest.mark.django_db
def test_resend_verification_email_view_honeypot(client, create_user_with_profile):
    user, _ = create_user_with_profile
    url = reverse("users:resend_verification_email")
    response = client.post(
        url, {"email": user.email, "honeypot": "spam"})
    assert response.status_code == 302


@pytest.mark.django_db
def test_custom_login_view_success(client, create_user_with_profile):
    user, _ = create_user_with_profile
    user.email_verified = True
    user.save()
    url = reverse("users:login")
    response = client.post(
        url, {"email": user.email, "password": "password123", "honeypot": ""})
    assert response.status_code == 302


@pytest.mark.django_db
def test_custom_login_view_unverified_email(client, create_user_with_profile):
    user, _ = create_user_with_profile
    url = reverse("users:login")
    response = client.post(
        url, {"email": user.email, "password": "password123", "honeypot": ""})
    assert response.status_code == 302
    assert "Please verify your email" in str(response.content)


@pytest.mark.django_db
def test_interests_view(client, create_user_with_profile):
    user, profile = create_user_with_profile
    client.force_login(user)
    url = reverse("users:interests")
    response = client.post(url, {"interests": "coding"})
    assert response.status_code == 302
    profile.refresh_from_db()
    assert profile.interests.filter(name="coding").exists()


@pytest.mark.django_db
def test_profile_view(client, create_user_with_profile):
    user, profile = create_user_with_profile
    client.force_login(user)
    url = reverse("users:profile", args=[profile.id])
    response = client.get(url)
    assert response.status_code == 200
    assert profile.id in str(response.content)
