
from datetime import timedelta

from django.contrib.auth import get_user_model, logout, get_backends, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
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
    # Check if the request method is POST
    if request.method == "POST":
        # Instantiate the login form with POST data
        form = UserLoginForm(request.POST)

        # Validate the form
        if form.is_valid():
            # Check honeypot field for spam detection
            if form.cleaned_data['honeypot']:
                # If honeypot field is filled, treat as spam and show error
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to the home page to prevent bot resubmission
                return redirect('home')

            # Retrieve email and password from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate the user with provided email and password
            user = authenticate(request, email=email, password=password)

            # If authentication is successful
            if user is not None:
                # Check if the user's email is verified
                if user.email_verified:
                    # Identify the correct authentication backend for the user
                    for backend in get_backends():
                        if user == backend.get_user(user.id):
                            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                            break

                    # Log the user in
                    login(request, user)
                    # Access the user's profile
                    profile = user.profile
                    # Check if the user has interests
                    if profile.interests.count() > 0:
                        # Redirect to the user's profile page if interests are present
                        return redirect('users:profile')
                    else:
                        # Redirect to the interests page if no interests are set
                        return redirect('users:interests')
                else:
                    # Set timeout duration for email verification
                    timeout_duration = timedelta(minutes=10)

                    # Check if a verification email has been sent before
                    if user.last_verification_email_sent:
                        # Calculate time since the last email was sent
                        time_since_last_email = get_time_since_last_email(
                            user.last_verification_email_sent)

                        # Determine if the verification email can be resent
                        can_resend = get_can_resend(
                            timeout_duration, time_since_last_email)

                        if can_resend:
                            # Generate URL for resending verification email
                            resend_verification_url = reverse(
                                'users:resend_verification_email')

                            # Inform the user to verify their email
                            message = ("Please verify your email before logging in."
                                       "Please check your email for the verification link, including spam folder."
                                       f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")
                        else:
                            # Calculate minutes left before a new verification email can be sent
                            minutes_difference = get_minutes_left_before_resend(
                                time_since_last_email, timeout_duration)

                            # Inform the user of the wait time before resending the email
                            message = (f"""Please verify your email before logging in.
                                       Please check your email for the verification link, including spam folder.
                                       You must wait {round(minutes_difference)} minutes before resending the verification email.""")

                    else:
                        # If no verification email has been sent, provide URL to resend
                        resend_verification_url = reverse(
                            'users:resend_verification_email')

                        # Inform the user to verify their email
                        message = ("Please verify your email before logging in."
                                   "Please check your email for the verification link, including spam folder."
                                   f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")

                    # Display an error message with the verification instructions
                    messages.error(request, message)
                    # Redirect to the login page
                    return redirect('users:login')
            else:
                # If authentication fails, show error message
                messages.error(request, "Invalid login credentials")
                # Redirect to the login page
                return redirect('users:login')
    else:
        # If request method is not POST, instantiate an empty login form
        form = UserLoginForm()

    # Prepare context with the form to render the login page
    context = {'form': form}
    # Render the login page with the context
    return render(request, 'users/login.html', context)


@login_required
def interests_view(request):
    # Assuming one-to-one relation with User
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = InterestsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the profile or another relevant page
            return redirect('users:profile')
    else:
        form = InterestsForm(instance=profile)

    return render(request, 'users/interests.html', {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'  # Adjust based on your template
    slug_field = 'user.email'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected

    # Override get_object to use the logged-in user
    def get_object(self):
        # Return the logged-in user based on the slug
        return self.request.user
