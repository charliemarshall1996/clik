
from datetime import timedelta, timezone

from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, ProfileRegistrationForm, ResendVerificationEmailForm
from .utils import send_verification_email, get_time_since_last_email, get_minutes_left_before_resend
# Create your views here.

User = get_user_model()


def registration_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)

        if user_form.is_valid():  # noqa

            if user_form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')

            user = user_form.save()
            user.email_verified = False
            user.save()

            profile = profile_form.save()
            profile.user = user
            profile.clean()
            profile.save()

            # Send verification email
            send_verification_email(user, request)

            messages.success(
                request, "Your account has been created.\nPlease check your email to verify your account.")

            # Redirect to profile or job application list
            return redirect('users:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


def verify_email_view(request, user_id, token):
    from .tokens import email_verification_token  # Import the token generator
    user = get_object_or_404(User, id=user_id)

    if email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(
            request, 'Your email has been verified. You can now log in.')
        return redirect('users:login')
    else:
        messages.error(
            request, 'The verification link is invalid or has expired.')
        return redirect('users:login')


def resend_verification_email_view(request):
    if request.method == 'POST':
        form = ResendVerificationEmailForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')
            email = form.cleaned_data['email']

            # Look up the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(
                    request, "No user found with that email address.")
                return redirect('users:resend_verification_email')

            # Define timeout duration (10 minutes here)
            timeout_duration = timedelta(minutes=10)

            # Check if a verification email has already been sent and enforce the timeout
            if user.last_verification_email_sent:
                time_since_last_email = get_time_since_last_email(
                    user.last_verification_email_sent)
                timeout_duration = timedelta(minutes=10)
                minutes_difference = get_minutes_left_before_resend(
                    time_since_last_email, timeout_duration)

                if time_since_last_email < timeout_duration:
                    messages.error(
                        request, f"Please wait {minutes_difference} before resending the verification email.")
                    return redirect('users:resend_verification_email')

            # Send verification email and update `last_verification_email_sent`
            send_verification_email(user, request)
            user.last_verification_email_sent = timezone.now()
            user.save()

            # Redirect to a suitable page like login or home
            return redirect('users:login')
    else:
        form = ResendVerificationEmailForm()

    return render(request, 'users/resend_verification_email.html', {'form': form})
