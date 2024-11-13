
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_email(user, request):
    from .tokens import email_verification_token  # Import the token generator
    token = email_verification_token.make_token(user)
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={
                'user_id': user.id, 'token': token})
    )

    subject = "Verify your email"
    message = f"Please click the link to verify your email: {verification_url}"
    html_message = f"<p>Please click the link to verify your email: {verification_url}</p>"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              [user.email], html_message=html_message)
