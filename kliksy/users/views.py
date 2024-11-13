
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, ProfileRegistrationForm
# Create your views here.


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

            # TODO: Send verification email Logic
            # send_verification_email(user, request)

            messages.success(
                request, "Your account has been created.\nPlease check your email to verify your account.")

            # Redirect to profile or job application list
            return redirect('accounts:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()

    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})
