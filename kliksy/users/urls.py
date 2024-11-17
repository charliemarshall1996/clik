

from django.urls import path

from . import views
app_name = 'users'
urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path('verify-email/<int:user_id>/<str:token>/',
         views.verify_email_view, name='verify_email'),
    path('resend-verification-email/', views.resend_verification_email_view,
         name='resend_verification_email'),
    path('login/', views.custom_login_view, name='login'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/<slug:slug>/',
         views.ProfileUpdateView.as_view(), name='update_profile'),
]
