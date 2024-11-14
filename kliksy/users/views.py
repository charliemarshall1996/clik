
from datetime import timedelta

from django.contrib.auth import get_user_model, logout, get_backends, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import (UserRegistrationForm,
                    ProfileRegistrationForm,
                    ResendVerificationEmailForm,
                    UserLoginForm,
                    InterestsForm)
from .models import Profile
from .utils import (send_verification_email,
                    get_time_since_last_email,
                    get_minutes_left_before_resend,
                    get_can_resend)
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
                request, """Your account has been created.
                Please check your email to verify your account.""")

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


def custom_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:

                if user.email_verified:
                    for backend in get_backends():
                        if user == backend.get_user(user.id):
                            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                            break

                    login(request, user)
                    profile = user.profile
                    if profile.interests.count() > 0:
                        return redirect('users:profile')
                    else:
                        return redirect('users:interests')
                else:
                    timeout_duration = timedelta(minutes=10)

                    # Example time since last email logic
                    if user.last_verification_email_sent:
                        time_since_last_email = get_time_since_last_email(
                            user.last_verification_email_sent)

                        can_resend = get_can_resend(
                            timeout_duration, time_since_last_email)

                        if can_resend:
                            resend_verification_url = reverse(
                                'users:resend_verification_email')

                            message = ("Please verify your email before logging in."
                                       "Please check your email for the verification link, including spam folder."
                                       f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")
                        else:

                            minutes_difference = get_minutes_left_before_resend(
                                time_since_last_email, timeout_duration)

                            message = (f"""Please verify your email before logging in.
                                       Please check your email for the verification link, including spam folder.
                                       You must wait {round(minutes_difference)} minutes before resending the verification email.""")

                    else:
                        resend_verification_url = reverse(
                            'users:resend_verification_email')

                        message = ("Please verify your email before logging in."
                                   "Please check your email for the verification link, including spam folder."
                                   f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")

                    messages.error(
                        request, message)
                    # Redirect to the login page
                    return redirect('users:login')
            else:
                messages.error(request, "Invalid login credentials")
                return redirect('users:login')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


@login_required
def interests_view(request):
    return render(request, 'users/interests.html')
