from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailVerificationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Authenticate using the email field
            user = UserModel.objects.get(email=email)
            if user.check_password(password) and user.email_verified:
                print(f"User email verified: {user.email_verified}")
                return user
        except UserModel.DoesNotExist:
            return None
        return None

    def user_can_authenticate(self, user):
        """Override to add email verification logic."""
        is_active = super().user_can_authenticate(user)
        return is_active and user.email_verified
