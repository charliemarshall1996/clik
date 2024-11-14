from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from datetime import date

from core.utils import get_coordinates, calculate_distance

from .managers import CustomUserManager
# Create your models here.

ALLOWED_COORDS = [(51.2481, -0.7585)]
MAX_ALLOWED_DISTANCE = 7.5


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email instead of username."""

    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)

    last_verification_email_sent = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email instead of username for authentication
    # These fields will be prompted in createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=False, related_name='profile')
    email_comms_opt_in = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', default='default_profile_pic.jpg')
    date_of_birth = models.DateTimeField()
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=25)
    county = models.CharField(max_length=10)
    post_code = models.CharField(max_length=10)
    interests = models.ManyToManyField(
        'core.Category',
        null=True,
        blank=True,
        related_name='interests',
    )

    def clean(self):
        super().clean()
        self.get_age()
        if self.date_of_birth and not self.is_age_valid():
            raise ValidationError("Users must be at least 16 years old.")

        if self.address_line_1 and self.address_line_2 != None:
            street = f"{self.address_line_1} {self.address_line_2}"
        else:
            street = self.address_line_1

        coords = get_coordinates(street,
                                 self.town, self.county, self.post_code)
        print("Coords: ", coords)
        if coords:
            self.lat = coords[0]
            self.lon = coords[1]
        else:
            raise ValidationError(
                f"Address is invalid.")

        if not self.is_coords_valid():
            raise ValidationError(
                "Address is not within the allowed area. We currently only allow users in Rushmoor.")

    def is_age_valid(self):
        return self.age >= 16

    def get_age(self):
        today = date.today()
        self.age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (
                self.date_of_birth.month, self.date_of_birth.day)
        )

    def is_coords_valid(self):

        for allowed_lat, allowed_lon in ALLOWED_COORDS:
            distance = calculate_distance(
                self.lat, self.lon, allowed_lat, allowed_lon)
            print(f"Distance: {distance}")
            if distance <= MAX_ALLOWED_DISTANCE:
                return True
        return False

    def __str__(self):
        return self.user.email
